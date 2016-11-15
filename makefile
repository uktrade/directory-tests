build: docker_run_local

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

requirements:
	pip install -r requirements.txt

FLAKE8 := flake8 .
LOCUST := \
	locust \
		--locustfile ./locustfile.py \
		--clients=$$LOCUST_NUM_CLIENTS \
		--hatch-rate=$$LOCUST_HATCH_RATE \
		--no-web \
		--only-summary

PYTEST := \
	pytest tests \
		--capture=no \
		--driver PhantomJS \
		--driver-path /usr/bin/phantomjs $(pytest_args) \
		$(pytest_args)


DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS_LOCAL := ./docker/create_envs.sh
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose -f docker-compose.yml -f docker-compose-local.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-local.yml pull

SET_LOCAL_LOCUST_ENV_VARS := \
	export DIRECTORY_API_URL=http://www.api.dev.playground.directory.uktrade.io/; \
	export DIRECTORY_SSO_URL=http://www.sso.dev.playground.directory.uktrade.io/; \
	export DIRECTORY_UI_URL=http://www.dev.playground.directory.uktrade.io/; \
	export LOCUST_NUM_CLIENTS=5; \
	export LOCUST_HATCH_RATE=5; \
	export SSO_USER_ID=120

SET_LOCAL_LOCUST_PROPER_LOAD := \
	export LOCUST_NUM_CLIENTS=150; \
	export LOCUST_HATCH_RATE=150; \
	export LOCUST_TIMEOUT=120

# TODO: set these to docker network names when docker works fully
SET_LOCAL_PYTEST_ENV_VARS := \
	export DIRECTORY_API_URL=http://directory_api_webserver:8000/; \
	export DIRECTORY_SSO_URL=http://sso.trade.great.docker:8003/; \
	export DIRECTORY_UI_URL=http://find-a-buyer.trade.great.docker:8001/; \
	export SSO_USER_ID=120


# make test_load is the command for actual load test running
# unlike make test, this will run load tests with the proper load
# we're testing for
test_load:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(SET_LOCAL_LOCUST_PROPER_LOAD); \
	$(LOCUST)

# make test is what CircleCI runs. Load tests on CircleCI are run at
# 1 client per second, just to check the load tests themselves work.
test_load_minimal:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(LOCUST)

test_integration:
	$(SET_LOCAL_PYTEST_ENV_VARS); \
	$(PYTEST)

test_linting:
	$(FLAKE8)

test: test_linting test_integration test_load_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

DOCKER_SET_DIRECTORY_API_ENV_VARS := \
	export DIRECTORY_API_AWS_ACCESS_KEY_ID=debug; \
	export DIRECTORY_API_AWS_SECRET_ACCESS_KEY=debug; \
	export DIRECTORY_API_AWS_STORAGE_BUCKET_NAME=debug; \
	export DIRECTORY_API_COMPANIES_HOUSE_API_KEY=k_yNNwvPVA5cGyKDsmvQynJ-xUqklr-dVAECYzKY; \
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_FROM=debug; \
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_SUBJECT=debug; \
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_URL=debug ;\
	export DIRECTORY_API_DATABASE_URL=postgres://test:test@postgres:5432/directory_api_test; \
	export DIRECTORY_API_DEBUG=true; \
	export DIRECTORY_API_DEFAULT_FROM_EMAIL=debug; \
	export DIRECTORY_API_EMAIL_HOST=debug; \
	export DIRECTORY_API_EMAIL_HOST_PASSWORD=debug; \
	export DIRECTORY_API_EMAIL_HOST_USER=debug; \
	export DIRECTORY_API_EMAIL_PORT=debug; \
	export DIRECTORY_API_GOV_NOTIFY_API_KEY=debug; \
	export DIRECTORY_API_GOV_NOTIFY_SERVICE_ID=debug; \
	export DIRECTORY_API_GOV_NOTIFY_SERVICE_VERIFICATION_TEMPLATE_NAME=1; \
	export DIRECTORY_API_PORT=8000; \
	export DIRECTORY_API_SECRET_KEY=debug; \
	export DIRECTORY_API_SQS_ENROLMENT_QUEUE_NAME=debug; \
	export DIRECTORY_API_SQS_INVALID_ENROLMENT_QUEUE_NAME=debug; \
	export DIRECTORY_API_UI_SECRET=debug

DOCKER_SET_DIRECTORY_UI_ENV_VARS := \
	export DIRECTORY_UI_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_API_CLIENT_BASE_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_UI_SSO_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_SSO_API_CLIENT_BASE_URL=http://sso.trade.great.docker:8003/api/v1/; \
	export DIRECTORY_UI_SSO_LOGIN_URL=http://sso.trade.great.docker:8003/accounts/login/; \
	export DIRECTORY_UI_SSO_LOGOUT_URL=http://sso.trade.great.docker:8003/accounts/logout/?next=http://find-a-buyer.trade.great.docker:8001; \
	export DIRECTORY_UI_SSO_SIGNUP_URL=http://sso.trade.great.docker:8003/accounts/signup/; \
	export DIRECTORY_UI_SSO_REDIRECT_FIELD_NAME=next; \
	export DIRECTORY_UI_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export DIRECTORY_UI_PORT=8001; \
	export DIRECTORY_UI_SECRET_KEY=debug; \
	export DIRECTORY_UI_DEBUG=true; \
	export DIRECTORY_UI_COMPANIES_HOUSE_SEARCH_URL=https://beta.companieshouse.gov.uk

DOCKER_SET_DIRECTORY_TESTS_ENV_VARS := \
	export DIRECTORY_TESTS_DIRECTORY_API_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_TESTS_DIRECTORY_SSO_URL=http://sso.trade.great.docker:8003/; \
	export DIRECTORY_TESTS_DIRECTORY_UI_URL=http://find-a-buyer.trade.great.docker:8001; \
	export DIRECTORY_TESTS_LOCUST_HATCH_RATE=150; \
	export DIRECTORY_TESTS_LOCUST_NUM_CLIENTS=150; \
	export DIRECTORY_TESTS_DB_NAME=directory_api_test,sso_test; \
	export DIRECTORY_TESTS_DB_PASS=test; \
	export DIRECTORY_TESTS_DB_USER=test; \
	export DIRECTORY_TESTS_API_CLIENT_KEY=$$API_CLIENT_KEY

DOCKER_SET_DIRECTORY_SSO_ENV_VARS := \
	export SSO_PORT=8003; \
	export SSO_DEBUG=true; \
	export SSO_SECRET_KEY=debug; \
	export SSO_API_SECRET=debug; \
	export SSO_DATABASE_URL=postgres://test:test@postgres:5432/sso_test; \
	export SSO_SESSION_COOKIE_DOMAIN=.trade.great.docker; \
	export SSO_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SSO_EMAIL_HOST=debug; \
	export SSO_EMAIL_PORT=debug; \
	export SSO_EMAIL_HOST_USER=debug; \
	export SSO_EMAIL_HOST_PASSWORD=debug; \
	export SSO_DEFAULT_FROM_EMAIL=debug; \
	export SSO_LOGOUT_REDIRECT_URL=http://find-a-buyer.trade.great.docker:8001; \
	export SSO_REDIRECT_FIELD_NAME=next; \
	export SSO_ALLOWED_REDIRECT_DOMAINS=example.com; \
	export SSO_SSO_SESSION_COOKIE_SECURE=false

docker_run: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose run directory_tests


docker_run_local: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS_LOCAL) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local

docker_shell: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS_LOCAL) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local bash

.PHONY: build clean requirements test docker_remove_all docker_run_local docker_run docker_run_with_local
