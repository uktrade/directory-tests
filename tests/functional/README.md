DIT - Functional Tests
----------------------------------

This repository contains UI tests automated using:
* [Behave](https://pythonhosted.org/behave/)


**IMPORTANT NOTE**

Functional tests use `requests` library to perform all requests.
It means no browser is used to execute test scenarios defined in feature files.


# Requirements

* python 3.6
* pip
* required environment variables (see [env.json](../../docker/env.json)
* dependencies listed in [requirements_functional.txt](../../requirements_functional.txt)


# Installation

* Create a dedicated virtualenv → `mkvirtualenv -p python3.6 functional`
* Install dependencies from [requirements_functional.txt](../../requirements_functional.txt) → `pip install -r requirements_functional.txt`
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


# Run scenarios locally with "behave" command

Use `behave` command to run scenarios from a specific feature file:
```bash
workon functional
dev
behave features/fas/search.feature
```

This will run all scenarios (even those that should be skipped) from selected feature
file and produce rather verbose output.  
Thus it's better to provide some extra parameter and skip scenarios annotated with
`@wip`, `@skip` or `@fixme` tags, i.e.:

```bash
workon functional
dev
behave -k --format pretty --no-skipped features/fas/search.feature --tags=~@wip --tags=~@skip --tags=~@fixme --stop
```

PS.
* Test execution will also stop on first error because `--stop` parameter was used.
* You can use `--tags=` & `-t` interchangeably.


*IMPORTANT NOTE:*

`Auto-retry` scheme is enabled by default, it means that a test will be marked as
`failed` only when it fails twice in a row.  
If you'd like to disable `auto-retry` scheme, then set `AUTO_RETRY=false`, e.g.:
```bash
workon functional
dev
AUTO_RETRY=false behave -k --format pretty --no-skipped features/fas/search.feature --tags=~@wip --tags=~@skip --tags=~@fixme --stop
```


## Updating list of pre-selected companies

Some functional tests use pre-defined data of randomly selected companies.
This data is stored in [files/companies.json](files/companies.json).
Data in Companies House change quite frequently and because of this some discrepancies
arise once in a while making those tests fail more frequently than usual.
In such situation, updating the list of pre-defined companies might help with following
command might help:
```
make functional_update_companies
```
