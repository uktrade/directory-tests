# -*- coding: utf-8 -*-
"""Helpers added to the behave's `context` object."""
import logging
from collections import namedtuple
from typing import Union

from behave.runner import Context
from requests import Session

ScenarioData = namedtuple("ScenarioData", ["actors", "companies"])
Actor = namedtuple(
    "Actor",
    [
        "alias",
        "email",
        "password",
        "session",
        "csrfmiddlewaretoken",
        "email_confirmation_link",
        "email_confirmation_code",
        "company_alias",
        "has_sso_account",
        "type",
        "password_reset_link",
        "invitation_for_collaboration_link",
        "ex_owner",
        "ownership_request_link",
        "verification_letter",
        "notifications",
    ],
)
CaseStudy = namedtuple(
    "CaseStudy",
    [
        "alias",
        "title",
        "summary",
        "description",
        "sector",
        "website",
        "keywords",
        "image_1",
        "image_2",
        "image_3",
        "caption_1",
        "caption_2",
        "caption_3",
        "testimonial",
        "source_name",
        "source_job",
        "source_company",
        "slug",
    ],
)
AddressDetails = namedtuple(
    "AddressDetails",
    [
        "address_signature",
        "address_line_1",
        "address_line_2",
        "locality",
        "country",
        "postal_code",
        "po_box",
    ],
)

Company = namedtuple(
    "Company",
    [
        "alias",
        "title",
        "number",
        "summary",
        "description",
        "website",
        "keywords",
        "no_employees",
        "sector",
        "industry",
        "letter_recipient",
        "companies_house_details",
        "facebook",
        "linkedin",
        "twitter",
        "case_studies",
        "logo_picture",
        "logo_url",
        "logo_hash",
        "export_to_countries",
        "fas_profile_endpoint",
        "slug",
        "verification_code",
        "collaborators",
        "deleted",
        "owner",
        "owner_email",
        "has_exported_before",
        "is_uk_isd_company",
        "expertise_industries",
        "export_destinations",
        "export_destinations_other",
        "business_type",
    ],
)
Feedback = namedtuple(
    "Feedback",
    [
        "name",
        "email",
        "company_name",
        "country",
        "comment",
        "terms",
        "g_recaptcha_response",
    ],
)
Message = namedtuple(
    "Message",
    [
        "alias",
        "body",
        "company_name",
        "country",
        "email_address",
        "family_name",
        "given_name",
        "g_recaptcha_response",
        "sector",
        "subject",
        "terms",
    ],
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


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data.

    :param context: behave `context` object
    :param actor: an instance of Actor Named Tuple
    """
    assert isinstance(
        actor, Actor
    ), "Expected Actor named tuple but got '{}'" " instead".format(type(actor))
    context.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(context: Context, alias: str):
    """Get actor details from context Scenario Data.

    :param context: behave `context` object
    :param alias: alias of sought actor
    :return: an Actor named tuple
    :rtype actor: tests.functional.features.ScenarioData.Actor
    """
    return context.scenario_data.actors.get(alias, None)


def update_actor(context: Context, alias: str, **kwargs):
    actors = context.scenario_data.actors

    for arg in kwargs:
        if arg in Actor._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            actors[alias] = actors[alias]._replace(**{arg: kwargs[arg]})

    logging.debug("Successfully updated Actors's details %s: %s", alias, actors[alias])


def set_company_logo_detail(
    context: Context, alias: str, *, picture=None, url=None, hash=None
):
    companies = context.scenario_data.companies
    if picture:
        companies[alias] = companies[alias]._replace(logo_picture=picture)
    if url:
        companies[alias] = companies[alias]._replace(logo_url=url)
    if hash:
        companies[alias] = companies[alias]._replace(logo_hash=hash)


def reset_actor_session(context: Context, alias: str):
    """Reset `requests` Session object.

    Can be useful when interacting with multiple domains.

    :param context: behave `context` object
    :param alias: alias of sought actor
    """
    if alias in context.scenario_data.actors:
        actors = context.scenario_data.actors
        actors[alias] = actors[alias]._replace(session=Session())
        logging.debug("Successfully reset %s's session object", alias)
    else:
        logging.debug("Could not find an actor aliased '%s'", alias)


def add_company(context: Context, company: Company):
    """Will add an Company to Scenario Data.

    :param context: behave `context` object
    :param company: an instance of Company Tuple
    """
    assert isinstance(
        company, Company
    ), "Expected Company named tuple but got '{}' instead".format(type(company))
    context.scenario_data.companies[company.alias] = company
    logging.debug(
        "Successfully added Company: %s - %s to " "Scenario Data as '%s'",
        company.title,
        company.number,
        company.alias,
    )


def get_company(context: Context, alias: str) -> Union[Company, None]:
    """Get the details of an Unregistered Company from context Scenario Data.

    :param context: behave `context` object
    :param alias: alias of sought Unregistered Company
    :return: an Company named tuple or None if not found
    """
    return context.scenario_data.companies.get(alias)


def update_company(context: Context, alias: str, **kwargs):
    companies = context.scenario_data.companies

    for arg in kwargs:
        if arg in Company._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            companies[alias] = companies[alias]._replace(**{arg: kwargs[arg]})

    logging.debug(
        "Successfully updated Company's details %s: %s", alias, companies[alias]
    )


def add_case_study(
    context: Context, company_alias: str, case_alias: str, case_study: CaseStudy
):
    """This will add a CaseStudy to company's data or replace existing one.

    :param context: behave `context` object
    :param company_alias: alias of Company to update
    :param case_alias: alias of the case study to update
    :param case_study: a CaseStudy namedtuple
    """
    cases = get_company(context, company_alias).case_studies
    cases[case_alias] = case_study

    logging.debug(
        "Successfully added/replaced Case Study %s to Company %s. "
        "Case Study Data: %s",
        case_alias,
        company_alias,
        case_study,
    )


def update_case_study(
    context: Context, company_alias: str, case_alias: str, *, slug=None
):
    companies = context.scenario_data.companies
    if slug:
        cases = companies[company_alias].case_studies[case_alias]._replace(slug=slug)
        companies[company_alias].case_studies[case_alias] = cases

    logging.debug(
        "Successfully updated Case Study '%s' for Company %s", case_alias, company_alias
    )
