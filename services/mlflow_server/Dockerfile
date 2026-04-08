#services/mlflow_server/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${MLFLOW_PORT}

CMD mlflow server \
    --host ${MLFLOW_HOST} \
    --port ${MLFLOW_PORT} \
    --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} \
    --default-artifact-root ${MLFLOW_ARTIFACT_ROOT} \
    --allowed-hosts '*' \
    --cors-allowed-origins '*'