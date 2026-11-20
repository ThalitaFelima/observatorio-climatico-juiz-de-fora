-- KPI 1: Chuva acumulada (mm)
SELECT cidade, SUM(precipitacao_mm) AS precipitacao_total_mm,
 COUNT(precipitacao_mm) AS dias_com_dado, COUNT(*) AS dias_registrados
FROM clima_diario GROUP BY cidade;

-- KPI 2: Dias com precipitação acima de zero
SELECT cidade, COUNT(*) FILTER (WHERE precipitacao_mm > 0) AS dias_com_chuva,
 COUNT(precipitacao_mm) AS dias_com_dado
FROM clima_diario GROUP BY cidade;

-- KPI 3: Maior precipitação diária (mm) e data
SELECT data, precipitacao_mm FROM clima_diario
WHERE precipitacao_mm IS NOT NULL
ORDER BY precipitacao_mm DESC, data ASC LIMIT 1;

-- Análise adicional da temperatura máxima
SELECT ROUND(AVG(temperatura_max), 2) AS media_temperatura_max_c,
 COUNT(temperatura_max) AS dias_com_dado FROM clima_diario;

-- Registros para gráficos
SELECT data, temperatura_min, temperatura_max, precipitacao_mm
FROM clima_diario ORDER BY data;
