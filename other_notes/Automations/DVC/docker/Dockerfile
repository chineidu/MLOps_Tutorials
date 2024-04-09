# Base image
FROM python:3.11-slim

ARG MLFLOW_ARTIFACT_STORE
ARG USER_ID
ARG USERNAME
ENV HOME=/home/${USERNAME} \
    VIRTUAL_ENV=/home/${USERNAME}/venv

# 1. Disable Python's output buffering. Useful for debugging.
# 2. Set the environment variables
# 3. LC_ALL and LANG: ensures that the application can handle Unicode characters correctly.
# 4. DEBIAN_FRONTEND: prevents interactive prompts during package installations.
# 5. BUILD_POETRY_LOCK: specify the location of a Poetry lock file.
ENV \
    PYTHONUNBUFFERED=1 \
    PATH="${HOME}/venv/bin:${PATH}" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

# Update package info, install git, and cleans package management files to optimize image size.
# Git was installed because it is required by MLFlow.
RUN apt-get -qq update \
    && apt-get -qq -y install git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# 1. Create a system group and system user and assign the group id to the group.
# 2. Create a system user that's not for interactive login and specify a home directory path for the user.
# 3. Set a user id to the new user and add the user to 2 groups.
RUN addgroup --system --gid ${USER_ID} ${USERNAME} \
    && useradd --system -m --no-log-init --home-dir ${HOME} \
    --uid ${USER_ID} --gid ${USER_ID} ${USERNAME}

# 1. Creates directories (/MLFLOW_ARTIFACT_STORE & /app) using mkdir -p.
# 2. Recursively set ownership (chown -R) of these directories, plus /tmp and user's home to the specified user.
# This ensures the user running the container has access and write permissions to these directories.
RUN chown -R ${USER_NAME}:${USER_NAME} ${HOME}
RUN mkdir -p "${MLFLOW_ARTIFACT_STORE}" /app \
    && chown -R ${USER_NAME}:${USER_NAME} "${MLFLOW_ARTIFACT_STORE}" /app /tmp

# Set up Poetry for dependency management.
RUN HOME=/tmp pip install --no-cache-dir poetry==1.7.1

# 1. Switch the current user to the user specified.
# 2. Copy the `pyproject.toml` and lock files (e.g. `*.lock`) to the `/app` directory.
# 3. Set the current working directory to `/app`.
USER ${USERNAME}
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
COPY ./docker/*.sh /
RUN chmod +x /*.sh

# 1. Switch to the user that was created earlier.
# 2. Switch to the directory where the project files are located.
USER ${USERNAME}
COPY . /app/
# Entrypoint to start the MLflow server
CMD ["/run-server.sh"]
