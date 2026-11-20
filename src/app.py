"""Painel de consulta aos dados históricos do Observatório Climático Local."""
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
BANCO = ROOT / "dados" / "clima.duckdb"

st.set_page_config(page_title="Observatório Climático | Juiz de Fora", layout="wide")
st.title("Observatório Climático Local")
st.subheader("Juiz de Fora, Minas Gerais")
st.caption("Dados históricos da Open-Meteo | 1º a 30 de outubro de 2026")
st.write(
    "Consulte como a precipitação e as temperaturas variaram durante outubro. "
    "Os dados ajudam a conhecer o período analisado, mas não registram alagamentos."
)

if not BANCO.exists():
    st.error(
        "Banco de dados não encontrado. Na pasta do projeto, execute "
        "`python src/coleta.py` e depois `python src/banco.py`."
    )
    st.stop()

# O painel apenas consulta o banco pronto. Não refaz coleta nem carga de dados.
with duckdb.connect(str(BANCO), read_only=True) as con:
    df = con.execute(
        """SELECT data, temperatura_min, temperatura_max, precipitacao_mm
           FROM clima_diario
           WHERE cidade = 'Juiz de Fora'
             AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
           ORDER BY data"""
    ).df()

if df.empty:
    st.info("Não há registros disponíveis para Juiz de Fora no período selecionado.")
    st.stop()

df["data"] = pd.to_datetime(df["data"])
st.markdown("### Escolha os dias para consultar")
limites = st.slider(
    "Intervalo de dias de outubro de 2026",
    min_value=1,
    max_value=30,
    value=(1, 30),
    help="Ajuste o início e o fim para comparar partes do mês.",
)
selecionados = df.loc[df["data"].dt.day.between(limites[0], limites[1])].copy()
st.caption(
    f"Exibindo {len(selecionados)} registro(s), de "
    f"{selecionados['data'].min().strftime('%d/%m/%Y')} a "
    f"{selecionados['data'].max().strftime('%d/%m/%Y')}."
)

prec = selecionados["precipitacao_mm"]
total = prec.sum(min_count=1)
dias_com_chuva = int((prec > 0).sum())
dias_validos = int(prec.count())
maior = prec.max()

col1, col2, col3 = st.columns(3)
col1.metric("Chuva acumulada", f"{total:.1f} mm" if pd.notna(total) else "Sem dados")
col2.metric("Dias com chuva", f"{dias_com_chuva} de {dias_validos} válidos")
col3.metric("Maior chuva em um dia", f"{maior:.1f} mm" if pd.notna(maior) else "Sem dados")

st.caption(
    "Dia com chuva: precipitação maior que 0 mm. "
    "A chuva acumulada é a soma dos valores disponíveis no intervalo selecionado."
)

st.markdown("### Como a chuva variou durante o período?")
st.bar_chart(selecionados.set_index("data")["precipitacao_mm"])
st.caption("Cada barra corresponde ao acumulado diário de precipitação, em milímetros (mm).")

st.markdown("### Como variaram as temperaturas?")
st.line_chart(
    selecionados.set_index("data")[["temperatura_min", "temperatura_max"]]
)
st.caption(
    "As duas linhas correspondem à temperatura mínima e à temperatura máxima "
    "de cada dia, medidas em graus Celsius (°C)."
)

st.markdown("### Dados do período")
st.dataframe(
    selecionados.rename(
        columns={
            "data": "Data",
            "temperatura_min": "Temperatura mínima (°C)",
            "temperatura_max": "Temperatura máxima (°C)",
            "precipitacao_mm": "Precipitação (mm)",
        }
    ),
    use_container_width=True,
    hide_index=True,
)
csv = selecionados.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Baixar os registros selecionados (CSV)",
    data=csv,
    file_name="observatorio_climatico_juiz_de_fora.csv",
    mime="text/csv",
)

with st.expander("Fonte dos dados e limites da análise"):
    st.write(
        "Fonte: API histórica Open-Meteo. Os dados representam uma célula "
        "meteorológica de referência próxima a Juiz de Fora, e não medições "
        "em todos os bairros. A série tem 30 dias e não permite identificar "
        "alagamentos ocorridos ou tendências climáticas de longo prazo."
    )
    st.markdown(
        "[Documentação da Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api)"
    )
    st.markdown(
        "[Mapeamento municipal de suscetibilidade a inundações]"
        "(https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0)"
    )

st.info(
    "Este observatório apresenta informações históricas e não faz previsão "
    "do tempo nem substitui os avisos da Defesa Civil."
)
