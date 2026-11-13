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
NUEVE = datetime(2026, 7, 15, 9)
CALBLANQUE = ("Calblanque", "Cartagena")
def con_viento_desde(direccion_grados):
    return replace(CONDICIONES, viento=replace(CONDICIONES.viento, direccion_grados=direccion_grados))


class TestHoraAConsultar(unittest.TestCase):
    def test_toma_la_hora_en_punto_mas_cercana(self):
        casos = {
            datetime(2026, 7, 15, 9, 29): NUEVE,
            datetime(2026, 7, 15, 9, 30): datetime(2026, 7, 15, 10),
        }
        for llegada, hora in casos.items():
            with self.subTest(llegada=llegada):
                self.assertEqual(PlayasDeLaCosta().hora_a_consultar(llegada), hora)


class TestCondicionesALaLlegada(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(condiciones={BOLNUEVO: {NUEVE: CONDICIONES}})

    def test_da_las_condiciones_de_bolnuevo_a_las_nueve(self):
        self.assertEqual(self.playas.condiciones_a_la_llegada(BOLNUEVO, NUEVE), CONDICIONES)

    def test_sin_datos_da_error(self):
        casos = {
            "playa sin datos": (CALBLANQUE, NUEVE),
            "hora sin datos": (BOLNUEVO, datetime(2026, 7, 15, 23, 50)),
        }
        for caso, (playa, llegada) in casos.items():
            with self.subTest(caso):
                with self.assertRaises(KeyError):
                    self.playas.condiciones_a_la_llegada(playa, llegada)


class TestBanderaImpideSalir(unittest.TestCase):
    def test_solo_la_amarilla_y_la_roja_impiden_salir(self):
        casos = {
            Bandera.VERDE: False,
            Bandera.AMARILLA: True,
            Bandera.ROJA: True,
            None: False,
        }
        for bandera, impide in casos.items():
            with self.subTest(bandera=bandera):
                condiciones = replace(CONDICIONES, bandera=bandera)
                self.assertEqual(PlayasDeLaCosta().bandera_impide_salir(condiciones), impide)

class TestVientoPeligroso(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(orientaciones_grados={BOLNUEVO: 165, CALBLANQUE: 10})

    def test_grados_entre_viento_y_orientacion(self):
        casos = {
            (BOLNUEVO, 248): 83,
            (CALBLANQUE, 350): 20,
        }
        for (playa, direccion), grados in casos.items():
            with self.subTest(playa=playa, direccion=direccion):
                self.assertEqual(
                    self.playas.grados_entre_viento_y_orientacion(playa, con_viento_desde(direccion)), grados
                )

    def test_es_peligroso_a_partir_del_margen(self):
        casos = {248: False, 277: False, 278: True}
        for direccion, peligroso in casos.items():
            with self.subTest(direccion=direccion):
                self.assertEqual(self.playas.viento_peligroso(BOLNUEVO, con_viento_desde(direccion)), peligroso)

class TestVientoYOlasPasanDelLimite(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta()

    def test_viento_demasiado_fuerte_a_partir_del_umbral(self):
        casos = {12: False, 18: True}
        for fuerza_kmh, demasiado_fuerte in casos.items():
            with self.subTest(fuerza_kmh=fuerza_kmh):
                condiciones = replace(CONDICIONES, viento=replace(CONDICIONES.viento, fuerza_kmh=fuerza_kmh))
                self.assertEqual(self.playas.viento_demasiado_fuerte(condiciones), demasiado_fuerte)
    
    def test_olas_demasiado_altas_a_partir_del_umbral(self):
        casos = {0.4: False, 0.6: True}
        for altura_olas_metros, demasiado_altas in casos.items():
            with self.subTest(altura_olas_metros=altura_olas_metros):
                condiciones = replace(CONDICIONES, altura_olas_metros=altura_olas_metros)
                self.assertEqual(self.playas.olas_demasiado_altas(condiciones), demasiado_altas)

class TestMotivosNoApta(unittest.TestCase):
    def test_da_el_motivo_de_cada_condicion_que_impide_salir(self):
        casos = [
            (CONDICIONES, []),
            (replace(CONDICIONES, bandera=Bandera.ROJA), ["bandera"]),
            (con_viento_desde(278), ["viento de tierra"]),
            (replace(CONDICIONES, viento=replace(CONDICIONES.viento, fuerza_kmh=18)), ["viento fuerte"]),
            (replace(CONDICIONES, altura_olas_metros=0.6), ["olas"]),
        ]
        for condiciones, motivos in casos:
            with self.subTest(motivos=motivos):
                playas = PlayasDeLaCosta(
                    orientaciones_grados={BOLNUEVO: 165},
                    condiciones={BOLNUEVO: {NUEVE: condiciones}},
                )
                self.assertEqual(playas.motivos_no_apta(BOLNUEVO, NUEVE), motivos)
