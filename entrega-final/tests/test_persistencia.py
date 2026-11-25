"""Verifica a persistência do DuckDB e a reexecução da carga."""
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import banco


class TestePersistencia(unittest.TestCase):
    def test_reabertura_e_carga_sem_duplicacao(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "teste_clima.duckdb"
            diario = {
                "daily": {
                    "time": pd.date_range("2026-10-01", periods=30).strftime("%Y-%m-%d").tolist(),
                    "temperature_2m_min": [15.0] * 30,
                    "temperature_2m_max": [24.0] * 30,
                    "precipitation_sum": [2.0] * 30,
                }
            }
            df, _ = banco.tratar(diario)
            with patch.object(banco, "DESTINO", caminho):
                primeira_carga = banco.gravar(df)
                segunda_carga = banco.gravar(df)

            self.assertEqual(primeira_carga, 30)
            self.assertEqual(segunda_carga, 30)
            self.assertTrue(caminho.exists())

            # Nova conexão: confirma que as linhas persistiram no arquivo.
            with duckdb.connect(str(caminho), read_only=True) as con:
                total = con.execute("SELECT COUNT(*) FROM clima_diario").fetchone()[0]
                unicos = con.execute(
                    "SELECT COUNT(*) FROM (SELECT cidade, data FROM clima_diario GROUP BY cidade, data)"
                ).fetchone()[0]
                tipos = dict(con.execute(
                    "SELECT column_name, data_type FROM information_schema.columns "
                    "WHERE table_name='clima_diario'"
                ).fetchall())
                chuva = con.execute(
                    "SELECT SUM(precipitacao_mm) FROM clima_diario "
                    "WHERE cidade='Juiz de Fora' "
                    "AND data BETWEEN DATE '2026-10-01' AND DATE '2026-10-30'"
                ).fetchone()[0]

            self.assertEqual(total, 30)
            self.assertEqual(unicos, 30)
            self.assertEqual(tipos["data"], "DATE")
            self.assertEqual(tipos["cidade"], "VARCHAR")
            self.assertEqual(chuva, 60.0)


if __name__ == "__main__":
    unittest.main()
