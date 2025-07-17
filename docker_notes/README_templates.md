# Docker And Docker-Compose Templates

## Table of Content

- [Docker And Docker-Compose Templates](#docker-and-docker-compose-templates)
  - [Table of Content](#table-of-content)
  - [Dockerfile](#dockerfile)
    - [Poetry: Example 1](#poetry-example-1)
    - [Dockerfile: Example 2](#dockerfile-example-2)
    - [UV: Ex 3](#uv-ex-3)
  - [Multi-Stage Build](#multi-stage-build)
  - [Docker-Compose](#docker-compose)
    - [DC: Ex 1](#dc-ex-1)
    - [DC: Ex 2](#dc-ex-2)

## Dockerfile

### Poetry: Example 1

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

### Dockerfile: Example 2

```Dockerfile
# Base image
FROM python:3.10-slim

# 1. Disable Python's output buffering. Useful for debugging.
# 2. Set the environment variables
# 3. LC_ALL and LANG: ensures that the application can handle Unicode characters correctly.
# 4. DEBIAN_FRONTEND: prevents interactive prompts during package installations.
# 5. BUILD_POETRY_LOCK: specify the location of a Poetry lock file.
ENV \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="${HOME}/venv" \
    PATH="${HOME}/venv/bin:${PATH}" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

# Update package info and cleans package management files to optimize image size.
RUN apt-get -qq update \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean


# Set up Poetry for dependency management.
RUN HOME=/tmp pip install --no-cache-dir poetry==1.7.1


# 1. Copy the `pyproject.toml` and lock files (e.g. `*.lock`) to the `/app` directory.
# 2. Set the current working directory to `/app`.
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

# 1. Copy the Docker-related shell scripts to the root directory of the container.
# 2. Using root privileges, set the appropriate permissions for the scripts.
USER root
COPY ./docker/**/*.sh /
RUN chmod +x /*.sh

# 1. Switch to the directory where the project files are located.
COPY . /app/
# Entrypoint to start the MLflow server
CMD ["/startup-script.sh"]
```

### UV: Ex 3

```Dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Make the script executable
RUN chmod +x ./docker/run-producer.sh
# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

CMD ["bash", "docker/run-producer.sh"]

```

## Multi-Stage Build

- Image size: ~ 1.8 GB

```Dockerfile
# Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install build dependencies first
COPY requirements.txt .

# Install dependencies into the virtual environment
RUN pip install --no-cache-dir --upgrade pip \
    # Install PyTorch (CPU) first
    && pip install --no-cache-dir torch==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu \
    # Install other dependencies
    && pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only necessary application files
COPY api/ ./api/
COPY config/ ./config/
COPY docker/run.sh /run.sh
COPY models/ ./models/
COPY src/ ./src/
COPY tokenizers/ ./tokenizers/
RUN chmod +x /run.sh

# Set environment variables
ENV PORT=8000
EXPOSE $PORT

# Use non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Entrypoint
CMD ["/run.sh"]
```

## Docker-Compose

### DC: Ex 1

```yaml
# ===========================
# docker-compose.yaml
# ===========================
version: "3.8"

services:
  mlflow-db: # 1st service
    image: postgres:16-bullseye
    container_name: mlflow-backend-store # Also used as hostname
    env_file: # Location of file(s) containing the env vars. Only accessed by the container.
      - ./.envs/.postgres
    ports:
      - "5432:5432"
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
# Persist data outside the lifecycle of the container.
volumes:
  postgresql-data:
  artifact-store:
```

### DC: Ex 2

```yaml
services:
  local-rabbitmq: # 1st service
    image: rabbitmq:4.0-management
    container_name: local-rabbitmq # Also used as hostname
    env_file: # Location of file(s) containing the env vars. Only accessed by the container.
      - .env
    ports:
      - 5672:5672
      - 15672:15672
    volumes: # Persist the data volume
      - rabbitmq-data:/var/lib/rabbitmq

  worker: # 2nd service
    image: rmq-worker:v1
    build:
      context: ./
      dockerfile: Dockerfile.worker
    # Remove name to allow Docker to automatically generate a name
    # when you have more than one replica
    # container_name: local-rmq-worker
    environment:
      # Env for local deployment
      - RABBITMQ_HOST=local-rabbitmq
    env_file:
      - .env
    volumes:
      - ./db:/app/db  # Bind mount for the data folder
    deploy:
      replicas: 1  # Number of replicas
    develop:
    # Create a `watch` configuration to update the app
      watch:
        - action: sync
          path: ./
          target: /app
          # Folders and files to ignore
          ignore:
            - .venv
        # Rebuild image if any of these files change
        - action: rebuild
          path: ./pyproject.toml
    depends_on:
      - local-rabbitmq

  producer: # 3rd service
    image: rmq-producer:v1
    build:
      context: ./
      dockerfile: Dockerfile.producer
    container_name: local-rmq-producer
    environment:
      - RABBITMQ_HOST=local-rabbitmq
    env_file:
      - .env
    volumes:
      - ./data:/app/data  # Bind mount for the data folder
    develop:
    # Create a `watch` configuration to update the app
      watch:
        - action: sync
          path: ./
          target: /app
          # Folders and files to ignore
          ignore:
            - .venv
            - "**/**/*.ipynb"
        # Rebuild image if any of these files change
        - action: rebuild
          path: ./pyproject.toml
    depends_on:
      - local-rabbitmq


# Named volumes ONLY!
# Persist data outside the lifecycle of the container.
volumes:
  rabbitmq-data:

```

- To start/stop the services:

```sh
# Start all services
docker-compose up

# Build and start all services
docker-compose up --build

# Start all services in the background
docker-compose up -d

#  Start a specific service
docker-compose up -d worker

# Stop a specific service
docker-compose stop worker

# Start with N replicas
# NOTE: The container name of the service must be unique and determined by Docker automatically.
docker-compose up -d --scale worker=N

# Stop all services
docker-compose down
```
