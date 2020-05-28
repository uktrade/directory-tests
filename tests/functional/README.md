GREAT platform - Functional (Integration) Tests
-----------------------------------------------

This repository contains UI tests automated using:
* [Behave](https://pythonhosted.org/behave/)


**IMPORTANT NOTE**

Functional tests use `requests` library to perform all HTTP requests (GET, PUT, DELETE etc).
It means that no browser is used to drive the tests.

## Development

### Requirements

* python 3.8+
* pip
* dependencies listed in [requirements_functional.txt](../../requirements_functional.txt)
* all required env vars exported (e.g. using [Convenience shell scripts](../../README.md#Convenience-shell-scripts))


### How to run tests locally

To run functional tests locally against `DEV` environment:

1. Enable venv for functional tests (`workon` command is part of [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) package)
    ```bash
    workon functional
    ```
2. Export env vars with `dir-dev.sh` convenience script
    ```bash
    # if you configured an alias then:
    dev
    # or source directly with:
    source ~/dir-dev.sh
    ```
3. To run all functional tests:
    ```bash
    TEST_ENV=dev \
       make functional_tests
    ```
4. To run tests for specific service:
    ```bash
    FEATURE_DIR=international TEST_ENV=dev \
       make functional_tests_feature_dir
    ```
5. To disable `AUTO_RETRY` on failures (which is enabled by default):
    ```bash
    FEATURE_DIR=international TEST_ENV=dev AUTO_RETRY=false \
       make functional_tests_feature_dir
    ```
6. To run scenarios annotated with specific tag(s):
    ```bash
    FEATURE_DIR=international TEST_ENV=dev AUTO_RETRY=false TAGS="--tags=~@stage-only --tags=~@uat-only" \
       make functional_tests_feature_dir
    ```


### How to run functional tests locally with "behave" command

To locally run all functional tests with `behave` command simply execute:

```bash
behave tests/functional
```

This will run all scenarios (even those that should be skipped) and produce rather verbose output.  
Thus it's better to provide some extra parameters and skip scenarios annotated with `@wip`, `@skip` or `@fixme` tags, i.e.:

```bash
behave \
    --format pretty \
    --no-skipped \
    --tags=~@wip \
    --tags=~@skip \
    --tags=~@fixme \
    --stop \
    tests/functional/
```

Or execute tests from specific feature file:
```bash
behave \
    --format pretty \
    --no-skipped \
    --tags=~@wip \
    --tags=~@skip \
    --tags=~@fixme \
    --stop \
    tests/functional/features/fas/search.feature
```

*IMPORTANT NOTE:*

`Auto-retry` scheme is enabled by default, it means that a test will be marked as `failed` only when it fails twice in a row.  
If you'd like to disable this feature, then set `AUTO_RETRY` to `false`, e.g.:
```bash
AUTO_RETRY=false \
    behave \
        --format pretty \
        --no-skipped \
        --tags=~@wip \
        --tags=~@skip \
        --tags=~@fixme \
        --stop \
        tests/functiona/features/fas/search.feature
```
