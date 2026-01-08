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

### Example 1

```Dockerfile
# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

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
RUN chmod +x ./docker/run-worker.sh

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Use the non-root user to run our application
USER nonroot

CMD ["bash", "docker/run-worker.sh"]
```

## Multi-Stage Build

### MSB: Example 1

```Dockerfile
# ==============================================================================
# Stage 1: Base Setup
# Use Slim Linux for minimal base image size
# ==============================================================================
FROM python:3.13-slim AS python_base

# Python optimizations to avoid buffering issues and improve performance
ENV PYTHONUNBUFFERED=1
# Enable bytecode compilation for faster imports
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Set working directory for all subsequent commands
WORKDIR /app

# ==============================================================================
# Stage 2: Builder - Install dependencies in isolation
# ==============================================================================
FROM python_base AS builder
# Copy uv package manager from official image for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using cache mount to avoid re-downloading
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ==============================================================================
# Stage 3: Production - Final lightweight image
# ==============================================================================
FROM python_base AS prod

# Create non-root user for security best practices
RUN groupadd -r appuser \
    && useradd -r -g appuser -d /app appuser

WORKDIR /app

# Create directories that the app needs to write to, with proper ownership
RUN mkdir -p models \
    && chown -R appuser:appuser models

# Copy pre-built virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application source code and configuration files (respecting .dockerignore)
# Assign ownership to non-root user
COPY --chown=appuser:appuser . /app

# Make startup scripts executable (must be done before switching to non-root user)
RUN chmod +x /app/docker/*.sh

# Switch to non-root user to run application
USER appuser

# Add virtual environment to PATH for direct command access
ENV PATH="/app/.venv/bin:$PATH"

# ==============================================================================
# Entry point: Default command to run the application
# `CMD`: Used to start the main application at RUN time and NOT build time
# CMD can be overridden at runtime as needed BUT ENTRYPOINT cannot
# Here we default to starting the main app server
# ==============================================================================
CMD ["bash", "docker/run.sh"]
```

### MSB: Example 2

- Using UV package manager with multi-stage build for CPU/GPU support

```Dockerfile
# ==============================================================================
# Stage 1: Base Setup - Choose base image based on build target
# For GPU: use NVIDIA CUDA base (CUDA libs pre-installed, smaller venv)
# For CPU: use slim Python (minimal size)
# ==============================================================================
ARG BASE_IMAGE=python:3.13-slim
FROM ${BASE_IMAGE} AS python_base

# Python optimizations to avoid buffering issues and improve performance
ENV PYTHONUNBUFFERED=1
# UV_COMPILE_BYTECODE: Pre-compile Python files to bytecode for faster startup
ENV UV_COMPILE_BYTECODE=1
# UV_LINK_MODE: Copy packages instead of symlinking (required for mounted volumes)
# Without this, volumes mounted at runtime won't have access to symlinked dependencies
ENV UV_LINK_MODE=copy

WORKDIR /app

# ==============================================================================
# Stage 2: Builder - Install dependencies in isolation
# ==============================================================================
FROM python_base AS builder

# Select Torch index (CPU default, GPU uses CUDA base image + cu124 wheels)
ARG TORCH_INDEX_URL="https://download.pytorch.org/whl/cpu"

# Copy uv package manager from official image for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Copy dependency files only (better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using cache mount to avoid re-downloading
# Only re-runs if uv.lock or pyproject.toml changes
# For GPU builds with NVIDIA base: CUDA libs are in base image, not bundled in venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev \
    --extra-index-url "${TORCH_INDEX_URL}" && \
    # Aggressive cleanup to reduce venv size for CI/CD
    find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type d -name "docs" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type f -name "*.pyc" -delete && \
    find /app/.venv -type f -name "*.pyo" -delete && \
    find /app/.venv -type f -name "*.c" -delete && \
    find /app/.venv -type f -name "*.h" -delete && \
    # Remove pip/setuptools build artifacts
    rm -rf /app/.venv/lib/python*/site-packages/pip/_vendor/distlib/*.exe && \
    rm -rf /app/.venv/lib/python*/site-packages/setuptools/_distutils

# ==============================================================================
# Stage 3: Production - Final lightweight image
# ==============================================================================
FROM python_base AS prod

# Create non-root user for security
# uid=1000, gid=1000: Matches Kubernetes fsGroup and job container permissions
# This ensures worker can read model files downloaded by the job to PVCs
RUN groupadd -r --gid 1000 celeryuser \
    && useradd -r --uid 1000 --gid celeryuser --home /app celeryuser

WORKDIR /app

# Install supervisord for process management in the final image
RUN apt-get update \
    && apt-get install -y --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create directories that the app needs to write to, with proper ownership
RUN mkdir -p models data \
    && chown -R celeryuser:celeryuser models data

# Copy pre-built virtual environment from builder stage (no uv needed in final image)
# Using --link for more efficient copying in BuildKit
COPY --from=builder --link /app/.venv /app/.venv

# Copy application source code and configuration files (respecting .dockerignore)
COPY --chown=celeryuser:celeryuser . /app

# Make startup scripts executable (must be done before switching to non-root user)
RUN chmod +x /app/docker/*.sh

# Switch to non-root user (uid=1000, gid=1000)
# This user will have access to files created by the job (via fsGroup=1000)
USER celeryuser

# Add virtual environment to PATH for direct access to installed packages
ENV PATH="/app/.venv/bin:$PATH"

# ==============================================================================
# Entry point: Default command to run the application
# `CMD`: Used to start the main application at RUN time and NOT build time
# CMD can be overridden at runtime as needed BUT ENTRYPOINT cannot
# Here we default to starting the main app server
# ==============================================================================
CMD ["bash", "docker/run.sh"]
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
    restart: unless-stopped

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
    restart: unless-stopped

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
    restart: unless-stopped

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
    restart: unless-stopped

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
    restart: unless-stopped


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
