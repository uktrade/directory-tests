# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
from collections import namedtuple

from behave.model import Scenario, Step
from behave.runner import Context

import drivers
from settings import BROWSER, HEIGHT, WIDTH
from utils import init_loggers, take_screenshot

ScenarioData = namedtuple(
    "ScenarioData",
    [
        "actors"
    ]
)
Actor = namedtuple(
    "Actor",
    [
        "alias", "classification"
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


def before_step(context: Context, step: Step):
    """Place here code which that has to be executed before every step.

    :param context: Behave Context object
    :param step: Behave Step object
    """
    logging.debug('Step: %s %s', step.step_type, str(repr(step.name)))


def after_step(context: Context, step: Step):
    """Place here code which that has to be executed after every step.

    :param context: Behave Context object
    :param step: Behave Step object
    """
    logging.debug('Step: %s %s', step.step_type, str(repr(step.name)))
    if step.status == "failed":
        logging.debug(
            'Step "%s %s" failed. Reason: "%s"', step.step_type, step.name,
            step.exception)
        if hasattr(context, "driver"):
            if hasattr(context, "current_page"):
                page_name = "{}-{}_failure".format(step.name, context.current_page.NAME)
            else:
                page_name = "{}-last_page_failure".format(step.name)
            take_screenshot(context.driver, page_name)


def before_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed before every Scenario.

    :param context: Behave Context object
    :param scenario: Behave Scenario object
    """
    logging.debug('Starting scenario: %s', scenario.name)
    context.scenario_data = initialize_scenario_data()
    logging.debug('Starting Selenium Driver for scenario: %s', scenario.name)
    context.driver = drivers.get(
        context.browser_name, width=context.viewport_width,
        height=context.viewport_height)


def after_scenario(context: Context, scenario: Scenario):
    """Place here code which has to be executed after every scenario.

    :param context: Behave Context object
    :param scenario: Behave Scenario object
    """
    logging.debug('Quitting Selenium Driver after scenario: %s', scenario.name)
    context.driver.close()
    context.driver.quit()


def before_all(context: Context):
    """Place here code which has to be executed before all scenarios.

    :param context: Behave Context object
    """
    init_loggers(context)
    context.browser_name = BROWSER
    context.viewport_width = WIDTH
    context.viewport_height = HEIGHT
