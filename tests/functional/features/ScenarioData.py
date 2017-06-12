# -*- coding: utf-8 -*-
"""Contains named tuple that are used to create the Scenario Data."""
import logging
from types import MethodType

from collections import namedtuple


ScenarioData = namedtuple('ScenarioData', ['actors', 'unregistered_companies'])
Actor = namedtuple('Actor', ['alias', 'http_client'])
UnregisteredCompany = namedtuple('UnregisteredCompany', ['alias', 'title',
                                                         'number', 'details'])


def initialize_scenario_data():
    """Will initialize the Scenario Data.

    :return an empty ScenarioData named tuple
    :rtype ScenarioData
    """
    actors = []
    unregistered_companies = []
    scenario_data = ScenarioData(actors, unregistered_companies)
    return scenario_data


def add_actor(self, actor):
    """Will add Actor to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param actor: an instance of Actor Named Tuple
    :type actor: features.ScenarioData.Actor
    """
    assert isinstance(actor, Actor), ("Expected Actor named tuple but got '{}' "
                                      "instead".format(type(actor)))
    self.scenario_data.actors.append(actor)
    logging.debug("Successfully added actor: {} to Scenario Data"
                  .format(actor.alias))


def get_actor(self, alias):
    """Get actor details from context scenario data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    :return: an Actor named tuple
    """
    res = None
    for actor in self.scenario_data.actors:
        if actor.alias == alias:
            res = actor
            logging.debug("Found actor: '{}' in Scenario Data".format(alias))
    assert res is not None, ("Couldn't find actor '{}' in Scenario Data"
                             .format(alias))
    return res


def get_actor_client(self, alias):
    """Get actor's HTTP client from context scenario data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    :return: Actor's HTTP client
    """
    actor = self.get_actor(alias)
    assert actor.http_client is not None, ("{}'s HTTP client is not set!"
                                           .format(alias))
    return actor.http_client


def add_unregistered_company(self, company):
    """Will add an Unregistered Company to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param company: an instance of UnregisteredCompany Tuple
    :type company: features.ScenarioData.UnregisteredCompany
    """
    assert isinstance(company, UnregisteredCompany), (
        "Expected UnregisteredCompany named tuple but got '{}' instead"
        .format(type(company)))
    self.scenario_data.unregistered_companies.append(company)
    logging.debug("Successfully added Unregistered Company: {} - {} to "
                  "Scenario Data as '{}'".format(company.title, company.number,
                                                 company.alias))


def get_unregistered_company(self, alias):
    """Get the details of an Unregistered Company from context Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought Unregistered Company
    :type alias: str
    :return: an UnregisteredCompany named tuple
    :rtype features.ScenarioData.UnregisteredCompany
    """
    res = None
    for company in self.scenario_data.unregistered_companies:
        if company.alias == alias:
            res = company
            logging.debug("Found Unregistered Company: '{}' in Scenario Data"
                          .format(alias))
    assert res is not None, ("Couldn't find Unregistered Company '{}' in "
                             "Scenario Data".format(alias))
    return res


def patch_context(context):
    """Will patch the Behave's `context` object with some handy functions.

    This will add methods that allow to easily access Scenario Data.

    :param context: Behave context object
    """
    context.add_actor = MethodType(add_actor, context)
    context.get_actor = MethodType(get_actor, context)
    context.get_actor_client = MethodType(get_actor_client, context)
    context.add_unregistered_company = MethodType(add_unregistered_company, context)
    context.get_unregistered_company = MethodType(get_unregistered_company, context)

