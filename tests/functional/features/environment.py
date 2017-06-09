# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from tests.functional.features.ScenarioData import initialize_scenario_data
from tests.functional.features.ScenarioData import patch_context
from tests.functional.features.utils import init_loggers


def before_step(context, step):
    logging.debug('Step: {} {}'.format(step.step_type, str(repr(step.name))))


def after_step(context, step):
    logging.debug(context.scenario_data)
    if step.status == "failed":
        msg = 'Step "{} {}" has failed. Reason: "{}".'.format(
            step.step_type, step.name, step.exception)
        logging.debug(msg)


def before_scenario(context, scenario):
    logging.debug('Starting scenario: {}'.format(scenario.name))
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def after_scenario(context, scenario):
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug('Finished scenario: {}'.format(scenario.name))


def before_all(context):
    init_loggers()
    # this will add some handy functions to the `context` object
    patch_context(context)
