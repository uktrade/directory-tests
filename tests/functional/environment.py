# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
from pprint import pformat

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import Feature, Scenario, Step
from behave.runner import Context

from directory_tests_shared.pdf import NoPDFMinerLogEntriesFilter
from directory_tests_shared.settings import AUTO_RETRY, AUTO_RETRY_MAX_ATTEMPTS
from directory_tests_shared.utils import blue, green, red
from tests.functional.utils.context_utils import initialize_scenario_data
from tests.functional.utils.generic import (
    extract_form_errors,
    extract_main_error,
    extract_section_error,
    print_response,
)
from tests.functional.utils.request import REQUEST_EXCEPTIONS


def before_all(context: Context):
    context.config.setup_logging(configfile=".behave_logging")
    logger = logging.getLogger()
    logger.addFilter(NoPDFMinerLogEntriesFilter())


def before_feature(context: Context, feature: Feature):
    """Use autoretry feature which automatically retries failing scenarios."""
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(
                scenario, max_attempts=AUTO_RETRY_MAX_ATTEMPTS
            )


def before_scenario(context: Context, scenario: Scenario):
    logging.debug(f"Starting scenario: {scenario.name}")
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def before_step(context: Context, step: Step):
    logging.debug(f"Started step: {step.step_type.capitalize()} {step.name}")


def after_step(context: Context, step: Step):
    logging.debug(
        f"Finished step: {round(step.duration, 3)} {step.step_type.capitalize()} "
        f"{step.name}"
    )
    if step.status == "failed":
        logging.debug(
            f"Step: {step.step_type.capitalize()} {step.name} failed. Reason: "
            f"{step.exception}"
        )
        logging.debug(context.scenario_data)
        red("\nScenario data:")
        print(pformat(context.scenario_data))
        has_content = hasattr(context, "response")
        is_request_exception = isinstance(step.exception, REQUEST_EXCEPTIONS)
        if not is_request_exception and has_content:
            res = context.response
            content = res.content.decode("utf-8")
            main_errors = extract_main_error(content)
            section_errors = extract_section_error(content)
            form_errors = extract_form_errors(content)
            if main_errors:
                red(
                    "Found words in the `main` part of the response that might"
                    " suggest the root cause of the error"
                )
                print(main_errors)
            if section_errors:
                red(
                    "Found words in the `section` part of the response that "
                    "might suggest the root cause of the error"
                )
                print(section_errors)
            if form_errors:
                red(
                    "Found words in the `form` part of the response that might"
                    " suggest the root cause of the error"
                )
                print(form_errors)
            green("Last recorded request & response")
            print_response(res, trim=True, content_only=True)
        else:
            blue("There's no response content to log")


def after_scenario(context: Context, scenario: Scenario):
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.session:
            actor.session.close()
            logging.debug(f"Closed Requests session for {actor.alias}")
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug(f"Finished scenario: {round(scenario.duration, 3)} → {scenario.name}")
