Check if all Production CMS pages are available
-----------------------------------------------

This test goes through all published & draft versions of pages found with the
use of CMS API and checks whether those pages can be visited without any error.


## Why is it here?

This module should be placed in `tests/periodic_tasks` so it could make use of common
helpers. Unfortunately it would mean that we'd have to have all required env vars
(see [./env_vars/env.json](./env_vars/env.json) ) for Production environment set in CircleCI.
This solution is rather far from ideal. Thus I've decided to keep these tests in a separate package.  


## Requirements

* [pytest](https://pypi.org/project/pytest/)
* [requests](http://docs.python-requests.org/en/master/)
* [directory_cms_client](https://pypi.org/project/directory-cms-client/)


## Check if all Production CMS pages return 200 OK

When in project's root directory run:
```bash
make test_cms_pages_return_200
```

or:
```bash
cd test_prod_cms_pages
pytest --capture=no --verbose
```

or in case you have some importing issues set `PYTHONPATH` to `.`:
```bash
cd test_prod_cms_pages
PYTHONPATH=. pytest --capture=no --verbose test_cms_pages_return_200.py
```


## Generate report for CMS page status

[generate_page_status_report.py](./generate_page_status_report.py) script generates a simple HTML report for all
Production CMS pages. The report contains

```bash
make cms_page_status_report
```

A link to the latest version of that that report is published on `Great - CMS stats and dead links` geckoboard.
