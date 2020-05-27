GREAT platform - Load tests
---------------------------

This package contains a set of rudimentary load tests for various DIT services.  
Tests are driven by load test tool called [locust](https://locust.io/).

Services covered with load tests:

* `CMS API`
* `ERP`
* `Find a buyer`
* `Find a supplier`
* `Domestic site`
* `International site`
* `Invest pages`
* `ISD`
* `Selling Online Overseas`


## Development

### Requirements

* python 3.8+
* dependencies listed in [requirements_load.txt](../../requirements_load.txt)
* all required env vars exported (e.g. using [Convenience shell scripts](../../README.md#Convenience-shell-scripts))

Although load tests explicitly depend only on following env vars:
* `BASICAUTH_USER`, `BASICAUTH_PASS`, `CMS_API_DEFAULT_TIMEOUT`, `CMS_API_KEY` & `CMS_API_SENDER_ID`

All other environment variables defined in [env.json](../../env_vars/env.json) must be also set.  
This is because load tests depend on `directory_tests_shared` package, which requires all env vars from `env.json`.


### Installing

You'll need [pip](https://pypi.org/project/pip/) to install required dependencies and [virtualenv](https://pypi.org/project/virtualenv/) to create a virtual python environment:

```bash
git clone https://github.com/uktrade/directory-tests
virtualenv .venv -p python3.8
source .venv/bin/activate
make requirements_load
```

or if you use [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) then:

```bash
git clone https://github.com/uktrade/directory-tests
cd directory-tests
mkvirtualenv -p python3.8 load
make requirements_load
```

## Running the tests

### Run in headless mode

[Makefile](../../makefile) contains dedicated targets which can execute load tests without WEB GUI (headless mode).  

In order to run load tests locally, you'll need to specify `3` arguments (env vars):

* `NUM_USERS` - number of concurrent Locust users
* `HATCH_RATE` - the rate per second in which clients are spawned
* `RUN_TIME` - stop after the specified amount of time

Once you have those numbers, then simply run following command from repo's root directory:

```bash
NUM_USERS=5 HATCH_RATE=2 RUN_TIME=35 make load_test_{service_name}
```

Where `{service_name}` is one of the following:

* cms
* domestic
* erp
* fab
* fas
* international
* invest
* isd
* profile
* soo

Once test is finished, locust will:
* print out the results to the console
* and save CSV result files in `./reports/`
    * `results_stats.csv` - this file is used by [Geckoboard Updater](../periodic_tasks/geckoboard_updater/README.md) script to populate 2 [Geckoboards](https://readme.trade.gov.uk/docs/playbooks/qa-geckoboards.html)
    * `results_stats_history.csv` - might come in handy during debugging
    * `results_failures.csv` - this one is generated only when at least 1 error occured

Example results printed to console:
```bash
 Name                                   # reqs      # fails     Avg     Min     Max  |  Median   req/s
------------------------------------------------------------------------------------------------------
 GET /industries/[industry]/                11     0(0.00%)     333     280     466  |     300    0.40
 GET /search/?q=[term]&sectors=[sectors]    17     0(0.00%)     340     291     538  |     310    0.50
 GET /trade/                                23     0(0.00%)     319     259     485  |     300    0.40
------------------------------------------------------------------------------------------------------
 Total                                      51     0(0.00%)                                       1.30

Percentage of the requests completed within given times
 Name                                   # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
-------------------------------------------------------------------------------------------------------------
 GET /industries/[industry]/                11    300    360    360    360    380    470    470    470    470
 GET /search/?q=[term]&sectors=[sectors]    17    310    330    330    340    530    540    540    540    540
 GET /trade/                                23    300    320    340    380    390    420    490    490    490
-------------------------------------------------------------------------------------------------------------
 Total                                      51    310    320    340    360    390    490    530    540    540
```

### Run via Web GUI

Locust also offers an option to run tests from a nice Web GUI.

In order to start the Web GUI from repo's root directory run:
```bash
locust -f locustfile_{service_name}.py
```

Once web monitor is up, go to [http://localhost:8089/](http://localhost:8089/) and you'll be prompted to enter:

* Number of users to simulate
* Hatch rate (users spawned/second)

Clicking on `Start swarming` will start the test and allow you to see:

* current statistics
* nice charts
* failures
* exceptions
* and download test results


## Run on CircleCI

All load tests are executed against staging environment every night (Mon through Fri) on CircleCI.  
Load test workflows are defined in [config.yml](../../.circleci/config.yml).

List of load test workflow (at the time of writing May 2020)

* run_cms_load_tests_on_stage
* run_domestic_load_tests_on_stage
* run_fab_load_tests_on_stage
* run_fas_load_tests_on_stage
* run_international_load_tests_on_stage
* run_invest_load_tests_on_stage
* run_isd_load_tests_on_stage
* run_profile_load_tests_on_stage
* run_soo_load_tests_on_stage

Thes workflows are are controlled with the same `3` variables defined at the top of [config.yml](../../.circleci/config.yml):

```yaml
load_hatch_rate: &load_hatch_rate
    HATCH_RATE: 3

load_num_users: &load_num_users
    NUM_USERS: 1000

load_run_time: &load_run_time
    RUN_TIME: 5m
```


### Artifacts & Geckoboards

After each load test run, CircleCI will keep all CSV result files as a job artifacts.  

These `CSV` files are processed by [Geckoboard Updater](../periodic_tasks/geckoboard_updater/README.md) in order to
populate load test [Geckoboards](https://readme.trade.gov.uk/docs/playbooks/qa-geckoboards.html).
