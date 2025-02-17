# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.2
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /app

ARG UID=10001 
ARG GID=10001 

RUN addgroup \
    --system \
    --gid "${GID}" \
    app

RUN adduser \
    --system \
    --uid "${UID}" \
    --ingroup app \
    app


RUN apt update && apt upgrade -y\
    && apt install -y --no-install-recommends \
    build-essential \
    curl python3-venv libpq5 gcc\
    && apt clean \
    && rm -rf /var/lib/apt/lists/*


COPY --from=ghcr.io/astral-sh/uv:0.5.25 /uv /uvx /bin/

COPY --chown=app:app pyproject.toml .

RUN uv pip install -r pyproject.toml --system

RUN chown -R app:app .

USER app

COPY --chown=app:app . .

EXPOSE 8000