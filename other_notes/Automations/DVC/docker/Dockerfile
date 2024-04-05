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

# Create the directories.
RUN mkdir -p "${MLFLOW_ARTIFACT_STORE}" /app

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

# Entrypoint to start the MLflow server
CMD ["run-server.sh"]
