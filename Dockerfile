FROM python:3.15.2-alpine3.24

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/entorno

COPY pyproject.toml uv.lock /opt/proyecto/

RUN apk add --no-cache --virtual compilar gcc musl-dev linux-headers \
    && uv sync --frozen --no-cache --project /opt/proyecto \
    && apk del compilar

RUN adduser -D pruebas
USER pruebas

ENV UV_NO_SYNC=1 UV_NO_CACHE=1

WORKDIR /app/test

ENTRYPOINT ["uv", "run", "task", "test"]