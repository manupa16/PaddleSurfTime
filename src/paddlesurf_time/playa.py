from datetime import datetime

from paddlesurf_time.condiciones_mar import CondicionesMar


class Playa:
    def __init__(
        self,
        *,
        nombre: str,
        municipio: str,
        orientacion_grados: int,
    ) -> None:
        self._nombre = nombre
        self._municipio = municipio
        self._orientacion_grados = orientacion_grados
        self._condiciones: dict[datetime, CondicionesMar] = {}
