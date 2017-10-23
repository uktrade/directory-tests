Export Readiness - UI Automated Tests
-------------------------------------

This repository contains UI tests automated using Behave and Selenium.  
They can be run:
* using locally running browsers attached to a Selenium Hub
* or inside a isolated Docker environment


# Requirements

* python 3.5
* pip
* docker
* docker-compose


## Run locally

To run tests against local Selenium Hub (*) with some browsers attached to it,
you can use following command:

```bash
make exred_local
```

An equivalent `behave` command is:

```bash
cd tests/exred
BROWSER=chrome \
WIDTH=1280 \
HEIGHT=768 \
EXRED_UI_URL=https://exred-prototype.herokuapp.com/export \
behave -k --format progress3 --no-logcapture --stop --tags=-wip --tags=-skip --tags=~fixme
```

(*) - this will also work if you have a Selenium Hub running locally inside 
a docker container accessible via port `4444` and some browsers attached to it.

## Run with docker

To run all tests inside dedicated Docker containers, simply execute:

```bash
make exred_docker_tests
```


# TODO
* make Paver detect number of browsers in config file
* add support for local test run

## Useful BrowserStack related links

* tutorial on using [browserstack with python](https://www.browserstack.com/automate/python)
* tutorial on using [behave with browserstack](https://www.browserstack.com/automate/behave)
* example [browserstack behave project](https://github.com/browserstack/behave-browserstack)
* [browser capabilities]()https://www.browserstack.com/automate/capabilities)