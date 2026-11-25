"""Coleta de dados históricos, com preservação da resposta original e registro da requisição."""
from pathlib import Path
from datetime import datetime, timezone
import json
import requests

from config import CIDADE, LATITUDE, LONGITUDE, INICIO, FIM, FUSO, VARIAVEIS, URL

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "dados" / "original_open_meteo.json"
METADADOS = ROOT / "dados" / "metadados_coleta.json"


def coletar():
    parametros = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": INICIO,
        "end_date": FIM,
        "daily": ",".join(VARIAVEIS),
        "timezone": FUSO,
    }
    try:
        resposta = requests.get(URL, params=parametros, timeout=45)
        resposta.raise_for_status()
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("A consulta à Open-Meteo excedeu o tempo de espera.") from exc
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError("Não foi possível estabelecer conexão com a Open-Meteo.") from exc
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"A Open-Meteo retornou um erro HTTP: {exc}") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Falha ao solicitar dados à Open-Meteo: {exc}") from exc

    # O texto é guardado sem reformatar o JSON recebido.
    try:
        conteudo = json.loads(resposta.text)
    except json.JSONDecodeError as exc:
        raise ValueError("O conteúdo recebido da API não é um JSON válido.") from exc

    if not isinstance(conteudo, dict) or conteudo.get("error"):
        raise ValueError("A API retornou uma mensagem de erro ou uma estrutura inesperada.")
    diario = conteudo.get("daily")
    if not isinstance(diario, dict):
        raise ValueError("A resposta não contém o objeto 'daily' esperado.")
    campos = ["time", *VARIAVEIS]
    if any(not isinstance(diario.get(campo), list) for campo in campos):
        raise ValueError("Datas ou variáveis diárias estão ausentes na resposta.")
    if len({len(diario[campo]) for campo in campos}) != 1:
        raise ValueError("As listas diárias apresentam quantidades diferentes de elementos.")

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(resposta.text, encoding="utf-8")
    metadados = {
        "fonte": URL,
        "localidade": CIDADE,
        "parametros": parametros,
        "url_consultada": resposta.url,
        "coletado_em_utc": datetime.now(timezone.utc).isoformat(),
        "dias_retornados": len(diario["time"]),
    }
    METADADOS.write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Coleta concluída: {len(diario['time'])} registros; JSON preservado em {DESTINO}")


if __name__ == "__main__":
    coletar()
