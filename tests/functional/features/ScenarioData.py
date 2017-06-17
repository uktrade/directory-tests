# -*- coding: utf-8 -*-
"""Define Scenario Data structure & additional behave's `context` functions."""
import logging
from collections import namedtuple
from types import MethodType

from requests import Session


ScenarioData = namedtuple('ScenarioData', ['actors', 'unregistered_companies'])
Actor = namedtuple('Actor', ['alias', 'email', 'password', 'session',
                             'csrfmiddlewaretoken', 'email_confirmation_link'])
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
    """Will add Actor details to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param actor: an instance of Actor Named Tuple
    :type actor: tests.functional.features.ScenarioData.Actor
    """
    assert isinstance(actor, Actor), ("Expected Actor named tuple but got '{}' "
                                      "instead".format(type(actor)))
    self.scenario_data.actors.append(actor)
    logging.debug("Successfully added actor: {} to Scenario Data"
                  .format(actor.alias))


def get_actor(self, alias):
    """Get actor details from context Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    :return: an Actor named tuple
    :rtype actor: tests.functional.features.ScenarioData.Actor
    """
    res = None
    for actor in self.scenario_data.actors:
        if actor.alias == alias:
            res = actor
            logging.debug("Found actor: '{}' in Scenario Data".format(alias))
    assert res is not None, ("Couldn't find actor '{}' in Scenario Data"
                             .format(alias))
    return res


def set_actor_csrfmiddlewaretoken(self, alias, token):
    for idx, actor in enumerate(self.scenario_data.actors):
        if actor.alias == alias:
            self.scenario_data.actors[idx] = \
                actor._replace(csrfmiddlewaretoken=token)
            logging.debug("Successfully set csrfmiddlewaretoken={} for Actor: "
                          "{}".format(token, alias))


def set_actor_email_confirmation_link(self, alias, link):
    for idx, actor in enumerate(self.scenario_data.actors):
        if actor.alias == alias:
            self.scenario_data.actors[idx] = \
                actor._replace(email_confirmation_link=link)
            logging.debug("Successfully set email_confirmation_link={} for "
                          "Actor: {}".format(link, alias))


def reset_actor_session(self, alias):
    """Reset `requests` Session object.

    Can be useful when interacting with multiple domains.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    """
    for idx, actor in enumerate(self.scenario_data.actors):
        if actor.alias == alias:
            self.scenario_data.actors[idx] = actor._replace(session=Session())
            logging.debug("Successfully reset {}' session object".format(alias))


def add_unregistered_company(self, company):
    """Will add an Unregistered Company to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param company: an instance of UnregisteredCompany Tuple
    :type company: test.functional.features.ScenarioData.UnregisteredCompany
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
    :rtype tests.functional.features.ScenarioData.UnregisteredCompany
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

    This adds methods that allow to easily get & add data from/to Scenario Data.

    :param context: behave `context` object
    :type context: behave.runner.Context
    """
    context.add_actor = MethodType(add_actor, context)
    context.get_actor = MethodType(get_actor, context)
    context.reset_actor_session = MethodType(reset_actor_session, context)
    context.set_actor_csrfmiddlewaretoken = MethodType(set_actor_csrfmiddlewaretoken, context)
    context.set_actor_email_confirmation_link = MethodType(set_actor_email_confirmation_link, context)
    context.add_unregistered_company = MethodType(add_unregistered_company, context)
    context.get_unregistered_company = MethodType(get_unregistered_company, context)

