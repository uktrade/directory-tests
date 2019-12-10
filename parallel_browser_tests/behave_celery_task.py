# -*- coding: utf-8 -*-
import contextlib
import io
import os
import sys
import time
from contextlib import redirect_stdout
from typing import Dict

from behave.__main__ import main as behave_main

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
    def replace_char(string: str) -> str:
        for chars in REPLACE_CHARS:
            string = string.replace(chars, "")
        return string

    feature_dir = os.environ["FEATURE_DIR"].lower()
    args_list = [
        f"features/{feature_dir}/",
        "--no-skipped",
        "--format=allure_behave.formatter:AllureFormatter",
        f"--outfile={browser}_results/",
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
    sys.exit(exit_code)


def get_task_stats() -> tuple:
    tasks = app.control.inspect()
    nodes = list(tasks.stats().keys())
    node_name = nodes[0]

    # get number of active tasks
    active = len(tasks.active()[node_name])

    # get number of tasks that have been claimed by workers
    reserved = len(tasks.reserved()[node_name])

    total = tasks.stats()[node_name]["total"][TASK_NAME]

    return active, reserved, total


if __name__ == "__main__":
    if len(sys.argv) == 2:
        delegate_test.delay(browser=sys.argv[1], scenario=sys.argv[2])
    else:
        active, reserved, total = get_task_stats()
        while active != 0 and reserved != 0:
            print(f"Task stats: active={active} reserved={reserved} total={total}")
            time.sleep(5)
