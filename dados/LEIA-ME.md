# Dados

Após instalar as dependências e executar `python src/coleta.py`, esta pasta conterá o JSON original e metadados da coleta. Execute em seguida `python src/banco.py` para gerar `clima.duckdb`, `clima_diario.csv` e `qualidade.json`.

**Atenção:** arquivos não estão incluídos inicialmente; não confundir resultados sintéticos dos testes com dados reais. A carga é idempotente para a chave (cidade, data).
