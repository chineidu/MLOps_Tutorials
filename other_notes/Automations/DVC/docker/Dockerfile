# Base image
FROM python:3.11-slim

ARG MLFLOW_ARTIFACTS_STORE

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
    && rm-rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# Create the directory with subdirectories.
RUN mkdir -p "{MLFLOW_BACKEND_STORE}"/app

# 1. Copy the run-server.sh script for starting the mlflow server
# 2. Make the script executable.
# 3. Set up Poetry for dependency management.
# NB: I didn't combine the RUN commands because the temporary HOME var only affects
# Poetry install. If combined, changes to run-server.sh (irrelevant to Poetry) would
# rebuild the whole layer, wasting space
COPY ["./docker/run-server.sh", "./"]
RUN chmod +x ./run-server.sh
RUN HOME=/tmp pip install --no-cache-dir poetry==1.7.1
COPY ["./pyproject.toml", "./poetry.lock", "./"]

WORKDIR /app

RUN python -m venv ${VIRTUAL_ENV} \
    && pip install --upgrade pip \
    && poetry install \
    && cp poetry.lock ${BUILD_POETRY_LOCK} \
    && rm -rf "${HOME}/.cache"

CMD ["./run-server.sh"]
