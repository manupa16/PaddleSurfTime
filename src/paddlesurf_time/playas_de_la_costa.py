from dataclasses import dataclass, field
from datetime import datetime

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
