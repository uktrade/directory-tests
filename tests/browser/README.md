DIT - Functional Browser Tests
----------------------------------

This repository contains UI tests automated using:
* [Behave](https://pythonhosted.org/behave/)
* [Selenium with Python](https://selenium-python.readthedocs.io/)
* [BrowserStack](https://www.browserstack.com/automate) 


# Requirements

* python 3.6
* pip
* dependencies listed in [requirements_browser.txt](../../requirements_browser.txt)
* required environment variables (see [env_browser.json](../../docker/env_browser.json)
* [browser driver binaries](https://selenium-python.readthedocs.io/installation.html#drivers) installed in `$PATH`
* a [BrowserStack](https://www.browserstack.com/users/sign_up) account (check Rattic)


# Installation

* Create dedicated virtualenv → `mkvirtualenv -p python3.6 browser`
* Install dependencies from [requirements_browser.txt](../../requirements_browser.txt) → `pip install -r requirements_browser.txt`
* set required env vars (see [Env Vars](#env-vars))


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


# Run scenarios locally with "behave" command

You can also run the scenarios with `behave` command (defaults to Chrome): 
```bash
cd tests/browser
workon browser
dev
behave -k --format pretty --no-skipped features/domestic/home-page.feature --tags=~@wip --tags=~@skip --tags=~@fixme --stop
```

This command will run all scenarios from specified feature file which are not annotated 
with `@wip`, `@skip` or `@fixme` tags. Test execution will also stop on first error 
because `--stop` parameter was used.

*IMPORTANT NOTE:*

You can increase the control over test execution by using one or all of the following env vars:

* `AUTO_RETRY` (defaults to `true`) - toggle `auto-retry` scheme (when on, then test will be marked as `failed` only when they fails twice in a row)
* `BROWSERS` (defaults to `chrome`) - change it to `firefox` if need be
* `HEADLESS` (defaults to `true`) - run in a headless mode or not

So for example, if you'd like to run scenarios using `headless` Firefox and disable `auto-retry` scheme, then run:
```bash
HEADLESS=false BROWSERS=firefox AUTO_RETRY=false behave -k --format pretty --no-skipped features/domestic/home-page.feature --tags=~@wip --tags=~@skip --tags=~@fixme --stop
```

# Run scenarios on BrowserStack

Run specific scenario on [BrowserStack](https://www.browserstack.com/automate) using specific browser and browser version:
```bash
TAG=ED-2366 BROWSERS=Edge VERSIONS=18.0 make browserstack_single
```


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) in parallel with `paver` command:
```bash
cd tests/browser
paver run --config=browserstack
```


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) with `behave` command (always defaults to `Chrome`):   
```bash
cd tests/browser
CONFIG=browserstack behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```


To run specific scenario on [BrowserStack](https://www.browserstack.com/automate) with `behave` command):   
```bash
cd tests/browser
BROWSERS=Edge VERSIONS=18.0 CONFIG=browserstack-single behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme --tags={YOUR_TAG}
```


# Run scenarios in Docker container on BrowserStack

To run all tests in a container using one of two browser sets on [BrowserStack](https://www.browserstack.com/automate):  
```bash
make docker_browserstack_first_set
make docker_browserstack_second_set
```


## BrowserStack - Custom browser capabilities

In order to use custom browser capabilities, please provide them as a dict string in `CAPABILITIES` env var:
```shell
CAPABILITIES='{"pageLoadStrategy":"eager","marionette":true}' AUTO_RETRY=false BROWSERS=firefox behave -k --no-logcapture -t ~wip -t ~fixme features/ --stop -t <your_tag>
```

PS. When using custom browser capabilities in Firefox, then the [geckodriver](https://github.com/mozilla/geckodriver/) will always expect `marionette` set to `true`.

In order to change `pageLoadStrategy` to `eager` in Chrome you'll have to set its value to `none`.
See [this answer](https://stackoverflow.com/a/43737358) for more details.
```shell
CAPABILITIES='{"pageLoadStrategy":"none"}' AUTO_RETRY=false BROWSERS=chrome behave -k --no-logcapture -t ~wip -t ~fixme features/ --stop -t <your_tag>
```


# Run all scenarios using locally installed browser

This command is not recommended as it will also execute scenarios which are not meant 
to work on the environment you want to run the tests against.

Run all scenarios locally using default browser (defaults to Chrome):  
```bash
make browser_local
```


## Use specific browser

If you want to run all the scenarios in a specific browser, then use `BROWSERS` environment variable:  
```bash
BROWSERS=firefox make browser_local
```

## Run scenarios for specific tag

If you want to run specific scenario in a specific browser, then use `TAG` & `BROWSERS` environment variables:  
```bash
TAG=ED-2366 BROWSERS=firefox make browser_local
```


## Useful BrowserStack related links

* tutorial on using [browserstack with python](https://www.browserstack.com/automate/python)
* tutorial on using [behave with browserstack](https://www.browserstack.com/automate/behave)
* example [browserstack behave project](https://github.com/browserstack/behave-browserstack)
* [browser capabilities]()https://www.browserstack.com/automate/capabilities)
