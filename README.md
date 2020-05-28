GREAT platform - Tests
----------------------

[![circle-ci-image]][circle-ci]
[![snyk-image]][snyk]

Tests for [https://www.great.gov.uk](https://www.great.gov.uk).


## Contents

This repository contains:

* Tests suites:
    * [Functional (Browser) tests](tests/browser/README.md)
    * [Functional (Integration) tests](tests/functional/README.md)
    * [Load tests](tests/load/README.md)
    * [Smoke tests](tests/smoke/README.md)
* [directory_tests_shared](directory_tests_shared/README.md) - a sub-project with shared test code
* Additional non-functional tests & tasks:
    * [Content diff test](tests/periodic_tasks/content_diff/README.md) - discover content differences between the same page but hosted on two different environments
    * [Dead link checker](#Dead-link-checker) - identify broken and invalid links
    * [Geckoboard updater](tests/periodic_tasks/geckoboard_updater/README.md) - update Geckoboards with test results fetched from CircleCI and Jira board stats
    * [CMS page checker and reporter](test_prod_cms_pages/README.md) - two simple CMS related tests/tasks
        * [test_cms_pages_return_200.py](./test_prod_cms_pages/test_cms_pages_return_200.py) - check if all CMS pages can be visited without any error
        * [generate_page_status_report.py](./test_prod_cms_pages/generate_page_status_report.py) - generate a simple CMS page status report


## Development

### General requirements

You'll need:

* Python 3.8+
* [pip](https://pypi.org/project/pip/) to install required dependencies
* [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) to create a virtual python environment

### Installing

Following instructions apply to all test suites and tasks included in this repository.

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
mkvirtualenv -p python3.8 {browser|functional|load|periodic_tasks|smoke|tests_shared}
make requirements_{browser|functional|load|periodic_tasks|smoke|tests_shared}
```

For all additional configuration instructions please check dedicated [README](#Contents).


### Requirements

There are separate sets of `requirement` files for every test suite and also for `periodic tasks` & `directory_tests_shared`.

We use `pip-compile` (part of [pip-tools](https://pypi.org/project/pip-tools/) package) to compile pinned `requirements_*.txt` files from unpinned `requirement_*.in` files.

List of unpinned requirements files for all tests suites, tasks and sub-projects:

* [directory_tests_shared/requirements.in](directory_tests_shared/requirements.in)
* [requirements_browser.in](requirements_browser.in)
* [requirements_functional.in](requirements_functional.in)
* [requirements_load.in](requirements_load.in)
* [requirements_smoke.in](requirements_smoke.in)
* [requirements_periodic_tasks.i](requirements_periodic_tasks.in)
    * this is a common set of requirements for: [Geckoboard updater](tests/periodic_tasks/geckoboard_updater/README.md), [Content diff test](tests/periodic_tasks/content_diff/README.md), [Dead link checker](#Dead-link-checker) & [CMS page checker and reporter](test_prod_cms_pages/README.md)


#### Compiling requirements_*.txt files

To add, remove or change any dependency:
* first edit appropriate `requirements_*.in` file
* do not used pinned version of any dependency (unless the latest version of specific dependency introduced a braking change)
* recompile requirements file
    ```bash
    make compile_requirements_{browser|functional|load|periodic_tasks|smoke|test_tools|tests_shared}
    ```

To recompile all requirement files at once use:
```bash
make compile_all_requirements
```

## Convenience shell scripts

To easily switch between env var configurations for different test environments (DEV, Staging, UAT & periodic tasks),
please use dedicated convenience shell scripts. You can find those scripts in Rattic (look for `DIT test env vars`).  

Once you get hold of them you'll be able to locally run any test suite or task against specific test environment.

To make switching between configurations easier and faster, you can create handy shell aliases, like:

```bash
alias dev='source ~/dir-dev.sh';
alias stage='source ~/dir-stage.sh';
alias uat='source ~/dir-uat.sh';
alias geckoboard='source ~/geckoboard.sh';
alias periodic='source ~/periodic.sh';
```


### Env Vars

All required and optional Service URLs and Secrets such as API keys are specified in [env.json](env_vars/env.json).  
In order to run any test suite or task from this repository, locally or remotely, you'll have to have all of those env vars exported to shell.  

The reason why env vars are specified in aforementioned `env.json` file is because initially the tests we executed locally in docker containers and later on also in CircleCI.  
Setting env vars for a docker container via [env_file](https://docs.docker.com/compose/env-file/) requires a simple `key:val` file.
Whereas CircleCI allows you to either use a shell script that uses `export` command to set env vars or define env vars in project settings.
The latter solution is preferred but it's not ideal because there's no easy way to have a single project in CircleCI with different sets of secrets for different test environments.  
Moreover exporting env vars locally also requires a shell script that use `export` command to do the same.  

In order to address all of those requirements and have only one place where we specify all mandatory (and optional) env vars (for all test environments)
we've decided to use env vars prefixed with the name of test environment e.g. `DEV_`, `STAGE_`, `UAT_`, & `PROD_`.  
We've also wrote a convenience script [env_vars/env_writer.py](env_vars/env_writer.py) which:  

* checks if required env vars are set
* saves env vars without name prefix in files that can be used by locally, in a docker container or on a CI to export env vars.

#### env_writer.py

This scripts takes two arguments:
* `--env` - look for environment variables prefixed with "`ENV_`", where `ENV` can be e.g.: `DEV`, `STAGE`, `UAT` or `PROD`
* `--config` - specify input config file [defaults to: ./env_vars/env.json] with a list of required and optional env vars and output `file_path`.

Lets explain how this script works in a quasi-BDD scenario:

**Given** all required env vars are specified in `env.json` file e.g.: "`CMS_API_KEY`" & "`CMS_API_URL`"  
**When** `env_writer.py` is executed with `--env=DEV` and `--config=env.json`  
**Then** it will check if both "`DEV_CMS_API_KEY`" & "`DEV_CMS_API_URL`" env vars are set  
**And**  it will generate two env files (only if both env vars are set):  
    1) `.env_with_export` - a shell script which sets env vars with `export` command. (can be used with `source` or `.` shell commands)  
    2) `.env_without_export` - a simple `key:val` file. (can be used by `docker` or `docker-compose`)  
**Or** it will raise an exception if any required env var is missing

Using env vars with test environment prefixes allowed us to keep multiple sets of secrets in one CircleCI project.  

## Dead link checker

"Dead link checker" is a simple tests that use [pylinkvalidator](https://pypi.org/project/pylinkvalidator/) to crawl
any web site and report link errors like 500 ISE or 404 Not Found.

The main `makefile` includes a dedicated [makefile_dead_link_checker.mk](makefile_dead_link_checker.mk).  
In that additional `mk` file you'll find targets to run "Dead link checker" test against any test environment.

"Dead link checker" test is controlled with 3 env vars:
* `TEST_ENV` - name of the test environment, use `DEV`, `STAGE`, `UAT` or `PROD`
* `{DEV|STAGE|UAT}_BASICAUTH_USER` - username for IP Filtering Service authentication (required on all non-Production environments)
* `{DEV|STAGE|UAT}_BASICAUTH_PASS` - password for IP Filtering Service authentication (required on all non-Production environments)


To run this test locally against `DEV` environment:

1. Enable venv for periodic tasks (`workon` command is part of [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) package)
    ```bash
    workon periodic_tasks
    ```
2. Export env vars with `dir-dev.sh` convenience script
    ```bash
    # if you configured an alias then:
    dev
    # or source directly with:
    source ~/dir-dev.sh
    ```
3. Run the test
    ```bash
    make dead_links_check
    ```

It is also possible to run this test without using env var convenience script.  
Simply provide all required env vars to the make target:
```bash
workon periodic_tasks
TEST_ENV=DEV DOMESTIC_URL='https://url.to.dev.environment/' DEV_BASICAUTH_USER='username' DEV_BASICAUTH_PASS='password' \
    make dead_links_check
```

You can find credentials for IP Filtering Service:
* in env var convenience scripts
* Rattic
* or ask WebOps team about them


## CircleCI

All test suites, periodic tasks & tests are executed every day (Mon through Fri) in CircleCI against `Dev`, `Staging` & `UAT` environments.

Test workflows are defined in [.circleci/config.yml](.circleci/config.yml#L1259).

Workflows were designed with DRY rule in mind. Code duplication is kept to necessary minimum.

Every workflow consists of one or more jobs. A job is built with multi-step blocks.
Every step should have "Single Responsibility" like installing requirements or running tests.
Thanks to this approach we've reduced code duplication and increased readability.  
More on that topic in CircleCI [Reusable Config Reference Guide](https://circleci.com/docs/2.0/reusing-config/)


[circle-ci-image]: https://circleci.com/gh/uktrade/directory-tests/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-tests/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-tests/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-tests

[snyk-image]: https://snyk.io/test/github/uktrade/directory-tests/badge.svg
[snyk]: https://snyk.io/test/github/uktrade/directory-tests
