build: docker_run_local

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

requirements:
	pip install -r requirements.txt

FLAKE8 := flake8 .
PYTEST := pytest . $(pytest_args)

test:
	$(FLAKE8)
	$(PYTEST)

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-local.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-local.yml pull
DOCKER_COMPOSE_CREATE_ENVS := ./docker/create_envs.sh

DOCKER_SET_DIRECTORY_API_ENV_VARS := \
	export DIRECTORY_API_PORT=8000; \
	export DIRECTORY_API_DEBUG=true; \
	export DIRECTORY_API_SECRET_KEY=test; \
	export DIRECTORY_API_UI_SECRET=test; \
	export DIRECTORY_API_POSTGRES_USER=test; \
	export DIRECTORY_API_POSTGRES_PASSWORD=test; \
	export DIRECTORY_API_POSTGRES_DB=directory_test; \
    export DIRECTORY_API_SQS_ENROLMENT_QUEUE_NAME=directory-enrolment-test; \
    export DIRECTORY_API_SQS_INVALID_ENROLMENT_QUEUE_NAME=directory-enrolment-test-invalid; \
	export DIRECTORY_API_DATABASE_URL=postgres://test:test@postgres:5432/directory_test

DOCKER_SET_DIRECTORY_UI_ENV_VARS := \
	export DIRECTORY_UI_API_CLIENT_API_KEY=test; \
	export DIRECTORY_UI_API_CLIENT_BASE_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_UI_PORT=8001; \
	export DIRECTORY_UI_SECRET_KEY=test; \
	export DIRECTORY_UI_DEBUG=true

DOCKER_SET_DIRECTORY_TESTS_ENV_VARS := \
	export DIRECTORY_TESTS_DIRECTORY_API_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_TESTS_DIRECTORY_UI_URL=http://directory_ui_webserver:8001

docker_run: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose run directory_tests

docker_run_local: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local

docker_shell: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_shell

.PHONY: build clean requirements test docker_remove_all docker_run_local docker_run docker_run_with_local
