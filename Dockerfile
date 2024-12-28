# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}

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
    --disabled-password \
    --home "/home/app" \
    --shell "/bin/bash" \
    --uid "${UID}" \
    --ingroup app \
    app


RUN apt update \
    && apt install -y --no-install-recommends \
    build-essential \
    curl \
    python3-venv \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# RUN apt update
RUN pip install --upgrade pip 
RUN pip install "uv"

COPY --chown=app:app requirements.txt /app/

RUN uv pip install -r requirements.txt --system

RUN chown -R app:app ./

USER app

COPY --chown=app:app . ./

EXPOSE 8000