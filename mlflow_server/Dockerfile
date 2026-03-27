FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD mlflow server \
    --host 0.0.0.0 \
    --port $PORT \
    --backend-store-uri sqlite:////mlruns/mlflow.db \
    --default-artifact-root file:///mlruns