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
	export API_CLIENT_KEY=debug; \
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
	pytest tests/selenium \
		--capture=no \
		--driver PhantomJS \
		--driver-path /usr/bin/phantomjs $(pytest_args) \
		$(pytest_args)

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

test_smoke: test_smoke_buyer test_smoke_supplier test_smoke_sso

test: test_linting test_smoke test_integration test_load_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

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

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_run_local: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS_LOCAL) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-local.yml build && \
	docker-compose -f docker-compose-local.yml run directory_tests_local

.PHONY: build clean requirements test docker_remove_all docker_run_local
