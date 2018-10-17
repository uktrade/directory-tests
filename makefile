build: docker_integration_tests 

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete
	-find . -type f -name "behave.log" -delete
	-rm -fr ./tests/browser/reports/*.xml
	-rm -fr ./tests/functional/reports/*.xml
	-rm -fr ./tests/smoke/reports/*.xml

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

load_test:
	$(LOCUST)

load_test_cms_api:
	export LOCUST_FILE=./locustfile_cms_api.py; \
	$(LOCUST)

load_test_buyer:
	export LOCUST_FILE=./locustfile_buyer.py; \
	$(LOCUST)

load_test_supplier:
	export LOCUST_FILE=./locustfile_supplier.py; \
	$(LOCUST)

load_test_sso:
	export LOCUST_FILE=./locustfile_sso.py; \
	$(LOCUST)

load_test_exred:
	export LOCUST_FILE=./locustfile_exred.py; \
	$(LOCUST)

load_test_minimal:
	$(LOCUST)

# Pytest
PYTEST_ARGS := \
	--capture=no \
	--driver PhantomJS \
	--driver-path /usr/bin/phantomjs $(pytest_args)

TEST_ENV ?= dev

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := \
	python3 -m venv env_writer && \
	source env_writer/bin/activate && \
	pip install -U pip docopt docker-compose && \
	python3 ./docker/env_writer.py --env=$(TEST_ENV) --config=./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

smoke_tests:
	pytest --junitxml=tests/smoke/reports/smoke.xml tests/smoke $(pytest_args)

functional_tests:
	export extra_tags=$$([ ! -z "$${TAGS}" ] && echo "--tags=$${TAGS}" || echo "") && \
	[ ! -z "$${TAGS}" ] && echo "Will use extra: $${extra_tags}" || echo "No extra tags were provided" && \
	behave -k --format progress3 --logging-filter=-root --stop --tags=-wip --tags=-skip --tags=~fixme tests/functional/features ${extra_tags}

functional_tests_feature_dir:
	export extra_tags=$$([ ! -z "$${TAGS}" ] && echo "--tags=$${TAGS}" || echo "") && \
	[ ! -z "$${TAGS}" ] && echo "Will use extra: $${extra_tags}" || echo "No extra tags were provided" && \
	behave -k --format progress3 --logging-filter=-root --tags=-wip --tags=-skip --tags=~fixme tests/functional/features/${FEATURE_DIR} $${extra_tags}

functional_update_companies:
	python -c "from tests.functional.utils.generic import update_companies; update_companies()"

test: pep8 smoke_tests functional_tests load_test_minimal

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_integration_tests: docker_remove_all
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run smoke_tests && \
	docker-compose -f docker-compose.yml run functional_tests


BROWSER_SET_DOCKER_ENV_VARS := \
	export BROWSER_TESTS_CIRCLE_SHA1=$(CIRCLE_SHA1)

BROWSER_DOCKER_COMPOSE_CREATE_ENVS := \
	python3 ./docker/env_writer.py --env=$(TEST_ENV) --config=./docker/env_browser.json

BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := \
	docker-compose -f docker-compose-browser.yml -p browser rm -f && \
	docker-compose -f docker-compose-browser.yml -p browser pull

BROWSER_DOCKER_REMOVE_ALL:
	docker ps -a | \
	grep -e browser_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

browser_local:
	cd tests/browser && paver run --config=local --browsers=${BROWSERS} --tags=${TAGS}

browserstack:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tags=${TAGS}

browserstack_first_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-first-browser-set --tags=${TAGS}

browserstack_second_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-second-browser-set --tags=${TAGS}

browserstack_mobile:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-mobile --browsers=${BROWSERS} --versions=${VERSIONS} --tags=${TAGS}

browserstack_single:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tags=${TAGS}

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
