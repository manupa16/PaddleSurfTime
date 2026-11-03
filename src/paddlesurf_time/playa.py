from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Playa:
    nombre: str
    municipio: str
    orientacion_grados: int
