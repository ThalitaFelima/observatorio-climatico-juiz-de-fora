# AE1-2 — Relatório técnico preliminar

**Atenção:** este arquivo é um roteiro de relatório, não uma declaração de coleta ou de resultados já observados.

## Problema, público e recorte
Moradores de áreas suscetíveis a alagamentos em Juiz de Fora podem se beneficiar de uma apresentação clara do histórico de precipitações. A solução analisa a API histórica Open-Meteo no ponto de referência (-21.764, -43.350), entre 01 e 30 de outubro de 2026, usando temperaturas mínimas/máximas e precipitação diária.

## Metodologia prevista
1. Obter os dados pela API com Requests, especificando coordenadas, recorte, variáveis e `America/Sao_Paulo`; preservar a resposta JSON sem modificação e registrar data de coleta.
2. Converter e conferir os registros com pandas. Verificar 30 dias, tipos numéricos, ausências, duplicatas, valores negativos e coerência entre temperaturas.
3. Carregar `clima_diario` no DuckDB; chave composta (`cidade`, `data`) e UPSERT, sem multiplicar linhas em nova execução.
4. Calcular com SQL precipitação total (mm), dias com chuva (>0 mm) e maior precipitação diária (mm); registrar resultados, unidades, cobertura e interpretação.

## Evidências a acrescentar após execução real
- Data e parâmetros concretos da requisição e quantidade de datas retornadas.
- Saída legível do programa de coleta e do relatório de qualidade.
- Consulta `SELECT COUNT(*) FROM clima_diario` e verificação de reexecução idempotente.
- Resultados das três consultas e imagens do painel com dados reais.

**Não preencher resultados com dados sintéticos de teste.** Dados de modelo/grade em um único ponto não demonstram ocorrência de alagamento, nem representam todo bairro; o período de 30 dias não permite estimar mudança climática de longo prazo.

## Referências
Documentação da Open-Meteo: https://open-meteo.com/en/docs/historical-weather-api

Mapeamento municipal de suscetibilidade: https://sisurb.pjf.mg.gov.br/server/rest/services/SISURB_dcivil/inundacao/MapServer/0
