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


If you want to run the scenarios in a different browser then specify it using `BROWSERS` environment variable:  
```bash
BROWSERS=firefox make exred_local
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


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) in parallel with `paver` command:
```bash
cd tests/exred
paver run browserstack
```


To run all scenarios on [BrowserStack](https://www.browserstack.com/automate) with `behave` command (always defaults to `Chrome`):   
```bash
cd tests/exred
CONFIG=browserstack behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
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
