FROM docker.io/astral/uv:0.13.8-python3.15-trixie-slim

ENV UV_PROJECT_ENVIRONMENT=/opt/entorno

COPY pyproject.toml uv.lock /opt/proyecto/

RUN uv sync --frozen --no-cache --project /opt/proyecto

RUN useradd pruebas
USER pruebas

ENV UV_NO_SYNC=1 UV_NO_CACHE=1

WORKDIR /app/test

ENTRYPOINT ["uv", "run", "task", "test"]