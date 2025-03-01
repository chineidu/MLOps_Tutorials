# Docker And Docker-Compose Templates

## Table of Content

- [Docker And Docker-Compose Templates](#docker-and-docker-compose-templates)
  - [Table of Content](#table-of-content)
  - [Dockerfile](#dockerfile)
    - [Poetry Example 1](#poetry-example-1)
    - [Dockerfile: Example 2](#dockerfile-example-2)
  - [Docker-Compose](#docker-compose)
    - [Docker-Compose: Example 1](#docker-compose-example-1)
  - [Example 2](#example-2)
    - [Normal Build](#normal-build)
    - [Multi-Stage Build](#multi-stage-build)

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

## Example 2

- File Structure

```text
├── Dockerfile
├── README.md
├── api
│   ├── init.py
│   ├── config.py
│   ├── main.py
│   ├── routes
│   │   ├── init.py
│   │   └── v1
│   │       ├── init.py
│   │       ├── health.py
│   │       └── prediction.py
│   └── schemas
│       ├── init.py
│       ├── health_schema.py
│       ├── input_schema.py
│       └── output_schema.py
├── config
│   ├── init.py
│   └── config.yaml
├── constraints.txt
├── data
├── docker
│   └── run.sh
├── models
│   └── lightning
│       ├── income_model.ckpt
│       └── model_dependency_2.joblib
├── requirements.txt
├── src
│   ├── init.py
│   ├── config.py
│   ├── custom_datasets.py
│   ├── custom_tokenizers.py
│   ├── lit_train.py
│   ├── ml.py
│   ├── model.py
│   └── utilities.py
└── tokenizers
    └── transactions_tokenizer.json
```

### Normal Build

- Image size: ~ 2.84 GB

```Dockerfile
# Base image
FROM python:3.10-slim

WORKDIR /app

# Copy requirements before the whole app directory, so
# they are only updated when it changes
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    # Install PyTorch (CPU) first
    && pip install --no-cache-dir torch==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu \
    # Install other dependencies
    && pip install --no-cache-dir -r requirements.txt


COPY ./ /app/
COPY ./docker/run.sh /run.sh
RUN chmod +x /run.sh

# Set environment variables
ENV PORT=8000
EXPOSE $PORT

# Entrypoint
CMD ["/run.sh"]
```

### Multi-Stage Build

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
