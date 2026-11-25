import json
import re
from datetime import datetime
from itertools import batched


def horas_de_prevision(prevision: str) -> dict[str, list]:
    return json.loads(prevision)["hourly"]


def prevision_por_hora(horas: dict[str, list], dato: str) -> dict[datetime, float]:
    return dict(zip(map(datetime.fromisoformat, horas["time"]), horas[dato]))


def celdas_de_banderas(estado_playas: str) -> list[tuple[str, ...]]:
    return list(batched(re.findall(r"<span style='font-size: 8pt;'>([^<]*)</span>", estado_playas), 5))
