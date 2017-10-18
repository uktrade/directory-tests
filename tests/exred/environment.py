# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
import os
from collections import namedtuple

from behave.model import Scenario, Step
from behave.runner import Context

from tests.exred import drivers
from tests.functional.utils.generic import init_loggers

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
    init_loggers(context, log_file=os.path.join(
        ".", "tests", "exred", "reports", "behave.log"))
    context.browser_name = os.environ.get("BROWSER", "chrome")
    context.viewport_width = os.environ.get("WIDTH", 1600)
    context.viewport_height = os.environ.get("HEIGHT", 1200)
