DIT - Load tests
---------------------------------------

This package contains a set of rudimentary load tests for various DIT services.  
Tests are driven by load test tool called [locust.io](https://locust.io/).

Services covered with load tests:

* `CMS-API`
* `Find a buyer`
* `Find a supplier`
* `Domestic site`
* `Domestic search`
* `International site`
* `Invest`
* `ISD`
* `Selling Online Overseas`


# Requirements

* python 3.6
* pip
* dependencies listed in [requirements_load.txt](../../requirements_load.txt)
* required environment variables (see [env.json](../../docker/env.json)


# Installation and execution

1. Create dedicated virtualenv -> `mkvirtualenv -p python3.6 load`
2. Install dependencies from [requirements_load.txt](../../requirements_load.txt) → `pip install -r requirements_load.txt`
3. Set required env vars (see [Env Vars](#env-vars))
4. Run tests with or without Web GUI -> see steps below


# Env Vars

Before running tests you'll need to set all required environment variables.  
You can find those variables in Rattic.  

The next steps is to define handy command aliases to make that process as simple as possible:

```bash
alias dev='source ~/dev.sh';
alias stage='source ~/stage.sh';
alias uat='source ~/uat.sh';
```

Once that's done, remember to run `dev`, `stage` or `uat` command prior running tests 
against desired environment.


## Run without Web GUI

Makefile contains targets per service which execute load tests without WEB GUI.  
This is useful when executing on CI.

In order to run load tests locally, you'll need to specify `3` values:

* `NUM_CLIENTS` - number of concurrent Locust users
* `HATCH_RATE` - the rate per second in which clients are spawned
* `RUN_TIME` - stop after the specified amount of time

Once you have those numbers, then simply run following command from repo's root directory:

```bash
NUM_CLIENTS=5 HATCH_RATE=2 RUN_TIME=35 make rudimental_load_test_{service_name}
```

Where `{service_short_name}` is one of the following:

* cms
* fab
* fas
* international
* invest
* isd
* search
* soo

Once test is finished, locust will:
* print out the results to the console
* save 2 CSV files [`results_distribution.csv` & `results_requests.csv`] in `./reports/`

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

## Run from Web GUI

Locust also offers an option to run tests from a nice Web GUI.

In order to start the Web GUI, choose service name and from repo's root directory run:
```bash
locust -f locustfile_rudimental_{service_name}.py
```

Once web monitor is up, go to [http://localhost:8089/](http://localhost:8089/).   
You'll be prompted to enter:

* Number of users to simulate
* Hatch rate (users spawned/second)

Clicking on `Start swarming` will start the test and allow you to see:

* current statistics
* nice charts
* failures
* exceptions
* and download statistics in form of CSV files


# CircleCI

All load tests are executed against staging environment every night on CircleCI.  
Load test workflows are defined in [config.yml](../../.circleci/config.yml).

Below are the workflow names per specific service:
* run_cms_load_tests_on_stage
* run_fab_load_tests_on_stage
* run_fas_load_tests_on_stage
* run_international_load_tests_on_stage
* run_invest_load_tests_on_stage
* run_isd_load_tests_on_stage
* run_search_load_tests_on_stage
* run_soo_load_tests_on_stage

Tests are controlled by `3` variables defined at the top of [config.yml](../../.circleci/config.yml).

```yaml
load_hatch_rate: &load_hatch_rate
    HATCH_RATE: 5

load_num_clients: &load_num_clients
    NUM_CLIENTS: 20

load_run_time: &load_run_time
    RUN_TIME: 300
```


## Artifacts & Geckoboards

After each load test job is done, CircleCI will keep locust's test result files: 
`results_distribution.csv` & `results_requests.csv` as a job artifact.  

These `CSV` files are then consumed by [Geckoboard Updater](https://github.com/uktrade/directory-periodic-tests/tree/master/geckoboard_updater) script. 
Once fetched, parsed & converted into a JSON Dataset, Geckoboard Updater will push 
the load tests results to Geckoboard, where they're nicely visualised.


# env vars

In order to execute load tests following environment variables must be set:

* `DIRECTORY_CMS_API_CLIENT_API_KEY`
* `DIRECTORY_CMS_API_CLIENT_BASE_URL`
* `DIRECTORY_UI_BUYER_URL`
* `DIRECTORY_UI_INTERNATIONAL_URL`
* `DIRECTORY_UI_SUPPLIER_URL`
* `EXRED_UI_URL`
* `INVEST_UI_URL`
* `ISD_UI_URL`
* `SOO_UI_URL`


There are also optional environment variables which will use default values if unset:

* `DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=30`
* `DIRECTORY_CMS_API_CLIENT_SENDER_ID=directory`
* `LOCUST_MAX_WAIT=6000`
* `LOCUST_MIN_WAIT=500`
* `LOCUST_TIMEOUT=150`
