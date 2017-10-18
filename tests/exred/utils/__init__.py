# -*- coding: utf-8 -*-
"""ExRed utils."""
import logging
import os
import sys
import traceback
from os.path import abspath, join
from urllib.parse import urljoin
from functools import partial
from contextlib import contextmanager
from datetime import datetime

from behave.runner import Context

from settings import (
    DRIVERS,
    EXRED_UI_URL,
    SCREENSHOTS_DIR
)

URLS = {
    # Exporting Readiness
    "ExRed Home": "",
    "ExRed Triage - 1st question": "triage",
    "ExRed Triage - 2nd question": 'triage?q0={}&q1={}',
    "ExRed Triage - 3rd question": 'triage?q0={}&q1=Yes',
    "ExRed Triage - 4th question": "triage?q0={}&q1={}&q2={}&q3={}",
    "ExRed Triage - result": "triage/result",
}


def get_relative_url(name: str) -> str:
    return URLS[name]


def get_absolute_url(name: str) -> str:
    join_ui_exred = partial(urljoin, EXRED_UI_URL)
    relative_url = get_relative_url(name)
    return join_ui_exred(relative_url)


def take_screenshot(driver: DRIVERS, page_name: str):
    """Will take a screenshot of current page.

    :param driver: Any of the WebDrivers
    :param page_name: page name which will be used in the screenshot filename
    """
    stamp = datetime.isoformat(datetime.utcnow())
    file_name = "{}-{}.png".format(stamp, page_name)
    file_path = abspath(join(SCREENSHOTS_DIR, file_name))
    driver.get_screenshot_as_file(file_path)
    logging.debug("User took a screenshot of %s page. You can find it here:"
                  " %s", page_name, file_path)


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param message: a message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in message
                 like: %s, %d
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def get_file_log_handler(
        log_formatter, log_file: str = os.path.join("reports", "behave.log"),
        log_level=logging.DEBUG) -> logging.FileHandler:
    """Configure the console logger.

    Will use DEBUG logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_file: specifies log file path relative to the project's root
    :param log_level: specifies logging level, e.g.: logging.ERROR
    :return: configured console log handler
    """
    print("Behave log file: {}".format(log_file))
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def init_loggers(context: Context):
    """Will initialize console and file loggers."""
    # configure the formatter
    fmt = ('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: '
           '%(message)s')
    log_formatter = logging.Formatter(fmt)
    log_file_handler = get_file_log_handler(log_formatter)
    # Add log file handler to Behave's logging
    logging.getLogger("selenium").setLevel(logging.WARNING)
    context.config.setup_logging(handlers=[log_file_handler])
