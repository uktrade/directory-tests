Geckoboard Updater
------------------

This script does three things:
* fetch
    * workflow status and test reports files (XML & CSV) from CircleCI
    * ticket data from Jira
* transform
    * relevant data into [Geckoboard datasets](https://developer.geckoboard.com/hc/en-us/articles/360019745091-Getting-started-with-Datasets)
* push
    * datasets to GeckoBoard so underlying data can be visualised on any board
    * custom text widget data (a subset of HTML) to Geckoboard [text widgets](https://developer-custom.geckoboard.com/#text)

At the time of writing (May 2020) the [geckoboard_updater.py](./geckoboard_updater.py) script is scheduled to run twice a day.  
Please refer to `refresh_geckoboard_periodically` workflow in [.circleci/config.yml](../../../.circleci/config.yml) for scheduling details.


## General requirements

* Python 3.8+
* [CircleCI API client](https://pypi.org/project/circleclient/)
* [Geckoboard Datasets API client](https://pypi.org/project/geckoboard.py/)
* [Jira REST API client](https://pypi.org/project/jira/)


### Environment variables

All secrets required by this script are in Rattic (look for `Geckoboard updater` and then for `geckoboard.sh`)

Required environment variables:

* `CIRCLE_CI_API_TOKEN`: get a new token from https://circleci.com/account/api
* `GECKOBOARD_API_KEY`: get a new token from https://app.geckoboard.com/account/details
* `GECKOBOARD_TEST_RESULTS_WIDGET_KEY`: widget key for `Service workflow status (DEV)` text widget on [QA dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY`: widget key for `Last directory tests results` text widget on [QA dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY`: widget key for `Last Periodic tests results` text widget on [QA dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY`: widget key for `Links to test jobs` text widget on [CMS stats and dead links](https://app.geckoboard.com/edit/dashboards/277009) board
* `GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY`: widget key for `Jira links` text widget on [Tools team - Jira stats](https://app.geckoboard.com/edit/dashboards/296257) board
* `JIRA_HOST`: URL to your Jira instance e.g.: `https://{your_orgranisation}.atlassian.net/`
* `JIRA_USERNAME`: Jira username
* `JIRA_TOKEN`:  Jira API Token
    * see ["Jira API Token"](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) support article to learn how to get one
    * see ["Python Jira REST API client"](https://jira.readthedocs.io/en/latest/examples.html#http-basic) manual to understand how to use that token to authenticate

Optional environment variables:
* `GECKOBOARD_PUSH_URL`: Set it if you have a private instance of Geckoboard otherwise it will default to: `https://push.geckoboard.com/v1/send/`


## Running

From project's root directory run:
```bash
make geckoboard_updater

PYTHONPATH=. python3 ./tests/periodic_tasks/geckoboard_updater/geckoboard_updater.py
Finding or creating Geckoboard datasets...
Pushing datasets to Geckoboard...
Pushing Jira stats to Geckoboard
Found 'CMS Prod pages' build artifact cms_pages.xml in build #1
Fetching 'CMS Prod pages' build artifact: 'cms_pages.xml' from build #1
Found 'Stage Dead links' build artifact dead_links_report.xml in build #2
Found 'Dev Dead links' build artifact dead_links_report.xml in build #3
Found 'UAT Dead links' build artifact dead_links_report.xml in build #4
Found 'Prod Dead links' build artifact dead_links_report.xml in build #4
Fetching 'Stage Dead links' build artifact: 'dead_links_report.xml' from build #2
Fetching 'Dev Dead links' build artifact: 'dead_links_report.xml' from build #3
Fetching 'UAT Dead links' build artifact: 'dead_links_report.xml' from build #4
Fetching 'Prod Dead links' build artifact: 'dead_links_report.xml' from build #5
Pushing periodic tests results to Geckoboard
Pushing load tests result distribution results to Geckoboard
Pushing load test response times metrics to Geckoboard
Pushing aggregated Pa11y accessibility test results to Geckoboard
Pushing text widget data to GeckoBoard...
Pushing Jira Query links to Geckoboard
Couldn't find new links to content diff reports. Will keep the old ones in place
```


## Geckoboard

This section describes how Datasets are defined, created and pushed to Geckoboard.

### Geckoboard dataset schemas

[Datasets](https://developer.geckoboard.com/hc/en-us/articles/360019745091-Getting-started-with-Datasets) are simple JSON data structures.  
Before sending any dataset to Geckoboard, you have to find and verify an existing dataset or create a new one.  
This process is described in ["Find or create a new dataset"](https://developer.geckoboard.com/hc/en-us/articles/360019745091-Getting-started-with-Datasets) support article.

To create a new Dataset you will need to specify its schema.  
This is done by calling `client.datasets.find_or_create()` with:
* `id`: a string to help you identify your dataset from within the application.
* `fields`: an object with keys for each column in your dataset. The value describes the type for that column.
* `unique_by`: An optional array of one or more field names whose values will be unique across all your records.

The code snippet bellow shows how you can create a dataset for Jira ticket statistics grouped by labels:

```python
from geckoboard.client import Client

client = Client("GECKOBOARD_API_KEY")

date_team_metric_label_quantity = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
date_team_metric_label = ["date", "team", "metric", "label"]

jira_bugs_dataset = client.datasets.find_or_create(
    f"jira.bugs_by_labels",
    date_team_metric_label_quantity,
    unique_by=date_team_metric_label,
)
```

Calling `find_or_create()` is an idempotent operation.  
It means that if you call it multiple times with the same set of arguments it won't create a new dataset but just return a reference to an existing one.
When you call it with new and unique set of arguments it will create a new Dataset for you.

All dataset schemas used by this script are defined in [dataset.py](datasets.py).  
These schemas were designed to accommodate generic data sets we'd like to visualise.  


### geckoboard_utils.py

Once all the data from Jira & CircleCI is fetched & collated, then it pushed to Geckoboard,
by various

Utility functions from [geckoboard_utils.py](geckoboard_utils.py) are used to:
* format text data (HTML) for custom text widgets
* push all datasets and text widget data to Geckoboard (look for `def push_*()`)


## CircleCI

This section describes how workflow status and test results are fetched from CircleCI and transformed into datasets.

### circleci_utils.py

Utility functions from [circleci_utils.py](circleci_utils.py) are used to:
* get workflow status and test results data files from CircleCi
* parse test result files (like JUnit XML files generated by Behave or pytest & CSV files generated by locust.io)
* transform that data to usable Datasets


### Pulling test job results, test reports & transforming them into datasets

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

1) fetch a list of recent builds (see [def recent_builds()](circleci_utils.py))
2) find last build for specific job (see [def last_build_per_job()](circleci_utils.py) & `DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS`)
3) get test job artifacts from CircleCI (stored as XML Junit report files) (see [def get_build_artifacts()](circleci_utils.py))
4) parse those XML files and extract relevant metrics (see [def parse_junit_results()](circleci_utils.py))

All those steps are executed in [def last_tests_results_from_junit_artifacts()](circleci_utils.py)


### Fetching & parsing `CSV` files

1) fetch a list of recent builds (see [def recent_builds()](circleci_utils.py))
2) find last build for specific job (see [def last_build_per_job()](circleci_utils.py) & `DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS`)
3) get test job artifacts from CircleCI (stored as XML Junit report files) (see [def get_build_artifacts()](circleci_utils.py))
4) parse those CSV files and extract relevant metrics (see [def get_load_test_response_time_distribution()](circleci_utils.py) & [def get_load_test_response_time_metrics()](circleci_utils.py))

For more details check [circleci_utils.py](./circleci_utils.py)


### CircleCI build status report

This script also connects to CircleCI and extracts information about recent
builds for designated projects. It supports both `v1` and `v2` CircleCI jobs.

Please refer to function: [def last_directory_service_build_results()](circleci_utils.py) for
more details.

Below is a list of currently monitored projects:

* [directory-api](https://github.com/uktrade/directory-api)
* [directory-cms](https://github.com/uktrade/directory-cms)
* [directory-companies-house-search](https://github.com/uktrade/directory-companies-house-search)
* [directory-forms-api](https://github.com/uktrade/directory-forms-api)
* [directory-sso-profile](https://github.com/uktrade/directory-sso-profile)
* [directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)
* [directory-sso](https://github.com/uktrade/directory-sso)
* [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer)
* [great-domestic-ui](https://github.com/uktrade/great-domestic-ui)
* [great-international-ui](https://github.com/uktrade/great-international-ui)


## Jira

This section describes how ticket data is fetched from Jira, then how it's filtered, grouped and transformed into datasets.

#### jira_utils.py & jira_queries.py

Jira supports a query language called [JQL](https://www.atlassian.com/software/jira/guides/expand-jira/jql).  
Geckoboard updater script uses JQL queries to find information about tickets of interests (e.g. bugs).  
All `JQLs` are defined in [jira_queries.py](jira_queries.py).

Utility functions from [jira_utils.py](jira_utils.py) are used to:

* fetch ticket data from Jira
* filter and organise ticket data

### Jira labels

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

### Special Jira labels

There are also three Jira labels that have special purpose:

* `qa_auto` & `qa_manual` → tags issues which were found by automated tests or
    during manual testing. They're used to create a widget that compares the
    number of bugs found both ways.
* `qa_automated_scenario` → tag `Task` or `Sub-task` for automating a test
    scenario. This is used to generate the `Scenarios to automate` counter.
