ARGUMENTS=$(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))
include *.mk

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete
	-find . -type f -name "behave.log" -delete
	-find ./results/ -type f -not -name '.gitignore' -delete
	-find ./reports/ -type f -not -name '.gitignore' -delete
	-find ./tests/browser/results/ -type f -not -name '.gitignore' -delete
	-find ./tests/browser/reports/ -type f -not -name '.gitignore' -delete
	-rm -fr ./allure_report/
	-rm -fr ./tests/browser/reports/*.xml
	-rm -fr ./tests/functional/reports/*.xml
	-rm -fr ./tests/smoke/reports/*.xml

pep8:
	flake8 .

format:
	@isort --recursive .
	@black .

test_cms_pages_return_200:
	echo "Running CMS pages check against: $(CMS_API_URL)" && \
	pytest --capture=no --verbose --junit-xml=./reports/cms_pages.xml test_prod_cms_pages/ $(PYTEST_ARGS) || true

cms_page_status_report:
	echo "Generating CMS page status report for: $(CMS_API_URL)" && \
	python3 ./test_prod_cms_pages/generate_page_status_report.py

geckoboard_updater:
	PYTHONPATH=. python3 ./tests/periodic_tasks/geckoboard_updater/geckoboard_updater.py

# compare contents of Staging & Dev environments by default
SERVICE ?= invest
ENVS_TO_COMPARE ?= stage_dev

compare_content:
	behave --format=allure_behave.formatter:AllureFormatter --outfile=results/ --junit --junit-directory=./reports/ --no-skipped --format pretty --logging-filter=-root --tags=~@wip ./tests/periodic_tasks/content_diff/features/$(SERVICE)_$(ENVS_TO_COMPARE).feature || true

# Locust
LOCUST := \
	locust \
		--locustfile $$LOCUST_FILE \
		--users=$$NUM_USERS \
		--hatch-rate=$$HATCH_RATE \
		--run-time=$$RUN_TIME \
		--csv=./reports/results \
		--headless || true

load_test_cms:
	export LOCUST_FILE=./locustfile_cms.py; \
	$(LOCUST)

load_test_erp:
	export LOCUST_FILE=./locustfile_erp.py; \
	$(LOCUST)

load_test_profile:
	export LOCUST_FILE=./locustfile_profile.py; \
	$(LOCUST)

load_test_fab:
	export LOCUST_FILE=./locustfile_fab.py; \
	$(LOCUST)

load_test_fas:
	export LOCUST_FILE=./locustfile_fas.py; \
	$(LOCUST)

load_test_international:
	export LOCUST_FILE=./locustfile_international.py; \
	$(LOCUST)

load_test_invest:
	export LOCUST_FILE=./locustfile_invest.py; \
	$(LOCUST)

load_test_isd:
	export LOCUST_FILE=./locustfile_isd.py; \
	$(LOCUST)

load_test_soo:
	export LOCUST_FILE=./locustfile_soo.py; \
	$(LOCUST)

load_test_domestic:
	export LOCUST_FILE=./locustfile_domestic.py; \
	$(LOCUST)

TEST_ENV ?= DEV

smoke_tests:
	pytest --capture=no --verbose --alluredir=results/ --allure-link-pattern=issue:$(BUG_TRACKER_URL_PATTERN) --junitxml=reports/smoke.xml tests/smoke $(PYTEST_ARGS) || true

functional_tests:
	behave --no-skipped --format progress3 --logging-filter=-root --stop --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features ${TAGS}

functional_tests_feature_dir:
	behave --format=allure_behave.formatter:AllureFormatter --define AllureFormatter.issue_pattern=$(BUG_TRACKER_URL_PATTERN) --define AllureFormatter.link_pattern=$(BUG_TRACKER_URL_PATTERN) --outfile=results_${FEATURE_DIR}/ --no-skipped --format progress3 --logging-filter=-root --tags=~@wip --tags=~@skip --tags=~@fixme tests/functional/features/${FEATURE_DIR} ${TAGS} || true

BROWSER ?= chrome
HEADLESS ?= false
AUTO_RETRY ?= true
BROWSER_TYPE ?= desktop
VERSION ?= ""

browser_tests_locally:
	cd tests/browser && \
	BROWSER_ENVIRONMENT=local BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave -f pretty --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip ${TAGS}

browserstack:
	cd tests/browser && \
	BROWSER_ENVIRONMENT=remote BROWSER_TYPE=$(BROWSER_TYPE) BROWSER=$(BROWSER) VERSION=$(VERSION) HEADLESS=$(HEADLESS) AUTO_RETRY=$(AUTO_RETRY) behave --format progress3 --no-skipped --tags=~@wip --tags=~@fixme --tags=~@skip ${TAGS}

requirements_browser:
	pip install -r requirements_browser.txt

requirements_functional:
	pip install -r requirements_functional.txt

requirements_load:
	pip install -r requirements_load.txt

requirements_periodic_tasks:
	pip install -r requirements_periodic_tasks.txt

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

compile_requirements_periodic_tasks:
	@rm -fr requirements_periodic_tasks.txt
	python3 -m piptools compile --quiet requirements_periodic_tasks.in
	@sed -i 's/^\-e file.*/\-e .\/directory_tests_shared\//' requirements_periodic_tasks.txt

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

compile_all_requirements: compile_requirements_tests_shared compile_requirements_browser compile_requirements_functional compile_requirements_periodic_tasks compile_requirements_smoke compile_requirements_load compile_requirements_test_tools

find_duplicated_scenario_names: SHELL:=/usr/bin/env bash  # set shell for this target to bash
find_duplicated_scenario_names:
	@diff -u <(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort) \
		<(behave $(ARGUMENTS) --dry --no-source --no-summary --no-snippets | grep 'Scenario' | sort -u)

results_browser:
	@for directory in $(shell find ./ -maxdepth 1 -iname "results_chrome_*" -type d -printf '%P\n') ; do echo "Processing results from $${directory}"; ./update_results.py "$${directory}" Chrome; mv ./$${directory}/* results/ | true; done
	@for directory in $(shell find ./ -maxdepth 1 -iname "results_firefox_*" -type d -printf '%P\n') ; do echo "Processing results from $${directory}"; ./update_results.py "$${directory}" Firefox; mv ./$${directory}/* results/ | true; done

results_functional:
	@for suite in fas sso profile international ; \
	do \
		if test -d "./results_$$suite"; \
		then \
			if [ -n "$$(ls -A results_$$suite 2>/dev/null)" ]; \
				then \
					./update_results.py results_$$suite $$suite; \
					mv ./results_$$suite/* results/; \
				else \
					echo "./results_$$suite is empty"; \
				fi \
		else \
			echo ./results_$$suite does not exist; \
		fi \
	done

serve:
	@echo Allure
	@allure --version
	@allure serve results/

report:
	@echo Allure
	@allure --version
	@allure generate --clean --output ./allure_report results/

.PHONY: build clean test_cms_pages_return_200 cms_page_status_report compare_content dead_links_check dead_links_check_with_json_report smoke_tests functional_tests results_browser results_functional report
