# Dockerfile

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libjpeg-dev zlib1g-dev \
    libwebp-dev libmagic1 curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

# Настройки Poetry
ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .

CMD ["gunicorn", "dddoski.wsgi:application", "--bind", "0.0.0.0:8000"]
