# Docker And Docker-Compose Templates

## Table of Content

- [Docker And Docker-Compose Templates](#docker-and-docker-compose-templates)
  - [Table of Content](#table-of-content)
  - [Dockerfile](#dockerfile)
    - [Poetry Example 1](#poetry-example-1)
  - [Docker-Compose](#docker-compose)
    - [Docker-Compose: Example 1](#docker-compose-example-1)

## Dockerfile

### Poetry Example 1

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# First copy & install requirements to speed up the build process in case only the code changes.
COPY ["./pyproject.toml", "./poetry.lock", "README.md", "./"]

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-
poetry/poetry/master/get-poetry.py | python -

# Use Poetry to install Python dependencies
RUN /root/.poetry/bin/poetry config virtualenvs.create false \
  && /root/.poetry/bin/poetry install --no-interaction --no-ansi

# Copy the rest of the files.
ADD ["./", "./"]

# Specify the command to run on container start
CMD ["python", "earth_quake_predictor/train.py"]
```

## Docker-Compose

### Docker-Compose: Example 1

```yaml
# ===========================
# docker-compose.yaml
# ===========================
version: "3.8"

services:
  mlflow-db: # 1st service
    image: postgres:16-bullseye
    container_name: mlflow-backend-store # Also used as hostname
    env_file: # Location of file(s) containing the env vars
    - ./.envs/.postgres
    volumes: # Persist the data volume
      - postgresql-data:/var/lib/postgresql/data

  mlflow-server: # 2nd service
    image: local-mlflow-tracking-server
    build:
      context: ./
      dockerfile: ./docker/Dockerfile
      args:
        MLFLOW_ARTIFACT_STORE: ${MLFLOW_ARTIFACT_STORE}
    container_name: local-mlflow-tracking-server
    ports:
      - ${LOCAL_DEV_MLFLOW_SERVER_PORT}:${LOCAL_DEV_MLFLOW_SERVER_PORT}
    depends_on:
      - mlflow-db
    env_file:
      - ./.envs/.postgres
      - ./.envs/.mlflow.dev
      - ./.envs/.mlflow.prod
    volumes:
      - ./:/app
      - artifact-store:/${MLFLOW_ARTIFACT_STORE} # Named volume
    ipc: host

# Named volumes ONLY!
volumes:
  postgresql-data:
  artifact-store:
```
