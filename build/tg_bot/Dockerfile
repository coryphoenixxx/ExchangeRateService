FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock README.md ./

RUN poetry lock --no-update \
    && poetry install --no-ansi -vvv --only tg_bot --no-root \
    && rm -rf $POETRY_CACHE_DIR

COPY src/exchange_rate_service/tg_bot /app/src/exchange_rate_service/tg_bot
COPY src/exchange_rate_service/common /app/src/exchange_rate_service/common

WORKDIR /app/src/exchange_rate_service
RUN poetry install --only tg_bot

CMD poetry run python -m tg_bot
