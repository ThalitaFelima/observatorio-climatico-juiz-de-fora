"""Testes isolados da coleta: sem chamadas reais nem alteração dos dados do projeto."""
import json
import sys
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import coleta


class RespostaSimulada:
    def __init__(self, texto, erro=None):
        self.text = texto
        self.url = "https://archive-api.open-meteo.com/v1/archive?teste=1"
        self.erro = erro

    def raise_for_status(self):
        if self.erro:
            raise self.erro


class TesteColeta(TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.original = Path(self.temp.name) / "original.json"
        self.metadados = Path(self.temp.name) / "meta.json"
        p1 = patch.object(coleta, "DESTINO", self.original)
        p2 = patch.object(coleta, "METADADOS", self.metadados)
        p1.start()
        p2.start()
        self.addCleanup(p1.stop)
        self.addCleanup(p2.stop)

    def exemplo(self):
        return json.dumps({
            "daily": {
                "time": ["2026-10-01"],
                "temperature_2m_min": [15],
                "temperature_2m_max": [25],
                "precipitation_sum": [2.0],
            }
        }, indent=4)

    def test_guarda_texto_original_sem_reformatar(self):
        texto = self.exemplo()
        with patch.object(coleta.requests, "get", return_value=RespostaSimulada(texto)):
            coleta.coletar()
        self.assertEqual(self.original.read_text(encoding="utf-8"), texto)
        self.assertEqual(json.loads(self.metadados.read_text())["dias_retornados"], 1)

    def test_erro_json_nao_grava_arquivo(self):
        with patch.object(coleta.requests, "get", return_value=RespostaSimulada("{invalido")):
            with self.assertRaisesRegex(ValueError, "JSON válido"):
                coleta.coletar()
        self.assertFalse(self.original.exists())

    def test_resposta_sem_daily_nao_grava_arquivo(self):
        with patch.object(coleta.requests, "get", return_value=RespostaSimulada('{"error":true}')):
            with self.assertRaisesRegex(ValueError, "mensagem de erro"):
                coleta.coletar()
        self.assertFalse(self.original.exists())

    def test_timeout_exibe_mensagem_especifica(self):
        with patch.object(coleta.requests, "get", side_effect=requests.exceptions.Timeout()):
            with self.assertRaisesRegex(RuntimeError, "tempo de espera"):
                coleta.coletar()
        self.assertFalse(self.original.exists())

    def test_erro_http_exibe_mensagem_especifica(self):
        with patch.object(coleta.requests, "get", return_value=RespostaSimulada(self.exemplo(), requests.exceptions.HTTPError("503"))):
            with self.assertRaisesRegex(RuntimeError, "erro HTTP"):
                coleta.coletar()
        self.assertFalse(self.original.exists())
