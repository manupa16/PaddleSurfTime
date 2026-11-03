from dataclasses import dataclass, field
from datetime import datetime

from paddlesurf_time.condiciones_mar import CondicionesMar
from paddlesurf_time.playa import Playa


@dataclass(kw_only=True, eq=False)
class PrevisionPlaya:
    playa: Playa
    condiciones: dict[datetime, CondicionesMar] = field(default_factory=dict)
