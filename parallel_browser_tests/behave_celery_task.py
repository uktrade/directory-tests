# -*- coding: utf-8 -*-
"""A Celery task to run Behave scenario

Usage:
  behave_celery_task.py [--browser=chrome | --browser=firefox] [--scenario="name"]
  behave_celery_task.py (-h | --help)
  behave_celery_task.py --version

Options:
  -h --help             Show this screen.
  --browser=BROWSER     Specify browser name.
  --scenario="name"     Specify scenario to run.
  --version             Show version.
"""
import contextlib
import io
import os
import time
from contextlib import redirect_stdout
from datetime import datetime
from typing import Dict

from behave.__main__ import main as behave_main
from docopt import docopt

import redis
from celery import Celery, states
from celery.utils.log import get_task_logger

TASK_NAME = "run scenario"
QUEUE_NAME = "behave"
REPLACE_CHARS = ("Scenario: ", "Scenario Outline: ", "\r")

app = Celery("tasks", broker="redis://redis@redis:6379//")
app.conf.task_default_queue = QUEUE_NAME
app.conf.broker_transport_options = {"visibility_timeout": 3600}
app.conf.send_events = True
app.conf.send_task_sent_event = True

logger = get_task_logger(__name__)


def get_datetime() -> str:
    return datetime.isoformat(datetime.now())


def replace_char(string: str) -> str:
    for chars in REPLACE_CHARS:
        string = string.replace(chars, "")
    return string


@contextlib.contextmanager
def set_env(environ: Dict[str, str]):
    """Temporarily set the process environment variables.

    SRC: https://stackoverflow.com/a/34333710
    """
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


@app.task(
    bind=True,
    autoretry_for=(),
    broker_pool_limit=1,
    ignore_result=True,
    name=TASK_NAME,
    queue=QUEUE_NAME,
)
def delegate_test(self, browser: str, scenario: str):
    args_list = [
        f"features/",
        "--no-skipped",
        "--format=allure_behave.formatter:AllureFormatter",
        f"--outfile={browser}_results/",
        "--format=pretty",
        "--logging-filter=-root",
        "--tags=~@wip",
        "--tags=~@fixme",
        "--tags=~@skip",
        "--tags=~@stage-only",
        "--name",
        replace_char(scenario),
    ]

    # set env var that decides in which browser the test should be executed
    env_vars = {
        "HUB_URL": "http://selenium-hub:4444/wd/hub",
        "BROWSER_ENVIRONMENT": "parallel",
        "HEADLESS": "true",
        "AUTO_RETRY": "false",
        "BROWSER": browser,
        "ALLURE_INDENT_OUTPUT": "2",
        "TAKE_SCREENSHOTS": "true",
    }
    with set_env(env_vars):
        temp_redirect = io.StringIO()
        with redirect_stdout(temp_redirect):
            exit_code = behave_main(args_list)

    behave_result = temp_redirect.getvalue()
    logger.info(behave_result)
    if exit_code == 1:
        self.update_state(state=states.FAILURE, meta=behave_result)


def get_redis_counter() -> int:
    connection = redis.Redis("redis")
    return connection.llen("behave")


if __name__ == "__main__":
    arguments = docopt(__doc__, version="env_writer 1.0")
    browser = arguments["--browser"]
    scenario = arguments["--scenario"]

    if browser and scenario:
        print(f"{get_datetime()} - Adding task to run '{scenario}' in {browser}")
        delegate_test.delay(browser=browser, scenario=scenario)
    else:
        print(f"{get_datetime()} - Monitoring queue...")
        wait_time = 5
        max_repetitions = 20
        counter = 0
        list_of_task_numbers = []
        remaining_tasks = get_redis_counter()
        print(
            f"{get_datetime()} - Number of tasks in 'behave' queue: {remaining_tasks}"
        )
        list_of_task_numbers.append(remaining_tasks)
        while remaining_tasks != 0 and len(list_of_task_numbers) < max_repetitions:
            counter += 1
            time.sleep(wait_time)
            remaining_tasks = get_redis_counter()
            print(f"{get_datetime()} - list_of_task_numbers -> {list_of_task_numbers}")
            if list(set(list_of_task_numbers))[0] == remaining_tasks:
                list_of_task_numbers.append(remaining_tasks)
            else:
                list_of_task_numbers = [remaining_tasks]
            print(
                f"{get_datetime()} - Number of tasks in 'behave' queue: {remaining_tasks}"
            )
        if len(list_of_task_numbers) >= max_repetitions:
            print(
                f"{get_datetime()} - Looks like queue got stale as for past "
                f"{wait_time * max_repetitions}s redis reported that there were "
                f"{list(set(list_of_task_numbers))[0]} tasks in 'behave' queue"
            )
        else:
            print(f"{get_datetime()} - Hooray! There are no more tests to run.")
