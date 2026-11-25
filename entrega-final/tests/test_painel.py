"""Verifica os indicadores do painel com o banco histórico já publicado."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class TestePainel(unittest.TestCase):
    def test_indicadores_e_filtro(self):
        app = AppTest.from_file(str(ROOT / "src" / "app.py")).run(timeout=60)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric), 3)
        self.assertEqual(app.metric[0].value, "214.5 mm")
        self.assertEqual(app.metric[1].value, "30 de 30 válidos")
        self.assertEqual(app.metric[2].value, "29.1 mm")
        self.assertEqual(len(app.slider), 1)
        app.slider[0].set_value((1, 10)).run(timeout=60)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric), 3)
        self.assertNotEqual(app.metric[0].value, "214.5 mm")


if __name__ == "__main__":
    unittest.main()
