from dataclasses import dataclass, field
from datetime import datetime, timedelta

from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.umbrales import Umbrales
from paddlesurf_time.bandera import Bandera

type Playa = tuple[str, str]


@dataclass(eq=False)
class PlayasDeLaCosta:
    orientaciones_grados: dict[Playa, int] = field(default_factory=dict)
    condiciones: dict[Playa, dict[datetime, CondicionesMar]] = field(
        default_factory=dict
    )
    umbrales: Umbrales = Umbrales(fuerza_viento_kmh=18, altura_olas_metros=0.6, margen_viento_peligroso_grados=112.5)

    def hora_a_consultar(self, llegada: datetime) -> datetime:
        return (llegada + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)

    def condiciones_a_la_llegada(self, playa: Playa, llegada: datetime) -> CondicionesMar:
        return self.condiciones[playa][self.hora_a_consultar(llegada)]
    
    def bandera_impide_salir(self, condiciones: CondicionesMar) -> bool:
        return condiciones.bandera in (Bandera.AMARILLA, Bandera.ROJA)

    def grados_entre_viento_y_orientacion(self, playa: Playa, condiciones: CondicionesMar) -> int:
        diferencia = abs(condiciones.viento.direccion_grados - self.orientaciones_grados[playa])
        return min(diferencia, 360 - diferencia)

    def viento_peligroso(self, playa: Playa, condiciones: CondicionesMar) -> bool:
        diferencia = abs(condiciones.viento.direccion_grados - self.orientaciones_grados[playa])
        return min(diferencia, 360 - diferencia) >= self.umbrales.margen_viento_peligroso_grados

    def viento_demasiado_fuerte(self, condiciones: CondicionesMar) -> bool:
        return condiciones.viento.fuerza_kmh >= self.umbrales.fuerza_viento_kmh

    def olas_demasiado_altas(self, condiciones: CondicionesMar) -> bool:
        return condiciones.altura_olas_metros >= self.umbrales.altura_olas_metros

    def motivos_no_apta(self, playa: Playa, llegada: datetime) -> list[str]:
        condiciones = self.condiciones_a_la_llegada(playa, llegada)
        motivos = []
        if self.bandera_impide_salir(condiciones):
            motivos.append("bandera")
        if self.viento_peligroso(playa, condiciones):
            motivos.append("viento de tierra")
        if self.viento_demasiado_fuerte(condiciones):
            motivos.append("viento fuerte")
        if self.olas_demasiado_altas(condiciones):
            motivos.append("olas")
        return motivos
