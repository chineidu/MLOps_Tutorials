# Make all targets .PHONY
.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))

# Include environment variables
include ./envs/mlflow_dev.env

# Make all the variables defined in the files above
# accessible throughout the Makefile.
export

# Generate environment variables from the shell
USER_ID=$(shell id -u)
USERNAME=$(shell whoami)

# Docker Compose Commands
DOCKER_COMPOSE_RUN = docker-compose run --rm mlflow-server
DOCKER_COMPOSE_EXEC = docker-compose exec mlflow-server

ifeq (${ENV_NAME}, dev)
	COMPOSE_FILE = docker-compose.yaml
else
	COMPOSE_FILE = docker-compose.prod.yaml
endif

## Set a variable within its context. It'll be used later in the Makefile.
lock-dependencies: BUILD_POETRY_LOCK = /poetry.lock.build

## Makefile Targets
print_compose_file:
	@echo "Using COMPOSE_FILE: $${COMPOSE_FILE}"

postgres: print_compose_file
	@echo " ${MLFLOW_BACKEND_STORE} ${MLFLOW_ARTIFACT_STORE} ${MLFLOW_TRACKING_URI}"
	# @echo $(shell docker-compose run mlflow)
	echo DOCKER_COMPOSE_RUN

## Build the docker image
build: print_compose_file
	docker-compose build

## Stop the docker image
down: print_compose_file
	docker-compose down

## Run the docker image
up: down
	docker-compose up -d

## Run a command in the docker image
exec-in: up
	docker exec -it local-mlflow-tracking-server bash
	# OR
	# ${DOCKER_COMPOSE_EXEC}

notebook: up
	$(DOCKER_COMPOSE_EXEC) jupyter lab --ip 0.0.0.0 --port 8888 --no-browser

## Copy pre-built poetry.lock if available, otherwise generate a new
# lock file with poetry lock.
lock-dependencies:
	${DOCKER_COMPOSE_RUN} bash -c "if [ -e ${BUILD_POETRY_LOCK} ]; then cp ${BUILD_POETRY_LOCK} ./poetry.lock; else poetry lock; fi"

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=36 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
