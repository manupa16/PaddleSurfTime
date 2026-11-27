FROM python:alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/entorno

RUN adduser -D pruebas \
    && mkdir /opt/entorno \
    && chown pruebas /opt/entorno

COPY pyproject.toml uv.lock /opt/proyecto/

RUN apk add --no-cache --virtual compilar gcc musl-dev linux-headers \
    && su pruebas -c "uv sync --frozen --no-cache --project /opt/proyecto" \
    && apk del compilar

USER pruebas

ENV UV_NO_SYNC=1 UV_NO_CACHE=1

WORKDIR /app/test

ENTRYPOINT ["uv", "run", "task", "test"]