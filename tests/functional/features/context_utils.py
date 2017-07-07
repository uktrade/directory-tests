# -*- coding: utf-8 -*-
"""Helpers added to the behave's `context` object."""
import logging
from collections import namedtuple
from types import MethodType

from requests import Session

ScenarioData = namedtuple(
    'ScenarioData',
    [
        'actors', 'unregistered_companies'
    ]
)
Actor = namedtuple(
    'Actor',
    [
        'alias', 'email', 'password', 'session', 'csrfmiddlewaretoken',
        'email_confirmation_link', 'company_alias', 'has_sso_account'
    ]
)
Company = namedtuple(
    'Company',
    [
        'alias', 'title', 'number', 'address_details', 'summary', 'description',
        'website', 'keywords', 'no_employees', 'sector', 'letter_recipient',
        'companies_house_details'
    ]
)
# Set all fields to None by default.
Company.__new__.__defaults__ = (None,) * len(Company._fields)


def initialize_scenario_data():
    """Will initialize the Scenario Data.

    :return an empty ScenarioData named tuple
    :rtype ScenarioData
    """
    actors = {}
    unregistered_companies = {}
    scenario_data = ScenarioData(actors, unregistered_companies)
    return scenario_data


def add_actor(self, actor):
    """Will add Actor details to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param actor: an instance of Actor Named Tuple
    :type actor: tests.functional.features.ScenarioData.Actor
    """
    assert isinstance(actor, Actor), ("Expected Actor named tuple but got '{}'"
                                      " instead".format(type(actor)))
    self.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(self, alias):
    """Get actor details from context Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    :return: an Actor named tuple
    :rtype actor: tests.functional.features.ScenarioData.Actor
    """
    return self.scenario_data.actors[alias]


def set_actor_csrfmiddlewaretoken(self, alias, token):
    if alias in self.scenario_data.actors:
        actors = self.scenario_data.actors
        actors[alias] = actors[alias]._replace(csrfmiddlewaretoken=token)
        logging.debug("Successfully set csrfmiddlewaretoken=%s for Actor: "
                      "%s", token, alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", alias)


def set_actor_email_confirmation_link(self, alias, link):
    if alias in self.scenario_data.actors:
        actors = self.scenario_data.actors
        actors[alias] = actors[alias]._replace(email_confirmation_link=link)
        logging.debug("Successfully set email_confirmation_link=%s for "
                      "Actor: %s", link, alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", alias)


def set_actor_has_sso_account(self, alias, has_sso_account: bool):
    if alias in self.scenario_data.actors:
        actors = self.scenario_data.actors
        actors[alias] = actors[alias]._replace(has_sso_account=has_sso_account)
        logging.debug("Successfully set has_sso_account=%s for "
                      "Actor: %s", has_sso_account, alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", alias)


def set_company_for_actor(self, actor_alias, company_alias):
    if actor_alias in self.scenario_data.actors:
        actors = self.scenario_data.actors
        actors[actor_alias] = actors[actor_alias]._replace(
            company_alias=company_alias)
        logging.debug("Successfully set company_alias=%s for "
                      "Actor: %s", company_alias, actor_alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", actor_alias)


def reset_actor_session(self, alias):
    """Reset `requests` Session object.

    Can be useful when interacting with multiple domains.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought actor
    :type alias: str
    """
    if alias in self.scenario_data.actors:
        actors = self.scenario_data.actors
        actors[alias] = actors[alias]._replace(session=Session())
        logging.debug("Successfully reset %s's session object", alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", alias)


def add_company(self, company):
    """Will add an Company to Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param company: an instance of Company Tuple
    :type company: test.functional.features.ScenarioData.Company
    """
    assert isinstance(company, Company), (
        "Expected Company named tuple but got '{}' instead"
        .format(type(company)))
    self.scenario_data.unregistered_companies[company.alias] = company
    logging.debug("Successfully added Company: %s - %s to "
                  "Scenario Data as '%s'", company.title, company.number,
                  company.alias)


def get_company(self, alias):
    """Get the details of an Unregistered Company from context Scenario Data.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought Unregistered Company
    :type alias: str
    :return: an Company named tuple
    :rtype tests.functional.features.ScenarioData.Company
    """
    return self.scenario_data.unregistered_companies[alias]


def set_company_details(self, alias, *, title=None, website=None, keywords=None,
                        no_employees=None, sector=None, letter_recipient=None,
                        address_details=None):
    companies = self.scenario_data.unregistered_companies
    if title:
        companies[alias] = companies[alias]._replace(title=title)
    if website:
        companies[alias] = companies[alias]._replace(website=website)
    if keywords:
        companies[alias] = companies[alias]._replace(keywords=keywords)
    if no_employees:
        companies[alias] = companies[alias]._replace(no_employees=no_employees)
    if sector:
        companies[alias] = companies[alias]._replace(sector=sector)
    if letter_recipient:
        companies[alias] = companies[alias]._replace(letter_recipient=letter_recipient)
    if address_details:
        companies[alias] = companies[alias]._replace(address_details=address_details)

    logging.debug("Successfully updated Company's details %s: %s", alias,
                  companies[alias])


def set_company_description(self, alias, summary, description):
    """Will set summary & description used when building up company's profile.

    Can come handy when validating whether these values are visible.

    :param self: behave `context` object
    :type self: behave.runner.Context
    :param alias: alias of sought Unregistered Company
    :type alias: str
    :param summary: Brief summary to make your company stand out to buyers
    :type summary: str
    :param description: Describe your business to overseas buyers
    :type description: str
    """
    if alias in self.scenario_data.unregistered_companies:
        companies = self.scenario_data.unregistered_companies
        companies[alias] = companies[alias]._replace(summary=summary,
                                                     description=description)
        logging.debug("Successfully set summary & description for company %s",
                      alias)
    else:
        raise KeyError("Could not find company with alias '%s'", alias)


def patch_context(context):
    """Will patch the Behave's `context` object with some handy functions.

    Adds methods that allow to easily get & add data from/to Scenario Data.

    :param context: behave `context` object
    :type context: behave.runner.Context
    """
    context.add_actor = MethodType(add_actor, context)
    context.get_actor = MethodType(get_actor, context)
    context.reset_actor_session = MethodType(reset_actor_session, context)
    context.set_actor_csrfmiddlewaretoken = MethodType(
        set_actor_csrfmiddlewaretoken, context)
    context.set_actor_email_confirmation_link = MethodType(
        set_actor_email_confirmation_link, context)
    context.set_actor_has_sso_account = MethodType(
        set_actor_has_sso_account, context)
    context.set_company_for_actor = MethodType(set_company_for_actor, context)
    context.set_company_description = MethodType(set_company_description, context)
    context.add_company = MethodType(add_company, context)
    context.get_company = MethodType(get_company, context)
    context.set_company_details = MethodType(set_company_details, context)
