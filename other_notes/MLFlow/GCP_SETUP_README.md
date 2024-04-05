# GCP MLFlow Setup

- **[Source](https://github.com/emkademy/mlflow-tracking-server-gcp-deployment)**

## Table of Contents

- [GCP MLFlow Setup](#gcp-mlflow-setup)
  - [Table of Contents](#table-of-contents)
  - [Steps](#steps)
    - [1. Install GCloud SDK](#1-install-gcloud-sdk)
    - [2. Create Database](#2-create-database)
    - [3. Create a Google Storage Cloud Bucket](#3-create-a-google-storage-cloud-bucket)
    - [4. Set Environment Variables](#4-set-environment-variables)
    - [5. Deployment](#5-deployment)
    - [6. Connect To The Server](#6-connect-to-the-server)

## Steps

### 1. Install GCloud SDK

- Check [docs](https://cloud.google.com/sdk/docs/install)

### 2. Create Database

- MLFlow uses a database in order to store logged parameters, and metrics (metadata).
- You can create a serverless PostgreSQL database that is running on GCP by following these steps:
  - Goto `CloudSQL` and create a `serverless PostgreSQL` instance on GCP.
  - Create a new user: `Users` -> `ADD USER ACCOUNT`, and save its password to `GCP Secret Manager`,
  - Create a new database: `Databases` -> `CREATE DATABASE`.
  - To enable only `Private` access, goto `Overview` -> `EDIT` `Connections` -> change `Public IP address` to `Private IP address`. (Optional)

### 3. Create a Google Storage Cloud Bucket

- MLFlow needs a storage to store your artifacts.

### 4. Set Environment Variables

- Create a file in order to set some environment variables.

```.env
# ===========================
# ./envs/.mlflow.prod
# ===========================
# ===== MLFlow =====
PROD_MLFLOW_SERVER_HOST=0.0.0.0
PROD_MLFLOW_SERVER_PORT=5251

# ===== Postgres =====
POSTGRES_CONNECTION_NAME=<postgres-connection-name> (you can find in on GCP -> SQL -> your database -> Connection Name)
POSTGRES_USER=<postgres-username>
POSTGRES_PASSWORD_SECRET_NAME=<postgres-secret-manager-name>
POSTGRES_HOST=<postgres-host>
POSTGRES_PORT=5432
POSTGRES_DATABASE_NAME=<postgres-database-name>

MLFLOW_ARTIFACT_STORE=gs://<your_gsc_bucket>

# ===== General =====
GCP_PROJECT_ID=<gcp-project-id>
PROJECT_NAME=<gcp-project-name>
DOCKER_IMAGE_NAME=${PROJECT_NAME}-mlflow
GCP_DOCKER_REGISTERY_NAME=<gcp-artifact-registery-name>
GCP_DOCKER_REGISTERY_URL=europe-west4-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_DOCKER_REGISTERY_NAME}/${DOCKER_IMAGE_NAME}

IMAGE_NAME=<gcp-machine-image-name> (recommended: ubuntu-2204-jammy-v20230714)
IMAGE_PROJECT_ID=<gcp-machine-image-project-name> (recommended: ubuntu-os-cloud)

# ===== Compute Instance =====
VM_NAME=${PROJECT_NAME}-mlflow
REGION=<region>
ZONE=<zone>
LABELS=<comma-seperated-key-value-pairs>
MACHINE_TYPE=<machine-type>
NETWORK=<network> (recommended: default)
SUBNET=<subnet> (recommended: default)
```

### 5. Deployment

- Once everything is set, you can deploy the MLFlow server by running the following command:

```sh
make deploy IMAGE_TAG=<docker-image-tag>
```

- As `IMAGE_TAG`, you can specify anything you like.
- A docker image will be built and pushed to GCP Docker Registery, and the image will be tagged with the specified `IMAGE_TAG` for versioning purposes.

### 6. Connect To The Server

- This setup doesn't use external IP, you need `ssh tunneling` in order to view the web API.
- Check VM Instances, to see if your VM was created:

```sh
Run gcloud compute ssh <vm-instance-name> --zone <vm-instance-zone> --tunnel-through-iap -- -N -L 610 0:localhost:5251
```

- Click [http://localhost:5251](http://localhost:5251) to access your MLFlow instance.
