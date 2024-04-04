#!/bin/bash

mlflow server -h 0.0.0.0 \
    -p ${LOCAL_DEV_MLFLOW_SERVER_PORT} \
    --backend-store-uri ${MLFLOW_BACKEND_STORE} \
    --default-artifact-root ${MLFLOW_ARTIFACT_STORE} \
