"""Coleta dados históricos da Open-Meteo, preservando o JSON original."""
from pathlib import Path
import json
from datetime import datetime, timezone
import requests
from config import CIDADE, LATITUDE, LONGITUDE, INICIO, FIM, FUSO, VARIAVEIS, URL

ROOT = Path(__file__).resolve().parents[1]
DESTINO = ROOT / "dados" / "original_open_meteo.json"

def coletar():
    parametros = {
        "latitude": LATITUDE, "longitude": LONGITUDE,
        "start_date": INICIO, "end_date": FIM,
        "daily": ",".join(VARIAVEIS), "timezone": FUSO
    }
    resposta = requests.get(URL, params=parametros, timeout=45)
    resposta.raise_for_status()
    conteudo = resposta.json()
    if conteudo.get("error") or not isinstance(conteudo.get("daily"), dict):
        raise ValueError(f"Resposta inesperada da API: {conteudo}")
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    metadados = {
        "fonte": URL, "localidade": CIDADE, "parametros": parametros,
        "url_consultada": resposta.url,
        "coletado_em_utc": datetime.now(timezone.utc).isoformat()
    }
    (ROOT / "dados" / "metadados_coleta.json").write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON preservado: {DESTINO}; registros retornados: {len(conteudo['daily'].get('time', []))}")

if __name__ == "__main__":
    coletar()
