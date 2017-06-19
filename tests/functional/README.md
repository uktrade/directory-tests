Functional Test for FAB, FAS & SSO
----------------------------------


# create virtualenv & install dependencies
```bash
virtualenv .venv -p python3.5
source ./.venv/bin/activate
pip install -r requirements.txt
```

# updating the requirements.txt

This project uses [pip-compile](https://pypi.python.org/pypi/pip-tools/) tool to generate `requirements.txt` with 
all project dependencies (and all underlying dependencies) pinned.

If you decide to add new dependency to the project, simply add it to the `requirements.in` and then regenerate 
`requirements.txt` with `pip-compile`:

```bash
pip install pip-tools
pip-compile
```

# Environment variables

Here's a list of environment variables currently required to run the tests.

```shell
export API_CLIENT_KEY=""
export DIRECTORY_API_URL=<MUST_BE_SET>
export DIRECTORY_UI_SUPPLIER_URL=<MUST_BE_SET>
export DIRECTORY_PROFILE_URL=""
export DIRECTORY_SSO_URL=<MUST_BE_SET>
export DIRECTORY_UI_BUYER_URL=<MUST_BE_SET>
export SSO_USER_USERNAME=""
export SSO_USER_TOKEN=""
export SSO_USER_PASSWORD=""
export SSO_USER_SSO_ID=1
export SSO_UNVERIFIED_USER_TOKEN=""
export S3_SECRET_ACCESS_KEY=<MUST_BE_SET>
export S3_ACCESS_KEY_ID=<MUST_BE_SET>
export S3_REGION=<MUST_BE_SET>
export S3_BUCKET=<MUST_BE_SET>
```

or when using `docker`

```commandline
export DIRECTORY_TESTS_API_CLIENT_KEY=""
export DIRECTORY_TESTS_DIRECTORY_API_URL=<MUST_BE_SET>
export DIRECTORY_TESTS_DIRECTORY_UI_SUPPLIER_URL=<MUST_BE_SET>
export DIRECTORY_TESTS_DIRECTORY_PROFILE_URL=""
export DIRECTORY_TESTS_DIRECTORY_SSO_URL=<MUST_BE_SET>
export DIRECTORY_TESTS_DIRECTORY_UI_BUYER_URL=<MUST_BE_SET>
export DIRECTORY_TESTS_SSO_USER_USERNAME=""
export DIRECTORY_TESTS_SSO_USER_TOKEN=""
export DIRECTORY_TESTS_SSO_USER_PASSWORD=""
export DIRECTORY_TESTS_SSO_USER_SSO_ID=1
export DIRECTORY_TESTS_SSO_UNVERIFIED_USER_TOKEN=""
export DIRECTORY_TESTS_S3_SECRET_ACCESS_KEY=<MUST_BE_SET>
export DIRECTORY_TESTS_S3_ACCESS_KEY_ID=<MUST_BE_SET>
export DIRECTORY_TESTS_S3_REGION=<MUST_BE_SET>
export DIRECTORY_TESTS_S3_BUCKET=<MUST_BE_SET>
```

Only the ones with `<MUST_BE_SET>` value, are actively used by `behave`.


# Running tests

All methods described below need all required environmental variables to be set 
(see. [Environment variables](#environment-variables) section).


## From IDE (ideally from PyCharm Pro):
In case of the IDE runner, you can set all required environment variables in
the `run configuration`.

Here's an example how this can be done:
![set required environment variable for test tun configuration](docs/set_env_vars_for_test_run_configuration.gif?raw=true)

Once all required environment variables are set, then simply:

* right-click on the selected scenario you want to run
* and hit "Run '...'"


## From CLI using `behave` directly:
```shell
behave tests/functional/features/
```

## From CLI using `make` & `functional_tests` target:

```commandline
# run all functional tests except ones tagged with @wip or @skip
make functional_tests

# run scenarios that match certain tag(s):
BEHAVE_ARGS="-t certain_tag" make functional_tests
```

## From CLI using `docker` container

This expects that all required environmental variables will be prefixed with 
`DIRECTORY_TESTS_` (see. [Environment variables](#environment-variables) section)

```commandline
make docker_functional_test
```
