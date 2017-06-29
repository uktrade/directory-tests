Functional Test for FAB, FAS & SSO
----------------------------------


# create virtualenv & install dependencies
```bash
mkvirtualenv .env -p python3.5
pip install -r requirements.txt
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

Only the ones with `<MUST_BE_SET>` value, are actively used by `behave`.


# Running tests

Both methods described below require all env variables to be set.
In case of the IDE runner, you can set all required environment variables in
the `run configuration`.

From CLI:
```shell
behave tests/functional/features/
```

From IDE (ideally from PyCharm Pro):

* right-click on the scenario to run
* hit "Run '...'"