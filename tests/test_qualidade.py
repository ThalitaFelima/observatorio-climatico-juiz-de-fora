"""Testes com valores ARTIFICIAIS, não observações meteorológicas."""
import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from banco import tratar

class TesteQualidade(unittest.TestCase):
    def setUp(self):
        self.exemplo = {"daily": {
            "time": pd.date_range("2026-10-01", periods=30).strftime("%Y-%m-%d").tolist(),
            "temperature_2m_min": [15.0]*30,
            "temperature_2m_max": [25.0]*30,
            "precipitation_sum": [0.0]*30
        }}
    def test_cobertura(self):
        df, q = tratar(self.exemplo)
        self.assertEqual(len(df), 30)
        self.assertEqual(q["duplicatas"], 0)
    def test_precipitacao_negativa(self):
        self.exemplo["daily"]["precipitation_sum"][0] = -1
        with self.assertRaises(ValueError): tratar(self.exemplo)
    def test_minima_maior_maxima(self):
        self.exemplo["daily"]["temperature_2m_min"][0] = 30
        with self.assertRaises(ValueError): tratar(self.exemplo)
    def test_data_duplicada(self):
        self.exemplo["daily"]["time"][1] = self.exemplo["daily"]["time"][0]
        with self.assertRaises(ValueError): tratar(self.exemplo)
    def test_dado_faltante_nao_vira_zero(self):
        self.exemplo["daily"]["precipitation_sum"][0] = None
        df, q = tratar(self.exemplo)
        self.assertTrue(pd.isna(df.loc[0, "precipitacao_mm"]))
        self.assertEqual(q["campos_ausentes"]["precipitacao_mm"], 1)
    def test_cobertura_incompleta(self):
        for v in self.exemplo["daily"].values(): v.pop()
        with self.assertRaises(ValueError): tratar(self.exemplo)

if __name__ == "__main__":
    unittest.main()
