# directory-tests
[Export Directory integration tests](https://www.directory.exportingisgreat.gov.uk/)

## Build status

[![CircleCI](https://circleci.com/gh/uktrade/directory-tests/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/directory-tests/tree/master)

## Requirements
[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)

## Local installation

    $ git clone https://github.com/uktrade/directory-tests
    $ cd directory-tests
    $ make

## Running with Docker

### Against any environment
Requires all host environment variables to be set.

    $ make docker_run

### Against locally provisioned environment
Provides defaults for all env vars but ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``

    $ make docker_run_local

### Provision local environment and open shell

    $ make docker_shell

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json`` and ``env-postgres.json``) by ``make docker_test``, based on host environment variables for each service.

#### directory-tests
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_TESTS_DIRECTORY_API_URL | DIRECTORY_API_URL |
| DIRECTORY_TESTS_DIRECTORY_UI_URL | DIRECTORY_UI_URL |


#### directory-api webserver, queue worker and database
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

#### directory-ui webserver
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_UI_SECRET_KEY | SECRET_KEY |
| DIRECTORY_UI_PORT | PORT |
| DIRECTORY_UI_API_CLIENT_API_KEY | API_CLIENT_API_KEY |
| DIRECTORY_UI_API_CLIENT_BASE_URL | API_CLIENT_BASE_URL |
