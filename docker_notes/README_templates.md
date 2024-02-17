# Docker Templates

## Table of Content

- [Docker Templates](#docker-templates)
  - [Table of Content](#table-of-content)
  - [Poetry Example 1](#poetry-example-1)

## Poetry Example 1

```Docker
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
