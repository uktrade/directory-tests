# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context

from directory_tests_shared.pdf import NoPDFMinerLogEntriesFilter
from directory_tests_shared.settings import (
    AUTO_RETRY,
    BROWSER_ENVIRONMENT,
    BROWSER_RESTART_POLICY,
)
from pages import sso
from pages.common_actions import initialize_scenario_data
from utils.browser import (
    clear_driver_cookies,
    flag_browserstack_session_as_failed,
    get_driver_capabilities,
    is_driver_responsive,
    start_driver_session,
    terminate_driver,
)

DRIVER_CAPABILITIES = get_driver_capabilities()


def before_all(context: Context):
    context.driver_capabilities = DRIVER_CAPABILITIES
    print(f"CAPABILITIES: {DRIVER_CAPABILITIES}")
    logging.debug(f"CAPABILITIES: {DRIVER_CAPABILITIES}")

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
    if BROWSER_RESTART_POLICY == "feature":
        context.driver = start_driver_session(feature.name, DRIVER_CAPABILITIES)


def before_scenario(context: Context, scenario: Scenario):
    logging.debug(f"Starting scenario: {scenario.name}")
    context.scenario_data = initialize_scenario_data()
    if BROWSER_RESTART_POLICY == "scenario":
        context.driver = start_driver_session(scenario.name, DRIVER_CAPABILITIES)
    if BROWSER_RESTART_POLICY == "feature":
        if (not context.driver) or not is_driver_responsive(context.driver):
            context.driver = start_driver_session(scenario.name, DRIVER_CAPABILITIES)


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

    if not hasattr(context, "driver"):
        return

    driver = getattr(context, "driver")

    clear_driver_cookies(driver)

    if BROWSER_RESTART_POLICY == "scenario":
        if scenario.status == "failed" and BROWSER_ENVIRONMENT == "remote":
            session_id = driver.session_id
            reason = f"Scenario: '{scenario.name}' failed: {scenario.exception}"
            flag_browserstack_session_as_failed(session_id, reason)
        terminate_driver(driver)

    if BROWSER_RESTART_POLICY == "feature" and scenario.status == "failed":
        if not is_driver_responsive(driver) and BROWSER_ENVIRONMENT == "remote":
            session_id = driver.session_id
            reason = f"Scenario: '{scenario.name}' failed: {scenario.exception}"
            flag_browserstack_session_as_failed(session_id, reason)
            terminate_driver(driver)
    logging.debug(f"Finished scenario: {round(scenario.duration, 3)} → {scenario.name}")


def after_feature(context: Context, feature: Feature):
    if BROWSER_RESTART_POLICY == "feature":
        if hasattr(context, "driver"):
            driver = context.driver
            if (
                driver
                and feature.status == "failed"
                and BROWSER_ENVIRONMENT == "remote"
            ):
                scenarios = feature.scenarios
                failed = sum(1 for scenario in scenarios if scenario.status == "failed")
                session_id = driver.session_id
                reason = (
                    f"{failed} out of {len(feature.scenarios)} scenarios in "
                    f"'{feature.name}' failed"
                )
                flag_browserstack_session_as_failed(session_id, reason)
            terminate_driver(driver)
        else:
            logging.warning(f"context.driver == None after '{feature.name}'")


def after_all(context: Context):
    if hasattr(context, "driver"):
        terminate_driver(context.driver)
