Geckoboard Updater
------------------

It's a script which:
* fetches build data & test results from CircleCi
* fetches ticket statistics from Jira
* extracts relevant data and transforms it to datasets (JSON structures)
* pushes datasets to Geckoboard


How does it works:
* The [geckoboard_updater.py](./geckoboard_updater.py) script is periodically
    executed on CircleCI (check [.circleci/config.yml](../.circleci/config.yml))
* The script pulls stats and data from CircleCI and Jira
* It then pulls the test job results, test reports (XML & CSV) from CircleCI & ticket statistics from Jira
* Once the data is pulled from both CircleCI & Jira it's transformed into
    simple JSON data structures (called [datasets](https://developer.geckoboard.com/hc/en-us/articles/360019745091-Getting-started-with-Datasets)) which can be processed by Geckoboard.
    Before we send any data to Geckoboard, we have to define its structure.
    This is done by sending a [dataset schema](https://developer.geckoboard.com/hc/en-us/articles/360019475652-Find-or-create-a-new-dataset).
* Once datasets are pushed to GeckoBoard then you can visualize data using various diagrams


*FYI:*

CircleCI test workflows (for smoke, functional, load & browser tests) are defined in this CircleCI [config.yml](https://github.com/uktrade/directory-tests/blob/master/.circleci/config.yml)


# Geckoboard dataset schemas & helpers

### Geckoboard dataset schemas

All dataset schemas are defined in [dataset_schemas.py](dataset_schemas.py).  
They're were designed to accommodate various generic sets of data we'd like to visualise on a Geckoboard.  
Schemas are share between various datasets pushed to Geckoboard.

Here's an example dataset schema used to send statistics about Jira bug tickets grouped by labels:
```python
DATE_TEAM_METRIC_LABEL_QUANTITY = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
```

### Geckoboard helpers

Various helper functions are kept in [gecko_helpers.py](./gecko_helpers.py).
Helper functions are used to:
* create datasets using schemas
* transform
* generate HTML widget data
* push HTML widget data & test results data


# Jira

## Pulling ticket statistics & transforming them into datasets

Jira supports a query language called [JQL](https://confluence.atlassian.com/jiracore/blog/2015/07/search-jira-like-a-boss-with-jql).  
Geckoboard updater script uses JQL queries to find information about tickets of interests (e.g. bugs).  
All `JQLs` are defined in [jira_queries.py](./jira_queries.py).

* All queries are executed and their results exposed via properties in [jira_results.py](./jira_results.py)
* Results are transformed into datasets by various helpers defined in [jira_helpers.py](./jira_helpers.py)


# CircleCI

## Pulling test job results, test reports & transforming them into datasets

All our test jobs generate report files in form of:
* a `Junit XML` file
* or `CSV` files containing load test statistics (see [locust's documentation](https://docs.locust.io/en/stable/retrieving-stats.html))

Those files are stored on CircleCI as [build artifacts](https://circleci.com/docs/2.0/artifacts/).
In order to represent test results on Geckoboard in a meaningful way, we have to:
* fetch them first
* extract relevant data
* transform data into datasets
* and finally push them to Geckoboard

### Fetching & parsing Junit XML files

1) fetch a list of recent builds (see [def recent_builds()](./circleci_helpers.py))
2) find last build for specific job (see [def last_build_per_job()](./circleci_helpers.py) & `DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS`)
3) get test job artifacts from CircleCI (stored as XML Junit report files) (see [def get_build_artifacts()](./circleci_helpers.py))
4) parse those XML files and extract relevant metrics (see [def parse_junit_results()](./circleci_helpers.py))

All those steps are executed in [def last_tests_results_from_junit_artifacts()](./circleci_helpers.py)

### Fetching & parsing `CSV` files

1) fetch a list of recent builds (see [def recent_builds()](./circleci_helpers.py))
2) find last build for specific job (see [def last_build_per_job()](./circleci_helpers.py) & `DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS`)
3) get test job artifacts from CircleCI (stored as XML Junit report files) (see [def get_build_artifacts()](./circleci_helpers.py))
4) parse those CSV files and extract relevant metrics (see [def get_results_distribution()](./circleci_helpers.py) & [def get_load_tests_requests_results()](./circleci_helpers.py))

For more details check [circleci_results.py](./circleci_results.py)


# Pushing datasets to Geckoboard

Once all the data from Jira & CircleCI is fetched & collated, then it pushed to Geckoboard,
by various `def push_*()` helpers from [gecko_helpers.py](./gecko_helpers.py).


# Requirements

* Python 3.6+
* [circleclient](https://pypi.org/project/circleclient/) → CircleCI API client
* [geckoboard.py](https://pypi.org/project/geckoboard.py/) → Geckoboard
    Datasetss API client
* [jira](https://pypi.org/project/jira/) → Jira REST API client


# Environment variables

All env variables are in rattic (look for Geckoboard updater)
Here's a list of required environment variables:

* `CIRCLE_CI_API_TOKEN` → API token which you can get [here](https://circleci.com/account/api)
* `GECKOBOARD_API_KEY` → API key which you can get [here](https://app.geckoboard.com/account/details)
* `GECKOBOARD_TEST_RESULTS_WIDGET_KEY` → Custom widget key, to which a HTML test results report is sent, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY` → Custom widget key, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY` → Custom widget key, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY` → Custom widget key, [CMS - content stats dashboard](https://app.geckoboard.com/edit/dashboards/277009)
* `GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY` → Custom widget key, [TT - Jira stats](https://app.geckoboard.com/edit/dashboards/296257)
* `JIRA_HOST` → URL to your Jira instance e.g.: `https://{your_orgranisation}.atlassian.net/`
* `JIRA_USERNAME` → Jira username
* `JIRA_TOKEN` →  [Jira API Token][1]

Optional env var:
* `GECKOBOARD_PUSH_URL` → Set it if you have a private instance of Geckoboard otherwise it will default to: `https://push.geckoboard.com/v1/send/`


[1]: → more on [Jira API Tokens](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) used by [Python Jira REST API client](https://jira.readthedocs.io/en/latest/examples.html#http-basic)


# Running

Once all required environment variables are set, simply run it:
```
./geckoboard_updater.py
```

# Jira labels

This script requires that bugs raised in Jira are labelled with tags prefixed
with `qa_`, e.g.:

* `qa_accessibility` → accessibility issue
* `qa_backend` → backend issue, e.g. caching, DB, parsing etc.
* `qa_browser` → a browser compatibility issue
* `qa_content` → content related issues, typos, missing or invalid text etc.
* `qa_functional` → functional issue
* `qa_mobile` → an issue affecting only mobile devices
* `qa_ui` → UI specific issue e.g. missing or invalid styling etc.

These labels will be used to generate datasets for Geckoboard widgets.


## Special Jira labels

There are also three Jira labels that have special purpose:

* `qa_auto` & `qa_manual` → tags issues which were found by automated tests or
    during manual testing. They're used to create a widget that compares the
    number of bugs found both ways.
* `qa_automated_scenario` → tag `Task` or `Sub-task` for automating a test
    scenario. This is used to generate the `Scenarios to automate` counter.


# CircleCI build status report

This script also connects to CircleCI and extracts information about recent
builds for designated projects. It supports both `v1` and `v2` CircleCI jobs.

Please refer to function: [def last_directory_service_build_results()](./circleci_helpers.py) for
more details.

Below is a list of currently monitored projects:

* [directory-api](https://github.com/uktrade/directory-api)
* [directory-companies-house-search](https://github.com/uktrade/directory-companies-house-search)
* [directory-sso-profile](https://github.com/uktrade/directory-sso-profile)
* [directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)
* [directory-sso](https://github.com/uktrade/directory-sso)
* [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer)
* [directory-ui-supplier](https://github.com/uktrade/directory-ui-supplier)
* [great-domestic-ui](https://github.com/uktrade/great-domestic-ui)
