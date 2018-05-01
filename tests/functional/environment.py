# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
from pprint import pformat

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from tests.functional.utils.context_utils import (
    initialize_scenario_data,
    patch_context
)
from tests.functional.utils.generic import (
    blue,
    delete_supplier_data_from_dir,
    delete_supplier_data_from_sso,
    extract_form_errors,
    extract_main_error,
    extract_section_error,
    green,
    print_response,
    red
)
from tests.functional.utils.request import REQUEST_EXCEPTIONS
from tests.settings import AUTO_RETRY, AUTO_RETRY_MAX_ATTEMPTS


def before_feature(context, feature):
    """Use autoretry feature of upcoming Behave 1.2.6 which automatically
    retries failing scenarios.
    Here PR for it https://github.com/behave/behave/pull/328
    """
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(
                scenario, max_attempts=AUTO_RETRY_MAX_ATTEMPTS)


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
                red(
                    "Found words in the `main` part of the response that might"
                    " suggest the root cause of the error")
                print(main_errors)
            if section_errors:
                red(
                    "Found words in the `section` part of the response that "
                    "might suggest the root cause of the error")
                print(section_errors)
            if form_errors:
                red(
                    "Found words in the `form` part of the response that might"
                    " suggest the root cause of the error")
                print(form_errors)
            green("Last recorded request & response")
            print_response(res, trim=True, content_only=True)
        else:
            blue("There's no response content to log")


def before_scenario(context, scenario):
    logging.debug('Starting scenario: %s', scenario.name)
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def after_scenario(context, scenario):
    logging.debug("Deleting supplier data from Directory & SSO DBs")
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.session:
            actor.session.close()
            logging.debug("Closed Requests session for %s", actor.alias)
        if actor.type == "supplier":
            delete_supplier_data_from_sso(actor.email, context=context)
            if actor.company_alias:
                company = context.get_company(actor.company_alias)
                if company.deleted:
                    continue
                delete_supplier_data_from_dir(company.number, context=context)
                context.set_company_details(alias=company.alias, deleted=True)
            if scenario.status == "failed":
                red("Deleted %s supplier data from DIR & SSO DB" % actor.email)
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug('Finished scenario: %s', scenario.name)


def before_all(context):
    context.config.setup_logging(configfile=".behave_logging")
    # this will add some handy functions to the `context` object
    patch_context(context)
