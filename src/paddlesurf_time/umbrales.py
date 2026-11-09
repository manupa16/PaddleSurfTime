from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Umbrales:
    fuerza_viento_kmh: float
    altura_olas_metros: float
