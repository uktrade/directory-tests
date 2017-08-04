# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from tests.functional.features.context_utils import (
    initialize_scenario_data,
    patch_context
)
from tests.functional.features.db_cleanup import (
    delete_expired_django_sessions,
    delete_supplier_data
)
from tests.functional.features.utils import (
    BLUE,
    GREEN,
    RED,
    init_loggers,
    printout
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
        printout("\nScenario data:\n", RED)
        print(context.scenario_data)
        if hasattr(context, "response"):
            res = context.response
            content = res.content.decode("utf-8")
            printout("\nLast recorded request & response\n", RED)
            if res.history:
                printout("\nRequest was redirected\n", GREEN)
                for resp in res.history:
                    printout("\nIntermediate REQ:\n", GREEN)
                    print(resp.request.method, resp.url)
                    printout("Intermediate REQ Headers:", GREEN)
                    print(resp.request.headers)
                    printout("Intermediate RESP:", GREEN)
                    print(resp.status_code, resp.reason)
                    printout("Intermediate RESP Headers:", GREEN)
                    print(resp.headers)
                    printout("\nFinal REQ URL:\n", BLUE)
            else:
                printout("\nREQ URL:\n", BLUE)
            print(res.request.method, res.request.url)
            printout("\nREQ Headers:\n", BLUE)
            print(res.request.headers)
            if hasattr(res.request, "body"):
                if res.request.body:
                    if len(res.request.body) > offset:
                        printout("\nREQ Body (trimmed):\n", BLUE)
                        print(res.request.body[:offset])
                    else:
                        printout("\nREQ Body:\n", BLUE)
                        print(res.request.body)
            printout("\nRESP Headers:\n", BLUE)
            print(res.headers)
            printout("\nRESP Content:\n", BLUE)
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
