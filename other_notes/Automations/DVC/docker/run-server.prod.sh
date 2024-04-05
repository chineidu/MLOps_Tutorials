#!/bin/bash

# Enforce stricter error handling in the script.
set -euo pipefail

BACKEND_STORE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE_NAME}"

mlflow server \
    -h ${PROD_MLFLOW_SERVER_HOST} \
    -p ${PROD_MLFLOW_SERVER_PORT} \
    --backend-store-uri ${BACKEND_STORE_URI} \
    --default-artifact-root ${MLFLOW_ARTIFACT_STORE} \
