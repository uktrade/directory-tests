Export Readiness - UI Automated Tests
-------------------------------------

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


# Run scenarios using locally installed browser

Run all scenarios using local browser (defaults to Chrome):  
```bash
make exred_local
```


If you want to run all the scenarios in a specific browser, then use `BROWSERS` environment variable:  
```bash
BROWSERS=firefox make exred_local
```


If you want to run specific scenario in a specific browser, then use `TAG` & `BROWSERS` environment variables:  
```bash
TAG=ED-2366 BROWSERS=firefox make exred_local
```


You can also run the scenarios with `behave` command (defaults to Chrome): 
```bash
cd tests/exred
behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```

You can also use different browser when running the scenarios with `behave` command:  
```bash
cd tests/exred
BROWSERS=firefox behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```


# Run scenarios on BrowserStack

Run all scenarios on [BrowserStack](https://www.browserstack.com/automate) in parallel:  
```bash
make exred_browserstack
```

Run specific scenario on [BrowserStack](https://www.browserstack.com/automate) in parallel:  
```bash
TAG=ED-2366 make exred_browserstack
```


Run specific scenario on [BrowserStack](https://www.browserstack.com/automate) using specific browser and browser version:
```bash
TAG=ED-2366 BROWSERS=Edge VERSIONS=16.0 make exred_browserstack_single
```


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) in parallel with `paver` command:
```bash
cd tests/exred
paver run --config=browserstack
```


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) with `behave` command (always defaults to `Chrome`):   
```bash
cd tests/exred
CONFIG=browserstack behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```


To run specific scenario on [BrowserStack](https://www.browserstack.com/automate) with `behave` command):   
```bash
cd tests/exred
BROWSERS=Edge VERSIONS=16.0 CONFIG=browserstack-single behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme --tags={YOUR_TAG}
```

# Run scenarios in Docker container on BrowserStack

To run all tests in a container which will use [BrowserStack](https://www.browserstack.com/automate):  
```bash
make exred_docker_browserstack
```


## Useful BrowserStack related links

* tutorial on using [browserstack with python](https://www.browserstack.com/automate/python)
* tutorial on using [behave with browserstack](https://www.browserstack.com/automate/behave)
* example [browserstack behave project](https://github.com/browserstack/behave-browserstack)
* [browser capabilities]()https://www.browserstack.com/automate/capabilities)
