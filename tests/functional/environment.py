# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
import os
from pprint import pformat

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry

from tests.functional.utils.context_utils import (
    initialize_scenario_data,
    patch_context
)
from tests.functional.utils.db_utils import (
    delete_expired_django_sessions,
    delete_supplier_data
)
from tests.functional.utils.generic import (
    blue,
    extract_form_errors,
    extract_main_error,
    extract_section_error,
    green,
    init_loggers,
    print_response,
    red
)
from tests.functional.utils.request import REQUEST_EXCEPTIONS


def before_feature(context, feature):
    """Use autoretry feature of upcoming Behave 1.2.6 which automatically
    retries failing scenarios.
    Here PR for it https://github.com/behave/behave/pull/328
    """
    for scenario in feature.scenarios:
        patch_scenario_with_autoretry(scenario, max_attempts=2)


def before_step(context, step):
    logging.debug('Step: %s %s', step.step_type, str(repr(step.name)))


def after_step(context, step):
    if step.status == "failed":
        logging.debug(
            'Step "%s %s" failed. Reason: "%s"', step.step_type, step.name,
            step.exception)
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
                red("Found errors in the `main` part of the response")
                print(main_errors)
            if section_errors:
                red("Found errors in the `section` of the response")
                print(section_errors)
            if form_errors:
                red("Found form related error(s)")
                print(form_errors)
            green("Last recorded request & response")
            print_response(res, trim=False)
        else:
            blue("There's no response content to log")


def before_scenario(context, scenario):
    logging.debug('Starting scenario: %s', scenario.name)
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def after_scenario(context, scenario):
    logging.debug("Deleting supplier data from FAB & SSO DBs")
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.session:
            actor.session.close()
            logging.debug("Closed Requests session for %s", actor.alias)
        if actor.type == "supplier":
            delete_supplier_data("DIRECTORY", actor.email)
            delete_supplier_data("SSO", actor.email)
            if scenario.status == "failed":
                red("Deleted data from DIR/SSO DBs for user: %s" % actor.email)
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug('Finished scenario: %s', scenario.name)


def before_all(context):
    suffix = ""
    task_id = os.environ.get("TASK_ID", "")
    feature_dir = os.environ.get("FEATURE_DIR", "")
    if task_id and feature_dir:
        suffix = "{}-{}".format(task_id, feature_dir)
    init_loggers(context, suffix=suffix)
    # this will add some handy functions to the `context` object
    patch_context(context)


def after_all(context):
    delete_expired_django_sessions()
