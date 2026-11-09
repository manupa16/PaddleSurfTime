import unittest
from dataclasses import replace
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


class TestCondicionesALaLlegada(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(
            condiciones={BOLNUEVO: {datetime(2026, 7, 15, 9): CONDICIONES}}
        )

    def test_da_las_condiciones_de_bolnuevo_a_las_nueve(self):
        condiciones = self.playas.condiciones_a_la_llegada(
            BOLNUEVO, datetime(2026, 7, 15, 9)
        )
        self.assertEqual(condiciones, CONDICIONES)

    def test_calblanque_sin_condiciones_da_error(self):
        with self.assertRaises(KeyError):
            self.playas.condiciones_a_la_llegada(
                ("Calblanque", "Cartagena"), datetime(2026, 7, 15, 9)
            )


class TestBanderaImpideSalir(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta()

    def test_bolnuevo_con_bandera_verde_no_impide(self):
        self.assertFalse(self.playas.bandera_impide_salir(CONDICIONES))

    def test_bolnuevo_con_bandera_amarilla_impide(self):
        condiciones = replace(CONDICIONES, bandera=Bandera.AMARILLA)
        self.assertTrue(self.playas.bandera_impide_salir(condiciones))

    def test_bolnuevo_con_bandera_roja_impide(self):
        condiciones = replace(CONDICIONES, bandera=Bandera.ROJA)
        self.assertTrue(self.playas.bandera_impide_salir(condiciones))

    def test_bolnuevo_sin_bandera_conocida_no_impide(self):
        condiciones = replace(CONDICIONES, bandera=None)
        self.assertFalse(self.playas.bandera_impide_salir(condiciones))

class TestVientoPeligroso(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(orientaciones_grados={BOLNUEVO: 165})

    def test_viento_lateral_en_bolnuevo_no_es_peligroso(self):
        self.assertFalse(self.playas.viento_peligroso(BOLNUEVO, CONDICIONES))

    def test_viento_de_tierra_en_bolnuevo_es_peligroso(self):
        condiciones = replace(CONDICIONES, viento=Viento(fuerza_kmh=12, direccion_grados=345))
        self.assertTrue(self.playas.viento_peligroso(BOLNUEVO, condiciones))

    def test_viento_justo_en_el_margen_es_peligroso(self):
        condiciones = replace(CONDICIONES, viento=Viento(fuerza_kmh=12, direccion_grados=278))
        self.assertTrue(self.playas.viento_peligroso(BOLNUEVO, condiciones))

    def test_al_dar_la_vuelta_al_circulo_no_es_peligroso(self):
        calblanque = ("Calblanque", "Cartagena")
        playas = PlayasDeLaCosta(orientaciones_grados={calblanque: 10})
        condiciones = replace(CONDICIONES, viento=Viento(fuerza_kmh=12, direccion_grados=350))
        self.assertFalse(playas.viento_peligroso(calblanque, condiciones))
