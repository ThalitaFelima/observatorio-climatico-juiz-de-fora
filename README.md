# Observatório Climático Local — Juiz de Fora/MG

Projeto educativo/extensionista de análise de chuva histórica para comunicação acessível aos moradores de **áreas suscetíveis a alagamentos** em Juiz de Fora. **Não é sistema de alerta, nem prova de alagamento em um bairro ou rua específica.**

## Recorte
- Cidade: Juiz de Fora/MG, coordenadas de referência **-21.764, -43.350** (aproximação do centro urbano).
- Período: **01/10/2026 a 30/10/2026**, 30 dias consecutivos.
- API histórica Open-Meteo: `temperature_2m_min` (°C), `temperature_2m_max` (°C), `precipitation_sum` (mm).
- Banco DuckDB: tabela `clima_diario` com chave primária (`cidade`, `data`).
- KPIs: precipitação acumulada (mm), dias de chuva (dias) e maior precipitação diária (mm).

## Como executar
Python 3.10+ e internet na fase de coleta:

```bash
python -m venv .venv
# Ative .venv (Windows PowerShell: .venv\Scripts\Activate.ps1)
pip install -r requirements.txt
python src/coleta.py
python src/banco.py
streamlit run src/app.py
python -m unittest discover -s tests -v
```

A coleta preserva o JSON original, e a carga verifica registros e evita duplicações. Valores ausentes **não** devem ser substituídos automaticamente por zero.

## Organização
- `src/`: configuração, coleta, tratamento e dashboard.
- `sql/consultas.sql`: análises SQL.
- `dados/`: JSON coletado e banco, gerados na execução.
- `docs/escopo-1/AE2-2/`: planejamento e wireframe.
- `docs/escopo-1/AE1-2/`: relatório de execução.
- `docs/final/`: relatório de consolidação.
- `tests/`: testes de qualidade.
- `.github/ISSUE_TEMPLATE/`: planejamento das tarefas.

## Atenção aos resultados
**Os KPIs reais e as evidências ainda não foram verificados neste repositório.** Testes com dados sintéticos não devem ser apresentados como medições reais. A análise de 30 dias não caracteriza tendência climática nem permite concluir onde houve alagamento; tampouco substitui alertas da Defesa Civil.

Mapeamento oficial da Prefeitura: https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0

Documentação da API: https://open-meteo.com/en/docs/historical-weather-api

Os enunciados mencionam uma AE1 anterior, não disponibilizada. O recorte acima foi estabelecido para esta proposta e deve ser validado com o docente.
