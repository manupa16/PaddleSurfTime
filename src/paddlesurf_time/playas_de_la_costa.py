import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from itertools import batched

from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.umbrales import Umbrales
from paddlesurf_time.bandera import Bandera
from paddlesurf_time.bandera_publicada import BanderaPublicada
from paddlesurf_time.paginas import prevision_por_hora
from paddlesurf_time.viento import Viento

type Playa = tuple[str, str]


@dataclass(eq=False)
class PlayasDeLaCosta:
    orientaciones_grados: dict[Playa, int] = field(default_factory=dict)
    condiciones: dict[Playa, dict[datetime, CondicionesMar]] = field(
        default_factory=dict
    )
    banderas: dict[Playa, BanderaPublicada] = field(default_factory=dict)
    umbrales: Umbrales = Umbrales(fuerza_viento_kmh=18, altura_olas_metros=0.6, margen_viento_peligroso_grados=112.5)

    @staticmethod
    def hora_a_consultar(llegada: datetime) -> datetime:
        return (llegada + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)

    def condiciones_a_la_llegada(self, playa: Playa, llegada: datetime) -> CondicionesMar:
        return self.condiciones[playa][self.hora_a_consultar(llegada)]
    
    def bandera_a_la_llegada(self, playa: Playa, llegada: datetime) -> Bandera | None:
        publicada = self.banderas[playa]
        return publicada.bandera if publicada.actualizada == llegada.date() else None

    def bandera_impide_salir(self, playa: Playa, llegada: datetime) -> bool:
        return self.bandera_a_la_llegada(playa, llegada) in (Bandera.AMARILLA, Bandera.ROJA)

    def grados_entre_viento_y_orientacion(self, playa: Playa, condiciones: CondicionesMar) -> int:
        diferencia = abs(condiciones.viento.direccion_grados - self.orientaciones_grados[playa])
        return min(diferencia, 360 - diferencia)

    def viento_peligroso(self, playa: Playa, condiciones: CondicionesMar) -> bool:
        return self.grados_entre_viento_y_orientacion(playa, condiciones) >= self.umbrales.margen_viento_peligroso_grados

    def viento_demasiado_fuerte(self, condiciones: CondicionesMar) -> bool:
        return condiciones.viento.fuerza_kmh >= self.umbrales.fuerza_viento_kmh

    def olas_demasiado_altas(self, condiciones: CondicionesMar) -> bool:
        return condiciones.altura_olas_metros >= self.umbrales.altura_olas_metros

    def motivos_no_apta(self, playa: Playa, llegada: datetime) -> list[str]:
        condiciones = self.condiciones_a_la_llegada(playa, llegada)
        comprobaciones = {
            "bandera": self.bandera_impide_salir(playa, llegada),
            "viento de tierra": self.viento_peligroso(playa, condiciones),
            "viento fuerte": self.viento_demasiado_fuerte(condiciones),
            "olas": self.olas_demasiado_altas(condiciones),
        }
        return [motivo for motivo, se_cumple in comprobaciones.items() if se_cumple]

    def actualizar_banderas(self, estado_playas: str) -> None:
        celdas = re.findall(r"<span style='font-size: 8pt;'>([^<]*)</span>", estado_playas)
        self.banderas.update({
            (playa, municipio): BanderaPublicada(
                bandera=Bandera.__members__.get(bandera),
                actualizada=None if actualizada == "NO DISPONIBLE" else datetime.strptime(actualizada, "%d/%m/%Y %H:%M").date(),
            )
            for playa, municipio, bandera, _, actualizada in batched(celdas, 5)
        })

    def juntar_condiciones(self, playa: Playa, prevision_viento: str, prevision_olas: str) -> None:
        viento = json.loads(prevision_viento)["hourly"]
        olas = json.loads(prevision_olas)["hourly"]
        fuerzas = prevision_por_hora(viento, "wind_speed_10m")
        direcciones = prevision_por_hora(viento, "wind_direction_10m")
        alturas = prevision_por_hora(olas, "wave_height")
        self.condiciones[playa] = {
            hora: CondicionesMar(
                viento=Viento(fuerza_kmh=fuerzas[hora], direccion_grados=direcciones[hora]),
                altura_olas_metros=alturas[hora],
            )
            for hora in fuerzas
        }

