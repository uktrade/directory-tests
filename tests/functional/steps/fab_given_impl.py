# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random
import uuid
from string import ascii_letters, digits
from urllib.parse import urlsplit

from behave.runner import Context
from requests import Session
from retrying import retry
from tests.functional.pages import (
    fas_ui_profile,
    profile_ui_landing,
)
from tests.functional.steps.fab_then_impl import (
    bp_should_be_prompted_to_build_your_profile,
    prof_should_be_on_profile_page,
    prof_should_be_told_about_missing_description,
    reg_should_get_verification_email,
    reg_sso_account_should_be_created,
    sso_should_be_signed_in_to_sso_account,
    sso_should_be_told_about_password_reset,
    sso_should_get_password_reset_email,
)
from tests.functional.steps.fab_when_impl import (
    bp_provide_company_details,
    bp_select_random_sector_and_export_to_country,
    bp_verify_identity_with_letter,
    can_find_supplier_by_term,
    enrol_user,
    find_unregistered_company,
    finish_registration_after_flagging_as_verified,
    profile_add_business_description,
    profile_verify_company_profile,
    reg_confirm_company_selection,
    reg_create_sso_account,
    reg_create_standalone_unverified_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    select_random_company,
    sso_go_to_create_trade_profile,
    sso_request_password_reset,
    sso_sign_in,
)
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.generic import (
    assertion_msg,
    filter_out_legacy_industries,
    flag_sso_account_as_verified,
    get_active_company_without_fas_profile,
    get_published_companies,
    get_published_companies_with_n_sectors,
    get_verification_code,
    is_verification_letter_sent,
    send_verification_letter,
    sentence,
)


def unauthenticated_supplier(supplier_alias: str) -> Actor:
    """Create an instance of an unauthenticated Supplier Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
     * initialize `requests` Session object that allows you to keep the cookies
        across multiple requests
    """
    session = Session()
    email = (
        "test+{}{}@directory.uktrade.io".format(
            supplier_alias, str(uuid.uuid4())
        )
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    password_length = 15
    password = "".join(
        random.choice(ascii_letters) + random.choice(digits)
        for _ in range(password_length)
    )
    return Actor(
        alias=supplier_alias,
        email=email,
        password=password,
        session=session,
        csrfmiddlewaretoken=None,
        email_confirmation_link=None,
        company_alias=None,
        has_sso_account=False,
        type="supplier",
    )


def unauthenticated_buyer(buyer_alias: str) -> Actor:
    """Create an instance of an unauthenticated Buyer Actor.

    Will:
     * set rudimentary Actor details, all omitted ones will default to None
     * initialize `requests` Session object that allows you to keep the cookies
        across multiple requests
    """
    session = Session()
    email = (
        "test+buyer_{}{}@directory.uktrade.io".format(
            buyer_alias, str(uuid.uuid4())
        )
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    company_name = f"{sentence()} AUTOTESTS"
    return Actor(
        alias=buyer_alias,
        email=email,
        session=session,
        company_alias=company_name,
        type="buyer",
    )


def reg_create_sso_account_associated_with_company(
    context: Context, supplier_alias: str, company_alias: str
):
    if not context.get_actor(supplier_alias):
        context.add_actor(unauthenticated_supplier(supplier_alias))
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    reg_create_sso_account(context, supplier_alias, company_alias)
    reg_sso_account_should_be_created(context.response, supplier_alias)
    context.update_actor(supplier_alias, has_sso_account=True)


def profile_create_unverified_business_profile(
        context: Context, supplier_alias: str, company_alias: str
):
    if not context.get_actor(supplier_alias):
        context.add_actor(unauthenticated_supplier(supplier_alias))
    find_unregistered_company(context, supplier_alias, company_alias)
    enrol_user(context, supplier_alias, company_alias)
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
        context.response, supplier_alias
    )


def profile_create_verified_and_published_business_profile(
    context: Context, supplier_alias: str, company_alias: str
):
    """Create a verified FAB profile with a quick SSO account verification."""
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias
    )
    supplier = context.get_actor(supplier_alias)
    flag_sso_account_as_verified(context, supplier.email)
    sso_sign_in(context, supplier_alias)
    finish_registration_after_flagging_as_verified(context, supplier_alias)
    bp_build_company_profile(context, supplier_alias)
    prof_set_company_description(context, supplier_alias)
    prof_verify_company(context, supplier_alias)
    prof_should_be_on_profile_page(context.response, supplier_alias)
    fab_ui_profile.should_see_profile_is_verified(context.response)


def sso_create_standalone_unverified_sso_account(
    context: Context, supplier_alias: str
):
    supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)
    reg_create_standalone_unverified_sso_account(context, supplier_alias)


def sso_create_standalone_verified_sso_account(
    context: Context, supplier_alias: str
):
    sso_create_standalone_unverified_sso_account(context, supplier_alias)
    supplier = context.get_actor(supplier_alias)
    flag_sso_account_as_verified(context, supplier.email)
    sso_sign_in(context, supplier_alias)
    profile_ui_landing.should_be_here(context.response)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)
    context.update_actor(supplier_alias, has_sso_account=True)


def reg_select_random_company_and_confirm_export_status(
    context: Context, supplier_alias: str, company_alias: str
):
    sso_create_standalone_verified_sso_account(context, supplier_alias)
    sso_go_to_create_trade_profile(context, supplier_alias)
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)


def fas_find_company_by_name(
    context: Context, buyer_alias: str, company_alias: str
):
    buyer = context.get_actor(buyer_alias)
    session = buyer.session
    company = context.get_company(company_alias)
    found, response, profile_endpoint = can_find_supplier_by_term(
        session=session,
        name=company.title,
        term=company.title,
        term_type="company title",
    )
    context.response = response
    with assertion_msg(
        "%s could not find company '%s' of FAS using company's title",
        buyer_alias,
        company.title,
    ):
        assert found
    with assertion_msg(
        "Could not extract URL to '%s' profile page", company.title
    ):
        assert profile_endpoint
    context.set_company_details(
        company_alias, fas_profile_endpoint=profile_endpoint
    )


@retry(wait_fixed=3000, stop_max_attempt_number=5)
def fab_find_published_company(
    context: Context,
    actor_alias: str,
    company_alias: str,
    *,
    min_number_sectors: int = None
):
    if min_number_sectors:
        companies = get_published_companies_with_n_sectors(
            context, min_number_sectors
        )
    else:
        companies = get_published_companies(context)

    with assertion_msg(
        "Expected to find at least 1 published company but got none!"
    ):
        assert len(companies) > 0
    filtered_companies = [
        c
        for c in companies
        if "@directory.uktrade.io" not in c["company_email"]
    ]
    company_dict = random.choice(filtered_companies)
    sectors = filter_out_legacy_industries(company_dict)
    company = Company(
        alias=company_alias,
        title=company_dict["name"],
        number=company_dict["number"],
        sector=sectors,
        description=company_dict["description"],
        summary=company_dict["summary"],
        no_employees=company_dict["employees"],
        keywords=company_dict["keywords"],
        website=company_dict["website"],
        facebook=company_dict["facebook_url"],
        twitter=company_dict["twitter_url"],
        linkedin=company_dict["linkedin_url"],
    )
    context.update_actor(actor_alias, company_alias=company_alias)
    context.add_company(company)
    logging.debug("%s found a published company: %s", actor_alias, company)


def fas_get_company_slug(
    context: Context, actor_alias: str, company_alias: str
):
    actor = context.get_actor(actor_alias)
    session = actor.session
    company = context.get_company(company_alias)
    response = fas_ui_profile.go_to(session, company_number=company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    url = response.request.url
    last_item_idx = -1
    slash_idx = 1
    slug = urlsplit(url).path.split(company.number)[last_item_idx][slash_idx:]
    logging.debug("%s got company's slug: %s", actor_alias, slug)
    context.set_company_details(company_alias, slug=slug)


def reg_should_get_verification_letter(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    sent = is_verification_letter_sent(context, company.number)

    with assertion_msg("Verification letter wasn't sent"):
        assert sent

    verification_code = get_verification_code(context, company.number)
    context.set_company_details(
        company.alias, verification_code=verification_code
    )

    logging.debug(
        "%s received the verification letter with code: %s",
        supplier_alias,
        verification_code,
    )


def sso_get_password_reset_link(context: Context, supplier_alias: str):
    sso_request_password_reset(context, supplier_alias)
    sso_should_be_told_about_password_reset(context, supplier_alias)
    sso_should_get_password_reset_email(context, supplier_alias)


def reg_create_verified_sso_account_associated_with_company(
    context: Context, supplier_alias: str, company_alias: str
):
    """Select a Company, create a SSO account for it, and verify the email."""
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias
    )
    supplier = context.get_actor(supplier_alias)
    flag_sso_account_as_verified(context, supplier.email)
    sso_sign_in(context, supplier_alias)
    finish_registration_after_flagging_as_verified(context, supplier_alias)


def create_actor_with_or_without_sso_account(
    context: Context, actor_aliases: str, has_or_does_not_have: str
):
    actor_aliases = [alias.strip() for alias in actor_aliases.split(",")]
    for actor_alias in actor_aliases:
        if has_or_does_not_have in ["has", "have"]:
            sso_create_standalone_verified_sso_account(context, actor_alias)
        else:
            supplier = unauthenticated_supplier(actor_alias)
            context.add_actor(supplier)


def create_actor_with_verified_or_unverified_fab_profile(
    context: Context,
    actor_alias: str,
    verified_or_not: str,
    company_alias: str,
):
    if verified_or_not == "a verified":
        profile_create_verified_and_published_business_profile(context, actor_alias, company_alias)
    else:
        profile_create_unverified_business_profile(context, actor_alias, company_alias)


def stannp_send_verification_letter(context: Context, actor_alias: str):
    company_alias = "Test"
    company = get_active_company_without_fas_profile(alias=company_alias)
    context.add_company(company)
    if not context.get_actor(actor_alias):
        context.add_actor(unauthenticated_buyer(actor_alias))
    context.update_actor(actor_alias, company_alias=company_alias)
    verification_code = str(random.randint(1000000, 9999999))
    context.set_company_details(
        company_alias, verification_code=verification_code, owner=actor_alias
    )
    company = context.get_company(company_alias)
    response = send_verification_letter(context, company)
    context.response = response
    logging.debug("Successfully sent letter in test mode via StanNP")
