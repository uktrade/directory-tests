# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from behave.model import Scenario, Step
from behave.runner import Context
from selenium import webdriver

from settings import (
    BROWSER_STACK_CONFIG,
    BROWSER_STACK_EXECUTOR_URL,
    BROWSER_STACK_TASK_ID
)
from utils import (
    flag_browserstack_session_as_failed,
    init_loggers,
    initialize_scenario_data
)


def before_step(context: Context, step: Step):
    """Place here code which that has to be executed before every step.

    :param context: Behave Context object
    :param step: Behave Step object
    """
    logging.debug('Started Step: %s %s', step.step_type, str(repr(step.name)))


def after_step(context: Context, step: Step):
    """Place here code which that has to be executed after every step.

    :param context: Behave Context object
    :param step: Behave Step object
    """
    logging.debug("Finished Step: %s %s", step.step_type, str(repr(step.name)))
    if step.status == "failed":
        message = "Step '%s %s' failed. Reason: '%s'" % (step.step_type,
                                                         step.name,
                                                         step.exception)
        logging.error(message)
        if hasattr(context, "driver"):
            session_id = context.driver.session_id
            flag_browserstack_session_as_failed(session_id, message)


def before_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed before every Scenario.

    :param context: Behave Context object
    :param scenario: Behave Scenario object
    """
    logging.debug('Starting scenario: %s', scenario.name)
    context.scenario_data = initialize_scenario_data()
    desired_capabilities = context.desired_capabilities
    desired_capabilities["name"] = scenario.name
    context.driver = webdriver.Remote(
        desired_capabilities=desired_capabilities,
        command_executor=BROWSER_STACK_EXECUTOR_URL
    )
    context.driver.maximize_window()


def after_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed after every scenario.

    :param context: Behave Context object
    :param scenario: Behave Scenario object
    """
    logging.debug(
        "Deleting all cookies and closing Selenium Driver after scenario: %s",
        scenario.name)
    # if context.driver.get_cookies():
    #     context.driver.delete_all_cookies()
    context.driver.quit()


def before_all(context: Context):
    """Place here code which has to be executed before all scenarios.

    :param context: Behave Context object
    """
    desired_capabilities = BROWSER_STACK_CONFIG["environments"][BROWSER_STACK_TASK_ID]
    browser_name = desired_capabilities["browser"]

    for key in BROWSER_STACK_CONFIG["capabilities"]:
        if key not in desired_capabilities:
            desired_capabilities[key] = BROWSER_STACK_CONFIG["capabilities"][key]

    task_id = "{}-{}".format(BROWSER_STACK_TASK_ID, browser_name)
    init_loggers(context, task_id=task_id)

    context.desired_capabilities = desired_capabilities
    context.browser_name = browser_name
