# AE1-2 — Evidências da execução real

**Origem:** API histórica Open-Meteo. **Data da coleta (UTC):** 2026-11-20T20:19:53.646964+00:00.
**Localidade:** Juiz de Fora, MG (coordenadas de referência -21.764, -43.350).
**Recorte:** 01 a 30 de outubro de 2026; fuso America/Sao_Paulo.
**Parâmetros:** `https://archive-api.open-meteo.com/v1/archive?latitude=-21.764&longitude=-43.35&start_date=2026-10-01&end_date=2026-10-30&daily=temperature_2m_min%2Ctemperature_2m_max%2Cprecipitation_sum&timezone=America%2FSao_Paulo`.

## Qualidade dos dados

- Registros no DuckDB: **30**.
- Datas distintas: **30**.
- Duplicatas por cidade/data: **0**.
- Precipitação disponível: **30 de 30 dias**.
- Temperaturas mínimas disponíveis: **30 de 30 dias**.
- Temperaturas máximas disponíveis: **30 de 30 dias**.
- Ausências por variável: `{'temperatura_min': 0, 'temperatura_max': 0, 'precipitacao_mm': 0}`.
- Regras de validação: **aprovadas**.

## Indicadores e interpretação

1. **Precipitação total:** **214,5 mm** (soma dos dias com informação). Indica o volume acumulado no ponto de referência, não volume de inundação urbana.
2. **Dias com chuva:** **30 dias** com precipitação superior a zero, entre **30 dias** válidos. Não deve ser confundido com dias de alagamento.
3. **Maior precipitação diária:** **29,1 mm**, em **30/10/2026**. Isso não comprova evento de inundação.

## Limitações
A Open-Meteo disponibiliza dados meteorológicos históricos modelados/em grade, não necessariamente leituras de estação local. Uma única coordenada e 30 dias não descrevem a distribuição espacial nos bairros, nem demonstram ocorrência de alagamentos ou tendência climática. Em caso de risco, consultar Defesa Civil e alertas oficiais.

## Evidências reproduzíveis
- JSON original: `dados/original_open_meteo.json`.
- Parâmetros e data: `dados/metadados_coleta.json`.
- Relatório de qualidade: `dados/qualidade.json`.
- Banco DuckDB: `dados/clima.duckdb`.
- Dados tabulares: `dados/clima_diario.csv`.
- Consultas: `sql/consultas.sql`.
