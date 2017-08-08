# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
from pprint import pformat

from tests.functional.features.context_utils import (
    initialize_scenario_data,
    patch_context
)
from tests.functional.features.db_cleanup import (
    delete_expired_django_sessions,
    delete_supplier_data
)
from tests.functional.features.utils import (
    blue,
    extract_form_errors,
    extract_section_error,
    green,
    init_loggers,
    red
)


def before_step(context, step):
    logging.debug('Step: %s %s', step.step_type, str(repr(step.name)))


def after_step(context, step):
    offset = 1024
    if step.status == "failed":
        logging.debug(
            'Step "%s %s" failed. Reason: "%s"', step.step_type, step.name,
            step.exception)
        logging.debug(context.scenario_data)
        red("\nScenario data:")
        print(pformat(context.scenario_data))
        if hasattr(context, "response"):
            res = context.response
            content = res.content.decode("utf-8")
            section_errors = extract_section_error(content)
            form_errors = extract_form_errors(content)
            if section_errors:
                red("Found errors in the main section of the response")
                print(section_errors)
            if form_errors:
                red("Found form related error(s)")
                print(form_errors)
            red("Last recorded request & response")
            if res.history:
                green("Request was redirected")
                for resp in res.history:
                    green("Intermediate REQ:")
                    print(resp.request.method, resp.url)
                    green("Intermediate REQ Headers:")
                    print(pformat(resp.request.headers))
                    green("Intermediate RESP:")
                    print(resp.status_code, resp.reason)
                    green("Intermediate RESP Headers:")
                    print(pformat(resp.headers))
                    blue("Final REQ URL:")
            else:
                blue("REQ URL: ")
            print(res.request.method, res.request.url)
            blue("REQ Headers: ")
            print(pformat(res.request.headers))
            if hasattr(res.request, "body"):
                if res.request.body:
                    if len(res.request.body) > offset:
                        blue("REQ Body (trimmed):")
                        print(res.request.body[:offset])
                    else:
                        blue("REQ Body:")
                        print(res.request.body)
            blue("RESP Headers:")
            print(pformat(res.headers))
            blue("RESP Content:")
            print(content)
            delattr(context, "response")
        else:
            print("\nThere's no response content to log")


def before_scenario(context, scenario):
    logging.debug('Starting scenario: %s', scenario.name)
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def after_scenario(context, scenario):
    logging.debug("Deleting supplier data from FAB & SSO DBs")
    actors = context.scenario_data.actors
    for actor in actors.values():
        delete_supplier_data("DIRECTORY", actor.email)
    for actor in actors.values():
        delete_supplier_data("SSO", actor.email)
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug('Finished scenario: %s', scenario.name)


def before_all(context):
    init_loggers(context)
    # this will add some handy functions to the `context` object
    patch_context(context)


def after_all(context):
    delete_expired_django_sessions()
