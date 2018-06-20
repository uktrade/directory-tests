Automated Functional Browser Tests
----------------------------------

This repository contains UI tests automated using:
* [Behave](https://pythonhosted.org/behave/)
* [Selenium with Python](https://selenium-python.readthedocs.io/)
* [BrowserStack](https://www.browserstack.com/automate) 


# Requirements

* python 3.5
* pip
* docker
* docker-compose
* [BrowserStack](https://www.browserstack.com/users/sign_up) account (Devs can find them in Rattic)
* appropriate [browser driver binaries](https://selenium-python.readthedocs.io/installation.html#drivers) installed in `$PATH`
* a set of environment variables (see `../docker/env_browser.json`)


# Run scenarios using locally installed browser

Run all scenarios using local browser (defaults to Chrome):  
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

## Run scenarios with "behave" command

You can also run the scenarios with `behave` command (defaults to Chrome): 
```bash
cd tests/browser
behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```

### Use specific browser with "behave" command

You can also use different browser when running the scenarios with `behave` command:  
```bash
cd tests/browser
BROWSERS=firefox behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```

## Custom capabilities

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

# Run scenarios on BrowserStack

Run all scenarios on [BrowserStack](https://www.browserstack.com/automate) in parallel:  
```bash
make browserstack
```

Run specific scenario on [BrowserStack](https://www.browserstack.com/automate) in parallel:  
```bash
TAG=ED-2366 make browserstack
```


Run specific scenario on [BrowserStack](https://www.browserstack.com/automate) using specific browser and browser version:
```bash
TAG=ED-2366 BROWSERS=Edge VERSIONS=16.0 make browserstack_single
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
BROWSERS=Edge VERSIONS=16.0 CONFIG=browserstack-single behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme --tags={YOUR_TAG}
```

# Run scenarios in Docker container on BrowserStack

To run all tests in a container using one of two browser sets on [BrowserStack](https://www.browserstack.com/automate):  
```bash
make docker_browserstack_first_set
make docker_browserstack_second_set
```


## Useful BrowserStack related links

* tutorial on using [browserstack with python](https://www.browserstack.com/automate/python)
* tutorial on using [behave with browserstack](https://www.browserstack.com/automate/behave)
* example [browserstack behave project](https://github.com/browserstack/behave-browserstack)
* [browser capabilities]()https://www.browserstack.com/automate/capabilities)
