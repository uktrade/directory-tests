GREAT platform - Load tests
---------------------------

A set of rudimentary load tests for various GREAT services.  

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
* [locust](https://locust.io/)
* dependencies listed in [requirements_load.txt](../../requirements_load.txt)
* all required env vars exported (e.g. using [Convenience shell scripts](../../README.md#Convenience-shell-scripts))

Although load tests explicitly depend only on following env vars:
* `BASICAUTH_USER`, `BASICAUTH_PASS`, `CMS_API_DEFAULT_TIMEOUT`, `CMS_API_KEY` & `CMS_API_SENDER_ID`

All other environment variables defined in [env.json](../../env_vars/env.json) must be also set.  
This is because load tests depend on `directory_tests_shared` package, which requires all env vars from `env.json`.


## How to run load tests

### Enable venv and export env vars

Before running load tests against lets say DEV test environment you want to enable venv and export env vars:

1. Enable venv for load tests (`workon` command is part of [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/) package)
    ```bash
    workon load
    ```
2. Export env vars with `dir-dev.sh` convenience script
    ```bash
    # if you configured an alias then:
    dev
    # or source directly with:
    source ~/dir-dev.sh
    ```

### Run in headless mode

The main [makefile](../../makefile) contains dedicated targets for running load tests in headless mode (without WEB GUI).

To run load tests locally, you'll need to specify `3` arguments (env vars):

* `NUM_USERS` - number of concurrent Locust users
* `HATCH_RATE` - the rate per second in which clients are spawned
* `RUN_TIME` - stop after the specified amount of time

Once you have those numbers in place, then run following command from repo's root directory:

```bash
NUM_USERS=5 HATCH_RATE=2 RUN_TIME=35 \
    make load_test_{service_name}
```

Where `{service_name}` can be one of the following options:

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

Once the test is finished, locust will:
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

All of those workflows are controlled with the same `3` variables.  
They're defined at the top of [config.yml](../../.circleci/config.yml#L3):

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
