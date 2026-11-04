from dataclasses import dataclass, field
from datetime import datetime

from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.playa import Playa


@dataclass(eq=False)
class PlayasDeLaCosta:
    playas: dict[tuple[str, str], Playa] = field(default_factory=dict)
    condiciones: dict[tuple[str, str], dict[datetime, CondicionesMar]] = field(
        default_factory=dict
    )
