from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Viento:
    fuerza_kmh: float
    direccion_grados: int
