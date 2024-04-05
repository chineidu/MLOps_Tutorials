#!/usr/bin/env bash

set -euo pipefail

# Create VM
gcloud compute instances create "${VM_NAME}" \
  --image "${IMAGE_NAME}" \
  --image-project "${IMAGE_PROJECT_ID}" \
  --boot-disk-auto-delete \
  --labels="${LABELS}" \
  --machine-type="${MACHINE_TYPE}" \
  --zone="${ZONE}" \
  --no-address \
  --network="${NETWORK}" \
  --subnet="${SUBNET}" \
  --scopes https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/cloud.useraccounts.readonly,https://www.googleapis.com/auth/cloudruntimeconfig \
  --project="${GCP_PROJECT_ID}" \
  --metadata-from-file=startup-script=./scripts/startup-script.sh \
  --metadata \
gcp_docker_registery_url="${GCP_DOCKER_REGISTERY_URL}:${IMAGE_TAG}",\
mlflow_host="${MLFLOW_HOST}",\
mlflow_port="${MLFLOW_PORT}",\
artifact_store="${ARTIFACT_STORE}",\
postgres_user="${POSTGRES_USER}",\
postgres_host="${POSTGRES_HOST}",\
postgres_port="${POSTGRES_PORT}",\
postgres_database_name="${POSTGRES_DATABASE_NAME}",\
postgres_password_secret_name="${POSTGRES_PASSWORD_SECRET_NAME}"
