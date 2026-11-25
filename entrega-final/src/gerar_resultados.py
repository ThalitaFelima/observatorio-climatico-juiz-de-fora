"""Calcula indicadores com SQL e gera evidências textuais verificáveis."""
from pathlib import Path
import json
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "dados" / "clima.duckdb"
DEST = ROOT / "docs" / "escopo-1" / "AE1-2" / "RESULTADOS_EXECUCAO.md"

def main():
    with duckdb.connect(str(DB), read_only=True) as con:
        rows = con.execute("""SELECT COUNT(*) AS n,
            COUNT(DISTINCT data) AS datas,
            SUM(precipitacao_mm) AS chuva_total,
            COUNT(*) FILTER (WHERE precipitacao_mm > 0) AS dias_chuva,
            MAX(precipitacao_mm) AS maior_chuva,
            COUNT(precipitacao_mm) AS dias_com_chuva_disponivel,
            COUNT(temperatura_min) AS min_validos,
            COUNT(temperatura_max) AS max_validos
            FROM clima_diario""").fetchone()
        if rows[0] != 30 or rows[1] != 30:
            raise RuntimeError(f"Banco não contém 30 datas únicas: {rows[:2]}")
        primeira = con.execute("""SELECT data FROM clima_diario
            WHERE precipitacao_mm = (SELECT MAX(precipitacao_mm) FROM clima_diario)
            ORDER BY data LIMIT 1""").fetchone()
        contagem_dupla = con.execute("""SELECT COUNT(*) FROM
            (SELECT cidade, data, COUNT(*) n FROM clima_diario GROUP BY 1,2 HAVING COUNT(*) > 1)""").fetchone()[0]
        if contagem_dupla:
            raise RuntimeError("Foram encontradas duplicatas")
    qualidade = json.loads((ROOT / "dados" / "qualidade.json").read_text(encoding="utf-8"))
    meta = json.loads((ROOT / "dados" / "metadados_coleta.json").read_text(encoding="utf-8"))
    n, datas, total, dias, maxima, cobertura, valid_min, valid_max = rows
    texto = f"""# AE1-2 — Evidências da execução real

**Origem:** API histórica Open-Meteo. **Data da coleta (UTC):** {meta['coletado_em_utc']}.
**Localidade:** Juiz de Fora, MG (coordenadas de referência -21.764, -43.350).
**Recorte:** 01 a 30 de outubro de 2026; fuso America/Sao_Paulo.
**Parâmetros:** `{meta['url_consultada']}`.

## Qualidade dos dados

- Registros no DuckDB: **{n}**.
- Datas distintas: **{datas}**.
- Duplicatas por cidade/data: **{contagem_dupla}**.
- Precipitação disponível: **{cobertura} de 30 dias**.
- Temperaturas mínimas disponíveis: **{valid_min} de 30 dias**.
- Temperaturas máximas disponíveis: **{valid_max} de 30 dias**.
- Ausências por variável: `{qualidade['campos_ausentes']}`.
- Regras de validação: **{qualidade['validacoes']}**.

## Indicadores e interpretação

1. **Precipitação total:** **{total if total is not None else 'N/D'} mm** (soma dos dias com informação). Indica o volume acumulado no ponto de referência, não volume de inundação urbana.
2. **Dias com chuva:** **{dias} dias** com precipitação superior a zero, entre **{cobertura} dias** válidos. Não deve ser confundido com dias de alagamento.
3. **Maior precipitação diária:** **{maxima if maxima is not None else 'N/D'} mm**, em **{primeira[0] if primeira else 'N/D'}**. Isso não comprova evento de inundação.

## Limitações
A Open-Meteo disponibiliza dados meteorológicos históricos modelados/em grade, não necessariamente leituras de estação local. Uma única coordenada e 30 dias não descrevem a distribuição espacial nos bairros, nem demonstram ocorrência de alagamentos ou tendência climática. Em caso de risco, consultar Defesa Civil e alertas oficiais.

## Evidências reproduzíveis
- JSON original: `dados/original_open_meteo.json`.
- Parâmetros e data: `dados/metadados_coleta.json`.
- Relatório de qualidade: `dados/qualidade.json`.
- Banco DuckDB: `dados/clima.duckdb`.
- Dados tabulares: `dados/clima_diario.csv`.
- Consultas: `sql/consultas.sql`.
"""
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(texto, encoding="utf-8")
    print(texto)

if __name__ == "__main__":
    main()
