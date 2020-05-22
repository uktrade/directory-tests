# directory-tests

[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![snyk-image]][snyk]

Smoke, load, functional/integration & functional browser tests for [https://www.great.gov.uk](https://www.great.gov.uk).

---

For all instructions please refer to specific readme file:

* [Smoke tests](tests/smoke/README.md)
* [Load tests](tests/load/README.md)
* [Functional/Integration tests](tests/functional/README.md)
* [Functional Browser tests](tests/browser/README.md)


# Requirements

There are separate `requirements` files for `smoke`, `load`, `functional` & `browser` tests.  
You can find then in:
* [requirements_smoke.txt](requirements_smoke.txt)
* [requirements_load.txt](requirements_load.txt)
* [requirements_functional.txt](requirements_functional.txt)
* [requirements_browser.txt](requirements_browser.txt)

Please use a dedicated `virtualenv` for each type of tests.  
[virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) is highly recommended
for creating & managing [virtual envs](https://pypi.org/project/virtualenv/).


# Env Vars

Before you can run any load tests you'll need to set all required environment variables.  
You can find shell scripts with all env vars in Rattic (look for `DIT test env vars`).

Once you get access to those shell scripts, you can add some handy aliases to your shell config, e.g.:

```bash
alias dev='source ~/dir-dev.sh';
alias stage='source ~/dir-stage.sh';
alias uat='source ~/dir-uat.sh';
alias gecko='source ~/geckoboard.sh';
alias periodic='source ~/periodic.sh';
```

Thanks to this you'll be able to can quickly change between test environments when running tests locally.

## Updating requirements_*.txt files

We're using [pip-tools](https://pypi.org/project/pip-tools/) to generate pinned `requirements.txt`.  

In order to generate (or update) dependencies for i.e. `smoke` tests:

* `pip install pip-tools`
* update `requirements_smoke.in` file (remember not to pin dependency version in it)
* generate `requirements_smoke.txt` with `pip-compile -U -o requirements_smoke.txt requirements_smoke.in`


# CircleCI

All tests are executed nightly on CircleCI against `Dev` & `Staging` environments and in
the evening against `UAT` environment.  
Test workflows are defined in [config.yml](.circleci/config.yml#L595).


[circle-ci-image]: https://circleci.com/gh/uktrade/directory-tests/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-tests/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-tests/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-tests

[snyk-image]: https://snyk.io/test/github/uktrade/directory-tests/badge.svg
[snyk]: https://snyk.io/test/github/uktrade/directory-tests
