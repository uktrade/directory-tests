Check if all Production CMS pages are available
-----------------------------------------------

This test goes through all published & draft versions of pages found with the
use of CMS API and checks whether those pages can be visited without any error.


# Why is it here?

This module should be placed in `tests/periodic_tasks` so it could make use of common
helpers. Unfortunately it would mean that we'd have to have all required env vars
(see [docker/env.json](docker/env.json) ) for Production environment set in CircleCI.
And this is rather far from ideal. Thus I've decided to keep this module separate and
have some duplicated code so the number of required secrets to run is minimal.


# Requirements

* [pytest](https://pypi.org/project/pytest/)
* [requests](http://docs.python-requests.org/en/master/)
* [directory_cms_client](https://pypi.org/project/directory-cms-client/)


# Usage

When in root dir of this repo use:
```bash
make cms_pages_check
```

or:
```bash
cd test_prod_cms_pages
pytest --capture=no --verbose
```

or in case you have some importing issues set `PYTHONPATH` to `.`:
```bash
cd test_prod_cms_pages
PYTHONPATH=. pytest --capture=no --verbose test_cms_pages.py
```
