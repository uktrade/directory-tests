build: docker_integration_tests 

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

requirements_load:
	pip install -r requirements_load.txt

requirements_smoke:
	pip install -r requirements_smoke.txt

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
		--only-summary \
		--run-time=$$LOCUST_RUN_TIME

SET_LOCUST_ENV_VARS := \
	export DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com/; \
	export DIRECTORY_SSO_URL=https://www.dev.sso.uktrade.io/; \
	export DIRECTORY_UI_BUYER_URL=https://dev.buyer.directory.uktrade.io/; \
	export DIRECTORY_PROFILE_URL=https://www.dev.profile.uktrade.io; \
	export DIRECTORY_UI_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io/; \
	export EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io/; \
	export LOCUST_NUM_CLIENTS=500; \
	export LOCUST_HATCH_RATE=2; \
	export LOCUST_TIMEOUT=30; \
	export LOCUST_RUN_TIME=5m; \
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

load_test_exred:
	$(SET_LOCUST_ENV_VARS); \
	export LOCUST_FILE=./locustfile_exred.py; \
	$(LOCUST)

load_test_minimal:
	$(SET_LOCUST_ENV_VARS); \
	$(LOCUST)

# Pytest
PYTEST_ARGS := \
	--capture=no \
	--driver PhantomJS \
	--driver-path /usr/bin/phantomjs $(pytest_args)

SET_PYTEST_ENV_VARS := \
	export DIRECTORY_API_CLIENT_KEY=debug; \
	export DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com; \
	export DIRECTORY_BUYER_API_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_SSO_URL=https://www.dev.sso.uktrade.io; \
	export DIRECTORY_PROFILE_URL=https://dev.profile.uktrade.io; \
	export DIRECTORY_UI_BUYER_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_UI_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io; \
	export SSO_USER_ID=120

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

smoke_tests:
	$(SET_PYTEST_ENV_VARS) && \
	pytest --maxfail=2 --junitxml=tests/smoke/reports/smoke.xml tests/smoke $(pytest_args)

functional_tests:
	behave -k --format progress3 --logging-filter=-root --stop --tags=-wip --tags=-skip --tags=~fixme tests/functional/features $(BEHAVE_ARGS)

functional_tests_feature_dir:
	behave -k --format progress3 --logging-filter=-root --tags=-wip --tags=-skip --tags=~fixme tests/functional/features/${FEATURE_DIR} $(BEHAVE_ARGS)

functional_update_companies:
	python -c "from tests.functional.utils.generic import update_companies; update_companies()"

test: pep8 smoke_tests integration_test load_test_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

DOCKER_SET_DIRECTORY_TESTS_ENV_VARS := \
	export DIRECTORY_TESTS_DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com; \
	export DIRECTORY_TESTS_DIRECTORY_BUYER_API_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_SSO_URL=https://www.dev.sso.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io; \
	export DIRECTORY_TESTS_DIRECTORY_PROFILE_URL=https://dev.profile.uktrade.io; \
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


BROWSER_SET_DOCKER_ENV_VARS := \
	export BROWSER_TESTS_EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io && \
	export BROWSER_TESTS_CIRCLE_SHA1=$(CIRCLE_SHA1)

BROWSER_SET_LOCAL_ENV_VARS := \
	export EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io

BROWSER_DOCKER_COMPOSE_CREATE_ENVS := \
	python ./docker/env_writer.py ./docker/env_browser.json

BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := \
	docker-compose -f docker-compose-browser.yml -p browser rm -f && \
	docker-compose -f docker-compose-browser.yml -p browser pull

BROWSER_DOCKER_REMOVE_ALL:
	docker ps -a | \
	grep -e browser_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

browser_local:
	$(BROWSER_SET_LOCAL_ENV_VARS) && \
	cd tests/browser && paver run --config=local --browsers=${BROWSERS} --tag=${TAG}

browserstack:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS}

browserstack_first_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-first-browser-set --tag=${TAG}

browserstack_second_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-second-browser-set --tag=${TAG}

browserstack_mobile:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-mobile --browsers=${BROWSERS} --versions=${VERSIONS} --tag=${TAG}

browserstack_single:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tag=${TAG}

docker_browserstack_first_set: BROWSER_DOCKER_REMOVE_ALL
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	$(BROWSER_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-browser.yml -p browser build && \
	docker-compose -f docker-compose-browser.yml -p browser run tests_first_browser_set

docker_browserstack_second_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	$(BROWSER_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-browser.yml -p browser build && \
	docker-compose -f docker-compose-browser.yml -p browser run tests_second_browser_set

compile_requirements:
	python3 -m piptools compile requirements.in

compile_browser_requirements:
	python3 -m piptools compile requirements_browser.in

compile_functional_requirements:
	python3 -m piptools compile requirements_functional.in

compile_smoke_requirements:
	python3 -m piptools compile requirements_smoke.in

compile_load_requirements:
	python3 -m piptools compile requirements_load.in

compile_all_requirements: compile_requirements compile_browser_requirements compile_functional_requirements compile_smoke_requirements compile_load_requirements

.PHONY: build clean requirements test docker_remove_all docker_integration_tests smoke_tests load_test load_test_buyer load_test_supplier load_test_sso load_test_minimal functional_tests pep8
