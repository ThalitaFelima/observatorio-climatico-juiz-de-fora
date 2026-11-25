"""Validação e carga idempotente dos dados diários no DuckDB."""
from pathlib import Path
import json
import pandas as pd
from config import CIDADE, UF, LATITUDE, LONGITUDE, INICIO, FIM

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "dados" / "original_open_meteo.json"
DESTINO = ROOT / "dados" / "clima.duckdb"
CSV = ROOT / "dados" / "clima_diario.csv"
RELATORIO = ROOT / "dados" / "qualidade.json"
COLUNAS = {"time": "data", "temperature_2m_min": "temperatura_min",
           "temperature_2m_max": "temperatura_max", "precipitation_sum": "precipitacao_mm"}

def tratar(conteudo):
    diario = conteudo.get("daily")
    if not isinstance(diario, dict):
        raise ValueError("JSON não contém objeto daily.")
    for campo in COLUNAS:
        if campo not in diario or not isinstance(diario[campo], list):
            raise ValueError(f"Campo ausente/inválido: {campo}")
    if len({len(diario[campo]) for campo in COLUNAS}) != 1:
        raise ValueError("Listas diárias não possuem mesmo tamanho.")
    df = pd.DataFrame({destino: diario[origem] for origem, destino in COLUNAS.items()})
    df["cidade"], df["uf"] = CIDADE, UF
    df["latitude"], df["longitude"] = LATITUDE, LONGITUDE
    datas = pd.to_datetime(df["data"], errors="coerce", format="%Y-%m-%d")
    if datas.isna().any():
        raise ValueError("Datas inválidas.")
    df["data"] = datas.dt.date
    for c in ("temperatura_min", "temperatura_max", "precipitacao_mm"):
        nao_nulo = df[c].notna()
        df[c] = pd.to_numeric(df[c], errors="coerce")
        if (nao_nulo & df[c].isna()).any():
            raise ValueError(f"Tipo numérico inválido: {c}")
    esperado = list(pd.date_range(INICIO, FIM).date)
    if len(esperado) != 30:
        raise ValueError("Recorte diferente de 30 dias.")
    if df[["cidade", "data"]].duplicated().any():
        raise ValueError("Datas duplicadas para a cidade.")
    if set(df["data"]) != set(esperado) or len(df) != 30:
        raise ValueError("Cobertura incompleta ou fora do período.")
    if (df["temperatura_min"] > df["temperatura_max"]).fillna(False).any():
        raise ValueError("Temperatura mínima maior que máxima.")
    if (df["precipitacao_mm"] < 0).fillna(False).any():
        raise ValueError("Precipitação negativa.")
    for c in ("temperatura_min", "temperatura_max"):
        if ((df[c] < -30) | (df[c] > 60)).fillna(False).any():
            raise ValueError(f"Temperatura fora da faixa de triagem: {c}")
    faltantes = {c: int(df[c].isna().sum()) for c in ("temperatura_min", "temperatura_max", "precipitacao_mm")}
    qualidade = {
        "localidade": CIDADE, "periodo": [INICIO, FIM], "registros": len(df),
        "dias_esperados": len(esperado), "duplicatas": 0, "campos_ausentes": faltantes,
        "validacoes": "aprovadas",
        "observacao": "Ausências permanecem NULL; indicadores desconsideram NULL."
    }
    return df.sort_values("data").reset_index(drop=True), qualidade

def gravar(df):
    import duckdb
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(DESTINO)) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS clima_diario (
            cidade VARCHAR NOT NULL, uf VARCHAR NOT NULL,
            latitude DOUBLE NOT NULL, longitude DOUBLE NOT NULL,
            data DATE NOT NULL, temperatura_min DOUBLE,
            temperatura_max DOUBLE, precipitacao_mm DOUBLE,
            PRIMARY KEY (cidade, data),
            CHECK (temperatura_min IS NULL OR temperatura_max IS NULL OR temperatura_min <= temperatura_max),
            CHECK (precipitacao_mm IS NULL OR precipitacao_mm >= 0)
        )""")
        con.register("novos_dados", df)
        con.execute("""INSERT INTO clima_diario
            (cidade, uf, latitude, longitude, data, temperatura_min, temperatura_max, precipitacao_mm)
            SELECT cidade, uf, latitude, longitude, data, temperatura_min, temperatura_max, precipitacao_mm
            FROM novos_dados
            ON CONFLICT (cidade, data) DO UPDATE SET
            uf = excluded.uf, latitude = excluded.latitude,
            longitude = excluded.longitude, temperatura_min = excluded.temperatura_min,
            temperatura_max = excluded.temperatura_max, precipitacao_mm = excluded.precipitacao_mm""")
        return con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0]

def executar():
    conteudo = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    df, qualidade = tratar(conteudo)
    total = gravar(df)
    df.to_csv(CSV, index=False)
    qualidade["linhas_no_banco_apos_carga"] = total
    RELATORIO.write_text(json.dumps(qualidade, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(qualidade, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    executar()
