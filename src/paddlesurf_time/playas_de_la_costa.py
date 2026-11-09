from dataclasses import dataclass, field
from datetime import datetime, timedelta

from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.umbrales import Umbrales

type Playa = tuple[str, str]


@dataclass(eq=False)
class PlayasDeLaCosta:
    orientaciones_grados: dict[Playa, int] = field(default_factory=dict)
    condiciones: dict[Playa, dict[datetime, CondicionesMar]] = field(
        default_factory=dict
    )
    umbrales: Umbrales = Umbrales(fuerza_viento_kmh=18, altura_olas_metros=0.6)

    def hora_a_consultar(self, playa: Playa, llegada: datetime) -> datetime:
        hora = llegada.replace(minute=0, second=0, microsecond=0)
        if llegada.minute >= 30:
            hora += timedelta(hours=1)
        if hora not in self.condiciones[playa]:
            raise ValueError(f"No hay condiciones de {playa} a las {hora}")
        return hora

    def condiciones_a_la_llegada(self, playa: Playa, llegada: datetime) -> CondicionesMar:
        return self.condiciones[playa][self.hora_a_consultar(playa, llegada)]
