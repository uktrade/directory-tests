build: docker_run_local

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

requirements:
	pip install -r requirements.txt

FLAKE8 := flake8 .
LOCUST := \
	locust \
		--locustfile $$LOCUST_FILE \
		--clients=$$LOCUST_NUM_CLIENTS \
		--hatch-rate=$$LOCUST_HATCH_RATE \
		--no-web \
		--only-summary

PYTEST_ARGS :=
	--capture=no \
	--driver PhantomJS \
	--driver-path /usr/bin/phantomjs $(pytest_args) \
	$(pytest_args)


DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS_LOCAL := ./docker/create_envs.sh
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose -f docker-compose.yml -f docker-compose-local.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-local.yml pull

SET_LOCAL_LOCUST_ENV_VARS := \
	export DIRECTORY_API_URL=http://directory-api-dev.herokuapp.com/; \
	export DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io/; \
	export DIRECTORY_UI_BUYER_URL=http://dev.buyer.directory.uktrade.io/; \
	export DIRECTORY_UI_SUPPLIER_URL=http://dev.supplier.directory.uktrade.io/; \
	export LOCUST_NUM_CLIENTS=5; \
	export LOCUST_HATCH_RATE=5; \
	export SSO_USER_ID=2147483647; \
	export LOCUST_FILE=./locustfile.py

SET_LOCAL_LOCUST_PROPER_LOAD := \
	export LOCUST_NUM_CLIENTS=50; \
	export LOCUST_HATCH_RATE=50; \
	export LOCUST_TIMEOUT=120

SET_LOCAL_LOCUST_BUYER := \
	export LOCUST_FILE=./locustfile_buyer.py

SET_LOCAL_LOCUST_SUPPLIER := \
	export LOCUST_FILE=./locustfile_supplier.py

SET_LOCAL_LOCUST_SSO := \
	export LOCUST_FILE=./locustfile_sso.py

# TODO: set these to docker network names when docker works fully
SET_LOCAL_PYTEST_ENV_VARS := \
	export DIRECTORY_API_URL=http://directory_api_webserver:8000/; \
	export DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io/; \
	export DIRECTORY_UI_BUYER_URL=http://www.dev.buyer.directory.uktrade.io/; \
	export DIRECTORY_UI_SUPPLIER_URL=http://www.dev.supplier.directory.uktrade.io; \
	export SSO_USER_ID=120


SET_LOCAL_SMOKE_TEST_ENV_VARS := \
	export API_CLIENT_KEY=debug; \
	export DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io/; \
	export DIRECTORY_UI_BUYER_URL=http://dev.buyer.directory.uktrade.io/; \
	export DIRECTORY_UI_SUPPLIER_URL=http://dev.supplier.directory.uktrade.io/

# Runs load tests on all servers. Number of defined clients will be
# spread across all servers, so you might want to define LOCUST_NUM_CLIENTS
# differently than for other commands
test_load:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(SET_LOCAL_LOCUST_PROPER_LOAD); \
	$(LOCUST)

test_load_buyer:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(SET_LOCAL_LOCUST_PROPER_LOAD); \
	$(SET_LOCAL_LOCUST_BUYER); \
	$(LOCUST)

test_load_supplier:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(SET_LOCAL_LOCUST_PROPER_LOAD); \
	$(SET_LOCAL_LOCUST_SUPPLIER); \
	$(LOCUST)

test_load_sso:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(SET_LOCAL_LOCUST_PROPER_LOAD); \
	$(SET_LOCAL_LOCUST_SSO); \
	$(LOCUST)

# make test is what CircleCI runs. Load tests on CircleCI are run at
# 1 client per second, just to check the load tests themselves work.
test_load_minimal:
	$(SET_LOCAL_LOCUST_ENV_VARS); \
	$(LOCUST)

test_integration:
	$(SET_LOCAL_PYTEST_ENV_VARS); \
	pytest tests/integration $(PYTEST_ARGS)

test_linting:
	$(FLAKE8)

test_smoke_buyer:
	$(SET_LOCAL_PYTEST_ENV_VARS); \
	$(SET_LOCAL_SMOKE_TEST_ENV_VARS); \
	pytest tests/smoke/test_buyer.py $(PYTEST_ARGS)

test_smoke_supplier:
	$(SET_LOCAL_PYTEST_ENV_VARS); \
	$(SET_LOCAL_SMOKE_TEST_ENV_VARS); \
	pytest tests/smoke/test_supplier.py $(PYTEST_ARGS)

test_smoke_sso:
	$(SET_LOCAL_PYTEST_ENV_VARS); \
	$(SET_LOCAL_SMOKE_TEST_ENV_VARS); \
	pytest tests/smoke/test_sso.py $(PYTEST_ARGS)

test: test_linting test_integration test_load_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

DOCKER_SET_DIRECTORY_API_ENV_VARS := \
	export DIRECTORY_API_PORT=8000; \
	export DIRECTORY_API_DEBUG=true; \
	export DIRECTORY_API_SECRET_KEY=debug; \
	export DIRECTORY_API_UI_SECRET=debug; \
	export DIRECTORY_API_POSTGRES_USER=debug; \
	export DIRECTORY_API_POSTGRES_PASSWORD=debug; \
	export DIRECTORY_API_POSTGRES_DB=directory_api_debug; \
	export DIRECTORY_API_SQS_ENROLMENT_QUEUE_NAME=debug; \
	export DIRECTORY_API_SQS_INVALID_ENROLMENT_QUEUE_NAME=debug; \
	export DIRECTORY_API_DATABASE_URL=postgres://debug:debug@postgres:5432/directory_api_debug; \
	export DIRECTORY_API_COMPANIES_HOUSE_API_KEY=debug; \
	export DIRECTORY_API_GOV_NOTIFY_SERVICE_ID=debug; \
	export DIRECTORY_API_GOV_NOTIFY_API_KEY=debug; \
	export DIRECTORY_API_GOV_NOTIFY_SERVICE_VERIFICATION_TEMPLATE_NAME=1; \
	export DIRECTORY_API_EMAIL_HOST=debug; \
	export DIRECTORY_API_EMAIL_PORT=debug; \
	export DIRECTORY_API_EMAIL_HOST_USER=debug; \
	export DIRECTORY_API_EMAIL_HOST_PASSWORD=debug; \
	export DIRECTORY_API_DEFAULT_FROM_EMAIL=debug; \
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_URL=debug ;\
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_FROM=debug; \
	export DIRECTORY_API_COMPANY_EMAIL_CONFIRMATION_SUBJECT=debug; \
	export DIRECTORY_API_AWS_STORAGE_BUCKET_NAME=debug; \
	export DIRECTORY_API_SESSION_COOKIE_DOMAIN=.great.docker; \
	export DIRECTORY_API_CSRF_COOKIE_SECURE=false; \
	export DIRECTORY_API_SESSION_COOKIE_SECURE=false; \
	export DIRECTORY_API_GECKO_API_KEY=gecko; \
	export DIRECTORY_API_STANNP_API_KEY=debug; \
	export DIRECTORY_API_STANNP_VERIFICATION_LETTER_TEMPLATE_ID=debug; \
	export DIRECTORY_API_STANNP_TEST_MODE=true

DOCKER_SET_DIRECTORY_UI_BUYER_ENV_VARS := \
	export DIRECTORY_UI_BUYER_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_BUYER_API_CLIENT_BASE_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_UI_BUYER_SSO_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_BUYER_SSO_API_CLIENT_BASE_URL=http://www.dev.sso.uktrade.io/api/v1/; \
	export DIRECTORY_UI_BUYER_SSO_LOGIN_URL=http://www.dev.sso.uktrade.io/accounts/login/; \
	export DIRECTORY_UI_BUYER_SSO_LOGOUT_URL=http://www.dev.sso.uktrade.io/accounts/logout/?next=http://www.dev.buyer.directory.uktrade.io; \
	export DIRECTORY_UI_BUYER_SSO_SIGNUP_URL=http://www.dev.sso.uktrade.io/accounts/signup/; \
	export DIRECTORY_UI_BUYER_SSO_REDIRECT_FIELD_NAME=next; \
	export DIRECTORY_UI_BUYER_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export DIRECTORY_UI_BUYER_PORT=8001; \
	export DIRECTORY_UI_BUYER_SECRET_KEY=debug; \
	export DIRECTORY_UI_BUYER_DEBUG=true; \
	export DIRECTORY_UI_BUYER_COMPANIES_HOUSE_SEARCH_URL=https://beta.companieshouse.gov.uk; \
	export DIRECTORY_UI_BUYER_FEATURE_PUBLIC_PROFILES_ENABLED=true; \
	export DIRECTORY_UI_BUYER_SUPPLIER_CASE_STUDY_URL=http://www.dev.supplier.directory.uktrade.io/company/case-study/view/{id}; \
	export DIRECTORY_UI_BUYER_SUPPLIER_PROFILE_LIST_URL=http://www.dev.supplier.directory.uktrade.io/suppliers?sectors={sectors}; \
	export DIRECTORY_UI_BUYER_SUPPLIER_PROFILE_URL=http://www.dev.supplier.directory.uktrade.io/suppliers/{number}

DOCKER_SET_DIRECTORY_UI_SUPPLIER_ENV_VARS := \
	export DIRECTORY_UI_SUPPLIER_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_SUPPLIER_API_CLIENT_BASE_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_UI_SUPPLIER_PORT=8002; \
	export DIRECTORY_UI_SUPPLIER_SECRET_KEY=debug; \
	export DIRECTORY_UI_SUPPLIER_DEBUG=true

DOCKER_SET_DIRECTORY_SSO_PROXY_ENV_VARS := \
	export SSO_PROXY_PORT=8004; \
	export SSO_PROXY_DEBUG=true; \
	export SSO_PROXY_SIGNATURE_SECRET=proxy_signature_debug; \
	export SSO_PROXY_SECRET_KEY=debug; \
	export SSO_PROXY_SSO_UPSTREAM=http://directory_sso_webserver:8003

DOCKER_SET_DIRECTORY_SSO_ENV_VARS := \
	export SSO_PORT=8003; \
	export SSO_DEBUG=true; \
	export SSO_SECRET_KEY=debug; \
	export SSO_API_SIGNATURE_SECRET=api_signature_debug; \
	export SSO_PROXY_SIGNATURE_SECRET=proxy_signature_debug; \
	export SSO_POSTGRES_USER=debug; \
	export SSO_POSTGRES_PASSWORD=debug; \
	export SSO_POSTGRES_DB=sso_debug; \
	export SSO_DATABASE_URL=postgres://debug:debug@postgres:5432/sso_debug; \
	export SSO_SESSION_COOKIE_DOMAIN=.great.docker; \
	export SSO_SSO_SESSION_COOKIE=debug_sso_session_cookie; \
	export SSO_SSO_SESSION_COOKIE_SECURE=false; \
	export SSO_EMAIL_HOST=debug; \
	export SSO_EMAIL_PORT=debug; \
	export SSO_EMAIL_HOST_USER=debug; \
	export SSO_EMAIL_HOST_PASSWORD=debug; \
	export SSO_DEFAULT_FROM_EMAIL=debug; \
	export SSO_LOGOUT_REDIRECT_URL=http://www.dev.buyer.directory.uktrade.io; \
	export SSO_REDIRECT_FIELD_NAME=next; \
	export SSO_ALLOWED_REDIRECT_DOMAINS=gov.uk

DOCKER_SET_DIRECTORY_TESTS_ENV_VARS := \
	export DIRECTORY_TESTS_DIRECTORY_API_URL=http://directory_api_webserver:8000; \
	export DIRECTORY_TESTS_DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io/; \
	export DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=http://www.dev.buyer.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=http://www.dev.supplier.directory.uktrade.io; \
	export DIRECTORY_TESTS_LOCUST_HATCH_RATE=150; \
	export DIRECTORY_TESTS_LOCUST_NUM_CLIENTS=150; \
	export DIRECTORY_TESTS_DB_NAME=directory_api_debug,sso_debug; \
	export DIRECTORY_TESTS_DB_PASS=debug; \
	export DIRECTORY_TESTS_DB_USER=debug; \
	export DIRECTORY_TESTS_API_CLIENT_KEY=debug


docker_run: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose run directory_tests


docker_run_local: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_BUYER_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_SUPPLIER_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_PROXY_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS_LOCAL) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local

docker_shell: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_API_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_BUYER_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_UI_SUPPLIER_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_PROXY_ENV_VARS) && \
	$(DOCKER_SET_DIRECTORY_SSO_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS_LOCAL) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local bash

.PHONY: build clean requirements test docker_remove_all docker_run_local docker_run docker_run_with_local
