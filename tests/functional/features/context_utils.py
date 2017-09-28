# -*- coding: utf-8 -*-
"""Helpers added to the behave's `context` object."""
import logging
from collections import namedtuple
from types import MethodType

from behave.runner import Context
from requests import Session

ScenarioData = namedtuple(
    'ScenarioData',
    [
        'actors', 'companies'
    ]
)
Actor = namedtuple(
    'Actor',
    [
        'alias', 'email', 'password', 'session', 'csrfmiddlewaretoken',
        'email_confirmation_link', 'company_alias', 'has_sso_account', 'type',
        'password_reset_link'
    ]
)
CaseStudy = namedtuple(
    'CaseStudy',
    [
        'alias', 'title', 'summary', 'description', 'sector', 'website',
        'keywords', 'image_1', 'image_2', 'image_3', 'caption_1', 'caption_2',
        'caption_3', 'testimonial', 'source_name', 'source_job',
        'source_company', 'slug'
    ]
)
AddressDetails = namedtuple(
    "AddressDetails",
    [
        "address_signature", "address_line_1", "address_line_2", "locality",
        "country", "postal_code", "po_box"
    ]
)

Company = namedtuple(
    'Company',
    [
        'alias', 'title', 'number', 'summary', 'description',
        'website', 'keywords', 'no_employees', 'sector', 'letter_recipient',
        'companies_house_details', 'facebook', 'linkedin', 'twitter',
        'case_studies', 'logo_picture', 'logo_url', 'logo_hash',
        'export_to_countries', 'fas_profile_endpoint', 'slug',
        'verification_code'
    ]
)
Feedback = namedtuple(
    'Feedback',
    [
        'name', 'email', 'company_name', 'country', 'comment', 'terms'
    ]
)
Message = namedtuple(
    'Message',
    [
        'alias', 'body', 'company_name', 'country', 'email_address',
        'full_name', 'g_recaptcha_response', 'sector', 'subject', 'terms'
    ]
)
# Set all fields to None by default.
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
Company.__new__.__defaults__ = (None,) * len(Company._fields)
CaseStudy.__new__.__defaults__ = (None,) * len(CaseStudy._fields)
Message.__new__.__defaults__ = (None,) * len(Message._fields)
AddressDetails.__new__.__defaults__ = (None,) * len(AddressDetails._fields)


def initialize_scenario_data():
    """Will initialize the Scenario Data.

    :return an empty ScenarioData named tuple
    :rtype ScenarioData
    """
    actors = {}
    companies = {}
    scenario_data = ScenarioData(actors, companies)
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
    return self.scenario_data.actors.get(alias)


def update_actor(
        self, alias, *, password_reset_link: str = None,
        company_alias: str = None, has_sso_account: bool = None,
        email_confirmation_link: str = None, csrfmiddlewaretoken: str = None):
    actors = self.scenario_data.actors
    if password_reset_link:
        actors[alias] = actors[alias]._replace(password_reset_link=password_reset_link)
    if company_alias:
        actors[alias] = actors[alias]._replace(company_alias=company_alias)
    if has_sso_account:
        actors[alias] = actors[alias]._replace(has_sso_account=has_sso_account)
    if email_confirmation_link:
        actors[alias] = actors[alias]._replace(email_confirmation_link=email_confirmation_link)
    if csrfmiddlewaretoken:
        actors[alias] = actors[alias]._replace(csrfmiddlewaretoken=csrfmiddlewaretoken)

    logging.debug(
        "Successfully updated Actors's details %s: %s", alias, actors[alias])


def set_company_logo_detail(self, alias, *, picture=None, url=None, hash=None):
    companies = self.scenario_data.companies
    if picture:
        companies[alias] = companies[alias]._replace(logo_picture=picture)
    if url:
        companies[alias] = companies[alias]._replace(logo_url=url)
    if hash:
        companies[alias] = companies[alias]._replace(logo_hash=hash)


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
    self.scenario_data.companies[company.alias] = company
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
    return self.scenario_data.companies[alias]


def set_company_details(self, alias, *, title=None, website=None, keywords=None,
                        no_employees=None, sector=None, letter_recipient=None,
                        facebook=None, linkedin=None, twitter=None,
                        summary=None, description=None,
                        export_to_countries=None, fas_profile_endpoint=None,
                        slug=None, verification_code=None):
    companies = self.scenario_data.companies
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
    if facebook:
        companies[alias] = companies[alias]._replace(facebook=facebook)
    if linkedin:
        companies[alias] = companies[alias]._replace(linkedin=linkedin)
    if twitter:
        companies[alias] = companies[alias]._replace(twitter=twitter)
    if summary:
        companies[alias] = companies[alias]._replace(summary=summary)
    if description:
        companies[alias] = companies[alias]._replace(description=description)
    if export_to_countries:
        companies[alias] = companies[alias]._replace(export_to_countries=export_to_countries)
    if fas_profile_endpoint:
        companies[alias] = companies[alias]._replace(fas_profile_endpoint=fas_profile_endpoint)
    if slug:
        companies[alias] = companies[alias]._replace(slug=slug)
    if verification_code:
        companies[alias] = companies[alias]._replace(verification_code=verification_code)

    logging.debug("Successfully updated Company's details %s: %s", alias,
                  companies[alias])


def add_case_study(
        self: Context, company_alias: str, case_alias: str,
        case_study: CaseStudy):
    """This will add a CaseStudy to company's data or replace existing one.

    :param self: behave `context` object
    :param company_alias: alias of Company to update
    :param case_alias: alias of the case study to update
    :param case_study: a CaseStudy namedtuple
    """
    cases = self.get_company(company_alias).case_studies
    cases[case_alias] = case_study

    logging.debug("Successfully added/replaced Case Study %s to Company %s. "
                  "Case Study Data: %s", case_alias, company_alias, case_study)


def update_case_study(self, company_alias, case_alias, *, slug=None):
    # cases = self.get_company(company_alias).case_studies
    companies = self.scenario_data.companies
    if slug:
        companies[company_alias].case_studies[case_alias] = companies[company_alias].case_studies[case_alias]._replace(slug=slug)
        # cases[case_alias] = cases[case_alias]._replace(slug=slug)

    logging.debug("Successfully updated Case Study '%s' for Company %s",
                  case_alias, company_alias)


def patch_context(context):
    """Will patch the Behave's `context` object with some handy functions.

    Adds methods that allow to easily get & add data from/to Scenario Data.

    :param context: behave `context` object
    :type context: behave.runner.Context
    """
    context.add_actor = MethodType(add_actor, context)
    context.get_actor = MethodType(get_actor, context)
    context.update_actor = MethodType(update_actor, context)
    context.reset_actor_session = MethodType(reset_actor_session, context)
    context.add_company = MethodType(add_company, context)
    context.get_company = MethodType(get_company, context)
    context.add_case_study = MethodType(add_case_study, context)
    context.update_case_study = MethodType(update_case_study, context)
    context.set_company_details = MethodType(set_company_details, context)
    context.set_company_logo_detail = MethodType(set_company_logo_detail, context)
