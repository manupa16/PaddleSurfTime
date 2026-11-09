import unittest
from datetime import datetime

from paddlesurf_time.bandera import Bandera
from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.playas_de_la_costa import PlayasDeLaCosta
from paddlesurf_time.viento import Viento

BOLNUEVO = ("Bolnuevo", "Mazarrón")
CONDICIONES = CondicionesMar(
    viento=Viento(fuerza_kmh=12, direccion_grados=248),
    altura_olas_metros=0.4,
    bandera=Bandera.VERDE,
)


class TestHoraAConsultar(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(
            condiciones={
                BOLNUEVO: {
                    datetime(2026, 7, 15, 9): CONDICIONES,
                    datetime(2026, 7, 15, 10): CONDICIONES,
                }
            }
        )

    def test_antes_de_y_media_toma_esa_hora(self):
        hora = self.playas.hora_a_consultar(BOLNUEVO, datetime(2026, 7, 15, 9, 29))
        self.assertEqual(hora, datetime(2026, 7, 15, 9))

    def test_desde_y_media_toma_la_siguiente(self):
        hora = self.playas.hora_a_consultar(BOLNUEVO, datetime(2026, 7, 15, 9, 30))
        self.assertEqual(hora, datetime(2026, 7, 15, 10))

    def test_sin_datos_de_la_hora_siguiente_da_error(self):
        with self.assertRaises(ValueError):
            self.playas.hora_a_consultar(BOLNUEVO, datetime(2026, 7, 15, 23, 50))
