GREAT platform - Tests
----------------------

[![circle-ci-image]][circle-ci]
[![snyk-image]][snyk]

Functional (browser & integration), load and smoke tests for [https://www.great.gov.uk](https://www.great.gov.uk).

For installation & configuration instructions please refer to dedicated README:

* [Functional (Browser) tests](tests/browser/README.md)
* [Functional (Integration) tests](tests/functional/README.md)
* [Load tests](tests/load/README.md)
* [Smoke tests](tests/smoke/README.md)


Apart from said test suites this repo also contains:
* a sub-project with shared test code (see [directory_tests_shared](directory_tests_shared/README.md))
* a set of non-functional tests & tasks responsible for:
    * discovering content differences between pages hosted on two different environments (see [content_diff](tests/periodic_tasks/content_diff/README.md)
    * identifying broken and invalid links (see [Dead link checker](#Dead-link-checker)
    * updating Geckoboards with test results and Jira board stats (see [geckoboard_updater](tests/periodic_tasks/geckoboard_updater/README.md))
    * generating simple CMS page status report (see [test_prod_cms_pages](test_prod_cms_pages/README.md))


## Development

### Installing

You'll need [pip](https://pypi.org/project/pip/) to install required dependencies and [virtualenv](https://pypi.org/project/virtualenv/) to create a virtual python environment:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
virtualenv .venv -p python3.8
source .venv/bin/activate
make requirements_{browser|functional|load|periodic_tasks|smoke|tests_shared}
```

or if you use [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) then:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
mkvirtualenv -p python3.8 {browser|functional|load|periodic_tasks|smoke|tests_shared}
make requirements_{browser|functional|load|periodic_tasks|smoke|tests_shared}
```

The latter option is highly recommended as it allow for dependency separation a tad faster test runs or CircleCi.


### Requirements

There are separate sets of `requirement` files for every test suite and also for `periodic tasks` & `directory_tests_shared`.

We use `pip-compile` (part of [pip-tools](https://pypi.org/project/pip-tools/) package) to compile `requirements_*.txt` files from unpinned requirement files.

Unpinned requirements are defined in `requirements_*.in` and corresponding pinned versions are kept in `requirements_*.txt`:

* [directory_tests_shared/requirements.in](directory_tests_shared/requirements.in)
* [requirements_browser.in](requirements_browser.in)
* [requirements_functional.in](requirements_functional.in)
* [requirements_load.in](requirements_load.in)
* [requirements_smoke.in](requirements_smoke.in)
* [periodic tasks & tests](requirements_periodic_tasks.in)
    * common requirements for: `geckoboard_updater`, `content_diff`, `Dead link checker` & `test_prod_cms_pages`


#### Updating requirements_*.txt files

We're using [pip-tools](https://pypi.org/project/pip-tools/) to compile pinned `requirements_*.txt` files.  

Once you add, remove or change any dependency in a `requirements_*.in` file, then use dedicated make targets to compile the requirements file:

* `compile_requirements_browser`
* `compile_requirements_load`
* `compile_requirements_smoke`
* `compile_requirements_tests_shared`
* `compile_requirements_functional`
* `compile_requirements_periodic_tasks`
* `compile_requirements_test_tools`

Or simply use `make compile_all_requirements` to update all at once.


### Env Vars

All required and optional Service URLs and Secrets such as API keys are specified in [env.json](env_vars/env.json).  
In order to run any test suite from this repository locally or remotely you'll have to have all of them exported to your shell.  

The reason why those env vars are specified in aforementioned `env.json` is because initially the tests we executed locally in docker containers and later on also in CircleCI.  
Setting env vars for a docker container via [env_file](https://docs.docker.com/compose/env-file/) requires a simple `key:val` file.
On the other hand CircleCI allows you to: either use a shell script that uses `export` command to set env vars or define env vars in project settings.
The latter solution is preferred but it's not ideal because there's no easy way to have a single project in CircleCI with different sets of secrets for different test environments.  
Moreover exporting env vars locally requires a shell script that use `export` command to do the same.  

In order to address all of those requirements and have only one place where we specify all mandatory (and optional) env vars (for all test environments)
we've decided to use env vars prefixed with test environment name (e.g. `DEV_`, `STAGE_`, `UAT_`, & `PROD_`).  
We've also wrote a simple script [env_vars/env_writer.py](env_vars/env_writer.py) that:  

* checks if all env vars are set
* and saves "unprefixed" env vars in files that can be used by locally, in a docker container or on a CI to export env vars.

#### env_writer.py

This scripts takes two arguments:
* `--env` - look for environment variables prefixed with "`ENV_`", where `ENV` can be e.g.: `DEV`, `STAGE`, `UAT` or `PROD`
* `--config` - specify input config file [defaults to: ./env_vars/env.json] with a list of required and optional env vars and output `file_path`.

It'll will be explain how it works with a quasi-BDD scenarios:

**Given** that `env.json` specifies two required env vars e.g.: "`CMS_API_KEY`" & "`CMS_API_URL`"  
**When** `env_writer.py` is executed with `--env=DEV` and `--config=env.json`  
**Then** it will look for "`DEV_CMS_API_KEY`" & "`DEV_CMS_API_URL`" env vars  
**And** it will generate two env files if both env vars were found  
    1) `.env_with_export` - basically a shell script which sets env vars with `export` command. This one is to use with `source` or `.` shell commands.  
    2) `.env_without_export` - a simple `key:val` file. This one can be used by `docker` or `docker-compose`.  
**Or** it will raise an exception if any required env var wasn't found

Using env vars with test environment prefixes allowed us to keep multiple sets of secrets in one CircleCI project.  

#### Convenience shell scripts

You can find convenience shell scripts that set all required env vars for DEV, Staging & UAT environments in Rattic (look for `DIT test env vars`).
These scripts will allow you to run any test suite locally against specific test environment.

Once you get hold of those shell scripts, you can create handy aliases to quickly change between configurations:

```bash
alias dev='source ~/dir-dev.sh';
alias stage='source ~/dir-stage.sh';
alias uat='source ~/dir-uat.sh';
alias geckoboard='source ~/geckoboard.sh';
alias periodic='source ~/periodic.sh';
```

## Dead link checker

"Dead link checker" is a simple tests that use [pylinkvalidator](https://pypi.org/project/pylinkvalidator/) to crawl
a web site and report link errors like 500 ISE or 404.

The main `makefile` includes dedicated [makefile_dead_link_checker.mk](makefile_dead_link_checker.mk).
It specifies targets to run "Dead link checker" test against specific test environment.

"Dead link checker" is controller with 3 env vars:
* `TEST_ENV` - name of the test environment, use `DEV`, `STAGE`, `UAT` or `PROD`
* `{DEV|STAGE|UAT}_BASICAUTH_USER` - username for IP Filtering Service authentication (required for all non `PROD` environments)
* `{DEV|STAGE|UAT}_BASICAUTH_PASS` - password for IP Filtering Service authentication (required for all non `PROD` environments)

Given that you'd like to run this test locally against `DEV` environment,
 you can export `DEV_BASICAUTH_USER` & `DEV_BASICAUTH_PASS` env vars and run the test with:
```bash
TEST_ENV=DEV make dead_links_check
```

or explicitly pass them to the target:
```bash
TEST_ENV=DEV DEV_BASICAUTH_USER=some_user DEV_BASICAUTH_PASS=some_password make dead_links_check
```

You can ask WebOps team for credentials to IP Filtering Service or find them in Rattic.


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
