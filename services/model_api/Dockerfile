#services/model_api/Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Запуск приложения
CMD uvicorn app:app --host ${API_HOST} --port ${API_PORT}