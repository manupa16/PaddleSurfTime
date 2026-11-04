from dataclasses import dataclass, field

from paddlesurf_time.playa import Playa


@dataclass(eq=False)
class PlayasDeLaCosta:
    playas: dict[tuple[str, str], Playa] = field(default_factory=dict)
