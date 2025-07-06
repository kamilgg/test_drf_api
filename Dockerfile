# Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей системы
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev netcat-openbsd gcc \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Точка входа: ожидание базы и запуск сервера
ENTRYPOINT ["/app/entrypoint.sh"]
