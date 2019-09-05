# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
import http.client as httplib
import socket

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.command import Command

from pages import sso
from settings import (
    AUTO_RETRY,
    CONFIG,
    CONFIG_NAME,
    RESTART_BROWSER,
    TASK_ID,
    MAX_SESSION_RECOVERY_RETRIES,
)
from pages.common_actions import (
    clear_driver_cookies,
    flag_browserstack_session_as_failed,
    initialize_scenario_data,
    show_snackbar_message,
)
from utils.pdf import NoPDFMinerLogEntriesFilter


def start_driver_session(context: Context, session_name: str):
    remote_desired_capabilities = context.remote_desired_capabilities
    remote_desired_capabilities["name"] = session_name
    local_desired_capabilities = context.local_desired_capabilities
    if CONFIG["hub_url"]:
        context.driver = webdriver.Remote(
            desired_capabilities=remote_desired_capabilities,
            command_executor=CONFIG["hub_url"],
        )
        logging.warning(f"Started new remote session: {context.driver.session_id}")
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
        print(f"Starting local instance of {browser_name}")
        if local_desired_capabilities:
            print(
                f"Will use following browser capabilities: {local_desired_capabilities}"
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
            import os
            if browser_name.lower() == "chrome":
                from selenium.webdriver.chrome.options import Options
                options = Options()
                if os.getenv("HEADLESS", "false") == "true":
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1600x2200")
                options.add_argument("--start-maximized")
                options.add_argument("--disable-extensions")
                options.add_argument("--no-sandbox")
            elif browser_name.lower() == "firefox":
                from selenium.webdriver.firefox.options import Options
                options = Options()
                if os.getenv("HEADLESS", "false") == "true":
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1600x2200")
            context.driver = drivers[browser_name.lower()](options=options)
    context.driver.set_page_load_timeout(time_to_wait=27.0)
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
    logging.debug(f"Browser Capabilities: {context.driver.capabilities}")


def restart_webdriver_if_unresponsive(context: Context, scenario: Scenario):
    if hasattr(context, "driver"):
        session_id = context.driver.session_id
        clean_name = scenario.name.lower().replace(" ", "-")[0:220]
        try:
            response = context.driver.execute(Command.STATUS)
            logging.debug(f"WebDriver Status: {response}")
            if "sessionId" in response and response["sessionId"] is None:
                msg = (
                    f"Looks like current session_id: {session_id} became unresponsive, "
                    f"will try to spawn a new one"
                )
                print(msg)
                logging.error(msg)
                flag_browserstack_session_as_failed(session_id, msg)
                start_driver_session(
                    context, f"session-recovered-for-scenario-{clean_name}"
                )
                msg = (
                    f"An unresponsive session '{session_id}' was recovered and new "
                    f"session ID is: '{context.driver.session_id}'"
                )
                print(msg)
                logging.warning(msg)
        except (socket.error, httplib.CannotSendRequest):
            msg = (
                f"Remote driver became unresponsive after scenario: "
                f"{scenario.name}. Will try to recover the selenium session"
            )
            print(msg)
            logging.error(msg)
            flag_browserstack_session_as_failed(session_id, msg)
            start_driver_session(
                context, f"driver-recovered-for-scenario-{clean_name}"
            )
            msg = (
                f"An unresponsive driver with ID: '{session_id}' was recovered and new "
                f"driver session ID is: '{context.driver.session_id}'"
            )
            print(msg)
            logging.error(msg)
    else:
        logging.error("Context doesn't have 'driver' attribute")


def before_step(context: Context, step: Step):
    """Place here code which that has to be executed before every step."""
    logging.debug(f"Started Step: {step.step_type} {str(repr(step.name))}")


def after_step(context: Context, step: Step):
    """Place here code which that has to be executed after every step."""
    logging.debug(f"Finished Step: {step.step_type} {str(repr(step.name))}")
    logging.debug(f"Step Duration: {str(repr(step.name))} {step.duration}")
    if RESTART_BROWSER == "scenario":
        if step.status == "failed":
            message = (
                f"Step '{step.step_type} {step.name}' failed: '{step.exception}'"
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
            logging.debug(f"Quit driver after feature: '{feature.name}'")
            try:
                context.driver.quit()
            except WebDriverException as ex:
                logging.error(
                    f"Failed to quit the driver after feature '{feature.name}': "
                    f"{ex.msg}"
                )
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
                if hasattr(context, "driver"):
                    session_id = context.driver.session_id
                    message = (
                        f"Feature '{feature.name}' failed because of issues with "
                        f"{failed} scenarios"
                    )
                    flag_browserstack_session_as_failed(session_id, message)


@retry(stop_max_attempt_number=3)
def before_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed before every Scenario."""
    logging.debug("Starting scenario: %s", scenario.name)
    # message = f"Start: {scenario.name} | {scenario.filename}:{scenario.line}"
    # show_snackbar_message(context.driver, message)
    context.scenario_data = initialize_scenario_data()
    context.session_recovery_counter = 0
    if RESTART_BROWSER == "scenario":
        start_driver_session(context, scenario.name)


def after_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed after every scenario."""
    try:
        response = context.driver.execute(Command.STATUS)
        logging.debug(f"WebDriver Status: {response}")
    except (socket.error, httplib.CannotSendRequest):
        logging.error(
            f"Remote browser driver became unresponsive after scenario: {scenario.name}"
        )
    # message = f"Finish: {scenario.name} | {scenario.filename}:{scenario.line}"
    if scenario.status == "failed":
        if context.session_recovery_counter <= MAX_SESSION_RECOVERY_RETRIES:
            logging.error(
                f"Failed scenario: '{scenario.name}', will try to restart driver "
                f"session if it's unresponsive"
            )
            restart_webdriver_if_unresponsive(context, scenario)
            context.session_recovery_counter += 1
        else:
            logging.error(
                f"Failed to recover WebDriver session after "
                f"{MAX_SESSION_RECOVERY_RETRIES} attempts"
            )
    # try:
    #     show_snackbar_message(context.driver, message)
    # except WebDriverException:
    #     logging.error(f"Failed to show snackbar with message: {message}")
    # in order to show the snackbar message after scenario, an explicit wait
    # had to be added
    # time.sleep(0.2)
    logging.debug(context.scenario_data)
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.registered:
            sso.common.delete_supplier_data_from_sso(actor.email)
    if hasattr(context, "driver"):
        if RESTART_BROWSER == "scenario":
            logging.debug(
                f"Closing Selenium Driver after scenario: {scenario.name}")
            context.driver.quit()
        if RESTART_BROWSER == "feature":
            clear_driver_cookies(context.driver)
    else:
        logging.warning(
            "Context does not have Selenium 'driver' object. This might be "
            "happen when it wasn't initialized properly"
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
    logger = logging.getLogger()
    logger.addFilter(NoPDFMinerLogEntriesFilter())

    logging.debug(f"remote_desired_capabilities:\n{remote_desired_capabilities}")
    logging.debug(f"local_desired_capabilities:\n{local_desired_capabilities}")
