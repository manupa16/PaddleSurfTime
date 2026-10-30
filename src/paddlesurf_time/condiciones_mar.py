from dataclasses import dataclass
from datetime import datetime

from paddlesurf_time.bandera import Bandera
from paddlesurf_time.viento import Viento


@dataclass(frozen=True)
class CondicionesMar:
    momento: datetime
    viento: Viento
    altura_olas_metros: float
    bandera: Bandera | None
