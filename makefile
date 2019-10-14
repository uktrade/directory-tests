ARGUMENTS=$(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

build: docker_integration_tests

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete
	-find . -type f -name "behave.log" -delete
	-rm -fr ./tests/browser/reports/*.xml
	-rm -fr ./tests/functional/reports/*.xml
	-rm -fr ./tests/smoke/reports/*.xml
	-rm -fr ./reports/*.csv

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
		--clients=$$NUM_CLIENTS \
		--hatch-rate=$$HATCH_RATE \
		--only-summary \
		--no-web \
		--csv=./reports/results \
		--run-time=$$RUN_TIME

rudimental_load_test_cms:
	export LOCUST_FILE=./locustfile_rudimental_cms.py; \
	$(LOCUST)

rudimental_load_test_profile:
	export LOCUST_FILE=./locustfile_rudimental_profile.py; \
	$(LOCUST)

rudimental_load_test_fab:
	export LOCUST_FILE=./locustfile_rudimental_fab.py; \
	$(LOCUST)

rudimental_load_test_fas:
	export LOCUST_FILE=./locustfile_rudimental_fas.py; \
	$(LOCUST)

rudimental_load_test_international:
	export LOCUST_FILE=./locustfile_rudimental_international.py; \
	$(LOCUST)

rudimental_load_test_invest:
	export LOCUST_FILE=./locustfile_rudimental_invest.py; \
	$(LOCUST)

rudimental_load_test_isd:
	export LOCUST_FILE=./locustfile_rudimental_isd.py; \
	$(LOCUST)

rudimental_load_test_soo:
	export LOCUST_FILE=./locustfile_rudimental_soo.py; \
	$(LOCUST)

rudimental_load_test_search:
	export LOCUST_FILE=./locustfile_rudimental_search.py; \
	$(LOCUST)

TEST_ENV ?= DEV

smoke_tests:
	pytest --capture=no --verbose --junitxml=tests/smoke/reports/smoke.xml tests/smoke $(PYTEST_ARGS)

functional_tests:
	behave -k --format progress3 --logging-filter=-root --stop --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features ${TAGS}

functional_tests_feature_dir:
	behave -k --format progress3 --logging-filter=-root --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features/${FEATURE_DIR} ${TAGS}

test: smoke_tests functional_tests load_test_minimal

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := \
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -U pip docopt docker-compose && \
	python3 ./docker/env_writer.py --env=$(TEST_ENV) --config=./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

DOCKER_SET_ENV_VARS_FOR_DEV := \
	export DEV_DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com/; \
	export DEV_CMS_API_URL=https://dev.cms.directory.uktrade.io/; \
	export DEV_CONTACT_US_URL=https://contact-us.export.great.gov.uk/; \
	export DEV_PROFILE_URL=https://dev.profile.uktrade.io/; \
	export DEV_SSO_API_URL=https://directory-sso-dev.herokuapp.com/; \
	export DEV_SSO_URL=https://www.dev.sso.uktrade.io/; \
	export DEV_FIND_A_BUYER_URL=https://dev.buyer.directory.uktrade.io/; \
	export DEV_FIND_A_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io/; \
	export DEV_DOMESTIC_URL=https://dev.exportreadiness.directory.uktrade.io/; \
	export DEV_INVEST_URL=https://dev.invest.directory.uktrade.io/; \
	export DEV_SOO_URL=https://selling-online-overseas.export.staging.uktrade.io/

DOCKER_SET_ENV_VARS_FOR_STAGE := \
	export STAGE_DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com/; \
	export STAGE_CMS_API_URL=https://dev.cms.directory.uktrade.io/; \
	export STAGE_CONTACT_US_URL=https://contact-us.export.great.gov.uk/; \
	export STAGE_PROFILE_URL=https://dev.profile.uktrade.io/; \
	export STAGE_SSO_API_URL=https://directory-sso-dev.herokuapp.com/; \
	export STAGE_SSO_URL=https://www.dev.sso.uktrade.io/; \
	export STAGE_FIND_A_BUYER_URL=https://dev.buyer.directory.uktrade.io/; \
	export STAGE_FIND_A_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io/; \
	export STAGE_DOMESTIC_URL=https://dev.exportreadiness.directory.uktrade.io/; \
	export STAGE_INVEST_URL=https://dev.invest.directory.uktrade.io/; \
	export STAGE_SOO_URL=https://selling-online-overseas.export.staging.uktrade.io/

DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep -e directorytests_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_integration_tests: docker_remove_all
	$(DOCKER_SET_ENV_VARS_FOR_$(TEST_ENV)) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose.yml build && \
	docker-compose -f docker-compose.yml run smoke_tests && \
	docker-compose -f docker-compose.yml run functional_tests


BROWSER_SET_DOCKER_ENV_VARS := \
	export CIRCLE_SHA1=$(CIRCLE_SHA1)

BROWSER_DOCKER_COMPOSE_CREATE_ENVS := \
	python3 ./docker/env_writer.py --env=$(TEST_ENV) --config=./docker/env.json

BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := \
	docker-compose -f docker-compose-browser.yml -p browser rm -f && \
	docker-compose -f docker-compose-browser.yml -p browser pull

BROWSER_DOCKER_REMOVE_ALL:
	docker ps -a | \
	grep -e browser_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

BROWSER ?= chrome
HEADLESS ?= false
AUTO_RETRY ?= true
BROWSER_TYPE ?= desktop
VERSION ?= ""

browser_tests_locally:
	cd tests/browser && \
	BROWSER_ENVIRONMENT=local BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave -f pretty --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip --tags=~@decommissioned ${TAGS}

browserstack:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	BROWSER_ENVIRONMENT=remote BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave --format progress3 --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip --tags=~@decommissioned ${TAGS}

docker_browserstack: BROWSER_DOCKER_REMOVE_ALL
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	$(BROWSER_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-browser.yml -p browser build && \
	docker-compose -f docker-compose-browser.yml -p browser run browser_tests

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

find_duplicated_scenario_names: SHELL:=/usr/bin/env bash  # set shell for this target to bash
find_duplicated_scenario_names:
	@diff -u <(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort) \
		<(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort -u)

.PHONY: build clean requirements test docker_remove_all docker_integration_tests smoke_tests load_test load_test_buyer load_test_supplier load_test_sso load_test_minimal functional_tests
