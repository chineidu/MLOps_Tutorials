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
