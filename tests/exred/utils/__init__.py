# -*- coding: utf-8 -*-
"""ExRed utils."""
import json
import logging
import os
import random
import string
import sys
import traceback
import uuid
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime
from os.path import abspath, join

import requests
from behave.runner import Context
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from settings import (
    BROWSERSTACK_SESSIONS_URL,
    BROWSERSTACK_USER,
    BROWSERSTACK_PASS,
)

ScenarioData = namedtuple(
    "ScenarioData",
    [
        "actors"
    ]
)
Actor = namedtuple(
    "Actor",
    [
        "alias", "email", "password", "self_classification",
        "triage_classification", "what_do_you_want_to_export",
        "have_you_exported_before", "do_you_export_regularly",
        "are_you_incorporated", "company_name",
        "do_you_use_online_marketplaces"
    ]
)

# Set all fields to None by default.
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data.

    :return an empty ScenarioData named tuple
    """
    actors = {}
    scenario_data = ScenarioData(actors)
    return scenario_data


def unauthenticated_actor(
        alias: str, *, self_classification: str = None) -> Actor:
    """Create an instance of an unauthenticated Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.

    :param alias: alias of the Actor used within the scenario's scope
    :param self_classification: Actor's perception of its Export Status
    :return: an Actor namedtuple with all required details
    """
    email = ("test+{}{}@directory.uktrade.io"
             .format(alias, str(uuid.uuid4()))
             .replace("-", "").replace(" ", "").lower())
    password_length = 10
    password = ''.join(random.choice(string.ascii_letters)
                       for _ in range(password_length))
    return Actor(
        alias=alias, email=email, password=password,
        self_classification=self_classification)


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data.

    :param context: behave `context` object
    :param actor: an instance of Actor Named Tuple
    """
    assert isinstance(actor, Actor), ("Expected Actor named tuple but got '{}'"
                                      " instead".format(type(actor)))
    context.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(context, alias) -> Actor:
    """Get actor details from context Scenario Data.

    :param context: behave `context` object
    :param alias: alias of sought actor
    :return: an Actor named tuple
    """
    return context.scenario_data.actors.get(alias)


def update_actor(context: Context, alias: str, **kwargs):
    """Update Actor's details stored in context.scenario_data

    :param context: behave `context` object
    :param alias: alias of the Actor to update
    """
    actors = context.scenario_data.actors
    for arg in kwargs:
        if arg in Actor._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            actors[alias] = actors[alias]._replace(**{arg: kwargs[arg]})
    logging.debug(
        "Successfully updated %s's details: %s", alias, actors[alias])


def take_screenshot(driver: webdriver, page_name: str):
    """Will take a screenshot of current page.

    :param driver: Any of the WebDrivers
    :param page_name: page name which will be used in the screenshot filename
    """
    session_id = driver.session_id
    browser = driver.capabilities.get("browserName", "unknown_browser")
    version = driver.capabilities.get("version", "unknown_version")
    platform = driver.capabilities.get("platform", "unknown_platform")
    stamp = datetime.isoformat(datetime.utcnow())
    filename = ("{}-{}-{}-{}-{}-{}.png"
                .format(stamp, page_name, browser, version, platform,
                        session_id))
    file_path = abspath(join("screenshots", filename))
    driver.save_screenshot(file_path)
    logging.debug("Screenshot of %s page saved in: %s", page_name, filename)


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param message: message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in
                 message like: %s, %d
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


@contextmanager
def selenium_action(driver: webdriver, message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param driver: Selenium WebDriver required to extract browser information
    :param message: a message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in message
                 like: %s, %d
    """
    try:
        yield
    except WebDriverException as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = ("[{} v:{} os:{} session_id:{}]"
                .format(browser, version, platform, session_id))
        if args:
            message = message % args
        logging.error("%s - %s", info, message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def get_file_log_handler(
        log_formatter, *, log_level=logging.DEBUG, task_id: str = None) \
        -> logging.FileHandler:
    """Configure the console logger.

    Will use DEBUG logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_level: specifies logging level, e.g.: logging.ERROR
    :param task_id: (optional) ID of the parallel task
    :return: configured console log handler
    """
    if task_id:
        log_file = os.path.join("reports", ("behave-%s.log" % task_id))
    else:
        log_file = os.path.join("reports", "behave.log")
    print("Behave log file: {}".format(log_file))
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def init_loggers(context: Context, *, task_id: str = None):
    """Will initialize console and file loggers."""
    # configure the formatter
    fmt = ('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: '
           '%(message)s')
    log_formatter = logging.Formatter(fmt)
    log_file_handler = get_file_log_handler(log_formatter, task_id=task_id)
    # Add log file handler to Behave's logging
    logging.getLogger("selenium").setLevel(logging.WARNING)
    context.config.setup_logging(handlers=[log_file_handler])


def flag_browserstack_session_as_failed(session_id: str, reason: str):
    url = BROWSERSTACK_SESSIONS_URL.format(session_id)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "status": "failed",
        "reason": reason
    }
    auth = (BROWSERSTACK_USER, BROWSERSTACK_PASS)
    response = requests.put(
        url=url, headers=headers, data=json.dumps(data), auth=auth)
    if not response.ok:
        logging.error(
            "Failed to flagged BrowserStack session: %s as failed. "
            "BrowserStack responded with %d: %s", session_id,
            response.status_code, response.content)
    else:
        logging.error("Flagged BrowserStack session: %s as failed", session_id)
