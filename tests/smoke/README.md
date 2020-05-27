GREAT platform - Smoke Tests
----------------------------

## Development


### Installing

You'll need [pip](https://pypi.org/project/pip/) to install required dependencies and [virtualenv](https://pypi.org/project/virtualenv/) to create a virtual python environment:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
virtualenv .venv -p python3.8
source .venv/bin/activate
make requirements_smoke
```

or if you use [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) then:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
mkvirtualenv -p python3.8 smoke
make requirements_smoke
```

### Requirements

* python 3.8+
* dependencies from [requirements_smoke.txt](../../requirements_smoke.txt)
* all required env vars exported (e.g. using [Convenience shell scripts](../../README.md#Convenience-shell-scripts))

**IMPORTANT NOTE**

Majority of `smoke` tests use `requests` library to talk to DIT services and APIs.  
Some of tests also use: `directory_cms_client` or `directory_sso_api_client`.  

#### Configuration

Secrets such as API keys and service URLs are specified in [env.json](../../env_vars/env.json).  
You'll need to export all of them to your shell as environment variables prior
to running smoke tests.  
For more instructions please refer to `Env Vars` section of project's main [README](../../README.md#Env-vars).

Furthermore, you can control the execution of smoke tests with `PYTEST_ARGS` env var.  
It is an optional variable that is used to filter out tests which you don't want to run.

### Running the tests

To run smoke tests against specific `TEST_ENV` choose one of the following options:

```bash
TEST_ENV=DEV PYTEST_ARGS='-m "not stage and not uat and not prod"' make smoke_tests
TEST_ENV=STAGE PYTEST_ARGS='-m "not dev and not uat and not prod"' make smoke_tests
TEST_ENV=UAT PYTEST_ARGS='-m "not dev and not stage and not prod"' make smoke_tests
TEST_ENV=PROD PYTEST_ARGS='-m "not dev and not stage and not uat"' make smoke_tests
```

### Running the tests with pytest command

You can also use `pytest` command to run smoke tests:
```bash
pytest tests/smoke/test_sitemaps.py
```
This will run all tests from selected module (even those that should be skipped).

If you'd like to skip tests that are not meant to be run against currently selected environment,
then use `-m` argument to filter them out, i.e.:
```bash
pytest tests/smoke/test_cms.py -m "not stage and not prod"
```

To get a bit better out from `pytests` run it with `--capture=no --verbose`:

```bash
pytest --capture=no --verbose tests/smoke/test_sitemaps.py
```
