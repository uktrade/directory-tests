# directory-tests

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

**[Export Directory integration tests](https://www.directory.exportingisgreat.gov.uk/)**

---

## Requirements

* Python3
* [Docker >= 1.10](https://docs.docker.com/engine/installation/)
* [Docker Compose >= 1.8](https://docs.docker.com/compose/install/)
* libpq-dev -> `sudo apt install libpq-dev`

## Local installation

    $ git clone https://github.com/uktrade/directory-tests
    $ cd directory-tests
    $ make

## Updating list of pre-selected companies

Data in Companies House changes fairly frequently.
This can cause some discrepancies with our list of pre-defined companies.
In order to fix this run:
```
make functional_update_companies
```


## Running
Tests can be run either against locally provisioned environment or any other one, as long as:

* ``DIRECTORY_TESTS_DIRECTORY_API_URL``
* ``DIRECTORY_TESTS_DIRECTORY_BUYER_API_URL``
* ``DIRECTORY_TESTS_DIRECTORY_SSO_URL``
* ``DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL``
* ``DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL``
* ``DIRECTORY_TESTS_EXRED_UI_URL``
* ``DIRECTORY_TESTS_S3_SECRET_ACCESS_KEY``
* ``DIRECTORY_TESTS_S3_ACCESS_KEY_ID``
* ``DIRECTORY_TESTS_S3_REGION``
* ``DIRECTORY_TESTS_S3_BUCKET``
* ``DIRECTORY_TESTS_HEROKU_API_KEY``
* ``DIRECTORY_TESTS_SSO_USER_USERNAME``
* ``DIRECTORY_TESTS_SSO_USER_TOKEN``
* ``DIRECTORY_TESTS_SSO_USER_PASSWORD``
* ``DIRECTORY_TESTS_SSO_USER_SSO_ID``
* ``DIRECTORY_TESTS_SSO_UNVERIFIED_USER_TOKEN``

environment variables are set.

## Running tests

Before running the load tests, you will need to load all the fixtures in tests/fixtures/api-db to the API database. Django's loaddata command should work, for example:

    python manage.py loaddata ../directory-tests/tests/fixtures/api-db/*.json

1) To run tests the way CircleCI does:

    make test

This will run flake8 linting, integration tests and finally load tests. This doesn't do much more than check load tests haven't been broken, however. By default it tests the four servers (BUYER, SUPPLIER, SSO & API) with a load of about 2 clients/s on each server for 2.5 minutes (this time period more or less guarantees each endpoint we have tests for gets hit at least once - locust randomizes this, so there's no 100% guarantee).

2) For load testing with proper load (50 clients/s for 2min.):

    make test_load_buyer
    make test_load_supplier
    make test_load_sso
    make test_load_exred

3) To run functional tests locally:

    make functional_tests

4) To run functional tests that match specific tag:
 
    BEHAVE_ARGS="-t tag" make functional_tests 

5) To run functional tests using `behave`:

    behave -k tests/functional/features/
    # or
    behave -k tests/functional/features/ -t tag

6) To run functional tests using PyCharm Pro:

In order to get these tests running in the IDE, you need to set all required 
environment variables in the `run configuration`.

Here's an example how this can be done:
![set required environment variable for test tun configuration](tests/functional/docs/set_env_vars_for_test_run_configuration.gif?raw=true)

Once all required environment variables are set, then simply:

* right-click on the selected scenario you want to run
* and hit "Run '...'"


The env variables you are likely to need to change (please see the makefile - they are set in the test_load command) are:

- ``LOCUST_TIMEOUT`` The number of seconds you would like the tests to run for
- ``LOCUST_NUM_CLIENTS`` The number of clients per second you would like to test.
- ``LOCUST_HATCH_RATE`` How the load will grow when you leave the tests running. Presuming you want to start hammering the servers at full load straight away, this needs to be equal to ``LOCUST_NUM_CLIENTS``
- ``DIRECTORY_API_URL``, ``DIRECTORY_SSO_URL``, ``DIRECTORY_UI_BUYER_URL``, ``DIRECTORY_UI_SUPPLIER_URL``, ``EXRED_UI_URL`` The urls you want to load test.

You probably won't need to change these but you may also set:

- ``LOCUST_MIN_WAIT`` Minimum waiting time (I think locust takes microseconds here) between the execution of locust tasks. Currently set to 500
- ``LOCUST_MAX_WAIT`` Maximum waiting between the execution of locust tasks (currently set to 6000)
- ``SSO_USER_ID`` The sso id of a user that exists on the api site you're testing.

NOTE: Images used for testing image uploads have been taken from https://pixabay.com/

### Provision local environment and run against it
Requires ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` environment variables to be set.

    $ make

### Run against any environment
Requires just ``DIRECTORY_TESTS_DIRECTORY_API_URL``, ``DIRECTORY_TESTS_DIRECTORY_SSO_URL``, ``DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL`` and ``DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL`` environment variables to be set.

    $ make docker_run

### Provision local environment and open shell

    $ make docker_shell

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``./docker/env_writer.py`` based on ``./docker/env.json`` and service env files) by ``make docker_run``, based on host environment variables for each service.

#### directory-tests
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_TESTS_DIRECTORY_API_URL | DIRECTORY_API_URL |
| DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL | DIRECTORY_UI_BUYER_URL |
| DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL | DIRECTORY_UI_SUPPLIER_URL |
| DIRECTORY_TESTS_LOCUST_TIMEOUT | LOCUST_TIMEOUT |
| DIRECTORY_TESTS_LOCUST_NUM_CLIENTS | LOCUST_NUM_CLIENTS |
| DIRECTORY_TESTS_LOCUST_HATCH_RATE | LOCUST_HATCH_RATE |

#### Locally provisioned environment

##### directory-api webserver, queue worker and database
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_API_SQS_REGION_NAME | SQS_REGION_NAME |
| DIRECTORY_API_SQS_ENROLMENT_QUEUE_NAME | SQS_ENROLMENT_QUEUE_NAME |
| DIRECTORY_API_SQS_INVALID_ENROLMENT_QUEUE_NAME | SQS_INVALID_ENROLMENT_QUEUE_NAME |
| DIRECTORY_API_SQS_WAIT_TIME | SQS_WAIT_TIME |
| DIRECTORY_API_SQS_MAX_NUMBER_OF_MESSAGES | SQS_MAX_NUMBER_OF_MESSAGES |
| DIRECTORY_API_SQS_VISIBILITY_TIMEOUT | SQS_VISIBILITY_TIMEOUT |
| DIRECTORY_API_SECRET_KEY | SECRET_KEY |
| DIRECTORY_API_DATABASE_URL | DATABASE_URL |
| DIRECTORY_API_AWS_ACCESS_KEY_ID | AWS_ACCESS_KEY_ID |
| DIRECTORY_API_AWS_SECRET_ACCESS_KEY | AWS_SECRET_ACCESS_KEY |
| DIRECTORY_API_POSTGRES_USER | POSTGRES_USER |
| DIRECTORY_API_POSTGRES_PASSWORD | POSTGRES_PASSWORD |
| DIRECTORY_API_POSTGRES_DB | POSTGRES_DB |

##### directory-ui webserver
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_UI_BUYER_SECRET_KEY | SECRET_KEY |
| DIRECTORY_UI_BUYER_PORT | PORT |
| DIRECTORY_UI_BUYER_API_CLIENT_API_KEY | API_CLIENT_API_KEY |
| DIRECTORY_UI_BUYER_API_CLIENT_BASE_URL | API_CLIENT_BASE_URL |

[code-climate-image]: https://codeclimate.com/github/uktrade/directory-tests/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-tests

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-tests/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-tests/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-tests/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-tests

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-tests.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-tests
