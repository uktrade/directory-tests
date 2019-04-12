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

rudimental_load_test_fab:
	export LOCUST_FILE=./locustfile_rudimental_fab.py; \
	$(LOCUST)

rudimental_load_test_fas:
	export LOCUST_FILE=./locustfile_rudimental_fas.py; \
	$(LOCUST)

rudimental_load_test_invest:
	export LOCUST_FILE=./locustfile_rudimental_invest.py; \
	$(LOCUST)

rudimental_load_test_soo:
	export LOCUST_FILE=./locustfile_rudimental_soo.py; \
	$(LOCUST)

rudimental_load_test_search:
	export LOCUST_FILE=./locustfile_rudimental_search.py; \
	$(LOCUST)

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

TEST_ENV ?= DEV

smoke_tests:
	pytest --capture=no --verbose --junitxml=tests/smoke/reports/smoke.xml tests/smoke $(PYTEST_ARGS)

functional_tests:
	behave -k --format progress3 --logging-filter=-root --stop --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features ${TAGS}

functional_tests_feature_dir:
	behave -k --format progress3 --logging-filter=-root --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features/${FEATURE_DIR} ${TAGS}

functional_update_companies:
	python -c "from tests.functional.utils.generic import update_companies; update_companies()"

test: pep8 smoke_tests functional_tests load_test_minimal

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := \
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -U pip docopt docker-compose && \
	python3 ./docker/env_writer.py --env=$(TEST_ENV) --config=./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

DOCKER_SET_ENV_VARS_FOR_DEV := \
	export DEV_DIRECTORY_TESTS_DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_BUYER_API_URL=https://dev.buyer.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_CMS_API_CLIENT_BASE_URL=https://dev.cms.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_CONTACT_US_UI_URL=https://contact-us.export.great.gov.uk/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_PROFILE_URL=https://dev.profile.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_SSO_API_CLIENT_BASE_URL=https://directory-sso-dev.herokuapp.com/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_SSO_URL=https://www.dev.sso.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=https://dev.buyer.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_INVEST_UI_URL=https://dev.invest.directory.uktrade.io/; \
	export DEV_DIRECTORY_TESTS_SOO_UI_URL=https://selling-online-overseas.export.staging.uktrade.io/

DOCKER_SET_ENV_VARS_FOR_STAGE := \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_API_URL=https://directory-api-staging.cloudapps.digital/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_BUYER_API_URL=https://great.uat.uktrade.io/find-a-buyer/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_CMS_API_CLIENT_BASE_URL=https://stage.cms.directory.uktrade.io/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_CONTACT_US_UI_URL=https://contact-us.export.great.gov.uk/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_PROFILE_URL=https://great.uat.uktrade.io/profile/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_SSO_API_CLIENT_BASE_URL=https://directory-sso-staging.cloudapps.digital/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_SSO_URL=https://great.uat.uktrade.io/sso/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=https://great.uat.uktrade.io/find-a-buyer/; \
	export STAGE_DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=https://great.uat.uktrade.io/trade/; \
	export STAGE_DIRECTORY_TESTS_EXRED_UI_URL=https://great.uat.uktrade.io/; \
	export STAGE_DIRECTORY_TESTS_INVEST_UI_URL=https://invest-ui-staging.cloudapps.digital/; \
	export STAGE_DIRECTORY_TESTS_SOO_UI_URL=https://selling-online-overseas.export.staging.uktrade.io/

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
	cd tests/browser && paver run --config=local --browsers=${BROWSERS} --tags="${TAGS}"

browserstack:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tags="${TAGS}"

browserstack_first_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-first-browser-set --tags="${TAGS}"

browserstack_second_set:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	paver run --config=browserstack-second-browser-set --tags="${TAGS}"

browserstack_mobile:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-mobile --browsers=${BROWSERS} --versions=${VERSIONS} --tags="${TAGS}"

browserstack_single:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tags="${TAGS}"

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
