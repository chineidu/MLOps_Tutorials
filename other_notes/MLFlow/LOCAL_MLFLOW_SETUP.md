<!-- markdownlint-disable-file MD033 MD045-->
# Local MLFlow Setup

## Table of Content

- [Local MLFlow Setup](#local-mlflow-setup)
  - [Table of Content](#table-of-content)
  - [Archtecture](#archtecture)
  - [Setup](#setup)
    - [1. .gitignore](#1-gitignore)
    - [2. Docker-Compose File](#2-docker-compose-file)
    - [Env Variables Example](#env-variables-example)
    - [3. Dockerfile](#3-dockerfile)
    - [4. Shell Script](#4-shell-script)
    - [5. Makefile](#5-makefile)

## Archtecture

- This contains the MLFlow setup for local development and experiment tracking using:
  - `Docker` for local deployment
  - `localhost` as server
  - `local filesystem` as artifacts store
  - and `Postgres` as metadata store (database)

<img src="https://i.postimg.cc/MTyNNx2n/image.png" alt="Local Setuo" width="400" height="400">

## Setup

### 1. .gitignore

```.gitignore
# Ignore all!
.

# Except the following files/directories
!docker
!pyproject.toml

```

### 2. Docker-Compose File

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
      - ./.envs/.mlflow-dev
      - ./.envs/.mlflow-prod
    volumes:
      - ./:/app
      - artifact-store:/${MLFLOW_ARTIFACT_STORE} # Named volume
    ipc: host

# Named volumes ONLY!
volumes:
  postgresql-data:
  artifact-store:

```

### Env Variables Example

```.env
# ===========================
# /.envs/.mlflow-dev
# ===========================
MLFLOW_BACKEND_STORE=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@mlflow-backend-store/${POSTGRES_DB}
MLFLOW_ARTIFACT_STORE=/mlflow-artifact-store
MLFLOW_TRACKING_URI=http://${LOCAL_DEV_MLFLOW_SERVER_HOST}:${LOCAL_DEV_MLFLOW_SERVER_PORT}

# Note: `mlflow-backend-store` is the container name / hostname from a service


# ===========================
# ./.envs/.mlflow-prod
# ===========================
LOCAL_DEV_MLFLOW_SERVER_HOST=127.0.0.1
LOCAL_DEV_MLFLOW_SERVER_PORT=5252
PROD_DEV_MLFLOW_SERVER_PORT=5251


# ===========================
# ./.envs/.postgres
# ===========================
POSTGRES_USER=backend-store
POSTGRES_PASSWORD=backend-store
POSTGRES_DB=backend-store

```

### 3. Dockerfile

```Dockerfile
# ===========================
# ./docker/Dockerfile
# ===========================
# Base image
FROM python:3.11-slim

ARG MLFLOW_ARTIFACT_STORE

# 1. Disable Python's output buffering. Useful for debugging.
# 2. Set the environment variables
# 3. LC_ALL and LANG: ensures that the application can handle Unicode characters correctly.
# 4. DEBIAN_FRONTEND: prevents interactive prompts during package installations.
# 5. BUILD_POETRY_LOCK: specify the location of a Poetry lock file.
ENV \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=${HOME}/venv \
    PATH="${HOME}/venv/bin:${PATH}" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

# Updates package info, install git, and cleans package management files to optimize image size.
# Git was installed because it is required by MLFlow.
RUN apt-get -qq update \
    && apt-get -qq -y install git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# Create the directory with subdirectories.
RUN mkdir -p "${MLFLOW_ARTIFACT_STORE}"/app

# 1. Copy the run-server.sh script for starting the mlflow server
# 2. Make the script executable.
# 3. Adjust PATH so that the script can be accessed from anywhere within the container.
COPY ./docker/run-server.sh /usr/local/bin/run-server.sh
RUN chmod +x /usr/local/bin/run-server.sh
ENV PATH="/usr/local/bin:${PATH}"

# Set up Poetry for dependency management.
RUN HOME=/tmp pip install --no-cache-dir poetry==1.7.1
COPY ./pyproject.toml ./*.lock /app/

WORKDIR /app

# 1. Create a virtual environment,
# 2. Upgrade the pip package manager
# 3. Install project dependencies with poetry
# 4. Copy the dependency lock file
# 5. Clean up the cache directory.
RUN python -m venv "${VIRTUAL_ENV}" \
    && pip install --upgrade pip \
    && poetry install \
    && cp poetry.lock "${BUILD_POETRY_LOCK}" \
    && rm -rf "${HOME}/.cache/*"

CMD ["run-server.sh"]
```

### 4. Shell Script

```sh
# ===========================
# ./docker/run-server.sh
# ===========================
#!/bin/bash

mlflow server -h 0.0.0.0 \
    -p ${LOCAL_DEV_MLFLOW_SERVER_PORT} \
    --backend-store-uri ${MLFLOW_BACKEND_STORE} \
    --default-artifact-root ${MLFLOW_ARTIFACT_STORE} \

```

### 5. Makefile

```Makefile
# ===========================
# ./Makefile
# ===========================
# Include environment variables and export them
include ./.envs/.mlflow-dev
include ./.envs/.mlflow-prod
include ./.envs/.postgres
export # Make all the variables defined in the files above accessible throughout the Makefile.

# Docker Compose Commands
DOCKER_COMPOSE_RUN = docker-compose run --rm mlflow-server
DOCKER_COMPOSE_EXEC = docker-compose exec mlflow-server bash

# Set a variable within its context. It'll be used later in the Makefile.
lock-dependencies: BUILD_POETRY_LOCK = /poetry.lock.build

# Makefile Targets
build: # Build the docker image
    docker-compose build

up: # Run the docker image
    docker-compose up -d

down: # Stop the docker image
    docker-compose down

exec-in: up # Run a command in the docker image
    docker exec -it local-mlflow-tracking-server bash
    # OR
    # ${DOCKER_COMPOSE_EXEC}

lock-dependencies: # Copy pre-built poetry.lock if available, otherwise generate a new lock file with poetry lock.
    ${DOCKER_COMPOSE_RUN} bash -c "if [ -e ${BUILD_POETRY_LOCK} ]; then cp ${BUILD_POETRY_LOCK} ./poetry.lock; else poetry lock; fi"
```
