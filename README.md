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


## Entregas e execução verificadas (20/11/2026)
O GitHub Actions **executou com sucesso** a coleta histórica, o banco DuckDB com carga repetida, as consultas e a validação do dashboard em navegador. Os dados obtidos totalizam **214,5 mm** de precipitação no período, com **30 registros únicos** e **0 ausências** nas variáveis escolhidas.

**Documentos para entrega:**
- [Planejamento AE2-2 — PDF](docs/escopo-1/AE2-2/PLANEJAMENTO.pdf) · [DOCX](docs/escopo-1/AE2-2/PLANEJAMENTO.docx) · [Markdown](docs/escopo-1/AE2-2/PLANEJAMENTO.md)
- [Relatório técnico AE1-2 — PDF](docs/escopo-1/AE1-2/RELATORIO_FINAL.pdf) · [DOCX](docs/escopo-1/AE1-2/RELATORIO_FINAL.docx) · [Markdown](docs/escopo-1/AE1-2/RELATORIO_FINAL.md)
- [Consolidação final — PDF](docs/final/RELATORIO_FINAL.pdf) · [DOCX](docs/final/RELATORIO_FINAL.docx) · [Markdown](docs/final/RELATORIO_FINAL.md)
- [Captura do dashboard Streamlit](docs/evidencias/dashboard_streamlit.png) · [Validação](docs/evidencias/VALIDACAO.md)
- [Material educativo para moradores](docs/devolutiva/GUIA_PARA_MORADORES.md) · [Modelo de registro da devolutiva](docs/devolutiva/REGISTRO_E_AVALIACAO_MODELO.md)
- [Resultado SQL e qualidade](docs/escopo-1/AE1-2/RESULTADOS_EXECUCAO.md) · [Gráfico de precipitação](docs/graficos/precipitacao_diaria.svg)

**Limite extensionista:** a devolutiva à comunidade ainda **não foi realizada/comprovada** e depende de apresentação real e registro ético. O arquivo recebido como “Relatório Final” era uma proposta, não uma rubrica oficial confirmada. A resposta da API retornou célula próxima **(-21.75747, -43.384613)**, embora a solicitação tenha sido feita para **(-21.764, -43.350)**.
