DIT - Smoke Tests
----------------------------------

Smoke tests are executed using [pytest](https://pypi.org/project/pytest/) library.


**IMPORTANT NOTE**

Majority of `smoke` tests use `requests` library to talk to our services and APIs.  
Some of tests also use: `directory_client_core`, `directory_cms_client` or `directory_sso_api_client`.  


# Requirements

* python 3.6
* pip
* required environment variables (see [env.json](../../env_vars/env.json))
* dependencies listed in [requirements_smoke.txt](../../requirements_smoke.txt)


# Installation

* Create a dedicated virtualenv → `mkvirtualenv -p python3.6 smoke`
* Install dependencies from [requirements_smoke.txt](../../requirements_smoke.txt) → `pip install -r requirements_smoke.txt`
* set required env vars (see [Env Vars](#env-vars))


# Env Vars

Before running tests you'll need to set all required environment variables.  
You can find those variables in Rattic.  

The next steps is to define handy command aliases to make that process as simple as possible:

```bash
alias dev='source ~/dev.sh';
alias stage='source ~/stage.sh';
alias uat='source ~/uat.sh';
```

Once that's done, remember to run `dev`, `stage` or `uat` command prior running tests
against desired environment.


# Run scenarios locally

You can use a dedicated `smoke_tests` target to run all smoke tests:
```bash
workon smoke
dev
PYTEST_ARGS='-m "not stage and not prod"' make smoke_tests
```

* `PYTEST_ARGS` - are used to filter out tests which you don't want to run


You can also use `pytest` command to run scenarios from a specific test file:
```bash
workon smoke
dev
pytest tests/smoke/test_sitemaps.py
```

This will run all tests from selected module (even those that should be skipped) and
hide some logging on error.
Thus it's better to run it with `--capture=no --verbose`:

```bash
workon smoke
dev
pytest --capture=no --verbose tests/smoke/test_sitemaps.py
```

If you'd like to skip tests not meant to be run against currently selected environment,
then use `-m` to filter them out, i.e.:
```bash
pytest --capture=no --verbose tests/smoke/test_cms.py -m "not stage and not prod"
```
Will run all test except for those meant for `staging` and `production` environment.
