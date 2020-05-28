Check if all CMS pages are available
------------------------------------

There are two scripts in this directory:

* [test_cms_pages_return_200.py](./test_cms_pages_return_200.py) - a test goes through all published & draft versions of pages exposed via CMS API and checks whether those pages can be visited without any error
* [generate_page_status_report.py](./generate_page_status_report.py) - generates a simple CMS page status report

## Why is it here?

This module should be placed in `tests/periodic_tasks` so it could make use of common helpers.  
Unfortunately it would mean that we'd have to have all required env vars (see [./env_vars/env.json](./env_vars/env.json))
 for Production environment set in CircleCI.  
That would be rather far from ideal, thus I've decided to keep these tests in a separate package.  


## Requirements

* [directory_cms_client](https://pypi.org/project/directory-cms-client/)
* [envparse](https://pypi.org/project/envparse/)
* [pytest](https://pypi.org/project/pytest/)
* [requests](http://docs.python-requests.org/en/master/)
* [termcolor](https://pypi.org/project/termcolor/)
* and CMS credentials exported as 2 env vars: `CMS_API_URL` & `CMS_API_KEY`

## Development

You can create a dedicated virtual env or use the same one as for [periodic tasks](../tests/periodic_tasks/README.md).

If you decide to create a dedicated venv then do so and install all dependencies and export mandatory env vars as follows:

```bash
mkvirtualenv -p python3.8 cms_status
pip install directory-cms-client envparse pytest requests termcolor
export CMS_API_URL=https://cms.api.url
export CMS_API_KEY=SECRET_API_KEY
```

### Check if all CMS pages return 200 OK

This test goes through all published & draft versions of pages exposed via CMS API and checks whether those pages can be visited without any error.  

Moreover, [Geckoboard updater](../tests/periodic_tasks/geckoboard_updater/README.md) parses the result file from this tests and pushes them to `Great - CMS stats and dead links` geckoboard.

When in repo's root directory run:
```bash
make test_cms_pages_return_200
```

In case you encounter importing issues set `PYTHONPATH` to `.`:
```bash
cd test_prod_cms_pages
PYTHONPATH=. pytest --capture=no --verbose test_cms_pages_return_200.py
```

### Generate a report with CMS page status

This script generates a simple CMS page status report.  
A link to the latest version of such report is published daily on `Great - CMS stats and dead links` geckoboard.

To generate a report locally from repo's root directory run:

```bash
make cms_page_status_report
```
