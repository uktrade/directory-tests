# directory-tests
[Export Directory integration tests](https://www.directory.exportingisgreat.gov.uk/)

## Build status

[![CircleCI](https://circleci.com/gh/uktrade/directory-tests/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/directory-tests/tree/master)

## Requirements
[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)

Python2 (Locust doesn't work with 3 yet)

## Local installation

    $ git clone https://github.com/uktrade/directory-tests
    $ cd directory-tests
    $ make

## Running
Tests can be run either against locally provisioned environment or any other one, as long as ``DIRECTORY_TESTS_DIRECTORY_API_URL``, ``DIRECTORY_TESTS_DIRECTORY_SSO_URL``, ``DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL`` and ``DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL`` environment variables are set.

## Running load tests

Before running the load tests, you will need to load all the fixtures in tests/fixtures/api-db to the API database. Django's loaddata command should work, for example:

    python manage.py loaddata ../directory-tests/tests/fixtures/api-db/*.json

1) To run tests the way CircleCI does:

    make test

This will run flake8 linting, integration tests and finally load tests. This doesn't do much more than check load tests haven't been broken, however. By default it tests the three servers (UI, SSO & API) with a load of about 2 clients/s on each server for 2.5 minutes (this time period more or less guarantees each endpoint we have tests for gets hit at least once - locust randomizes this, so there's no 100% guarantee).

2) For real load testing:

    make test_load

This runs only the load tests and tests the three servers (UI, SSO & API) with a load of about 50 clients/s on each server and a default of 2 minutes.

The env variables you are likely to need to change (please see the makefile - they are set in the test_load command) are:

- ``LOCUST_TIMEOUT`` The number of seconds you would like the tests to run for
- ``LOCUST_NUM_CLIENTS`` The number of clients per second you would like to test. IMPORTANT: You need to set this to 3 times what you actually want as this is divided equally between 3 servers!
- ``LOCUST_HATCH_RATE`` How the load will grow when you leave the tests running. Presuming you want to start hammering the servers at full load straight away, this needs to be equal to ``LOCUST_NUM_CLIENTS``
- ``SSO_USER_ID`` The sso id of a user that exists on the api site you're testing.
- ``DIRECTORY_API_URL``, ``DIRECTORY_SSO_URL``, ``DIRECTORY_UI_BUYER_URL``, ``DIRECTORY_UI_SUPPLIER_URL`` The urls you want to load test.

You probably won't need to change these but you may also set:

- ``LOCUST_MIN_WAIT`` Minimum waiting time (I think locust takes microseconds here) between the execution of locust tasks. Currently set to 500
- ``LOCUST_MAX_WAIT`` Maximum waiting between the execution of locust tasks (currently set to 6000)

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
