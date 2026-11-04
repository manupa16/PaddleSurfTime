from dataclasses import dataclass, field
from datetime import datetime

from paddlesurf_time.condiciones_mar import CondicionesMar

type Playa = tuple[str, str]


@dataclass(eq=False)
class PlayasDeLaCosta:
    orientaciones_grados: dict[Playa, int] = field(default_factory=dict)
    condiciones: dict[Playa, dict[datetime, CondicionesMar]] = field(
        default_factory=dict
    )
