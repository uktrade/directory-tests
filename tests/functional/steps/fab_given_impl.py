# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random
import string
import uuid
from urllib.parse import urlsplit

from behave.runner import Context
from requests import Session

from tests.functional.pages import (
    fab_ui_profile,
    fas_ui_profile,
    profile_ui_landing
)
from tests.functional.steps.fab_then_impl import (
    bp_should_be_prompted_to_build_your_profile,
    prof_should_be_on_profile_page,
    prof_should_be_told_about_missing_description,
    reg_should_get_verification_email,
    reg_sso_account_should_be_created,
    sso_should_be_signed_in_to_sso_account,
    sso_should_be_told_about_password_reset,
    sso_should_get_password_reset_email
)
from tests.functional.steps.fab_when_impl import (
    bp_provide_company_details,
    bp_select_random_sector_and_export_to_country,
    bp_verify_identity_with_letter,
    can_find_supplier_by_term,
    prof_set_company_description,
    prof_verify_company,
    reg_confirm_company_selection,
    reg_confirm_export_status,
    reg_create_sso_account,
    reg_create_standalone_unverified_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    select_random_company,
    sso_go_to_create_trade_profile,
    sso_request_password_reset,
    sso_supplier_confirms_email_address
)
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.db_utils import (
    get_published_companies,
    get_published_companies_with_n_sectors,
    get_verification_code,
    is_verification_letter_sent
)
from tests.functional.utils.generic import assertion_msg, sentence


def unauthenticated_supplier(supplier_alias: str) -> Actor:
    """Create an instance of an unauthenticated Supplier Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
     * initialize `requests` Session object that allows you to keep the cookies
        across multiple requests

    :param supplier_alias: alias of the Actor used within the scenario's scope
    :return: an Actor namedtuple with all required details
    """
    session = Session()
    email = ("test+{}{}@directory.uktrade.io"
             .format(supplier_alias, str(uuid.uuid4()))
             .replace("-", "").replace(" ", "").lower())
    password_length = 10
    password = ''.join(random.choice(string.ascii_letters)
                       for _ in range(password_length))
    return Actor(
        alias=supplier_alias, email=email, password=password, session=session,
        csrfmiddlewaretoken=None, email_confirmation_link=None,
        company_alias=None, has_sso_account=False, type="supplier")


def unauthenticated_buyer(buyer_alias: str) -> Actor:
    """Create an instance of an unauthenticated Buyer Actor.

    Will:
     * set only rudimentary Actor details, all omitted ones will default to None
     * initialize `requests` Session object that allows you to keep the cookies
        across multiple requests

    :param buyer_alias: alias of the Actor used within the scenario's scope
    :return: an Actor namedtuple with all required details
    """
    session = Session()
    email = ("test+buyer_{}{}@directory.uktrade.io"
             .format(buyer_alias, str(uuid.uuid4()))
             .replace("-", "").replace(" ", "").lower())
    company_name = sentence()
    return Actor(
        alias=buyer_alias, email=email, session=session,
        company_alias=company_name, type="buyer")


def reg_create_sso_account_associated_with_company(
        context: Context, supplier_alias: str, company_alias: str):
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    reg_confirm_export_status(context, supplier_alias, exported=True)
    reg_create_sso_account(context, supplier_alias, company_alias)
    reg_sso_account_should_be_created(context.response, supplier_alias)
    context.update_actor(supplier_alias, has_sso_account=True)


def reg_confirm_email_address(context: Context, supplier_alias: str):
    reg_should_get_verification_email(context, supplier_alias)
    reg_open_email_confirmation_link(context, supplier_alias)
    reg_supplier_confirms_email_address(context, supplier_alias)
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)


def bp_build_company_profile(context: Context, supplier_alias: str):
    bp_provide_company_details(context, supplier_alias)
    bp_select_random_sector_and_export_to_country(context, supplier_alias)
    bp_verify_identity_with_letter(context, supplier_alias)
    prof_should_be_on_profile_page(context.response, supplier_alias)
    prof_should_be_told_about_missing_description(
        context.response, supplier_alias)


def reg_create_verified_profile(
        context: Context, supplier_alias: str, company_alias: str):
    # STEP 0 - use existing actor or initialize new one if necessary
    supplier = context.get_actor(supplier_alias)
    if not supplier:
        supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)

    # STEP 1 - select company, create SSO profile & verify email address
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias)
    reg_confirm_email_address(context, supplier_alias)

    # STEP 2 - build company profile after email verification
    bp_build_company_profile(context, supplier_alias)

    # STEP 3 - verify company with the code sent by post
    prof_set_company_description(context, supplier_alias)
    prof_verify_company(context, supplier_alias)
    prof_should_be_on_profile_page(context.response, supplier_alias)
    fab_ui_profile.should_see_profile_is_verified(context.response)


def sso_create_standalone_unverified_sso_account(
        context: Context, supplier_alias: str):
    supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)
    reg_create_standalone_unverified_sso_account(context, supplier_alias)
    reg_sso_account_should_be_created(context.response, supplier_alias)
    reg_should_get_verification_email(context, supplier_alias)


def sso_create_standalone_verified_sso_account(
        context: Context, supplier_alias: str):
    sso_create_standalone_unverified_sso_account(context, supplier_alias)
    reg_open_email_confirmation_link(context, supplier_alias)
    sso_supplier_confirms_email_address(context, supplier_alias)
    profile_ui_landing.should_be_here(context.response)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


def reg_select_random_company_and_confirm_export_status(
        context: Context, supplier_alias: str, company_alias: str):
    sso_create_standalone_verified_sso_account(context, supplier_alias)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)
    sso_go_to_create_trade_profile(context, supplier_alias)
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    reg_confirm_export_status(context, supplier_alias, exported=True)
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)


def reg_create_unverified_profile(context, supplier_alias, company_alias):
    supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias)
    reg_confirm_email_address(context, supplier_alias)
    bp_build_company_profile(context, supplier_alias)


def fas_find_company_by_name(
        context: Context, buyer_alias: str, company_alias: str):
    buyer = context.get_actor(buyer_alias)
    session = buyer.session
    company = context.get_company(company_alias)
    found, response, profile_endpoint = can_find_supplier_by_term(
        session=session, name=company.title, term=company.title,
        term_type="company title")
    context.response = response
    with assertion_msg(
            "%s could not find company '%s' of FAS using company's title",
            buyer_alias, company.title):
        assert found
    with assertion_msg(
            "Could not extract URL to '%s' profile page", company.title):
        assert profile_endpoint
    context.set_company_details(company_alias, fas_profile_endpoint=profile_endpoint)


def fab_find_published_company(
        context: Context, actor_alias: str, company_alias: str, *,
        min_number_sectors: int = None):
    if min_number_sectors:
        companies = get_published_companies_with_n_sectors(min_number_sectors)
    else:
        companies = get_published_companies()

    with assertion_msg(
            "Expected to find at least 1 published company but got none!"):
        assert len(companies) > 0
    company_dict = random.choice(companies)
    company = Company(
        alias=company_alias, title=company_dict['name'],
        number=company_dict['number'], sector=company_dict['sectors'],
        description=company_dict['description'],
        summary=company_dict['summary'],
        no_employees=company_dict['employees'],
        keywords=company_dict['keywords'],
        website=company_dict['website'],
        facebook=company_dict['facebook_url'],
        twitter=company_dict['twitter_url'],
        linkedin=company_dict['linkedin_url']
    )
    context.update_actor(actor_alias, company_alias=company_alias)
    context.add_company(company)
    logging.debug("%s found a published company: %s", actor_alias, company)


def fas_get_company_slug(context, actor_alias, company_alias):
    actor = context.get_actor(actor_alias)
    session = actor.session
    company = context.get_company(company_alias)
    response = fas_ui_profile.go_to(session, company_number=company.number)
    context.response = response
    url = response.request.url
    last_item_idx = -1
    slash_idx = 1
    slug = urlsplit(url).path.split(company.number)[last_item_idx][slash_idx:]
    logging.debug("%s got company's slug: %s", actor_alias, slug)
    context.set_company_details(company_alias, slug=slug)


def reg_should_get_verification_letter(context, supplier_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    sent = is_verification_letter_sent(company.number)

    with assertion_msg("Verification letter wasn't sent"):
        assert sent

    verification_code = get_verification_code(company.number)
    context.set_company_details(
        company.alias, verification_code=verification_code)

    logging.debug(
        "%s received the verification letter with code: %s", supplier_alias,
        verification_code)


def sso_get_password_reset_link(context: Context, supplier_alias: str):
    sso_request_password_reset(context, supplier_alias)
    sso_should_be_told_about_password_reset(context, supplier_alias)
    sso_should_get_password_reset_email(context, supplier_alias)


def reg_create_verified_sso_account_associated_with_company(
        context: Context, supplier_alias: str, company_alias: str):
    """Select a Company, create a SSO account for it, and verify the email.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used within the scenario's scope
    :param company_alias: alias of the Actor's Company
    """
    supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias)
    reg_confirm_email_address(context, supplier_alias)
