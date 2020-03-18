Periodically executed tests & tasks
------------------------

This package contains simple tests & tasks that have to be run periodically.

Currently hosted tests & tasks:

* Dead links checker
* Geckoboard updater
* Measure contingency of service unavailability
* Content diff between Dev, Staging & Production versions of services
* Find accessibility issues on DEV ExRed with [pa11y](http://pa11y.org/) (currently disabled)
* Check if Dev & Staging services return "X-Robots-Tag: noindex" header


# Dead links checker

This script will look for internal and external links that return status codes
other than `200 OK`.

An example error will look like this:
```ascii
ERROR Crawled 2055 urls with 13 error(s) in 128.82 seconds

  not found (404): https://invest.great.gov.uk/privacy-and-cookies/fair-processing-notice-export-opportunities
    from https://www.great.gov.uk/terms-and-conditions/
    from https://www.great.gov.uk/international/terms-and-conditions/?lang=en-gb
...
```

## Requirements

```shell
mkvirtualenv -p python3.5 dead_links
pip install -r requirements_dead_links.txt
```

## Running

```shell
TEST_ENV=DEV make dead_links_check
TEST_ENV=STAGE make dead_links_check
TEST_ENV=PROD make dead_links_check
```

# Geckoboard updater

Please refer to the documentation in [./geckoboard_updater](./geckoboard_updater/README.md) directory


# Measure contingency of service unavailability
In order to get a rough estimation how one unavailable service would affect
other DIT services you need to run a `dead link check` with an option to
generate a JSON report:

```shell
TEST_ENV=PROD make dead_links_check_with_json_report
```

Once the report is generated, you can generate contingency report with:
```shell
./test_contingency.py

Number of unique links (without links to static files, translations and queries), per service, scanned by Dead Links Checker:
If a link contains any of following strings: /static/, ?source=, ?lang=, /ar/, /de/, /es/, /fr/, /ja/, /pt/, /zh-hans/ then it won't be included in the contingency report
SUD            :     1 - (excluding   12 ignored links)
FAB            :     1 - (excluding    0 ignored links)
ExOpps         :     2 - (excluding    0 ignored links)
Other          :   700 - (excluding    0 ignored links)
SOO            :    43 - (excluding   27 ignored links)
Old Contact-us :     1 - (excluding   11 ignored links)
FAS            :    66 - (excluding  329 ignored links)
Old Help       :     1 - (excluding    0 ignored links)
Contact        :    40 - (excluding    0 ignored links)
Ignored links  : 379
Total          : 1234 (855+379)

Service contingency report:
If FAB (https://www.great.gov.uk/find-a-buyer/) was down then if would affect:
        70 pages on Other
        43 pages on SOO
         1 pages on SUD
         4 pages on Contact
If ExOpps (https://opportunities.export.great.gov.uk/) was down then if would affect:
         1 pages on Other
If SOO (https://www.great.gov.uk/selling-online-overseas/) was down then if would affect:
         1 pages on Old Contact-us
        30 pages on Other
If FAS (https://trade.great.gov.uk/) was down then if would affect:
        26 pages on Other
If Contact (https://www.great.gov.uk/contact/) was down then if would affect:
       609 pages on Other
         2 pages on FAB
        81 pages on SOO
         1 pages on FAS
         1 pages on SUD
         1 pages on Old Contact-us
```

# Content diff

See [./content_diff](./content_diff).  

A simple test which finds contents differences between Dev, Staging & Production
version of the same page.
At the moment it looks for content differences for FAS, Invest & Domestic sites.

This test uses:
* [Python Behave](https://pypi.org/project/behave/) to run the tests
* [requests](http://docs.python-requests.org/en/master/) to fetch page contents
* Python's built-in [difflib](https://docs.python.org/3.7/library/difflib.html) to find & generate diff report


# Find accessibility issues on DEV ExRed with [pa11y](http://pa11y.org/) (currently disabled)

See `accessibility_tests_export_readiness_dev` job in [.circleci/config.yml](.circleci/config.yml)

A test job that uses `pally-cli` to scan all pages listed in a `sitemap.xml`
in order to find accessibility issues.


# Check if Dev & Staging services return "X-Robots-Tag: noindex" header

A simple test that checks if all expected pages on Dev & Staging environments return
"X-Robots-Tag: noindex" header.
This header is used by various search engine crawlers to determine whether page
should be ignored or not.

This test uses:
* [Python Behave](https://pypi.org/project/behave/) to run the tests
* [requests](http://docs.python-requests.org/en/master/) to fetch page contents
