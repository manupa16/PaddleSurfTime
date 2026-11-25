from dataclasses import dataclass
from datetime import date

from paddlesurf_time.bandera import Bandera


@dataclass(frozen=True, kw_only=True)
class BanderaPublicada:
    bandera: Bandera | None
    actualizada: date | None
