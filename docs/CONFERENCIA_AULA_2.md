# Conferência da Aula 2 — Coleta e preparação dos dados

## Fluxo de trabalho

A segunda aula apresenta o caminho dos dados desde a solicitação à Open-Meteo até a montagem de uma tabela verificada, enfatizando a separação entre a resposta original e os registros preparados para análise.

| Etapa explicada na aula | Arquivo ou evidência do projeto |
| --- | --- |
| Definir coordenadas, datas, variáveis e fuso | `src/config.py` |
| Executar requisição HTTP com Requests | `src/coleta.py` |
| Conferir status HTTP e a estrutura da resposta | `src/coleta.py` |
| Preservar o JSON original antes do tratamento | `dados/original_open_meteo.json` e `src/coleta.py` |
| Documentar parâmetros e data da coleta | `dados/metadados_coleta.json` |
| Montar DataFrame com nomes padronizados | `src/banco.py` |
| Converter datas e identificar ausências | `src/banco.py` |
| Conferir cobertura, duplicidades e temperaturas | `src/banco.py` e `tests/test_qualidade.py` |
| Registrar as verificações executadas | `dados/qualidade.json` |
| Reproduzir o processo por outro computador | `README.md`, `requirements.txt` e GitHub Actions |

## Aprimoramentos efetuados após a aula

**Preservação da resposta:** o programa de coleta passou a salvar o texto original do JSON, sem reformatá-lo, depois de verificar se a resposta possui a estrutura diária esperada. O arquivo só é sobrescrito em uma coleta bem-sucedida.

**Tratamento de erros:** falhas de conexão, expiração do tempo de espera, respostas HTTP com erro e JSON inválido são identificados separadamente, para tornar mais fácil investigar o problema.

**Testes:** foram incluídos cenários de resposta válida, JSON inválido, erro retornado pela API, timeout e erro HTTP. As respostas de teste são simuladas e não interferem na base histórica publicada.

## Conferência dos registros reais

A execução anterior do projeto coletou 30 datas de outubro de 2026, sem duplicidades nem valores ausentes nas três variáveis. Os dados originais, as colunas padronizadas e os resultados podem ser conferidos nos arquivos da pasta `dados/`.

O tratamento mantém valores ausentes como ausentes, sem preenchê-los artificialmente com zero. As consultas usam somente a tabela após as validações.

## Observação sobre os dados meteorológicos

A API oferece registros históricos baseados em dados meteorológicos em grade e modelos de reanálise, e não necessariamente leituras de uma estação instalada nas coordenadas solicitadas. Por isso, o relatório apresenta os resultados como dados históricos obtidos da Open-Meteo e não como medição direta de uma estação de Juiz de Fora.

A aula também recomenda compreender e documentar os erros encontrados. O procedimento de coleta já prevê mensagens específicas para identificar falhas futuras. Na base utilizada no projeto, as verificações registradas foram concluídas sem inconsistências nos 30 registros analisados.
