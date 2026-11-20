"""Painel de chuva histórica (não oferece alerta de alagamento)."""
from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
BANCO = ROOT / "dados" / "clima.duckdb"
st.set_page_config(page_title="Observatório Climático | Juiz de Fora", layout="wide")
st.title("Observatório Climático Local — Juiz de Fora/MG")
st.caption("01 a 30/10/2026 | Dados históricos Open-Meteo | Chuva em mm; temperatura em °C")
st.warning("Não é previsão, aviso meteorológico, mapa de risco nem registro de alagamentos. Consulte a Defesa Civil.")
if not BANCO.exists():
    st.error("Banco não gerado. Execute python src/coleta.py e python src/banco.py primeiro.")
    st.stop()
with duckdb.connect(str(BANCO), read_only=True) as con:
    df = con.execute("SELECT * FROM clima_diario ORDER BY data").df()
if df.empty:
    st.info("Não há registros carregados.")
    st.stop()
prec = df["precipitacao_mm"]
c1, c2, c3 = st.columns(3)
c1.metric("Chuva acumulada (mm)", f"{prec.sum():.1f}" if prec.notna().any() else "N/D")
c2.metric("Dias com chuva (>0 mm)", f"{int((prec > 0).sum())} / {int(prec.count())} válidos")
maior = prec.max()
c3.metric("Maior chuva diária (mm)", f"{maior:.1f}" if pd.notna(maior) else "N/D")
st.subheader("Precipitação diária (mm)")
st.bar_chart(df.set_index("data")["precipitacao_mm"])
st.subheader("Temperaturas diárias (°C)")
st.line_chart(df.set_index("data")[["temperatura_min", "temperatura_max"]])
st.subheader("Registros consultáveis")
st.dataframe(df, use_container_width=True)
st.caption("Dados históricos de grade/modelo da Open-Meteo, não necessariamente medidos por estação local. Uma única coordenada não representa todos os bairros. Alagamentos dependem também de relevo, drenagem, solo e ocupação.")
st.markdown("[Mapeamento municipal de suscetibilidade](https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0)")
