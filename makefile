build: exred_docker_tests docker_integration_tests 

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

requirements_load:
	pip install -r requirements_load.txt

requirements_smoke:
	pip install -r requirements_smoke.txt

requirements_selenium:
	pip install -r requirements_selenium.txt

requirements_functional:
	pip install -r requirements_functional.txt

pep8:
	flake8 .

# Locust
LOCUST := \
	locust \
		--locustfile $$LOCUST_FILE \
		--clients=$$LOCUST_NUM_CLIENTS \
		--hatch-rate=$$LOCUST_HATCH_RATE \
		--no-web \
		--only-summary

SET_LOCUST_ENV_VARS := \
	export DIRECTORY_API_URL=http://directory-api-dev.herokuapp.com/; \
	export DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io/; \
	export DIRECTORY_UI_BUYER_URL=http://dev.buyer.directory.uktrade.io/; \
	export DIRECTORY_PROFILE_URL=http://www.dev.profile.uktrade.io; \
	export DIRECTORY_UI_SUPPLIER_URL=http://dev.supplier.directory.uktrade.io/; \
	export LOCUST_NUM_CLIENTS=5; \
	export LOCUST_HATCH_RATE=5; \
	export LOCUST_TIMEOUT=120; \
	export SSO_USER_ID=2147483647; \
	export LOCUST_FILE=./locustfile.py

load_test:
	$(SET_LOCUST_ENV_VARS); \
	$(LOCUST)

load_test_buyer:
	$(SET_LOCUST_ENV_VARS); \
	export LOCUST_FILE=./locustfile_buyer.py; \
	$(LOCUST)

load_test_supplier:
	$(SET_LOCUST_ENV_VARS); \
	export LOCUST_FILE=./locustfile_supplier.py; \
	$(LOCUST)

load_test_sso:
	$(SET_LOCUST_ENV_VARS); \
	export LOCUST_FILE=./locustfile_sso.py; \
	$(LOCUST)

load_test_minimal:
	$(SET_LOCUST_ENV_VARS); \
	$(LOCUST)

# Pytest
PYTEST_ARGS :=
	--capture=no \
	--driver PhantomJS \
	--driver-path /usr/bin/phantomjs $(pytest_args)

SET_PYTEST_ENV_VARS := \
	export API_CLIENT_KEY=debug; \
	export DIRECTORY_API_URL=http://directory-api-dev.herokuapp.com; \
	export DIRECTORY_BUYER_API_URL=http://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io; \
	export DIRECTORY_PROFILE_URL=http://dev.profile.uktrade.io; \
	export DIRECTORY_UI_BUYER_URL=http://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_UI_SUPPLIER_URL=http://dev.supplier.directory.uktrade.io; \
	export SSO_USER_ID=120

selenium_tests:
	$(SET_PYTEST_ENV_VARS); \
	pytest tests/selenium $(PYTEST_ARGS)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := ./docker/create_envs.sh ./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

smoke_tests:
	$(SET_PYTEST_ENV_VARS) && \
	pytest tests/smoke $(pytest_args)

SET_DB_URLS := \
	export DIR_DATABASE_URL=`heroku config:get DATABASE_URL -a directory-api-dev` && \
	export SSO_DATABASE_URL=`heroku config:get DATABASE_URL -a directory-sso-dev`

functional_tests:
	$(SET_PYTEST_ENV_VARS) && \
	$(SET_DB_URLS) && \
	behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme tests/functional/features $(BEHAVE_ARGS)

functional_update_companies:
	$(SET_PYTEST_ENV_VARS) && \
	$(SET_DB_URLS) && \
	python -c "from tests.functional.features.pages.utils import update_companies; update_companies()"

test: pep8 smoke_tests integration_test load_test_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

DOCKER_SET_DIRECTORY_TESTS_ENV_VARS := \
	export DIRECTORY_TESTS_DIRECTORY_API_URL=http://directory-api-dev.herokuapp.com; \
	export DIRECTORY_TESTS_DIRECTORY_BUYER_API_URL=http://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_SSO_URL=http://www.dev.sso.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=http://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=http://dev.supplier.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_PROFILE_URL=http://dev.profile.uktrade.io; \
	export DIRECTORY_TESTS_LOCUST_HATCH_RATE=150; \
	export DIRECTORY_TESTS_LOCUST_NUM_CLIENTS=150

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_integration_tests: docker_remove_all
	$(DOCKER_SET_DIRECTORY_TESTS_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run smoke_tests && \
	docker-compose -f docker-compose.yml run functional_tests


EXRED_SET_DOCKER_ENV_VARS := \
	export EXRED_TESTS_EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io

EXRED_SET_LOCAL_ENV_VARS := \
	export EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io

EXRED_DOCKER_COMPOSE_CREATE_ENVS := \
	./docker/create_envs.sh ./docker/env_exred.json

EXRED_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := \
	docker-compose -f docker-compose-exred.yml -p exred rm && \
	docker-compose -f docker-compose-exred.yml -p exred pull

EXRED_DOCKER_REMOVE_ALL:
	docker ps -a | \
	grep -e exred_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

exred_local:
	$(EXRED_SET_LOCAL_ENV_VARS) && \
	cd tests/exred && behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme $(BEHAVE_ARGS)

exred_docker:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	cd tests/exred && paver run parallel

exred_docker_tests: EXRED_DOCKER_REMOVE_ALL
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	$(EXRED_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(EXRED_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-exred.yml -p exred build && \
	docker-compose -f docker-compose-exred.yml -p exred run exred_tests

.PHONY: build clean requirements test docker_remove_all docker_integration_tests smoke_tests exred_docker_tests load_test load_test_buyer load_test_supplier load_test_sso load_test_minimal functional_tests pep8
