# Conferência da Aula 4 — Streamlit e entrega final

## Requisitos apresentados na aula

| Orientação da aula | Aplicação no observatório |
| --- | --- |
| Painel compreensível para quem não desenvolveu o sistema | Título, localidade, período e explicações em linguagem simples |
| Indicadores com unidade e cálculo definido | Chuva acumulada (mm), dias com chuva e maior chuva diária (mm) |
| Dois gráficos de séries temporais | Barras de precipitação e linhas das temperaturas mínima e máxima |
| Tabela para consultar registros | Tabela diária no painel, com nomes e unidades |
| Possibilidade de interação | Seleção de intervalo de dias, que atualiza métricas, gráficos e tabela |
| Acesso aos registros | Exportação dos dados selecionados em CSV |
| Consulta ao banco sem refazer a coleta | `src/app.py` usa DuckDB somente para leitura |
| Fonte e limites | Open-Meteo, série histórica de um ponto de grade e referência à Defesa Civil |
| Repositório reproduzível | README com dependências, comandos de execução, estrutura e documentos |
| Relatório com percurso e conclusões | `docs/final/RELATORIO_FINAL.md`, PDF e Word |
| Devolutiva com apresentação e escuta | `docs/devolutiva/RELATO_REAL.md`, cinco pessoas entre 17 e 20/11/2026 |
| Testes e evidências | GitHub Actions, `tests/`, captura de tela e relatórios |

## Ajustes após a aula

O painel ganhou um filtro de dias do mês para que o usuário possa comparar períodos sem executar novamente a coleta ou alterar o banco. Os três indicadores, os dois gráficos e a tabela são recalculados a partir do intervalo selecionado. Foi incluída a opção de baixar a seleção em CSV.

As legendas dos gráficos, a fonte e os limites do recorte passaram a ser apresentados no próprio painel, em frases acessíveis. Os dados históricos não indicam automaticamente alagamentos nem constituem previsão do tempo.

Foi incluído um teste automatizado dos indicadores do mês completo e do comportamento do filtro. A execução desse teste deve ser consultada no GitHub Actions; a presença do arquivo, por si só, não comprova aprovação.

## Distinção entre documentação técnica e relatório

O README descreve como instalar, coletar, gerar o banco e iniciar o painel. O relatório final apresenta o problema, a metodologia, os resultados encontrados, a devolutiva, as limitações e as conclusões.

O GitHub contém os arquivos de código, resultados e documentação; já o Streamlit, executado localmente ou em um ambiente de hospedagem, é a interface de consulta. A captura da aplicação no GitHub Actions registra a renderização, mas não significa que o painel esteja permanentemente publicado na internet.

## Resultados do mês completo

- 30 registros diários, correspondentes a outubro de 2026.
- 214,5 mm de precipitação acumulada.
- 30 dias com precipitação superior a zero, oito deles com menos de 1 mm.
- Maior precipitação diária de 29,1 mm, em 30/10/2026.
- Nenhuma duplicação e nenhuma ausência nas três variáveis analisadas.

Esses indicadores se referem ao recorte histórico de Juiz de Fora e são calculados com os registros da Open-Meteo. A seleção de um intervalo menor no painel modifica os resultados apresentados, com indicação dos dias exibidos.

## Conferência para apresentação

A demonstração deve começar pelo problema de acesso à informação, explicar a origem dos dados, mostrar os indicadores e os gráficos, apresentar a tabela e o filtro e terminar com a devolutiva e as limitações. Não é necessário introduzir funcionalidades que não ajudem a responder às perguntas do projeto.
