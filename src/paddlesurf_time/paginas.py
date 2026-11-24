from datetime import datetime


def prevision_por_hora(horas: dict[str, list], dato: str) -> dict[datetime, float]:
    return dict(zip(map(datetime.fromisoformat, horas["time"]), horas[dato]))
