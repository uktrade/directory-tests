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
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from settings import (
    BROWSERSTACK_SESSIONS_URL,
    BROWSERSTACK_USER,
    BROWSERSTACK_PASS,
    TAKE_SCREENSHOTS
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
        "do_you_use_online_marketplaces", "created_personalised_journey",
        "article_group", "article_category", "article_location",
        "visited_articles", "articles_read_counter",
        "articles_time_to_complete", "articles_total_number",
        "article_list_read_counter", "article_list_time_to_complete",
        "article_list_total_number",
        "case_study_title", "email_confirmation_link", "registered"
    ]
)

VisitedArticle = namedtuple(
    "VisitedArticle",
    [
        "index", "title", "time_to_read"
    ]
)

# Set all fields to None by default.
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
VisitedArticle.__new__.__defaults__ = (None,) * len(VisitedArticle._fields)


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
    password_length = 20
    password = ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(password_length))
    return Actor(
        alias=alias, email=email, password=password,
        self_classification=self_classification, visited_articles=[])


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


@retry(stop_max_attempt_number=3)
def take_screenshot(driver: webdriver, page_name: str):
    """Will take a screenshot of current page.

    :param driver: Any of the WebDrivers
    :param page_name: page name which will be used in the screenshot filename
    """
    if TAKE_SCREENSHOTS:
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
        logging.debug(
            "Screenshot of %s page saved in: %s", page_name, filename)
    else:
        logging.debug(
            "Taking screenshots is disabled. In order to turn it on please set"
            " n environment variable TAKE_SCREENSHOTS=true")


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
    :raises WebDriverException or NoSuchElementException
    """
    try:
        yield
    except (WebDriverException, NoSuchElementException) as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = ("[{} v:{} os:{} session_id:{}]"
                .format(browser, version, platform, session_id))
        if args:
            message = message % args
        print("%s - %s" % (info, message))
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


def wait_for_visibility(
        driver: webdriver, *, by_css: str = None,
        by_id: str = None, time_to_wait: int = 5):
    """Wait until element is visible.

    :param driver: Selenium driver
    :param by_css: CSS selector to locate the element to wait for
    :param by_id: ID of the element to wait for
    :param time_to_wait: maximum number of seconds to wait
    """
    assert by_id or by_css, "Provide ID or CSS selector"
    if by_css:
        by_locator = (By.CSS_SELECTOR, by_css)
    else:
        by_locator = (By.ID, by_id)
    WebDriverWait(driver, time_to_wait).until(
        expected_conditions.visibility_of_element_located(by_locator))


def check_if_element_is_not_present(
        driver: webdriver, *, by_css: str = None,
        by_id: str = None, element_name: str = ""):
    """Find element by CSS selector or it's ID.

    :param driver: Selenium driver
    :param by_css: CSS selector to locate the element to wait for
    :param by_id: ID of the element to wait for
    :return: found WebElement
    """
    assert by_id or by_css, "Provide ID or CSS selector"
    try:
        if by_css:
            driver.find_element_by_css_selector(by_css)
        else:
            driver.find_element_by_id(by_id)
        found = True
    except NoSuchElementException:
        found = False
    with assertion_msg(
            "Expected not to find %s element identified by '%s'", element_name,
            by_id or by_css):
        assert not found


def find_element(
        driver: webdriver, *, by_css: str = None,
        by_id: str = None, element_name: str = "") -> WebElement:
    """Find element by CSS selector or it's ID.

    :param driver: Selenium driver
    :param by_css: CSS selector to locate the element to wait for
    :param by_id: ID of the element to wait for
    :param element_name: (optional) human friend element name
    :return: found WebElement
    """
    assert by_id or by_css, "Provide ID or CSS selector"
    with selenium_action(
            driver, "Couldn't find element %s using '%s'", element_name,
            by_css or by_id):
        if by_css:
            element = driver.find_element_by_css_selector(by_css)
        else:
            element = driver.find_element_by_id(by_id)
    return element


def find_elements(
        driver: webdriver, *, by_css: str = None,
        by_id: str = None) -> list:
    """Find element by CSS selector or it's ID.

    :param driver: Selenium driver
    :param by_css: CSS selector to locate the element to wait for
    :param by_id: ID of the element to wait for
    :return: a list of found WebElements
    """
    assert by_id or by_css, "Provide ID or CSS selector"
    with selenium_action(
            driver, "Couldn't find elements using '%s'", by_css or by_id):
        if by_css:
            elements = driver.find_elements_by_css_selector(by_css)
        else:
            elements = driver.find_elements_by_id(by_id)
    return elements


def clear_driver_cookies(driver: webdriver):
    try:
        cookies = driver.get_cookies()
        logging.debug("COOKIES: %s", cookies)
        driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies")
        cookies = driver.get_cookies()
        logging.debug("Driver cookies after clearing them: %s", cookies)
    except WebDriverException as ex:
        logging.error("Failed to clear cookies: '%s'", ex.msg)
