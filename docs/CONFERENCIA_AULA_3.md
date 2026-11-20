# Conferência da Aula 3 — DuckDB e SQL

## Armazenamento e análise

A terceira aula explica como os dados preparados com pandas são armazenados em um banco DuckDB persistente e transformados em respostas por consultas SQL. O professor destaca que cada pergunta precisa estar bem definida, com localidade, período, indicador, unidade e interpretação.

| Critério trabalhado na aula | Aplicação no observatório |
| --- | --- |
| Banco em arquivo, disponível após encerrar o processo | `dados/clima.duckdb`, acessado por `src/banco.py` |
| Uma linha por cidade e data | Tabela `clima_diario`, chave primária composta |
| Tipos coerentes para os campos | `VARCHAR` (cidade), `DATE` (data), `DOUBLE` (variáveis) |
| DataFrame tratado registrado para uso no SQL | `con.register("novos_dados", df)` |
| Tabela persistente e carga repetível | `CREATE TABLE IF NOT EXISTS` e `INSERT ... ON CONFLICT DO UPDATE` |
| Consultas relacionadas às perguntas do projeto | `sql/consultas.sql` |
| Filtro de município e de período | `WHERE cidade = 'Juiz de Fora' AND data BETWEEN ...` |
| Cobertura e valores ausentes | `COUNT(*)` e `COUNT(precipitacao_mm)` |
| Maior precipitação com data correspondente | Ordenação decrescente por precipitação e desempate por data |
| Análise adicional de temperaturas | Média, extremos e amplitude térmica diária |
| Série cronológica para os gráficos | Consulta final ordenada por data |
| Persistência e ausência de duplicações | `tests/test_persistencia.py` |

## Perguntas e resultados

**1. Quanto choveu em Juiz de Fora entre 1º e 30 de outubro de 2026?** A soma SQL de precipitação diária disponível foi **214,5 mm**. Foram armazenados 30 registros, todos com valor de precipitação.

**2. Em quantos dias desse período houve precipitação acima de zero?** O banco registrou **30 dias**, dos quais **oito tiveram menos de 1 mm**. O indicador não expressa a quantidade de dias de alagamento.

**3. Qual foi o maior acumulado diário e quando ocorreu?** O maior valor foi **29,1 mm em 30/10/2026**.

As consultas incluem comentários e nomes descritivos, facilitando a revisão. A comparação entre `COUNT(*)` e `COUNT(precipitacao_mm)` permite identificar linhas com valor nulo, mas a cobertura completa das 30 datas é verificada também na etapa de tratamento.

## Melhorias realizadas após a aula

- Os filtros de cidade e período foram incluídos explicitamente em todas as consultas, evitando a mistura de localidades se o banco for ampliado futuramente.
- Foram adicionadas consultas complementares para médias e extremos de temperatura e amplitude térmica diária, sem alterar os três indicadores principais do painel.
- Foi acrescentado um teste que cria um banco temporário, executa a mesma carga duas vezes, fecha a conexão, reabre o arquivo e confere quantidade de registros, datas únicas, tipos das colunas e soma da precipitação.

## Limitações da análise

A série de 30 dias permite descrever o recorte selecionado, não estabelecer tendências de longo prazo. Os registros provêm da Open-Meteo e não comprovam a ocorrência de alagamentos. A organização dos dados e os testes do banco asseguram consistência técnica dentro das regras adotadas, mas não substituem o exame da adequação dos dados para cada finalidade.

A estrutura do projeto continua simples: uma tabela principal, três perguntas centrais, três indicadores e dois gráficos.
