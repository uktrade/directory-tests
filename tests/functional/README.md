GREAT platform - Functional (Integration) Tests
-----------------------------------------------

This repository contains UI tests automated using:
* [Behave](https://pythonhosted.org/behave/)


**IMPORTANT NOTE**

Functional tests use `requests` library to perform all HTTP requests (GET, PUT, DELETE etc).
It means that no browser is used to drive the tests.


# Requirements

* python 3.8+
* pip
* dependencies listed in [requirements_functional.txt](../../requirements_functional.txt)
* all required env vars exported (e.g. using [Convenience shell scripts](../../README.md#Convenience-shell-scripts))


# Installing

You'll need [pip](https://pypi.org/project/pip/) to install required dependencies and [virtualenv](https://pypi.org/project/virtualenv/) to create a virtual python environment:

```bash
git clone https://github.com/uktrade/directory-tests
virtualenv .venv -p python3.8
source .venv/bin/activate
make requirements_functional
```

or if you use [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) then:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
mkvirtualenv -p python3.8 functional
make requirements_functional
```

# Env Vars

Before running tests you'll need to set all required environment variables.  
You can find those variables in Rattic.  

The next steps is to define handy command aliases to make that process as simple as possible:

```bash
source ~/dir-{dev|stage|uat}.sh
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
