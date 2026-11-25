# Observatório Climático Local — Juiz de Fora/MG

**Projeto Integrador Extensionista 2**

O observatório apresenta informações históricas de chuva e temperatura de Juiz de Fora, com gráficos e indicadores que facilitam a consulta e a compreensão dos registros.

## Recorte analisado

- Localidade: Juiz de Fora, Minas Gerais.
- Período: 1º a 30 de outubro de 2026.
- Fonte: Open-Meteo Historical Weather API.
- Variáveis: precipitação diária (mm), temperatura mínima diária (°C) e temperatura máxima diária (°C).
- Resultados: 214,5 mm acumulados, 30 dias com precipitação acima de zero e máximo diário de 29,1 mm em 30/10/2026.

## Executar o observatório

Requisitos: Python 3.10 ou superior.

A partir da pasta `entrega-final`, execute:

```bash
python -m venv .venv
# Ative o ambiente virtual conforme seu sistema operacional
python -m pip install -r requirements.txt
python src/coleta.py
python src/banco.py
python src/gerar_resultados.py
python -m unittest discover -s tests -v
streamlit run src/app.py
```

No Windows PowerShell, o ambiente virtual pode ser ativado com `.venv\Scripts\Activate.ps1`. No Linux ou macOS, use `source .venv/bin/activate`.

A coleta utiliza conexão com a internet. Os arquivos de dados já incluídos permitem consultar a base sem repetir a coleta: basta iniciar `streamlit run src/app.py`.

## Estrutura da entrega

| Pasta | Conteúdo |
| --- | --- |
| `src/` | Programas de coleta, validação, banco, consultas de resultados e painel |
| `sql/` | Consultas SQL documentadas |
| `dados/` | Resposta da API, metadados, banco DuckDB, CSV e qualidade dos registros |
| `tests/` | Testes da coleta, da qualidade, da persistência e do painel |
| `docs/escopo-1/` | Planejamento e relatório técnico da atividade |
| `docs/final/` | Relatório final em PDF, Word e Markdown |
| `docs/graficos/` | Gráficos dos dados meteorológicos |
| `docs/evidencias/` | Captura e registro da validação do painel |
| `docs/devolutiva/` | Registro da conversa com a comunidade e guia de leitura |

## Documentos principais

- [Relatório final (PDF)](docs/final/RELATORIO_FINAL.pdf)
- [Relatório final (Word)](docs/final/RELATORIO_FINAL.docx)
- [Planejamento AE2-2 (PDF)](docs/escopo-1/AE2-2/PLANEJAMENTO.pdf)
- [Relatório técnico AE1-2 (PDF)](docs/escopo-1/AE1-2/RELATORIO_FINAL.pdf)
- [Registro da devolutiva](docs/devolutiva/RELATO_REAL.md)
- [Painel Streamlit — captura](docs/evidencias/dashboard_streamlit.png)

## Devolutiva e limites

Entre 17 e 20 de novembro de 2026, o projeto foi apresentado a cinco pessoas, com explicações sobre a API, o banco de dados e seus possíveis benefícios. O retorno foi positivo e destacou a importância de facilitar o acesso aos registros.

A análise utiliza informações históricas em grade, referentes a uma localização de referência próxima de Juiz de Fora. Não identifica a ocorrência de alagamentos nem substitui alertas oficiais.

**Fontes:** [Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api) · [Mapeamento de suscetibilidade a inundações — Prefeitura de Juiz de Fora](https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0).
