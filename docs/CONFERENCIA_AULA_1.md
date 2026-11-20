# Conferência do projeto com a Aula 1

## Critérios da aula e implementação

| Orientação apresentada pelo professor | Aplicação no Observatório Climático |
| --- | --- |
| Escolher um problema e um público específico | Acesso a dados de chuva para moradores de áreas sujeitas a alagamentos em Juiz de Fora |
| Uma localidade | Juiz de Fora/MG, com coordenadas de referência documentadas |
| Trinta dias consecutivos | 1º a 30 de outubro de 2026 |
| Até três variáveis meteorológicas | Temperatura mínima, máxima e precipitação diária |
| Uma tabela principal | `clima_diario`, com chave composta (cidade, data) |
| Três perguntas e indicadores | Chuva acumulada, dias com precipitação e maior acumulado diário |
| Dois gráficos | Barras de precipitação e linhas de temperatura |
| Coleta, tratamento, banco, consultas e painel | Scripts separados em `src/`, SQL em `sql/` e Streamlit |
| Qualidade e origem dos dados | Resposta JSON, parâmetros, regras de validação, testes e relatório de execução |
| Repositório compreensível e reproduzível | README, dependências, código, banco e documentos organizados |
| Contato com a comunidade | Conversas com cinco pessoas em 17–20/11/2026; devolutiva documentada |
| Relatório final | Análise, gráficos, resultados, limitações e referências em `docs/final/` |

## Conferências técnicas

- A coleta foi registrada e foram armazenadas 30 datas distintas no DuckDB.
- As três variáveis possuem 30 valores disponíveis no recorte.
- A segunda carga manteve 30 registros, sem duplicação.
- Os resultados foram confrontados com o CSV: 214,5 mm de precipitação total; 30 dias com chuva acima de zero; maior valor de 29,1 mm em 30/10/2026; médias de 16,73 °C (mínimas) e 24,97 °C (máximas).
- O painel Streamlit foi aberto em navegador no GitHub Actions, com imagem de execução em `docs/evidencias/dashboard_streamlit.png`.
- O fluxo automatizado também exporta os relatórios para PDF e DOCX.

## Considerações para a apresentação

O objetivo do projeto não é antecipar alagamentos, mas ampliar o acesso a dados históricos. Os resultados representam um ponto de grade meteorológica próximo das coordenadas selecionadas, sem informação sobre a situação de cada bairro. A principal observação recebida na devolutiva foi a importância de facilitar o acesso a essas informações.

A aplicação Streamlit pode ser executada localmente por meio de `streamlit run src/app.py`. O registro da execução automatizada demonstra o funcionamento técnico do painel, mas não corresponde a uma hospedagem pública permanente.
