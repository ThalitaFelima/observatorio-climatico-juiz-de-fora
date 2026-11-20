# Relatório Final — Observatório Climático Local

**Juiz de Fora/MG · Público-alvo: moradores de áreas suscetíveis a alagamentos**

> Este relatório consolida as atividades apresentadas. O arquivo “Relatório Final” recebido era uma **proposta de composição**, não um enunciado oficial confirmado.

## Problema e solução
O projeto busca ampliar a compreensão pública de precipitações históricas. Emprega API histórica Open-Meteo → coleta com Python/Requests e preservação de JSON → limpeza/validação com pandas → armazenamento DuckDB → consultas SQL → visualização no Streamlit → comunicação transparente sobre limites e unidades. O recorte é uma coordenada de referência (-21.764, -43.350) em Juiz de Fora, de **01 a 30 de outubro de 2026**; variáveis: precipitação diária (mm), temperatura mínima (°C) e máxima (°C).

## Dados, qualidade e reprodutibilidade
A coleta real foi realizada em **20/11/2026 às 19:47:24 UTC**. Foram recuperados 30 dias, sem ausências nas variáveis escolhidas; a chave primária composta `(cidade,data)` e `UPSERT` impediram duplicação na segunda execução. Seis testes de qualidade passaram. Os arquivos originais, código SQL e relatório automático estão disponíveis neste repositório.

## Indicadores observados
| Indicador | Resultado | Significado |
| --- | ---: | --- |
| Precipitação acumulada | **214,5 mm** | Soma no período selecionado |
| Dias com precipitação > 0 mm | **30/30 dias** | Oito dias abaixo de 1 mm |
| Maior chuva diária | **29,1 mm** | 30/10/2026 |
| Temperatura mínima diária média | **16,73 °C** | Média de 30 mínimas |
| Temperatura máxima diária média | **24,97 °C** | Média de 30 máximas |

![Gráfico de precipitação](../graficos/precipitacao_diaria.svg)

![Temperaturas mínimas e máximas](../graficos/temperaturas_diarias.svg)

## Dashboard e público
O painel `src/app.py` contém três cartões de KPI, série de chuva, série de temperaturas, tabela diária e advertências. A validação automática confirma comportamento técnico, mas isso não equivale à avaliação de usabilidade por moradores.

## Interpretação e limitações
O recorte permite comparar dias mais ou menos chuvosos e compreender unidades de precipitação. Não permite verificar alagamentos, prever novos eventos ou estabelecer risco para um bairro específico. Uma única coordenada não representa toda a cidade; 30 dias não caracterizam tendência climática. A fonte pode utilizar dados modelados/em grade. Os mapas municipais de suscetibilidade são uma fonte **distinta** dos dados de chuva; não se devem confundir suscetibilidade espacial e ocorrência de evento.

## Ética e devolutiva

Conforme relato da responsável pelo projeto, **cinco pessoas** foram consultadas em conversas realizadas de **17 a 20 de novembro de 2026**, durante as quais foram apresentados a API meteorológica, o banco de dados e os benefícios esperados do observatório. As pessoas demonstraram satisfação e consideraram o registro importante, mas apontaram que **a dificuldade de acesso às informações pode prejudicar sua utilidade**. Trata-se de retorno qualitativo inicial, sem questionário formal, transcrições ou identificação individual, que não deve ser interpretado como pesquisa representativa.

Esse retorno orienta a melhoria da linguagem, da navegação e da divulgação do painel para facilitar o acesso à informação. Não foram publicados dados pessoais e não se afirma que houve redução de risco ou impacto social mensurado. A descrição completa consta em [Relato da devolutiva](../devolutiva/RELATO_REAL.md).

## Critérios de sucesso
**Verificados:** coleta preservada, 30 registros, 0 duplicidades, três KPIs, documentação versionada, testes e CI aprovados. **Ainda dependem de ação real:** avaliação estruturada da usabilidade e da utilidade pública em uma amostra maior. Evoluções futuras: série maior, múltiplas coordenadas e integração responsável com registros oficiais de ocorrência.

## Fontes
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- [Prefeitura de Juiz de Fora — mapa de suscetibilidade a inundações](https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0)
- [Resultados verificados da AE1-2](../escopo-1/AE1-2/RESULTADOS_EXECUCAO.md)
- [Arquivos e scripts](../../README.md)

**Nota sobre a grade da API:** a requisição usou latitude -21.764 e longitude -43.350. A resposta da Open-Meteo identifica a célula retornada em **-21.75747, -43.384613** (elevação informada de 704 m). Essa diferença entre ponto solicitado e ponto retornado deve ser considerada na interpretação territorial. Fonte: `dados/original_open_meteo.json`.
