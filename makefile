build: exred_docker_browserstack docker_integration_tests 

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
PYTEST_ARGS :=
	--capture=no \
	--driver PhantomJS \
	--driver-path /usr/bin/phantomjs $(pytest_args)

SET_PYTEST_ENV_VARS := \
	export API_CLIENT_KEY=debug; \
	export DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com; \
	export DIRECTORY_BUYER_API_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_SSO_URL=https://www.dev.sso.uktrade.io; \
	export DIRECTORY_PROFILE_URL=https://dev.profile.uktrade.io; \
	export DIRECTORY_UI_BUYER_URL=https://dev.buyer.directory.uktrade.io; \
	export DIRECTORY_UI_SUPPLIER_URL=https://dev.supplier.directory.uktrade.io; \
	export SSO_USER_ID=120

selenium_tests:
	$(SET_PYTEST_ENV_VARS); \
	pytest tests/selenium $(PYTEST_ARGS)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose rm -f && docker-compose pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json
DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := docker-compose rm && docker-compose pull

smoke_tests:
	$(SET_PYTEST_ENV_VARS) && \
	pytest --junitxml=tests/smoke/reports/smoke.xml tests/smoke $(pytest_args)

SET_PYLINK_CHECKER_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk,https://euipo.europa.eu/,http://www.kwintessential.co.uk/resources/guides/,https://www.ukbaa.org.uk/,http://gb.kompass.com/,https://ico.org.uk/concerns/getting/,http://www.iata.org/whatwedo/cargo/e/efreight/Pages/index.aspx,https://developer.google.com/,http://www.yellow.com,https://www.contactus.trade.gov.uk,https://trade.great.gov.uk/search/,https://trade.great.gov.uk/suppliers/" && \
	export TEST_URLS="https://www.great.gov.uk/ https://www.export.great.gov.uk/ https://find-a-buyer.export.great.gov.uk/ https://sso.trade.great.gov.uk/accounts/login/ https://trade.great.gov.uk/ https://profile.great.gov.uk/about/"

SET_PYLINK_CHECKER_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk,https://euipo.europa.eu/,http://www.kwintessential.co.uk/resources/guides/,https://www.ukbaa.org.uk/,http://gb.kompass.com/,https://ico.org.uk/concerns/getting/,http://www.iata.org/whatwedo/cargo/e/efreight/Pages/index.aspx,https://developer.google.com/,http://www.yellow.com,https://www.contactus.trade.gov.uk,https://stage.supplier.directory.uktrade.io/search/,https://stage.supplier.directory.uktrade.io/suppliers/" && \
	export TEST_URLS="https://export.great.uat.uktrade.io/ https://stage.buyer.directory.uktrade.io/ https://stage.sso.uktrade.io/accounts/login/  https://stage.profile.uktrade.io/about/"

SET_PYLINK_CHECKER_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk,https://euipo.europa.eu/,http://www.kwintessential.co.uk/resources/guides/,https://www.ukbaa.org.uk/,http://gb.kompass.com/,https://ico.org.uk/concerns/getting/,http://www.iata.org/whatwedo/cargo/e/efreight/Pages/index.aspx,https://developer.google.com/,http://www.yellow.com,https://www.contactus.trade.gov.uk,https://dev.supplier.directory.uktrade.io/search/,https://dev.supplier.directory.uktrade.io/suppliers/" && \
	export TEST_URLS="https://dev.exportreadiness.directory.uktrade.io/ https://dev.buyer.directory.uktrade.io/ https://www.dev.sso.uktrade.io/accounts/login/  https://dev.profile.uktrade.io/about/"

# default to DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

smoke_tests_links_checker:
	$(SET_PYLINK_CHECKER_ENV_VARS_$(TEST_ENV)) && \
	echo "Running pylinkchecker agaisnt: $${TEST_URLS} environment" && \
	pylinkvalidate.py \
	    --progress \
	    --timeout=55 \
	    --depth=2 \
	    --workers=10 \
	    --types=a \
	    --test-outside \
	    --parser=lxml \
	    --header="User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)" \
	    --ignore="$${IGNORED_PREFIXES}" \
	    $${TEST_URLS}

SET_DB_URLS := \
	export DIR_DATABASE_URL=`heroku config:get DATABASE_URL -a directory-api-dev` && \
	export SSO_DATABASE_URL=`heroku config:get DATABASE_URL -a directory-sso-dev`

functional_tests:
	$(SET_PYTEST_ENV_VARS) && \
	$(SET_DB_URLS) && \
	behave -k --format progress3 --stop --tags=-wip --tags=-skip --tags=~fixme tests/functional/features $(BEHAVE_ARGS)

functional_tests_feature_dir:
	$(SET_PYTEST_ENV_VARS) && \
	$(SET_DB_URLS) && \
	behave -k --format progress3 --stop --tags=-wip --tags=-skip --tags=~fixme tests/functional/features/${FEATURE_DIR} $(BEHAVE_ARGS)

functional_update_companies:
	$(SET_PYTEST_ENV_VARS) && \
	$(SET_DB_URLS) && \
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


EXRED_SET_DOCKER_ENV_VARS := \
	export EXRED_TESTS_EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io
	export EXRED_TESTS_CIRCLE_SHA1=$(CIRCLE_SHA1)

EXRED_SET_LOCAL_ENV_VARS := \
	export EXRED_UI_URL=https://dev.exportreadiness.directory.uktrade.io

EXRED_DOCKER_COMPOSE_CREATE_ENVS := \
	python ./docker/env_writer.py ./docker/env_exred.json

EXRED_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL := \
	docker-compose -f docker-compose-exred.yml -p exred rm -f && \
	docker-compose -f docker-compose-exred.yml -p exred pull

EXRED_DOCKER_REMOVE_ALL:
	docker ps -a | \
	grep -e exred_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

exred_local:
	$(EXRED_SET_LOCAL_ENV_VARS) && \
	cd tests/exred && paver run --config=local --browsers=${BROWSERS} --tag=${TAG}

exred_browserstack:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	$(SET_DB_URLS) && \
	cd tests/exred && \
	paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS}

exred_browserstack_first_browser_set:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	cd tests/exred && \
	paver run --config=browserstack-first-browser-set --tag=${TAG}

exred_browserstack_second_browser_set:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	cd tests/exred && \
	paver run --config=browserstack-second-browser-set --tag=${TAG}

exred_browserstack_single:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	cd tests/exred && paver run --config=browserstack-single --browsers=${BROWSERS} --versions=${VERSIONS} --tag=${TAG}

exred_docker_browserstack_first_browser_set: EXRED_DOCKER_REMOVE_ALL
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	$(EXRED_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(EXRED_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-exred.yml -p exred build && \
	docker-compose -f docker-compose-exred.yml -p exred run tests_first_browser_set

exred_docker_browserstack_second_browser_set:
	$(EXRED_SET_DOCKER_ENV_VARS) && \
	$(EXRED_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(EXRED_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-exred.yml -p exred build && \
	docker-compose -f docker-compose-exred.yml -p exred run tests_second_browser_set

compile_requirements:
	python3 -m piptools compile requirements.in

compile_exred_requirements:
	python3 -m piptools compile requirements_exred.in

compile_functional_requirements:
	python3 -m piptools compile requirements_functional.in

compile_smoke_requirements:
	python3 -m piptools compile requirements_smoke.in

compile_selenium_requirements:
	python3 -m piptools compile requirements_selenium.in

compile_load_requirements:
	python3 -m piptools compile requirements_load.in

compile_all_requirements: compile_requirements compile_exred_requirements compile_functional_requirements compile_smoke_requirements compile_selenium_requirements compile_load_requirements

.PHONY: build clean requirements test docker_remove_all docker_integration_tests smoke_tests exred_docker_browserstack load_test load_test_buyer load_test_supplier load_test_sso load_test_minimal functional_tests pep8
