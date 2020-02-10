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

pep8:
	flake8 .

format:
	@isort --recursive .
	@black .

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

rudimental_load_test_erp:
	export LOCUST_FILE=./locustfile_rudimental_erp.py; \
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
	pytest --capture=no --verbose --alluredir=results/ --allure-link-pattern=issue:$(BUG_TRACKER_URL_PATTERN) --junitxml=reports/smoke.xml tests/smoke $(PYTEST_ARGS)

functional_tests:
	behave --no-skipped --format progress3 --logging-filter=-root --stop --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features ${TAGS}

functional_tests_feature_dir:
	behave --format=allure_behave.formatter:AllureFormatter --outfile=results_${FEATURE_DIR}/ --no-skipped --format progress3 --logging-filter=-root --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features/${FEATURE_DIR} ${TAGS}

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
	export DEV_CMS_API_URL=https://dev.cms.directory.uktrade.digital/; \
	export DEV_CONTACT_US_URL=https://contact-us.export.great.gov.uk/; \
	export DEV_PROFILE_URL=https://dev.profile.uktrade.digital/; \
	export DEV_SSO_API_URL=https://directory-sso-dev.herokuapp.com/; \
	export DEV_SSO_URL=https://www.dev.sso.uktrade.digital/; \
	export DEV_FIND_A_BUYER_URL=https://dev.buyer.directory.uktrade.digital/; \
	export DEV_FIND_A_SUPPLIER_URL=https://dev.supplier.directory.uktrade.digital/; \
	export DEV_DOMESTIC_URL=https://dev.exportreadiness.directory.uktrade.digital/; \
	export DEV_INVEST_URL=https://dev.invest.directory.uktrade.digital/; \
	export DEV_SOO_URL=https://selling-online-overseas.export.staging.uktrade.digital/

DOCKER_SET_ENV_VARS_FOR_STAGE := \
	export STAGE_DIRECTORY_API_URL=https://directory-api-dev.herokuapp.com/; \
	export STAGE_CMS_API_URL=https://dev.cms.directory.uktrade.digital/; \
	export STAGE_CONTACT_US_URL=https://contact-us.export.great.gov.uk/; \
	export STAGE_PROFILE_URL=https://dev.profile.uktrade.digital/; \
	export STAGE_SSO_API_URL=https://directory-sso-dev.herokuapp.com/; \
	export STAGE_SSO_URL=https://www.dev.sso.uktrade.digital/; \
	export STAGE_FIND_A_BUYER_URL=https://dev.buyer.directory.uktrade.digital/; \
	export STAGE_FIND_A_SUPPLIER_URL=https://dev.supplier.directory.uktrade.digital/; \
	export STAGE_DOMESTIC_URL=https://dev.exportreadiness.directory.uktrade.digital/; \
	export STAGE_INVEST_URL=https://dev.invest.directory.uktrade.digital/; \
	export STAGE_SOO_URL=https://selling-online-overseas.export.staging.uktrade.digital/

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
	BROWSER_ENVIRONMENT=local BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave -f pretty --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip ${TAGS}

browserstack:
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	cd tests/browser && \
	BROWSER_ENVIRONMENT=remote BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave --format progress3 --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip ${TAGS}

docker_browserstack: BROWSER_DOCKER_REMOVE_ALL
	$(BROWSER_SET_DOCKER_ENV_VARS) && \
	$(BROWSER_DOCKER_COMPOSE_CREATE_ENVS) && \
	$(BROWSER_DOCKER_COMPOSE_REMOVE_AND_PULL_LOCAL) && \
	docker-compose -f docker-compose-browser.yml -p browser build && \
	docker-compose -f docker-compose-browser.yml -p browser run browser_tests

requirements_browser:
	pip install -r requirements_browser.txt

requirements_functional:
	pip install -r requirements_functional.txt

requirements_load:
	pip install -r requirements_load.txt

requirements_smoke:
	pip install -r requirements_smoke.txt

requirements_tests_shared:
	pip install -r ./directory_tests_shared/requirements.txt

compile_requirements_browser:
	@rm -fr requirements_browser.txt
	python3 -m piptools compile --quiet requirements_browser.in
	@sed -i '/^file.*/d' requirements_browser.txt
	@sed -i '7i.\/directory_tests_shared\/' requirements_browser.txt

compile_requirements_functional:
	@rm -fr requirements_functional.txt
	python3 -m piptools compile --quiet requirements_functional.in
	@sed -i 's/^\-e file.*/\-e .\/directory_tests_shared\//' requirements_functional.txt

compile_requirements_smoke:
	@rm -fr requirements_smoke.txt
	python3 -m piptools compile --quiet requirements_smoke.in
	@sed -i 's/^\-e file.*/\-e .\/directory_tests_shared\//' requirements_smoke.txt

compile_requirements_load:
	@rm -fr requirements_load.txt
	python3 -m piptools compile --quiet requirements_load.in
	@sed -i 's/^\-e file.*/\-e .\/directory_tests_shared\//' requirements_load.txt

compile_requirements_test_tools:
	@rm -fr requirements_test_tools.txt
	python3 -m piptools compile --quiet requirements_test_tools.in

compile_requirements_tests_shared:
	@rm -fr ./directory_tests_shared/requirements.txt
	python3 -m piptools compile --quiet --no-annotate --output-file ./directory_tests_shared/requirements.txt ./directory_tests_shared/requirements.in

compile_all_requirements: compile_requirements_tests_shared compile_requirements_browser compile_requirements_functional compile_requirements_smoke compile_requirements_load compile_requirements_test_tools

find_duplicated_scenario_names: SHELL:=/usr/bin/env bash  # set shell for this target to bash
find_duplicated_scenario_names:
	@diff -u <(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort) \
		<(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort -u)

results_browser:
	@for directory in $(shell find ./ -maxdepth 1 -iname "results_chrome_*" -type d -printf '%P\n') ; do echo "Processing results from $${directory}"; ./update_results.py "$${directory}" Chrome; mv ./$${directory}/* results/ | true; done
	@for directory in $(shell find ./ -maxdepth 1 -iname "results_firefox_*" -type d -printf '%P\n') ; do echo "Processing results from $${directory}"; ./update_results.py "$${directory}" Firefox; mv ./$${directory}/* results/ | true; done

results_functional:
	@echo "Processing Allure results from functional FAS tests"; ./update_results.py "results_fas" FAS; mv ./results_fas/* results/ | true;
	@echo "Processing Allure results from functional SSO tests"; ./update_results.py "results_sso" SSO; mv ./results_sso/* results/ | true;
	@echo "Processing Allure results from functional Profile tests"; ./update_results.py "results_profile" Profile; mv ./results_profile/* results/ | true;
	@echo "Processing Allure results from functional International tests"; ./update_results.py "results_international" International; mv ./results_international/* results/ | true;

serve:
	@echo Allure
	@allure --version
	@allure serve results/

report:
	@echo Allure
	@allure --version
	@allure generate --output ./reports results/

.PHONY: build clean requirements test docker_remove_all docker_integration_tests smoke_tests load_test load_test_buyer load_test_supplier load_test_sso load_test_minimal functional_tests results_browser results_functional report
