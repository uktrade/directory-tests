# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context

from directory_tests_shared.pdf import NoPDFMinerLogEntriesFilter
from directory_tests_shared.settings import AUTO_RETRY
from pages import sso
from pages.common_actions import initialize_scenario_data
from utils.browser import get_driver_capabilities, start_driver_session

DRIVER_CAPABILITIES = get_driver_capabilities()


def before_all(context: Context):
    context.driver_capabilities = DRIVER_CAPABILITIES

    context.config.setup_logging(configfile=".behave_logging")
    logger = logging.getLogger()
    logger.addFilter(NoPDFMinerLogEntriesFilter())


def before_feature(context: Context, feature: Feature):
    """Use autoretry feature of upcoming Behave 1.2.6 which automatically
    retries failing scenarios.
    Here's a PR for it https://github.com/behave/behave/pull/328
    """
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(scenario, max_attempts=2)


def before_scenario(context: Context, scenario: Scenario):
    logging.debug(f"Starting scenario: {scenario.name}")
    context.scenario_data = initialize_scenario_data()
    session_name = f"{scenario.feature.name} -> {scenario.name}"
    context.driver = start_driver_session(session_name, DRIVER_CAPABILITIES)


def before_step(context: Context, step: Step):
    logging.debug(f"Started step: {step.step_type.capitalize()} {step.name}")


def after_step(context: Context, step: Step):
    logging.debug(
        f"Finished step: {round(step.duration, 3)} {step.step_type.capitalize()} {step.name}"
    )
    if round(step.duration, 3) > 5:
        logging.warning(
            f"SLOW step: {round(step.duration, 3)} {step.step_type.capitalize()} {step.name}"
        )


def after_scenario(context: Context, scenario: Scenario):
    logging.debug(f"Scenario data: {context.scenario_data}")
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.registered:
            sso.common.delete_supplier_data_from_sso(actor.email)

    logging.debug(f"Finished scenario: {round(scenario.duration, 3)} → {scenario.name}")
    context.driver.quit()
