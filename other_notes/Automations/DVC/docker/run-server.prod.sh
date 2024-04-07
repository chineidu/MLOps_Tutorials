#!/bin/bash

# Enforce stricter error handling in the script.
set -euo pipefail

BACKEND_STORE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE_NAME}"

mlflow server \
    -h ${MLFLOW_HOST} \
    -p ${MLFLOW_PORT} \
    --backend-store-uri ${BACKEND_STORE_URI} \
    --default-artifact-root ${ARTIFACT_STORE} \
