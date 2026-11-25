# Atividade de Estudo 1 — Relatório técnico e analítico

**Observatório Climático Local | Juiz de Fora (MG)**  
**Período analisado:** 1º a 30 de outubro de 2026

## 1. Contextualização e continuidade do planejamento

O Observatório Climático Local foi planejado para facilitar o acesso a informações históricas de chuva e temperatura em Juiz de Fora. O público beneficiário são moradores da cidade, especialmente pessoas interessadas nas condições de chuva em áreas suscetíveis a alagamentos. O projeto organiza os dados de forma compreensível, sem confundir chuva registrada com ocorrência de inundação.

Foi mantido o recorte definido no planejamento: **uma localidade**, com referência em **-21.764, -43.350**, **30 dias consecutivos** e três variáveis diárias: precipitação (mm), temperatura mínima (°C) e temperatura máxima (°C). As perguntas analíticas e seus indicadores são: **quanto choveu no período?** (soma da precipitação, em mm); **em quantos dias houve chuva?** (dias com precipitação maior que zero); e **qual foi o dia de maior chuva?** (maior acumulado diário em mm e sua data). Não foi necessário alterar esse recorte.

## 2. Fonte, coleta e arquivos gerados

Os registros foram obtidos da **API histórica da Open-Meteo**, por requisição HTTP com **Python e Requests**. A coleta documentada nos metadados ocorreu em **20/11/2026, às 20h19min53s UTC**. Os parâmetros foram: `latitude=-21.764`; `longitude=-43.350`; `start_date=2026-10-01`; `end_date=2026-10-30`; `daily=temperature_2m_min,temperature_2m_max,precipitation_sum`; e `timezone=America/Sao_Paulo`.

A resposta recebida foi preservada em `dados/original_open_meteo.json`. Os parâmetros e o momento da coleta constam em `dados/metadados_coleta.json`. O tratamento produziu `dados/clima_diario.csv`, `dados/qualidade.json` e o banco `dados/clima.duckdb`. A resposta da API contém **30 datas** no objeto `daily`.

## 3. Tratamento, qualidade e armazenamento

Com **pandas**, os arrays diários do JSON foram convertidos em uma tabela. A coluna `time` passou a `data`, e as variáveis foram padronizadas como `temperatura_min`, `temperatura_max` e `precipitacao_mm`. As datas foram convertidas e conferidas; os valores meteorológicos foram convertidos para tipos numéricos. O processo verifica cobertura do período, valores ausentes, duplicações, precipitação negativa e temperatura mínima superior à máxima. Dados ausentes são mantidos como ausentes, sem substituição por zero.

**Estrutura da tabela principal `clima_diario` (DuckDB):**

| Campo | Tipo | Significado |
| --- | --- | --- |
| `cidade`, `uf` | VARCHAR | Município e unidade federativa |
| `latitude`, `longitude` | DOUBLE | Coordenadas utilizadas na consulta |
| `data` | DATE | Dia do registro meteorológico |
| `temperatura_min`, `temperatura_max` | DOUBLE | Mínima e máxima diárias, em °C |
| `precipitacao_mm` | DOUBLE | Precipitação acumulada diária, em mm |

A chave primária é **(`cidade`, `data`)**: uma linha por cidade e dia. A carga usa `INSERT ... ON CONFLICT DO UPDATE`, de modo que uma nova execução atualiza o mesmo registro, em vez de criar duplicatas.

**Evidência da qualidade e da carga:**

| Verificação | Resultado |
| --- | ---: |
| Datas esperadas / registros carregados | 30 / 30 |
| Datas distintas / registros duplicados | 30 / 0 |
| Valores ausentes em temperatura mínima, máxima e precipitação | 0 / 0 / 0 |
| Registros no banco após a carga | 30 |

**Amostra da tabela carregada (dados reais, com datas e unidades):**

| Data | Mín. (°C) | Máx. (°C) | Chuva (mm) |
| --- | ---: | ---: | ---: |
| 01/10/2026 | 17,6 | 30,5 | 12,1 |
| 15/10/2026 | 18,1 | 28,3 | 4,7 |
| 30/10/2026 | 16,9 | 26,2 | 29,1 |

O arquivo de qualidade não registra inconsistências para esse recorte. O código interrompe a carga quando identifica problemas estruturais ou valores incompatíveis; não corrige números meteorológicos por suposição.

## 4. Consultas SQL, indicadores e interpretação

As consultas abaixo utilizam a tabela persistente, com filtro para **Juiz de Fora, de 01 a 30/10/2026**. A íntegra comentada está em `sql/consultas.sql`.

**Pergunta 1 — Quanto choveu no período?**
```sql
SELECT ROUND(SUM(precipitacao_mm), 1) AS chuva_total_mm,
       COUNT(*) AS registros, COUNT(precipitacao_mm) AS dias_validos
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30';
```
**Resultado:** **214,5 mm**, com **30 registros e 30 valores válidos**. É a soma da chuva diária disponível para a área de referência, e não um volume de inundação.

**Pergunta 2 — Em quantos dias houve precipitação acima de zero?**
```sql
SELECT COUNT(*) FILTER (WHERE precipitacao_mm > 0) AS dias_chuva,
       COUNT(precipitacao_mm) AS dias_validos
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30';
```
**Resultado:** **30 dias com chuva, de 30 dias válidos**. Em oito desses dias o acumulado foi inferior a 1 mm; portanto, a contagem inclui precipitação fraca.

**Pergunta 3 — Qual foi o maior acumulado diário e em que data ocorreu?**
```sql
SELECT data, precipitacao_mm AS maior_chuva_mm
FROM clima_diario
WHERE cidade = 'Juiz de Fora'
  AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'
  AND precipitacao_mm IS NOT NULL
ORDER BY precipitacao_mm DESC, data ASC LIMIT 1;
```
**Resultado:** **29,1 mm em 30/10/2026**. Esse foi o maior valor diário do recorte, sem comprovar ocorrência de alagamento.

## 5. Critérios de sucesso, relevância e limitações

O planejamento previa uma base com 30 dias consecutivos, três variáveis, uma tabela sem duplicações e três perguntas respondidas por SQL. **Esses critérios técnicos foram atendidos** na base publicada. A comunicação por meio de um painel acessível e a avaliação do uso pela comunidade pertencem à continuidade do projeto, não sendo condição para esta etapa da atividade.

A apresentação dos valores pode ajudar moradores a comparar a frequência e a intensidade das chuvas e a compreender melhor os registros históricos. Entretanto, os dados da Open-Meteo são **históricos e provenientes de grade/modelagem**, não necessariamente medições de uma estação instalada na localidade exata. Uma única referência espacial e 30 dias não descrevem diferenças entre bairros, não demonstram eventos de alagamento e não permitem identificar tendências climáticas de longo prazo. **Esta análise não é uma previsão meteorológica nem um sistema de alerta.**

O projeto utiliza informações meteorológicas públicas. Eventuais contribuições de moradores devem ser relatadas sem expor nomes, contatos ou outros dados pessoais sem autorização. O painel deve remeter a fontes oficiais quando o assunto envolver riscos e alertas.

**Evidências no repositório:** `dados/metadados_coleta.json` (requisição e data), `dados/original_open_meteo.json` (resposta original), `dados/qualidade.json` (validações), `dados/clima_diario.csv` e `dados/clima.duckdb` (registros), `sql/consultas.sql` (cálculos), `docs/escopo-1/AE1-2/RESULTADOS_EXECUCAO.md` (resultados).  
**Fonte:** Open-Meteo — https://open-meteo.com/en/docs/historical-weather-api
