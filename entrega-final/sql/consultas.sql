-- Observatório Climático Local | Juiz de Fora/MG
-- Período: 1º a 30 de outubro de 2026
-- Uma linha por cidade e data. Unidades: precipitação (mm) e temperatura (°C).
-- As consultas filtram explicitamente a cidade e o período, para manter o resultado
-- correto mesmo que outras localidades e datas sejam incluídas futuramente.

-- Pergunta 1: Quanto choveu em Juiz de Fora entre 01 e 30/10/2026?
-- COUNT(*) = dias registrados; COUNT(precipitacao_mm) = dias com valor disponível.
SELECT
    cidade,
    ROUND(SUM(precipitacao_mm), 1) AS precipitacao_total_mm,
    COUNT(*) AS dias_registrados,
    COUNT(precipitacao_mm) AS dias_com_dado
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
GROUP BY cidade;

-- Pergunta 2: Em quantos dias houve precipitação superior a zero?
-- Um dia com 0,2 mm é contado como chuvoso; zero não equivale a dado ausente.
SELECT
    cidade,
    COUNT(*) FILTER (WHERE precipitacao_mm > 0) AS dias_com_precipitacao,
    COUNT(precipitacao_mm) AS dias_com_dado,
    COUNT(*) AS dias_registrados
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
GROUP BY cidade;

-- Pergunta 3: Qual foi o maior acumulado diário de chuva e em que dia ocorreu?
-- Em caso de empate, a menor data aparece primeiro.
SELECT
    cidade,
    data,
    precipitacao_mm AS maior_precipitacao_diaria_mm
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
  AND precipitacao_mm IS NOT NULL
ORDER BY precipitacao_mm DESC, data ASC
LIMIT 1;

-- Análise complementar: médias e extremos das temperaturas disponíveis.
SELECT
    ROUND(AVG(temperatura_min), 2) AS media_minimas_c,
    ROUND(AVG(temperatura_max), 2) AS media_maximas_c,
    MIN(temperatura_min) AS menor_minima_c,
    MAX(temperatura_max) AS maior_maxima_c,
    COUNT(temperatura_min) AS minimas_validas,
    COUNT(temperatura_max) AS maximas_validas
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30';

-- Análise complementar: amplitude térmica diária (máxima - mínima).
SELECT
    data,
    ROUND(temperatura_max - temperatura_min, 1) AS amplitude_termica_c
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
  AND temperatura_min IS NOT NULL
  AND temperatura_max IS NOT NULL
ORDER BY amplitude_termica_c DESC, data ASC;

-- Dados para os dois gráficos: séries ordenadas cronologicamente.
SELECT
    data,
    temperatura_min,
    temperatura_max,
    precipitacao_mm
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
ORDER BY data;
