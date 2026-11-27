import unittest
from dataclasses import replace
from datetime import date, datetime
from pathlib import Path

from paddlesurf_time.bandera import Bandera
from paddlesurf_time.bandera_publicada import BanderaPublicada
from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.paginas import prevision_por_hora, horas_de_prevision
from paddlesurf_time.playas_de_la_costa import PlayasDeLaCosta
from paddlesurf_time.viento import Viento

BOLNUEVO = ("Bolnuevo", "Mazarrón")
CONDICIONES = CondicionesMar(
    viento=Viento(fuerza_kmh=12, direccion_grados=248),
    altura_olas_metros=0.4,
)
NUEVE = datetime(2026, 7, 15, 9)
def publicada_el_dia_de_llegada(bandera):
    return BanderaPublicada(bandera=bandera, actualizada=NUEVE.date())
CALBLANQUE = ("Calblanque", "Cartagena")
def con_viento_desde(direccion_grados):
    return replace(CONDICIONES, viento=replace(CONDICIONES.viento, direccion_grados=direccion_grados))
DATOS = Path(__file__).parent / "datos"
VIENTO = (DATOS / "viento_bolnuevo.json").read_text()
OLAS = (DATOS / "olas_bolnuevo.json").read_text()
HORAS_VIENTO = horas_de_prevision(VIENTO)
HORAS_OLAS = horas_de_prevision(OLAS)
BANDERAS = (DATOS / "banderas_murcia.html").read_text()
BOLNUEVO_OASIS = ("BOLNUEVO (OASIS)", "MAZARRON")



class TestCondicionesALaLlegada(unittest.TestCase):
    def setUp(self):
        self.a_las_diez = replace(CONDICIONES, altura_olas_metros=0.5)
        self.playas = PlayasDeLaCosta(
            condiciones={BOLNUEVO: {NUEVE: CONDICIONES, datetime(2026, 7, 15, 10): self.a_las_diez}}
        )

    def test_da_las_condiciones_de_la_hora_en_punto_mas_cercana(self):
        casos = {
            NUEVE: CONDICIONES,
            datetime(2026, 7, 15, 9, 29): CONDICIONES,
            datetime(2026, 7, 15, 9, 30): self.a_las_diez,
        }
        for llegada, condiciones in casos.items():
            with self.subTest(llegada=llegada):
                self.assertEqual(self.playas.condiciones_a_la_llegada(BOLNUEVO, llegada), condiciones)
    
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
                playas = PlayasDeLaCosta(banderas={BOLNUEVO: publicada_el_dia_de_llegada(bandera)})
                self.assertEqual(playas.bandera_impide_salir(BOLNUEVO, NUEVE), impide)

    def test_playa_sin_bandera_publicada_da_error(self):
        with self.assertRaises(KeyError):
            PlayasDeLaCosta().bandera_impide_salir(BOLNUEVO, NUEVE)

class TestBanderaALaLlegada(unittest.TestCase):
    def test_solo_cuenta_la_bandera_del_dia_de_llegada(self):
        casos = {
            "del día de llegada": (NUEVE.date(), Bandera.VERDE),
            "del día anterior": (date(2026, 7, 14), None),
            "sin fecha": (None, None),
        }
        for caso, (actualizada, bandera) in casos.items():
            with self.subTest(caso):
                playas = PlayasDeLaCosta(
                    banderas={BOLNUEVO: BanderaPublicada(bandera=Bandera.VERDE, actualizada=actualizada)}
                )
                self.assertEqual(playas.bandera_a_la_llegada(BOLNUEVO, NUEVE), bandera)

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
        casos = (
            (CONDICIONES, Bandera.VERDE, []),
            (CONDICIONES, Bandera.ROJA, ["bandera"]),
            (con_viento_desde(278), Bandera.VERDE, ["viento de tierra"]),
            (replace(CONDICIONES, viento=replace(CONDICIONES.viento, fuerza_kmh=18)), Bandera.VERDE, ["viento fuerte"]),
            (replace(CONDICIONES, altura_olas_metros=0.6), Bandera.VERDE, ["olas"]),
            (replace(CONDICIONES, viento=Viento(fuerza_kmh=18, direccion_grados=278), altura_olas_metros=0.6), Bandera.ROJA, ["bandera", "viento de tierra", "viento fuerte", "olas"]),
        )
        for condiciones, bandera, motivos in casos:
            with self.subTest(motivos=motivos):
                playas = PlayasDeLaCosta(
                    orientaciones_grados={BOLNUEVO: 165},
                    condiciones={BOLNUEVO: {NUEVE: condiciones}},
                    banderas={BOLNUEVO: publicada_el_dia_de_llegada(bandera)},
                )
                self.assertEqual(playas.motivos_no_apta(BOLNUEVO, NUEVE), motivos)

class TestPrevisionPorHora(unittest.TestCase):
    def test_da_el_valor_de_cada_dato_a_las_nueve(self):
        casos = {
            "wind_speed_10m": (HORAS_VIENTO, 6.7),
            "wind_direction_10m": (HORAS_VIENTO, 344),
            "wave_height": (HORAS_OLAS, 0.4),
        }
        for dato, (horas, valor) in casos.items():
            with self.subTest(dato=dato):
                self.assertEqual(prevision_por_hora(horas, dato)[datetime(2024, 9, 11, 9)], valor)

    def test_dato_que_no_esta_en_la_prevision_da_error(self):
        with self.assertRaises(KeyError):
            prevision_por_hora(HORAS_OLAS, "wind_speed_10m")

class TestActualizarBanderas(unittest.TestCase):
    def test_guarda_la_bandera_de_cada_playa(self):
        casos = {
            BOLNUEVO_OASIS: BanderaPublicada(bandera=Bandera.VERDE, actualizada=date(2024, 9, 11)),
            ("ENTREMARES", "CARTAGENA"): BanderaPublicada(bandera=Bandera.AMARILLA, actualizada=date(2024, 9, 11)),
            ("BOLNUEVO (CENTRO)", "MAZARRON"): BanderaPublicada(bandera=None, actualizada=date(2024, 9, 3)),
            ("ESTACIO (NORTE)", "SAN JAVIER"): BanderaPublicada(bandera=None, actualizada=date(2024, 9, 11)),
            ("BARCO PERDIDO III (ZEUS)", "CARTAGENA"): BanderaPublicada(bandera=None, actualizada=None),
        }
        playas = PlayasDeLaCosta()
        playas.actualizar_banderas(BANDERAS)
        for playa, bandera in casos.items():
            with self.subTest(playa=playa):
                self.assertEqual(playas.banderas[playa], bandera)

class TestJuntarCondiciones(unittest.TestCase):
    def setUp(self):
        self.playas = PlayasDeLaCosta(orientaciones_grados={BOLNUEVO_OASIS: 165})
        self.playas.actualizar_banderas(BANDERAS)

    def test_dice_si_bolnuevo_esta_apta_a_la_llegada(self):
        casos = {
            datetime(2024, 9, 11, 9): ["viento de tierra"],
            datetime(2024, 9, 11, 12): [],
            datetime(2024, 9, 11, 22): ["olas"],
        }
        self.playas.juntar_condiciones(BOLNUEVO_OASIS, VIENTO, OLAS)
        for llegada, motivos in casos.items():
            with self.subTest(llegada=llegada):
                self.assertEqual(self.playas.motivos_no_apta(BOLNUEVO_OASIS, llegada), motivos)
