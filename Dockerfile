FROM debian:13-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/entorno UV_PYTHON_INSTALL_DIR=/opt/python

COPY pyproject.toml uv.lock /opt/proyecto/

RUN uv sync --frozen --no-cache --python 3.15 --project /opt/proyecto

RUN useradd pruebas
USER pruebas

ENV UV_NO_SYNC=1 UV_NO_CACHE=1

WORKDIR /app/test

ENTRYPOINT ["uv", "run", "task", "test"]