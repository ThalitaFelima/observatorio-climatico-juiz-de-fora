# Observatório Climático Local — Juiz de Fora/MG

Projeto Integrador Extensionista 2 • análise de dados meteorológicos e comunicação com a comunidade.

## Sobre o projeto

O Observatório Climático Local organiza dados históricos de precipitação e temperatura de Juiz de Fora, com atenção à necessidade de informações claras para moradores de áreas sujeitas a alagamentos. A proposta é facilitar a consulta e a compreensão dos registros, apresentando indicadores e gráficos em linguagem acessível.

O projeto não substitui os avisos oficiais da Defesa Civil: **registros de chuva não indicam, por si só, a ocorrência de alagamentos**.

## Recorte e resultados

- **Localidade:** Juiz de Fora, Minas Gerais.
- **Período:** 1º a 30 de outubro de 2026 (30 dias consecutivos).
- **Fonte:** API histórica [Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api).
- **Variáveis:** temperatura mínima diária (°C), temperatura máxima diária (°C) e precipitação diária (mm).
- **Chuva acumulada:** 214,5 mm.
- **Dias com precipitação acima de zero:** 30, sendo oito com menos de 1 mm.
- **Maior precipitação diária:** 29,1 mm, em 30 de outubro.

Os 30 registros foram armazenados na tabela `clima_diario`, em DuckDB. A validação identificou zero duplicidades e zero valores ausentes nas três variáveis.

## Tecnologias

| Etapa | Ferramenta |
| --- | --- |
| Coleta e preservação da resposta original | Python, Requests, JSON |
| Preparação e verificação dos dados | pandas |
| Armazenamento | DuckDB |
| Consultas e indicadores | SQL |
| Painel de visualização | Streamlit |
| Versionamento e execução automatizada | GitHub e GitHub Actions |

## Executar o projeto

É necessário Python 3.10 ou superior e conexão à internet para a coleta.

```bash
python -m venv .venv
# No Windows PowerShell: .venv\Scripts\Activate.ps1
# No Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/coleta.py
python src/banco.py
python src/gerar_resultados.py
python -m unittest discover -s tests -v
streamlit run src/app.py
```

A pasta `dados/` contém a resposta original da API, o CSV diário, os metadados de coleta, o relatório de qualidade e o banco DuckDB. Os arquivos podem ser reproduzidos pelos scripts. A chave composta `(cidade, data)` evita duplicações em novas cargas.

## Arquivos e entregas

| Material | Acesso |
| --- | --- |
| Planejamento da AE2-2 | [PDF](docs/escopo-1/AE2-2/PLANEJAMENTO.pdf) · [Word](docs/escopo-1/AE2-2/PLANEJAMENTO.docx) |
| Implementação e análise da AE1-2 | [PDF](docs/escopo-1/AE1-2/RELATORIO_FINAL.pdf) · [Word](docs/escopo-1/AE1-2/RELATORIO_FINAL.docx) |
| Relatório de consolidação | [PDF](docs/final/RELATORIO_FINAL.pdf) · [Word](docs/final/RELATORIO_FINAL.docx) |
| Resultados e verificações | [Evidências de execução](docs/escopo-1/AE1-2/RESULTADOS_EXECUCAO.md) |
| Painel em funcionamento | [Captura do Streamlit](docs/evidencias/dashboard_streamlit.png) |
| Gráficos | [Precipitação](docs/graficos/precipitacao_diaria.svg) · [Temperaturas](docs/graficos/temperaturas_diarias.svg) |
| Comunicação com a comunidade | [Devolutiva](docs/devolutiva/RELATO_REAL.md) · [Guia de leitura](docs/devolutiva/GUIA_PARA_MORADORES.md) |

Os códigos estão em `src/`, as consultas em `sql/`, os testes em `tests/` e a documentação em `docs/`. As conferências das aulas estão em [Aula 1](docs/CONFERENCIA_AULA_1.md) e [Aula 2](docs/CONFERENCIA_AULA_2.md). O andamento das atividades foi acompanhado pelas [issues](https://github.com/ThalitaFelima/observatorio-climatico-juiz-de-fora/issues).

## Devolutiva à comunidade

Entre **17 e 20 de novembro de 2026**, conversei com cinco pessoas e apresentei a API, o banco de dados e os benefícios do observatório. O retorno foi positivo: elas consideraram importante reunir essas informações, mas chamaram a atenção para a dificuldade de acesso aos registros. A observação reforçou a necessidade de manter o painel simples, divulgar como consultá-lo e explicar os indicadores sem excesso de termos técnicos. O encontro e as contribuições estão descritos no [registro da devolutiva](docs/devolutiva/RELATO_REAL.md).

## Limitações e fontes

A consulta utiliza um ponto de referência na cidade, não dados específicos de todos os bairros. A Open-Meteo trabalha com dados históricos em grade, de modo que a localização efetiva do dado pode diferir das coordenadas solicitadas. O intervalo de 30 dias é útil para um exercício de análise, mas não permite identificar tendências climáticas de longo prazo nem confirmar episódios de inundação.

- [Open-Meteo — API histórica](https://open-meteo.com/en/docs/historical-weather-api)
- [Prefeitura de Juiz de Fora — suscetibilidade a inundações](https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0)
