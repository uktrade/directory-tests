# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
import socket

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from pages.sso_common import delete_supplier_data_from_sso
from settings import AUTO_RETRY, CONFIG, CONFIG_NAME, RESTART_BROWSER, TASK_ID
from utils import (
    clear_driver_cookies,
    flag_browserstack_session_as_failed,
    initialize_scenario_data,
)

try:
    import http.client as httplib
except ImportError:  # above is available in py3+, below is py2.7
    import httplib as httplib


def start_driver_session(context: Context, session_name: str):
    remote_desired_capabilities = context.remote_desired_capabilities
    remote_desired_capabilities["name"] = session_name
    local_desired_capabilities = context.local_desired_capabilities
    if CONFIG["hub_url"]:
        context.driver = webdriver.Remote(
            desired_capabilities=remote_desired_capabilities,
            command_executor=CONFIG["hub_url"],
        )
    else:
        browser_name = CONFIG["environments"][0]["browser"]
        drivers = {
            "chrome": webdriver.Chrome,
            "edge": webdriver.Edge,
            "firefox": webdriver.Firefox,
            "ie": webdriver.Ie,
            "phantomjs": webdriver.PhantomJS,
            "safari": webdriver.Safari,
        }
        print("Starting local instance of {}".format(browser_name))
        if local_desired_capabilities:
            print(
                "Will use following browser capabilities: {}".format(
                    local_desired_capabilities
                )
            )
            if browser_name.lower() in ["firefox", "edge", "ie"]:
                context.driver = drivers[browser_name.lower()](
                    capabilities=local_desired_capabilities
                )
            elif browser_name.lower() in ["chrome", "phantomjs", "safari"]:
                context.driver = drivers[browser_name.lower()](
                    desired_capabilities=local_desired_capabilities
                )
        else:
            print("Will use default browser capabilities")
            context.driver = drivers[browser_name.lower()]()
    context.driver.set_page_load_timeout(time_to_wait=27)
    try:
        context.driver.maximize_window()
        logging.debug("Maximized the window.")
    except WebDriverException:
        logging.debug("Failed to maximize the window.")
        try:
            context.driver.set_window_size(1600, 1200)
            logging.warning("Set window size to 1600x1200")
        except WebDriverException:
            logging.warning("Failed to set window size, will continue as is")
    logging.debug("Browser Capabilities: %s", context.driver.capabilities)


def before_step(context: Context, step: Step):
    """Place here code which that has to be executed before every step."""
    logging.debug("Started Step: %s %s", step.step_type, str(repr(step.name)))


def after_step(context: Context, step: Step):
    """Place here code which that has to be executed after every step."""
    logging.debug("Finished Step: %s %s", step.step_type, str(repr(step.name)))
    logging.debug("Step Duration: %s %s", str(repr(step.name)), step.duration)
    if RESTART_BROWSER == "scenario":
        if step.status == "failed":
            message = "Step '%s %s' failed. Reason: '%s'" % (
                step.step_type,
                step.name,
                step.exception,
            )
            logging.error(message)
            logging.debug(context.scenario_data)
            if "browserstack" in CONFIG_NAME:
                if hasattr(context, "driver"):
                    session_id = context.driver.session_id
                    flag_browserstack_session_as_failed(session_id, message)


def before_feature(context: Context, feature: Feature):
    """Use autoretry feature of upcoming Behave 1.2.6 which automatically
    retries failing scenarios.
    Here PR for it https://github.com/behave/behave/pull/328
    """
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(scenario, max_attempts=2)
    if RESTART_BROWSER == "feature":
        start_driver_session(context, feature.name)


def after_feature(context: Context, feature: Feature):
    if RESTART_BROWSER == "feature":
        if hasattr(context, "driver"):
            context.driver.quit()
        if feature.status == "failed":
            if hasattr(context, "scenario_data"):
                logging.debug(context.scenario_data)
            if "browserstack" in CONFIG_NAME:
                failed = len(
                    [
                        scenario
                        for scenario in feature.scenarios
                        if scenario.status == "failed"
                    ]
                )
                message = (
                    "Feature '%s' failed because of issues with %d "
                    "%s"
                    % (
                        feature.name,
                        failed,
                        "scenarios" if failed > 1 else "scenario",
                    )
                )
                if hasattr(context, "driver"):
                    session_id = context.driver.session_id
                    flag_browserstack_session_as_failed(session_id, message)
    logging.debug("QUIT DRIVER AFTER FEATURE: %s", feature.name)


@retry(stop_max_attempt_number=3)
def before_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed before every Scenario."""
    logging.debug("Starting scenario: %s", scenario.name)
    context.scenario_data = initialize_scenario_data()
    if RESTART_BROWSER == "scenario":
        start_driver_session(context, scenario.name)


def after_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed after every scenario."""
    logging.debug("Closing Selenium Driver after scenario: %s", scenario.name)
    logging.debug(context.scenario_data)
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.registered:
            delete_supplier_data_from_sso(actor.email)
    if hasattr(context, "driver"):
        if RESTART_BROWSER == "scenario":
            context.driver.quit()
        if RESTART_BROWSER == "feature":
            clear_driver_cookies(context.driver)
    else:
        logging.warning(
            "Context does not have Selenium 'driver' object. This might be "
            "happen when it wasn't initialized properly"
        )
    if scenario.status == "failed":
        if hasattr(context, "driver"):
            from selenium.webdriver.remote.command import Command

            try:
                context.driver.execute(Command.STATUS)
            except (socket.error, httplib.CannotSendRequest):
                msg = (
                    "Remote driver is unresponsive after scenario: %s. Will"
                    " try to recover selenium session" % scenario.name
                )
                print(msg)
                session_id = context.driver.session_id
                flag_browserstack_session_as_failed(session_id, msg)
                logging.error(msg)
                start_driver_session(
                    context, "session-recovered-after-scenario"
                )


def before_all(context: Context):
    """Place here code which has to be executed before all scenarios."""
    remote_desired_capabilities = CONFIG["environments"][TASK_ID]
    local_desired_capabilities = CONFIG["capabilities"]

    for key in CONFIG["capabilities"]:
        if key not in remote_desired_capabilities:
            remote_desired_capabilities[key] = CONFIG["capabilities"][key]

    context.remote_desired_capabilities = remote_desired_capabilities
    context.local_desired_capabilities = local_desired_capabilities

    context.config.setup_logging(configfile=".behave_logging")
