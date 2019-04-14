# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import os
import random
import re
import uuid
from random import choice, randrange
from string import ascii_letters, digits
from urllib.parse import parse_qsl, quote, urljoin, urlsplit

from behave.model import Table
from behave.runner import Context
from directory_constants.constants import choices
from requests import Response, Session
from retrying import retry
from scrapy import Selector

from tests import get_absolute_url
from tests.functional.common import DETAILS, PROFILES
from tests.functional.pages import get_page_object
from tests.functional.pages.fab import (
    fab_ui_account_add_collaborator,
    fab_ui_account_confrim_password,
    fab_ui_account_remove_collaborator,
    fab_ui_account_transfer_ownership,
    fab_ui_build_profile_basic,
    fab_ui_build_profile_sector,
    fab_ui_confim_your_collaboration,
    fab_ui_confim_your_ownership,
    fab_ui_confirm_company,
    fab_ui_confirm_export_status,
    fab_ui_confirm_identity,
    fab_ui_confirm_identity_letter,
    fab_ui_verify_company,
)
from tests.functional.pages.fas import (
    fas_ui_contact,
    fas_ui_feedback,
    fas_ui_find_supplier,
    fas_ui_profile,
)
from tests.functional.pages.profile import (
    profile_about,
    profile_case_study_basic,
    profile_case_study_images,
    profile_edit_company_business_details,
    profile_edit_company_description,
    profile_edit_company_profile,
    profile_edit_online_profiles,
    profile_edit_products_and_services_industry,
    profile_edit_products_and_services_keywords,
    profile_enrolment_finished,
    profile_enter_email_verification_code,
    profile_enter_your_business_details,
    profile_enter_your_business_details_part_2,
    profile_enter_your_email_and_password,
    profile_enter_your_personal_details,
    profile_find_a_buyer,
    profile_publish_company_profile,
    profile_upload_logo,
)
from tests.functional.pages.sso import (
    sso_ui_change_password,
    sso_ui_confim_your_email,
    sso_ui_login,
    sso_ui_password_reset,
    sso_ui_register,
    sso_ui_verify_your_email,
)
from tests.functional.steps.then_impl import (
    fab_should_get_request_for_becoming_owner,
    reg_should_get_verification_email,
    sso_should_be_signed_in_to_sso_account,
    sso_should_be_told_about_password_reset,
    sso_should_get_password_reset_email,
)
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.generic import (
    assertion_msg,
    escape_html,
    extract_csrf_middleware_token,
    extract_form_action,
    extract_logo_url,
    extract_registration_page_link,
    extract_text_from_pdf,
    filter_out_legacy_industries,
    flag_sso_account_as_verified,
    get_absolute_path_of_file,
    get_active_company_without_fas_profile,
    get_company_by_id,
    get_language_code,
    get_md5_hash_of_file,
    get_number_of_search_result_pages,
    get_pdf_from_stannp,
    get_published_companies,
    get_published_companies_with_n_sectors,
    get_verification_code,
    is_already_registered,
    is_inactive,
    is_verification_letter_sent,
    random_case_study_data,
    random_chars,
    random_feedback_data,
    random_message_data,
    rare_word,
    send_verification_letter,
    sentence,
)
from tests.functional.utils.gov_notify import get_email_verification_code
from tests.functional.utils.request import Method, check_response, make_request
from tests.settings import (
    COUNTRIES,
    NO_OF_EMPLOYEES,
    SECTORS,
    SEPARATORS,
    BMPs,
    JP2s,
    WEBPs,
)

INDUSTRIES_FOR_PRODUCTS_AND_SERVICES = {
    "financial": [
        'Opening bank accounts',
        'Accounting and Tax (including registration for VAT and PAYE)',
        'Insurance',
        'Raising Capital',
        'Regulatory support',
        'Mergers and Acquisitions',
    ],
    "management-consulting": [
        'Business development',
        'Product safety regulation and compliance',
        'Commercial/pricing strategy',
        'Workforce development',
        'Strategy & long-term planning',
        'Risk consultation',
    ],
    "human-resources": [
        'Staff management & progression',
        'Onboarding, including new starter support and contracts of employment',
        'Payroll',
        'Salary benchmarking and employee benefits ',
        'Succession planning',
        'Employment & talent research',
        'Sourcing and Hiring',
    ],
    "legal": [
        'Company incorporation',
        'Employment',
        'Immigration',
        'Land use planning',
        'Intellectual property',
        'Data Protection and Information Assurance',
    ],
    "publicity": [
        'Public Relations',
        'Branding',
        'Social Media',
        'Public Affairs',
        'Advertising',
        'Marketing',
    ],
    "further-services": [
        'Business relocation',
        'Planning consultants',
        'Facilities (water, wifi, electricity)',
        'Translation services',
        'Staff and family relocation including schooling for children',
    ],
    "other": sentence().split(),
}


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


def profile_create_unverified_business_profile(
        context: Context, supplier_alias: str, company_alias: str
):
    if not context.get_actor(supplier_alias):
        context.add_actor(unauthenticated_supplier(supplier_alias))
    find_unregistered_company(context, supplier_alias, company_alias)
    enrol_user(context, supplier_alias, company_alias)
    context.update_actor(supplier_alias, has_sso_account=True)


def profile_create_verified_and_published_business_profile(
        context: Context, supplier_alias: str, company_alias: str
):
    """Create a verified Business profile and publish it to FAS"""
    logging.debug("1 - find unregistered company & enrol user for that company")
    profile_create_unverified_business_profile(context, supplier_alias, company_alias)
    logging.debug("2 - add business description")
    profile_add_business_description(context, supplier_alias)
    logging.debug("3 - decide to confirm identity with letter code")
    fab_decide_to_verify_profile_with_letter(context, supplier_alias)
    logging.debug("4 - get confirmation code from DB")
    logging.debug("5 - confirm identity with letter code")
    logging.debug("6 - provide verification code")
    logging.debug("7 - check if verified")
    profile_verify_company_profile(context, supplier_alias)
    logging.debug("8 - Publish your business profile")
    profile_publish_profile_to_fas(context, supplier_alias)


def profile_create_verified_yet_unpublished_business_profile(
        context: Context, supplier_alias: str, company_alias: str
):
    """Create a verified Business profile and publish it to FAS"""
    logging.debug("1 - find unregistered company & enrol user for that company")
    profile_create_unverified_business_profile(context, supplier_alias, company_alias)
    logging.debug("2 - add business description")
    profile_add_business_description(context, supplier_alias)
    logging.debug("3 - decide to confirm identity with letter code")
    fab_decide_to_verify_profile_with_letter(context, supplier_alias)
    logging.debug("4 - get confirmation code from DB")
    logging.debug("5 - confirm identity with letter code")
    logging.debug("6 - provide verification code")
    logging.debug("7 - check if verified")
    profile_verify_company_profile(context, supplier_alias)


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
    profile_about.should_be_here(context.response)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)
    context.update_actor(supplier_alias, has_sso_account=True)


@retry(wait_fixed=2000, stop_max_attempt_number=5)
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


def select_random_company(
    context: Context, supplier_alias: str, company_alias: str
):
    """Will try to find an active company that doesn't have a FAS profile.

    Steps (repeat until successful):
        1 - generate a random Companies House Number
        2 - check if there's a FAS profile for it
        3 - check if such company is registered at Companies House & is active

    Once a matching company is found, then it's data will be stored in:
        context.scenario_data.companies[]
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    max_attempts = 15
    counter = 0

    while True:
        # Step 1 - find an active company without a FAS profile
        company = get_active_company_without_fas_profile(company_alias)

        # Step 2 - Go to the Confirm Company page
        response = fab_ui_confirm_company.go_to(session, company)
        registered = is_already_registered(response)
        inactive = is_inactive(response)
        counter += 1
        if counter >= max_attempts:
            with assertion_msg(
                "Failed to find an active company which is not registered "
                "with FAB after %d attempts",
                max_attempts,
            ):
                assert False
        if registered or inactive:
            logging.warning(
                "Company '%s' is already registered or inactive, will use "
                "a different one",
                company.title,
            )
            continue
        else:
            logging.warning(
                "Company '%s' is active and not registered with FAB",
                company.title,
            )
            context.response = response
            break

    # Step 3 - check if we're on the Confirm Company page
    fab_ui_confirm_company.should_be_here(response, company)

    # Step 4 - store Company, CSRF token & associate Actor with Company
    context.add_company(company)
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)
    context.update_actor(supplier_alias, company_alias=company_alias)


def find_unregistered_company(
        context: Context, supplier_alias: str, company_alias: str
) -> Company:
    max_attempts = 15
    counter = 0

    while True:
        # Step 1 - find an active company without a FAS profile
        company = get_active_company_without_fas_profile(company_alias)
        company_details = get_company_by_id(company.number)
        counter += 1
        if counter >= max_attempts:
            with assertion_msg(
                    "Failed to find an active company which is not registered "
                    "with FAB after %d attempts",
                    max_attempts,
            ):
                assert False
        if not company_details:
            logging.debug(f"Found company not registered with us: '{company.number}'")
            break

    context.add_company(company)
    context.update_actor(supplier_alias, company_alias=company_alias)
    return company


def reg_confirm_company_selection(
    context: Context, supplier_alias: str, company_alias: str
):
    """Will confirm that the selected company is the right one."""
    actor = context.get_actor(supplier_alias)
    token = actor.csrfmiddlewaretoken
    has_sso_account = actor.has_sso_account
    session = actor.session
    company = context.get_company(company_alias)

    # Step 1 - confirm the selection of the company
    response = fab_ui_confirm_company.confirm_company_selection(
        session, company, token
    )
    context.response = response

    logging.debug("Confirmed selection of Company: %s", company.number)

    if has_sso_account:
        logging.debug("Supplier already has a SSO account")
        fab_ui_build_profile_basic.should_be_here(response)
    else:
        logging.debug("Supplier doesn't have a SSO account")
        sso_ui_register.should_be_here(response)
        token = extract_csrf_middleware_token(response)
        context.update_actor(supplier_alias, csrfmiddlewaretoken=token)


def reg_supplier_is_not_ready_to_export(context: Context, supplier_alias: str):
    """Supplier decides that her/his company is not ready to export."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    # Step 1 - Submit the form with No Intention to Export
    response = fab_ui_confirm_export_status.submit(
        session, token, exported=False
    )

    # Step 2 - store response & check it
    context.response = response
    check_response(response, 200)


def reg_create_sso_account(
    context: Context, supplier_alias: str, company_alias: str
):
    """Will create a SSO account for selected company.

    NOTE:
    Will use credentials randomly generated at Actor's initialization.
    It will also store final response in `context`
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(company_alias)

    logging.debug("Submit SSO Registration form with Supplier's & Company's required details")
    context.response = sso_ui_register.submit(actor, company)


def reg_open_email_confirmation_link(context: Context, supplier_alias: str):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    link = actor.email_confirmation_link

    # Step 1 - open confirmation link
    response = sso_ui_confim_your_email.open_confirmation_link(session, link)
    context.response = response

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    sso_ui_confim_your_email.should_be_here(response)
    logging.debug("Supplier is on the SSO Confirm your email address page")

    # Step 4 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(response)
    context.form_action_value = form_action_value


def reg_supplier_confirms_email_address(context: Context, supplier_alias: str):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.
    """
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response


def bp_provide_company_details(context: Context, supplier_alias: str):
    """Build Profile - Provide company details: website (optional), keywords
    and number of employees.
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    company_alias = company.alias

    # Step 0 - generate random details & update Company matching details
    # Need to get Company details after updating it in the Scenario Data
    title = "{} {} AUTOTESTS".format(company.title, sentence())
    size = choice(NO_OF_EMPLOYEES)
    website = "http://{}.{}".format(rare_word(min_length=15), rare_word())
    keywords = ", ".join(sentence().split())
    context.set_company_details(
        company_alias,
        title=title,
        no_employees=size,
        website=website,
        keywords=keywords,
    )
    company = context.get_company(actor.company_alias)

    # Step 1 - submit the Basic details form
    response = fab_ui_build_profile_basic.submit(actor, company)
    context.response = response

    # Step 2 - check if Supplier is on Select Your Sector page
    fab_ui_build_profile_sector.should_be_here(response)

    # Step 3 - extract CSRF token
    logging.debug("Supplier is on the Select Sector page")
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)


def bp_select_random_sector_and_export_to_country(
    context: Context, supplier_alias: str
):
    """Build Profile - Randomly select one of available sectors our company is
    interested in working in.

    NOTE:
    This will set `context.details` which will contain company details
    extracted from the page displayed after Supplier selects the sector.
    """
    actor = context.get_actor(supplier_alias)
    sector = choice(SECTORS)
    countries = [COUNTRIES[choice(list(COUNTRIES))]]
    other = ""
    has_exported_before = get_form_value("true or false")

    # Step 1 - Submit the Choose Your Sector form
    response = fab_ui_build_profile_sector.submit(
        actor, sector, countries, other, has_exported_before
    )
    context.response = response

    # Step 2 - check if Supplier is on Confirm Address page
    fab_ui_confirm_identity.should_be_here(response, profile_building=True)
    logging.debug("Supplier is on the Confirm your Identity page")


def fab_decide_to_verify_profile_with_letter(context: Context, supplier_alias: str):
    """Build Profile - verify identity with a physical letter."""
    actor = context.get_actor(supplier_alias)

    # Step 1 - go to page where you choose to verify with a letter
    response = fab_ui_confirm_identity_letter.go_to(actor.session)
    context.response = response
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 2 - Choose to verify with a letter
    response = fab_ui_confirm_identity_letter.submit(actor)
    context.response = response

    # Step 2 - check if Supplier is on the We've sent you a verification letter
    fab_ui_confirm_identity_letter.should_be_here(response)
    logging.debug(
        "Supplier is on the 'Your company address' letter verification page"
    )


def profile_add_business_description(context: Context, supplier_alias: str):
    """Edit Profile - Will set company description.

    This is quasi-mandatory (*) step before Supplier can verify the company
    with the code sent in a letter.

    (*) it's quasi mandatory, because Supplier can actually go to the company
    verification page using the link provided in the letter without the need
    to set company description.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Submit company description
    summary = sentence()
    description = sentence()
    response = profile_edit_company_description.submit(
        session, summary, description
    )
    context.response = response

    # Step 3 - check if Supplier is on Profile page
    profile_edit_company_profile.should_see_profile_is_not_verified(response)

    # Step 4 - update company details in Scenario Data
    context.set_company_details(
        actor.company_alias, summary=summary, description=description
    )
    logging.debug("Supplier is back to the Profile Page")


def profile_edit_business_details(
    context: Context, supplier_alias: str, *, table_of_details: Table
):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    # Step 0 - prepare company's details to update
    table_of_details = table_of_details or []
    details_to_update = [row["detail"] for row in table_of_details]
    title = DETAILS["NAME"] in details_to_update
    website = DETAILS["WEBSITE"] in details_to_update
    size = DETAILS["SIZE"] in details_to_update
    sector = DETAILS["SECTOR"] in details_to_update

    logging.debug(f"Details to update: {details_to_update}")
    # Step 1 - Update company's details
    response, new_details = profile_edit_company_business_details.submit(
        actor,
        company,
        change_name=title,
        change_website=website,
        change_size=size,
        change_sector=sector,
    )
    context.response = response

    # Step 2 - Supplier should be on Edit Profile page
    profile_edit_company_profile.should_be_here(response)


def profile_verify_company_profile(context: Context, supplier_alias: str):
    """Will verify the company by submitting the verification code that is sent
    by post to the company's address.
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session

    # STEP 0 - get the verification code from DB
    verification_code = get_verification_code(context, company.number)

    # STEP 1 - go to the "Verify your company" page
    response = fab_ui_verify_company.go_to(session)
    context.response = response

    # STEP 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # STEP 3 - Submit the verification code
    response = fab_ui_verify_company.submit(session, token, verification_code)
    context.response = response

    # STEP 4 - check if code was accepted
    fab_ui_verify_company.should_see_company_is_verified(response)

    # STEP 5 - click on the "View or amend your company profile" link
    response = profile_edit_company_profile.go_to(session)
    context.response = response

    # STEP 6 - check if Supplier is on Verified Profile Page
    profile_edit_company_profile.should_see_profile_is_verified(response)


def profile_publish_profile_to_fas(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    response = profile_publish_company_profile.submit(actor.session)
    context.response = response

    profile_edit_company_profile.should_see_profile_is_published(response)


def profile_view_published_profile(context: Context, supplier_alias: str):
    """Whilst being on Profile page it will `click` on
    the `View published profile` link.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # STEP 1 - go to the "View published profile" page
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    logging.debug("Supplier is on the company's FAS page")


def prof_attempt_to_sign_in_to_sso(context: Context, supplier_alias: str):
    """Try to sign in to FAB as a Supplier without verified email address."""
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign In page
    response = sso_ui_login.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on SSO Login page & extract CSRF token
    sso_ui_login.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - submit the login form
    response = sso_ui_login.login(actor)
    context.response = response


def reg_create_standalone_unverified_sso_account(
    context: Context, supplier_alias: str
):
    """Will create a standalone SSO/great.gov.uk account.

    NOTE:
    There will be no association between this account and any company.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1: Go to the SSO/great.gov.uk registration page
    response = sso_ui_register.go_to(session)
    context.response = response
    sso_ui_register.should_be_here(response)

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)
    actor = context.get_actor(supplier_alias)

    # Step 3: Check if User is not logged in
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 4: POST SSO accounts/signup/
    response = sso_ui_register.submit_no_company(actor)
    context.response = response

    # Step 5: Check if Supplier is on Verify your email page & is not logged in
    sso_ui_verify_your_email.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"


def sso_collaborator_confirm_email_address(
    context: Context, supplier_alias: str
):
    """Given that invited collaborator has clicked on the email confirmation
     link, he/she has to confirm that the provided email address is the
      correct one.
    """
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if Supplier if on SSO Profile Landing page
    fab_ui_confim_your_collaboration.should_be_here(response)

    # STEP 3 - Update Actor's data
    context.update_actor(supplier_alias, has_sso_account=True)


def sso_new_onwer_confirm_email_address(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if new account owner is on the correct page
    fab_ui_confim_your_ownership.should_be_here(response)

    # STEP 3 - Update Actor's data
    context.update_actor(supplier_alias, has_sso_account=True)


def sso_supplier_confirms_email_address(context: Context, supplier_alias: str):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.
    """
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if Supplier if on SSO Profile Landing page
    profile_about.should_be_here(response)

    # STEP 3 - Update Actor's data
    context.update_actor(supplier_alias, has_sso_account=True)


def profile_upload_unsupported_file_as_logo(
    context: Context, supplier_alias: str, file: str
):
    """Try to upload unsupported file type as Company's logo.

    NOTE:
    file must exist in ./tests/functional/files

    :param file: name of the file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    file_path = get_absolute_path_of_file(file)

    logging.debug("Attempting to upload %s as company logo", file)
    # Step 1 - Try to upload a file of unsupported type as company's logo
    response = profile_upload_logo.upload(session, file_path)
    context.response = response

    # Step 2 - check if upload was rejected
    rejected = profile_upload_logo.was_upload_rejected(response)

    # There are 2 different error message that you can get, depending of the
    # type of uploaded file.
    # Here, we're checking if `any` of these 2 message is visible.
    if rejected:
        logging.debug("%s was rejected", file)
    else:
        logging.error("%s was accepted", file)
    return rejected


def profile_to_upload_unsupported_logos(
        context: Context, supplier_alias: str, table: Table
):
    """Upload a picture and set it as Company's logo."""
    files = [row["file"] for row in table]
    rejections = []
    for file in files:
        rejected = profile_upload_unsupported_file_as_logo(
            context, supplier_alias, file
        )
        rejections.append(rejected)
    context.rejections = rejections


def profile_supplier_uploads_logo(
    context: Context, supplier_alias: str, picture: str
):
    """Upload a picture and set it as Company's logo.

    :param picture: name of the picture file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    file_path = get_absolute_path_of_file(picture)

    # Step 1 - upload the logo
    response = profile_upload_logo.upload(session, file_path)
    context.response = response

    # Step 2 - check if Supplier is on the FAB profile page
    profile_edit_company_profile.should_be_here(response)
    logging.debug("Successfully uploaded logo picture: %s", picture)

    # Step 3 - Keep logo details in Company's scenario data
    logo_url = extract_logo_url(response)
    md5_hash = get_md5_hash_of_file(file_path)
    context.set_company_logo_detail(
        actor.company_alias, picture=picture, hash=md5_hash, url=logo_url
    )


def profile_update_company_details(
    context: Context, supplier_alias: str, table_of_details: Table
):
    """Update selected Company's details."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    # Step 0 - prepare company's details to update
    details_to_update = [row["detail"] for row in table_of_details]
    change_name = DETAILS["NAME"] in details_to_update
    change_website = DETAILS["WEBSITE"] in details_to_update
    change_size = DETAILS["SIZE"] in details_to_update
    change_sector = DETAILS["SECTOR"] in details_to_update
    change_keywords = DETAILS["KEYWORDS"] in details_to_update

    # Step 1 - Update company's details
    if any([change_name, change_website, change_size, change_sector]):
        response, new_details = profile_edit_company_business_details.submit(
            actor,
            company,
            change_name=change_name,
            change_website=change_website,
            change_size=change_size,
            change_sector=change_sector,
        )
        context.response = response

        # Step 2 - Supplier should be on Edit Profile page
        profile_edit_company_profile.should_be_here(response)

        # Step 3 - update company's details stored in context.scenario_data
        context.set_company_details(
            actor.company_alias,
            title=new_details.title,
            website=new_details.website,
            no_employees=new_details.no_employees,
            sector=new_details.sector,
        )

    # Step 3 - Go to the Edit Sector page
    industries = INDUSTRIES_FOR_PRODUCTS_AND_SERVICES
    if change_keywords:
        industry = random.choice(list(industries.keys()))
        response = profile_edit_products_and_services_industry.submit(
            actor.session,
            industry=industry,
        )
        context.response = response
        profile_edit_products_and_services_keywords.should_be_here(
            response, industry=industry
        )

        number_of_keywords = random.randint(1, len(industries[industry]))
        keywords = list(
            set(
                random.choice(industries[industry]) for _ in range(number_of_keywords)
            )
        )
        response = profile_edit_products_and_services_keywords.submit(
            actor.session,
            industry=industry,
            keywords=keywords,
        )
        context.response = response

        # Step 3' - Check if Supplier is on FAB Profile page
        profile_edit_company_profile.should_be_here(response)

        # Step 4 - update company's details stored in context.scenario_data
        context.set_company_details(
            actor.company_alias,
            industry=industry,
            keywords=", ".join(keywords),
        )


def profile_add_online_profiles(
    context: Context, supplier_alias: str, online_profiles: Table
):
    """Update links to Company's Online Profiles."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    profiles = [row["online profile"] for row in online_profiles]
    facebook = PROFILES["FACEBOOK"] in profiles
    linkedin = PROFILES["LINKEDIN"] in profiles
    twitter = PROFILES["TWITTER"] in profiles

    # Step 1 - Update links to Online Profiles
    response, new_details = profile_edit_online_profiles.update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )
    context.response = response

    # Step 2 - Check if Supplier is on FAB Profile page
    profile_edit_company_profile.should_be_here(response)

    # Step 3 - Update company's details stored in context.scenario_data
    context.set_company_details(
        company.alias,
        facebook=new_details.facebook,
        linkedin=new_details.linkedin,
        twitter=new_details.twitter,
    )
    logging.debug(
        "%s set Company's Online Profile links to: Facebook=%s, LinkedId=%s, "
        "Twitter=%s",
        supplier_alias,
        new_details.facebook,
        new_details.linkedin,
        new_details.twitter,
    )


def profile_add_invalid_online_profiles(
    context: Context, supplier_alias: str, online_profiles: Table
):
    """Attempt to update links to Company's Online Profiles using invalid URLs.
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    facebook = False
    linkedin = False
    twitter = False
    facebook_url = "http://notfacebook.com"
    linkedin_url = "http://notlinkedin.com"
    twitter_url = "http://nottwitter.com"
    for row in online_profiles:
        if row["online profile"] == PROFILES["FACEBOOK"]:
            facebook = True
            facebook_url = row.get("invalid link", facebook_url)
        if row["online profile"] == PROFILES["LINKEDIN"]:
            linkedin = True
            linkedin_url = row.get("invalid link", linkedin_url)
        if row["online profile"] == PROFILES["TWITTER"]:
            twitter = True
            twitter_url = row.get("invalid link", twitter_url)

    logging.debug(
        "Will use following invalid URLs to Online Profiles: %s %s %s",
        facebook_url if facebook else "",
        linkedin_url if linkedin else "",
        twitter_url if twitter else "",
    )
    response, _ = profile_edit_online_profiles.update_profiles(
        actor,
        company,
        facebook=facebook,
        linkedin=linkedin,
        twitter=twitter,
        specific_facebook=facebook_url,
        specific_linkedin=linkedin_url,
        specific_twitter=twitter_url,
    )
    context.response = response


def profile_remove_links_to_online_profiles(
    context: Context, supplier_alias: str
):
    """Will remove links to existing Online Profiles."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    context.response = profile_edit_online_profiles.remove_links(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )

    # Update company's details stored in context.scenario_data
    context.set_company_details(
        company.alias,
        facebook=None,
        linkedin=None,
        twitter=None,
    )


def profile_add_case_study(
    context: Context, supplier_alias: str, case_alias: str
):
    """Will add a complete case study (all fields will be filled out)."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    case_study = random_case_study_data(case_alias)

    # Step 1 - go to "Add case study" form & extract CSRF token
    response = profile_case_study_basic.go_to(session)
    context.response = response
    profile_case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 2 - submit the "basic case study data" form & extract CSRF token
    response = profile_case_study_basic.submit(session, token, case_study)
    context.response = response
    profile_case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "case study images" form
    response = profile_case_study_images.submit(session, token, case_study)
    context.response = response

    # Step 4 - check if we're on the FAB Profile page
    profile_edit_company_profile.should_be_here(response)

    # Step 5 - Store Case Study data in Scenario Data
    context.add_case_study(actor.company_alias, case_alias, case_study)


def profile_update_case_study(
    context: Context, supplier_alias: str, case_alias: str
):
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    # get content from last response (which contains Edit Business Profile Page)
    content = context.response.content.decode("utf-8")

    # Step 0 - extract links to Case Studies and do a crude mapping to
    # Case Study titles.
    css_titles = "#case-studies span::text"
    css_links = "#case-studies a::attr(href)"
    titles = Selector(text=content).css(css_titles).extract()
    links = Selector(text=content).css(css_links).extract()
    case_link_mappings = {k: v for (k, v) in zip(titles, links)}
    current = company.case_studies[case_alias]
    current_link = case_link_mappings[current.title]
    # link format is "/profile/find-a-buyer/case-study/35309/basic/"
    index_of_case_id_in_url = 4
    current_number = int(current_link.split("/")[index_of_case_id_in_url])
    logging.debug(
        "Extracted link for case study: %s is: %s", case_alias, current_link
    )

    # Step 1 - generate new case study data
    new_case = random_case_study_data(case_alias)
    logging.debug("Now will replace case study data with: %s", new_case)

    # Step 2 - go to specific "Case study" page form & extract CSRF token
    response = profile_case_study_basic.go_to(
        session, case_number=current_number
    )
    context.response = response
    profile_case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "basic case study data" form & extract CSRF token
    response = profile_case_study_basic.submit(session, token, new_case)
    context.response = response
    profile_case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 4 - submit the "case study images" form
    response = profile_case_study_images.submit(session, token, new_case)
    context.response = response

    # Step 5 - check if we're on the FAB Profile page
    profile_edit_company_profile.should_be_here(response)

    # Step 5 - Store new Case Study data in Scenario Data
    # `add_case_study` apart from adding will replace existing case study.
    context.add_case_study(actor.company_alias, case_alias, new_case)
    logging.debug(
        "Successfully updated details of case study: '%s', title:'%s', link:"
        "'%s'",
        case_alias,
        current.title,
        current_link,
    )


def fas_search_using_company_details(
    context: Context,
    buyer_alias: str,
    company_alias: str,
    *,
    table_of_details: Table = None
):
    """Search for Company on FAS using it's all or selected details."""
    actor = context.get_actor(buyer_alias)
    session = actor.session
    company = context.get_company(company_alias)
    keys = [
        "title",
        "number",
        "summary",
        "description",
        "website",
        "keywords",
        "facebook",
        "linkedin",
        "twitter",
        "slug",
    ]

    # use selected company details
    if table_of_details:
        keys = [row["company detail"] for row in table_of_details]

    search_terms = {}
    search_results = {}
    search_responses = {}
    for key in keys:
        if key == "keywords":
            for index, keyword in enumerate(company.keywords.split(", ")):
                search_terms[f"keyword #{index}"] = keyword
        else:
            search_terms[key] = getattr(company, key)
    logging.debug(
        "Now %s will try to find '%s' using following search terms: %s",
        buyer_alias,
        company.title,
        search_terms,
    )
    for term_name in search_terms:
        term = search_terms[term_name]
        response = fas_ui_find_supplier.go_to(session, term=term)
        context.response = response
        fas_ui_find_supplier.should_be_here(response)
        number_of_pages = get_number_of_search_result_pages(response)

        if number_of_pages == 0:
            found = fas_ui_find_supplier.should_see_company(
                response, company.title
            )
            search_results[term_name] = found
            search_responses[term_name] = response
            logging.debug(
                "Couldn't find Supplier '%s' on the first and only FAS search "
                "result page. Search was done using '%s' : '%s'",
                company.title,
                term_name,
                term,
            )
            continue

        for page_number in range(1, number_of_pages + 1):
            search_responses[term_name] = response
            found = fas_ui_find_supplier.should_see_company(
                response, company.title
            )
            search_results[term_name] = found
            if found:
                logging.debug(
                    "Found Supplier '%s' on FAS using '%s' : '%s' on %d page "
                    "out of %d",
                    company.title,
                    term_name,
                    term,
                    page_number,
                    number_of_pages,
                )
                break
            else:
                logging.debug(
                    "Couldn't find Supplier '%s' on the %d page out of %d of "
                    "FAS search results. Search was done using '%s' : '%s'",
                    company.title,
                    page_number,
                    number_of_pages,
                    term_name,
                    term,
                )
                next_page = page_number + 1
                if next_page <= number_of_pages:
                    response = fas_ui_find_supplier.go_to(
                        session, term=term, page=next_page
                    )
                else:
                    logging.debug(
                        "Couldn't find the Supplier even on the last"
                        " page of the search results"
                    )
    context.search_results = search_results
    context.search_responses = search_responses


def generic_view_pages_in_selected_language(
    context: Context, buyer_alias: str, pages_table: Table, language: str,
    language_argument: str = "lang",
):
    """View specific FAS pages in selected language.

    NOTE:
    This will store a dict with all page views responses in context.views
    """
    pages = [row["page"] for row in pages_table]
    views = {}
    actor = context.get_actor(buyer_alias)
    session = actor.session
    for page_name in pages:
        language_code = get_language_code(language)
        page_url = get_page_object(page_name).URL
        page_url += f"?{language_argument}={language_code}"
        response = make_request(Method.GET, page_url, session=session)
        views[page_name] = response
    context.views = views


def fas_search_with_empty_query(context: Context, buyer_alias: str):
    actor = context.get_actor(buyer_alias)
    session = actor.session
    context.response = fas_ui_find_supplier.go_to(session, term="")
    fas_ui_find_supplier.should_be_here(context.response)


def fas_should_be_told_about_empty_search_results(
    context: Context, buyer_alias: str
):
    fas_ui_find_supplier.should_see_no_matches(context.response)
    logging.debug(
        "%s was told that the search did not match any UK trade profiles",
        buyer_alias,
    )


def fas_send_feedback_request(
    context: Context, buyer_alias: str, page_name: str
):
    actor = context.get_actor(buyer_alias)
    session = actor.session
    referer_url = get_page_object(page_name).URL

    # Step 1: generate random form data for our Buyer
    feedback = random_feedback_data(email=actor.email)

    # Step 2: submit the form
    response = fas_ui_feedback.submit(session, feedback, referer=referer_url)
    context.response = response
    logging.debug("%s submitted the feedback request", buyer_alias)


def fas_feedback_request_should_be_submitted(
    context: Context, buyer_alias: str
):
    response = context.response
    fas_ui_feedback.should_see_feedback_submission_confirmation(response)
    logging.debug(
        "%s was told that the feedback request has been submitted", buyer_alias
    )


def fas_get_company_profile_url(response: Response, name: str) -> str:
    content = response.content.decode("utf-8")
    links_to_profiles_selector = "#ed-search-list-container .span9 a"
    href_selector = "a::attr(href)"
    links_to_profiles = (
        Selector(text=content).css(links_to_profiles_selector).extract()
    )
    profile_url = None
    for link in links_to_profiles:
        # try to find Profile URL by escaping html chars or not in found link
        if (escape_html(name).lower() in link.lower()) \
                or (escape_html(name).lower() in escape_html(link).lower()):
            profile_url = Selector(text=link).css(href_selector).extract()[0]
    with assertion_msg(
        "Couldn't find link to '%s' company profile page in the response", name
    ):
        assert profile_url
    return profile_url


def can_find_supplier_by_term(
    session: Session, name: str, term: str, term_type: str
) -> (bool, Response, str):
    """

    :param session: Buyer's session object
    :param name: sought Supplier name
    :param term: a text used to find the Supplier
    :param term_type: type of the term, e.g.: product, service, keyword etc.
    :return: a tuple with search result (True/False), last search Response and
             an endpoint to company's profile
    """
    found = False
    endpoint = None
    response = fas_ui_find_supplier.go_to(session, term=term)
    fas_ui_find_supplier.should_be_here(response)
    number_of_pages = get_number_of_search_result_pages(response)
    if number_of_pages == 0:
        return found, response, endpoint
    for page_number in range(1, number_of_pages + 1):
        found = fas_ui_find_supplier.should_see_company(response, name)
        if found:
            endpoint = fas_get_company_profile_url(response, name)
            break
        else:
            logging.debug(
                "Couldn't find Supplier '%s' on the %d page out of %d of "
                "FAS search results. Search was done using '%s' : '%s'",
                name,
                page_number,
                number_of_pages,
                term_type,
                term,
            )
            next_page = page_number + 1
            if next_page <= number_of_pages:
                response = fas_ui_find_supplier.go_to(
                    session, term=term, page=next_page
                )
                fas_ui_find_supplier.should_be_here(response)
            else:
                logging.debug(
                    "Couldn't find the Supplier even on the last page of the "
                    "search results"
                )
    return found, response, endpoint


def fas_search_with_product_service_keyword(
    context: Context, buyer_alias: str, search_table: Table
):
    """Search for Suppliers with one of the following:
    * Product name
    * Service name
    * keyword

    NOTE: this will add a dictionary `search_results` to `context`
    """
    actor = context.get_actor(buyer_alias)
    session = actor.session
    search_results = {}
    for row in search_table:
        terms = []
        if row["product"]:
            terms.append({"type": "product", "term": row["product"]})
        if row["service"]:
            terms.append({"type": "service", "term": row["service"]})
        if row["keyword"]:
            terms.append({"type": "keyword", "term": row["keyword"]})
        search_results[row["company"]] = terms

    for company in search_results:
        search_terms = search_results[company]
        for search_term in search_terms:
            term_type = search_term["type"]
            term = search_term["term"]
            logging.debug(
                "%s is searching for company '%s' using %s term '%s'",
                buyer_alias,
                company,
                term_type,
                term,
            )
            found, response, _ = can_find_supplier_by_term(
                session, company, term, term_type
            )
            search_term["found"] = found
            search_term["response"] = response

    context.search_results = search_results


def fas_send_message_to_supplier(
    context: Context, buyer_alias: str, company_alias: str
):
    buyer = context.get_actor(buyer_alias)
    session = buyer.session
    company = context.get_company(company_alias)
    endpoint = company.fas_profile_endpoint
    with assertion_msg(
        "Company '%s' doesn't have FAS profile URL set", company.title
    ):
        assert endpoint
    # Step 0 - generate message data
    message = random_message_data()

    # Step 1 - go to Company's profile page
    response = fas_ui_profile.go_to_endpoint(session, endpoint)
    context.response = response
    fas_ui_profile.should_be_here(response, number=company.number)

    # Step 2 - go to the "email company" form
    response = fas_ui_contact.go_to(session, company_number=company.number)
    context.response = response
    fas_ui_contact.should_be_here(response)

    # Step 3 - submit the form with the message data
    response = fas_ui_contact.submit(session, message, company.number)
    context.response = response


def profile_provide_business_details(
        context: Context, supplier_alias: str, table: Table
):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    results = []
    for row in table:
        if row["trading name"] == "unchanged":
            new_name = company.title
            change_name = False
        elif row["trading name"] == "empty string":
            new_name = "empty string"
            change_name = True
        elif row["trading name"].endswith(" characters"):
            number = [
                int(word)
                for word in row["trading name"].split()
                if word.isdigit()
            ][0]
            new_name = random_chars(number)
            change_name = True
        else:
            new_name = company.title
            change_name = False

        if row["website"] == "unchanged":
            new_website = company.website
            change_website = False
        elif row["website"] == "empty string":
            new_website = "empty string"
            change_website = True
        elif row["website"] == "valid http":
            new_website = "http://{}.{}".format(rare_word(), rare_word())
            change_website = True
        elif row["website"] == "valid https":
            new_website = "https://{}.{}".format(rare_word(), rare_word())
            change_website = True
        elif row["website"] == "invalid http":
            new_website = "http"
            change_website = True
        elif row["website"] == "invalid https":
            new_website = "https"
            change_website = True
        elif row["website"].endswith(" characters"):
            number = [
                int(word) for word in row["website"].split() if word.isdigit()
            ][0]
            new_website = random_chars(number)
            change_website = True
        else:
            new_website = company.website
            change_website = False

        if row["size"] == "unchanged":
            new_size = None
            change_size = False
        elif row["size"] == "unset":
            new_size = "unset"
            change_size = True
        else:
            new_size = row["size"]
            change_size = True

        if row["industry"] == "unchanged":
            new_sector = None
            change_sector = False
        elif row["industry"] == "unset":
            new_sector = "unset"
            change_sector = True
        elif row["industry"] == "random":
            new_sector, _ = random.choice(choices.INDUSTRIES)
            change_sector = True
        else:
            new_sector = company.sector
            change_sector = False

        modified_details = Company(
            title=new_name, website=new_website, no_employees=new_size,
            sector=new_sector
        )

        logging.debug(f"Details to update: {modified_details}")
        response, new_details = profile_edit_company_business_details.submit(
            actor,
            company,
            change_name=change_name,
            specific_name=new_name,
            change_website=change_website,
            specific_website=new_website,
            change_size=change_size,
            specific_size=new_size,
            change_sector=change_sector,
            specific_sector=new_sector,
        )
        results.append((new_details, response, row["error"]))

    context.results = results


def profile_provide_products_and_services(
        context: Context, supplier_alias: str, table: Table
):
    actor = context.get_actor(supplier_alias)
    results = []
    for row in table:
        if row["keywords"] == "empty string":
            keywords = ""
        elif row["keywords"].endswith(" characters"):
            number = [
                int(word) for word in row["keywords"].split() if word.isdigit()
            ][0]
            keywords = random_chars(number)
        else:
            keywords = row["keywords"]
            separate_keywords = keywords.split(", ")
            if row["separator"] == "pipe":
                keywords = "| ".join(separate_keywords)
            if row["separator"] == "semi-colon":
                keywords = "; ".join(separate_keywords)
            if row["separator"] == "colon":
                keywords = ": ".join(separate_keywords)
            if row["separator"] == "full stop":
                keywords = ". ".join(separate_keywords)

        modified_details = Company(keywords=keywords)
        logging.debug(f"Keywords to update: {keywords}")
        response = profile_edit_products_and_services_keywords.submit(
            actor.session,
            industry=industry,
            keywords=keywords
        )
        results.append((modified_details, response, row["error"]))

    context.results = results


def fas_follow_case_study_links_to_related_sectors(
    context: Context, actor_alias: str
):
    actor = context.get_actor(actor_alias)
    session = actor.session
    content = context.response.content.decode("utf-8")
    links_css_selector = "#company-showcase .case-study-info a"
    links_to_sectors = Selector(text=content).css(links_css_selector).extract()
    with assertion_msg(
        "Expected to find at least 1 link to Industry sector"
        "associated with Company Showcase Case Study"
    ):
        assert links_css_selector
    results = {}
    fas_url = get_absolute_url("ui-supplier:landing")
    for link in links_to_sectors:
        industry = Selector(text=link).css("a::text").extract()[0]
        href = Selector(text=link).css("a::attr(href)").extract()[0]
        url = urljoin(fas_url, href)
        sectors = [value for _, value in parse_qsl(urlsplit(href).query)]
        logging.debug(
            "%s will look for Suppliers in '%s' Industry sectors '%s'",
            actor_alias,
            industry,
            ", ".join(sectors),
        )
        response = make_request(Method.GET, url=url, session=session)
        results[industry] = {
            "url": url,
            "sectors": sectors,
            "response": response,
        }
    context.results = results


def fas_browse_suppliers_using_every_sector_filter(
    context: Context, actor_alias: str
):
    actor = context.get_actor(actor_alias)
    session = actor.session

    response = fas_ui_find_supplier.go_to(session, term="")
    context.response = response
    fas_ui_find_supplier.should_be_here(response)

    sector_filters_selector = "#id_sectors input::attr(value)"
    content = response.content.decode("utf-8")
    sector_filters = (
        Selector(text=content).css(sector_filters_selector).extract()
    )
    results = {}
    for sector in sector_filters:
        logging.debug(
            "%s will browse Suppliers by Industry sector filter '%s'",
            actor_alias,
            sector,
        )
        response = fas_ui_find_supplier.go_to(session, sectors=[sector])
        fas_ui_find_supplier.should_be_here(response)
        results[sector] = {
            "url": response.request.url,
            "sectors": [sector],
            "response": response,
        }
    context.results = results


def fas_browse_suppliers_by_multiple_sectors(
    context: Context, actor_alias: str
):
    actor = context.get_actor(actor_alias)
    session = actor.session

    response = fas_ui_find_supplier.go_to(session, term="")
    context.response = response
    fas_ui_find_supplier.should_be_here(response)

    sector_selector = "#id_sectors input::attr(value)"
    content = response.content.decode("utf-8")
    filters = Selector(text=content).css(sector_selector).extract()

    sectors = list(
        set(choice(filters) for _ in range(randrange(1, len(filters))))
    )
    results = {}
    logging.debug(
        "%s will browse Suppliers by multiple Industry sector filters '%s'",
        actor_alias,
        ", ".join(sectors),
    )
    response = fas_ui_find_supplier.go_to(session, sectors=sectors)
    fas_ui_find_supplier.should_be_here(response)
    results["multiple choice"] = {
        "url": response.request.url,
        "sectors": sectors,
        "response": response,
    }
    context.results = results


def fas_browse_suppliers_by_invalid_sectors(
    context: Context, actor_alias: str
):
    actor = context.get_actor(actor_alias)
    session = actor.session

    response = fas_ui_find_supplier.go_to(session, term="")
    context.response = response
    fas_ui_find_supplier.should_be_here(response)

    sector_selector = "#id_sectors input::attr(value)"
    content = response.content.decode("utf-8")
    filters = Selector(text=content).css(sector_selector).extract()

    sectors = list(
        set(choice(filters) for _ in range(randrange(1, len(filters))))
    )

    sectors.append("this_is_an_invalid_sector_filter")
    logging.debug(
        "%s will browse Suppliers by multiple Industry sector filters and will"
        " inject an invalid filter: '%s'",
        actor_alias,
        ", ".join(sectors),
    )
    context.response = fas_ui_find_supplier.go_to(session, sectors=sectors)


def fas_clear_search_filters(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    session = actor.session

    logging.debug("%s will clear the search filter", actor_alias)
    response = fas_ui_find_supplier.go_to(session, term="")
    context.response = response
    fas_ui_find_supplier.should_be_here(response)


def fas_browse_suppliers_by_company_sectors(
    context: Context, actor_alias: str, company_alias: str, pages_to_scan: int
):
    actor = context.get_actor(actor_alias)
    session = actor.session
    company = context.get_company(company_alias)
    sectors = company.sector
    results = {}

    response = fas_ui_find_supplier.go_to(session, sectors=sectors)
    context.response = response
    fas_ui_find_supplier.should_be_here(response)

    found = fas_ui_find_supplier.should_see_company(response, company.title)

    results[1] = {
        "url": response.request.url,
        "sectors": sectors,
        "response": response,
        "found": found,
    }

    last_page = get_number_of_search_result_pages(response)
    logging.debug("Search results have %d pages", last_page)
    if last_page > 1:
        last_page = pages_to_scan if pages_to_scan < last_page else last_page
        logging.debug("Will scan only first %d pages", last_page)
        for page_number in range(2, last_page):
            logging.debug("Going to search result page no.: %d", page_number)
            response = fas_ui_find_supplier.go_to(
                session, page=page_number, sectors=sectors
            )
            found = fas_ui_find_supplier.should_see_company(
                response, company.title
            )
            results[page_number] = {
                "url": response.request.url,
                "sectors": sectors,
                "response": response,
                "found": found,
            }

    logging.debug(
        "%s browsed first %d pages of search results filtered by multiple "
        "sector filters '%s'",
        actor_alias,
        last_page,
        ", ".join(sectors),
    )
    context.results = results


def fas_get_case_study_slug(
    context: Context, actor_alias: str, case_alias: str
):
    result = None
    actor = context.get_actor(actor_alias)
    company = context.get_company(actor.company_alias)
    case = context.get_company(actor.company_alias).case_studies[case_alias]

    response = fas_ui_profile.go_to(actor.session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)

    case_studies_details = fas_ui_profile.get_case_studies_details(response)
    for title, summary, href, slug in case_studies_details:
        if title == case.title:
            result = slug

    with assertion_msg("Could not find slug for case study '%s'", case_alias):
        assert result is not None

    context.update_case_study(company.alias, case_alias, slug=result)
    logging.debug(
        "%s got case study '%s' slug: '%s'", actor_alias, case_alias, result
    )


def fas_search_with_term(context: Context, actor_alias: str, search_term: str):
    actor = context.get_actor(actor_alias)
    session = actor.session
    context.response = fas_ui_find_supplier.go_to(session, term=search_term)
    fas_ui_find_supplier.should_be_here(context.response)


def profile_go_to_letter_verification(
    context: Context, supplier_alias: str, logged_in: bool
):
    actor = context.get_actor(supplier_alias)
    response = fab_ui_confirm_identity.go_to(actor.session)
    context.response = response

    if logged_in:
        fab_ui_verify_company.should_be_here(response)
    else:
        sso_ui_login.should_be_here(response)

        token = extract_csrf_middleware_token(response)
        context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

        sso_login_url = get_absolute_url("sso:login")
        fab_verify_url = quote(get_absolute_url("ui-buyer:confirm-identity"))
        referer = "{sso_login_url}?next={fab_verify_url}".format(
            sso_login_url=sso_login_url, fab_verify_url=fab_verify_url
        )
        next = get_absolute_url("ui-buyer:confirm-identity")
        logging.debug(
            "After successful login %s should be redirected to: %s",
            supplier_alias,
            referer,
        )
        response = sso_ui_login.login(actor, referer=referer, next_param=next)
        context.response = response

        fab_ui_verify_company.should_be_here(response)


def fab_choose_to_verify_with_code(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    referer = get_absolute_url("ui-buyer:confirm-identity")
    response = fab_ui_verify_company.go_to(actor.session, referer=referer)
    context.response = response
    fab_ui_verify_company.should_be_here(response)


def fab_submit_verification_code(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    verification_code = company.verification_code
    referer = get_absolute_url("ui-buyer:confirm-company-address")
    response = fab_ui_verify_company.submit(
        actor.session,
        actor.csrfmiddlewaretoken,
        verification_code,
        referer=referer,
    )
    context.response = response


def get_form_value(key: str) -> str or list or int or None:
    def get_number_from_key(key: str) -> int:
        numbers = [int(word) for word in key.split() if word.isdigit()]
        return numbers[0] if numbers else 0

    def get_n_chars(number: int) -> str:
        return random_chars(number)

    def get_n_words(number: int) -> str:
        return sentence(min_words=number, max_words=number, max_length=0)

    def get_n_country_codes(number: int) -> list:
        country_codes = ["CN", "DE", "IN", "JP", "US"]
        max = number if number <= len(country_codes) else len(country_codes)
        return [country_codes[idx] for idx in range(max)]

    result = None

    mappings = [
        ("empty string", ""),
        ("valid http", "http://{}.{}".format(rare_word(), rare_word())),
        ("valid https", "https://{}.{}".format(rare_word(), rare_word())),
        ("invalid http", "http:{}.{}".format(rare_word(), rare_word())),
        ("invalid https", "https:{}.{}".format(rare_word(), rare_word())),
        ("invalid sector", "this is an invalid sector"),
        ("no image", None),
        ("invalid image", choice(BMPs + JP2s + WEBPs)),
        (" characters$", get_n_chars(get_number_from_key(key))),
        (" words$", get_n_words(get_number_from_key(key))),
        (
            " predefined countries$",
            get_n_country_codes(get_number_from_key(key)),
        ),
        ("1 predefined country$", get_n_country_codes(1)),
        ("none selected", None),
        ("sector", choice(SECTORS)),
        ("true or false", choice([True, False])),
    ]

    found = False
    for pattern, value in mappings:
        r = re.compile(pattern)
        if r.findall(key):
            result = value
            found = True
            break

    if not found:
        result = key

    return result


def profile_attempt_to_add_case_study(
    context: Context, supplier_alias: str, table: Table
):
    actor = context.get_actor(supplier_alias)
    session = actor.session

    page_1_fields = [
        "title",
        "summary",
        "description",
        "sector",
        "website",
        "keywords",
    ]
    page_2_fields = [
        "image_1",
        "caption_1",
        "image_2",
        "caption_2",
        "image_3",
        "caption_3",
        "testimonial",
        "source_name",
        "source_job",
        "source_company",
    ]

    results = []
    for row in table:
        case_study = random_case_study_data("test")
        field = row["field"]
        value_type = row["value type"]
        separator = row["separator"]
        error = row["error"]

        value = get_form_value(value_type)

        if field == "keywords":
            separator = SEPARATORS.get(separator, ",")
            value = "{} ".format(separator).join(value.split())

        case_study = case_study._replace(**{field: value})

        response = profile_case_study_basic.go_to(session)
        context.response = response
        profile_case_study_basic.should_be_here(response)

        token = extract_csrf_middleware_token(response)

        if field in page_1_fields:
            response = profile_case_study_basic.submit(
                session, token, case_study
            )
            context.response = response
        elif field in page_2_fields:
            response = profile_case_study_basic.submit(
                session, token, case_study
            )
            context.response = response
            token = extract_csrf_middleware_token(response)
            response = profile_case_study_images.submit(
                session, token, case_study
            )
            context.response = response
        else:
            raise KeyError(
                "Could not recognize field '{}' as valid case study field"
            )

        results.append((field, value_type, case_study, response, error))

    context.results = results


def sso_request_password_reset(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    if actor.company_alias is None:
        next_param = get_page_object("profile - about").URL
    else:
        next_param = get_page_object("fab - landing").URL

    response = sso_ui_password_reset.go_to(
        actor.session, next_param=next_param
    )
    context.response = response

    sso_ui_password_reset.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    response = sso_ui_password_reset.reset(actor, token, next_param=next_param)
    context.response = response


def sso_sign_in(context: Context, supplier_alias: str, *, from_page: str = None):
    """Sign in to standalone SSO account."""
    actor = context.get_actor(supplier_alias)
    from_page = get_page_object(from_page).URL if from_page else None
    next_param = from_page or get_absolute_url("profile:about")
    referer = from_page or get_absolute_url("profile:about")
    response = sso_ui_login.go_to(
        actor.session, next_param=next_param, referer=referer
    )
    context.response = response

    sso_ui_login.should_be_here(response)
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    context.response = sso_ui_login.login(
        actor, next_param=next_param, referer=referer
    )
    error = f"User is not logged in. Could not find 'Sign out' in the response from {context.response.url}"
    assert "Sign out" in context.response.content.decode("UTF-8"), error
    logging.debug(f"{actor.email} is logged in")


def sso_change_password_with_password_reset_link(
    context: Context,
    supplier_alias: str,
    *,
    new: bool = False,
    same: bool = False,
    mismatch: bool = False,
    letters_only: bool = False
):
    actor = context.get_actor(supplier_alias)
    session = actor.session
    link = actor.password_reset_link

    response = sso_ui_password_reset.open_link(session, link)
    context.response = response

    sso_ui_change_password.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)
    action = extract_form_action(response)

    password = None
    password_again = None

    if new:
        password_length = 15
        if letters_only:
            password = "".join(
                choice(ascii_letters) for _ in range(password_length)
            )
        else:
            password = "".join(
                choice(ascii_letters) + choice(digits)
                for _ in range(password_length)
            )
        context.update_actor(supplier_alias, password=password)
    if same:
        password = actor.password
    if mismatch:
        password = "first password"
        password_again = "this password does not match"

    actor = context.get_actor(supplier_alias)

    response = sso_ui_change_password.submit(
        actor, action, password=password, password_again=password_again
    )
    context.response = response


def sso_open_password_reset_link(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    session = actor.session
    link = actor.password_reset_link
    context.response = sso_ui_password_reset.open_link(session, link)


def go_to_page(context: Context, supplier_alias: str, page_name: str):
    actor = context.get_actor(supplier_alias)
    url = get_page_object(page_name).URL
    context.response = make_request(Method.GET, url, session=actor.session)


def go_to_pages(context: Context, actor_alias: str, table: Table):
    actor = context.get_actor(actor_alias)
    results = {}
    for row in table:
        page_name = row["page name"]
        url = get_page_object(page_name).URL
        response = make_request(Method.GET, url, session=actor.session)
        context.response = response
        results[page_name] = response

    context.results = results


def fab_select_preferred_countries_of_export(
    context: Context, supplier_alias: str, country_names, other_countries
):
    actor = context.get_actor(supplier_alias)
    country_codes = get_form_value(country_names)
    other = get_form_value(other_countries)
    sector = get_form_value("sector")
    has_exported_before = get_form_value("true or false")
    response = fab_ui_build_profile_sector.submit(
        actor, sector, country_codes, other, has_exported_before
    )
    context.response = response


def finish_registration_after_flagging_as_verified(
    context: Context, supplier_alias: str
):
    """Go to the `/register-submit` endpoint which, when Actor has a verified
     SSO account, should redirect to `company-profile/edit` (Create Profile)
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    register_url = get_absolute_url("ui-buyer:register-submit-account-details")
    url = "{}?company_number={}&has_exported_before=True".format(
        register_url, company.number
    )
    response = make_request(Method.GET, url, session=actor.session)
    context.response = response


def profile_add_collaborator(
    context: Context, supplier_alias: str, collaborator_aliases: str
):

    aliases = [alias.strip() for alias in collaborator_aliases.split(",")]

    for collaborator_alias in aliases:
        supplier = context.get_actor(supplier_alias)
        company = context.get_company(supplier.company_alias)
        collaborator = context.get_actor(collaborator_alias)
        response = fab_ui_account_add_collaborator.go_to(supplier.session)
        context.response = response

        fab_ui_account_add_collaborator.should_be_here(response)

        token = extract_csrf_middleware_token(response)
        context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

        response = fab_ui_account_add_collaborator.add_collaborator(
            supplier.session, token, collaborator.email
        )
        context.response = response

        profile_find_a_buyer.should_be_here(response, user_added=True)
        collaborators = company.collaborators
        if collaborators:
            collaborators.append(collaborator_alias)
        else:
            collaborators = [collaborator_alias]
        context.set_company_details(company.alias, collaborators=collaborators)


def fab_confirm_collaboration_request(
    context: Context,
    collaborator_alias: str,
    company_alias: str,
    open_invitation_link: bool = True,
):
    collaborator = context.get_actor(collaborator_alias)
    session = collaborator.session
    link = collaborator.invitation_for_collaboration_link

    # Step 1 - open confirmation link
    if open_invitation_link:
        response = fab_ui_confim_your_collaboration.open(session, link)
        context.response = response

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    fab_ui_confim_your_collaboration.should_be_here(context.response)
    logging.debug(
        "Collaborator %s is on the FAB Confirm your collaboration page",
        collaborator_alias,
    )

    # Step 4 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(context.response)
    context.update_actor(collaborator_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(context.response)
    context.form_action_value = form_action_value

    # Step 5 - submit the form
    response = fab_ui_confim_your_collaboration.confirm(session, token, link)
    context.response = response
    context.update_actor(collaborator_alias, company_alias=company_alias)
    logging.debug(
        "%s confirmed that he/she wants to be added to the profile for %s",
        collaborator_alias,
        company_alias,
    )


def fab_open_collaboration_request_link(
    context: Context, collaborator_alias: str, company_alias: str
):
    collaborator = context.get_actor(collaborator_alias)
    session = collaborator.session
    link = collaborator.invitation_for_collaboration_link

    response = fab_ui_confim_your_collaboration.open(session, link)
    context.response = response
    logging.debug(
        "%s opened the collaboration request link from company %s",
        collaborator_alias,
        company_alias,
    )


def reg_create_standalone_unverified_sso_account_from_sso_login_page(
    context: Context, actor_alias: str
):
    """Create a standalone SSO/great.gov.uk account."""
    actor = context.get_actor(actor_alias)
    response = context.response

    # Step 1: Check if we are on the SSO/great.gov.uk login page
    sso_ui_login.should_be_here(response)

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor_alias, csrfmiddlewaretoken=token)

    # Step 3 - extract Registration link
    referer = response.url
    registration_page_link = extract_registration_page_link(response)

    # Step 4: Go to the SSO/great.gov.uk registration page
    response = sso_ui_register.go_to(
        actor.session, next=registration_page_link, referer=referer
    )
    context.response = response

    # Step 5 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor_alias, csrfmiddlewaretoken=token)

    # Step 6: Check if User is not logged in
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 7: POST SSO accounts/signup/
    response = sso_ui_register.submit_no_company(
        actor, next=registration_page_link, referer=response.url
    )
    context.response = response

    # Step 8: Check if Supplier is on Verify your email page & is not logged in
    sso_ui_verify_your_email.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"


def sso_create_standalone_unverified_sso_account_from_collaboration_request(
        context: Context, actor_alias: str
):
    """Create a standalone SSO/great.gov.uk account."""
    actor = context.get_actor(actor_alias)
    next = actor.invitation_for_collaboration_link

    # Step 1: Go to the SSO/great.gov.uk registration page
    referer = get_absolute_url("sso:signup") + f"?next={next}"
    response = sso_ui_register.go_to(
        actor.session, next=next, referer=referer
    )
    context.response = response

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor_alias, csrfmiddlewaretoken=token)

    # Step 3: Check if User is not logged in
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 4: POST SSO accounts/signup/
    response = sso_ui_register.submit_no_company(
        actor, next=next, referer=referer
    )
    context.response = response

    # Step 8: Check if Supplier is on Verify your email page & is not logged in
    sso_ui_verify_your_email.should_be_here(response)
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"


def fab_collaborator_create_sso_account_and_confirm_email(
    context: Context, collaborator_alias: str, company_alias: str
):
    fab_open_collaboration_request_link(
        context, collaborator_alias, company_alias
    )
    sso_ui_login.should_be_here(context.response)
    sso_create_standalone_unverified_sso_account_from_collaboration_request(
        context, collaborator_alias
    )
    reg_should_get_verification_email(context, collaborator_alias)
    reg_open_email_confirmation_link(context, collaborator_alias)
    sso_collaborator_confirm_email_address(context, collaborator_alias)
    fab_confirm_collaboration_request(
        context, collaborator_alias, company_alias, open_invitation_link=False
    )


def fab_send_transfer_ownership_request(
    context: Context,
    supplier_alias: str,
    company_alias: str,
    new_owner_alias: str,
):
    """
    Due to bug ED-2268 the first time you visit SUD pages by going directly
    to SUD "Find a Buyer" page, then you're redirected to SUD "About" page
    To circumvent this behaviour we have to go to the "About" page first, and
    then visit the SUD "Find a Buyer" page
    """
    supplier = context.get_actor(supplier_alias)
    company = context.get_company(company_alias)
    new_owner = context.get_actor(new_owner_alias)

    context.response = profile_about.go_to(
        supplier.session, set_next_page=False
    )
    profile_about.should_be_here(context.response)

    response = fab_ui_account_transfer_ownership.go_to(supplier.session)
    context.response = response

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    response = fab_ui_account_transfer_ownership.submit(
        supplier.session, token, new_owner.email
    )
    context.response = response

    fab_ui_account_confrim_password.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    response = fab_ui_account_confrim_password.submit(
        supplier.session, token, supplier.password
    )
    context.response = response

    profile_find_a_buyer.should_be_here(response, owner_transferred=True)

    context.update_actor(supplier_alias, ex_owner=True)
    context.update_actor(new_owner_alias, company_alias=company_alias)
    context.set_company_details(
        company.alias, owner=new_owner_alias, owner_email=new_owner.email
    )
    logging.debug(
        "%s successfully sent a account ownership transfer request to %s %s",
        supplier_alias,
        new_owner_alias,
        new_owner.email,
    )


def fab_open_transfer_ownership_request_link_and_create_sso_account_if_needed(
    context: Context, new_owner_alias: str, company_alias: str
):
    new_owner = context.get_actor(new_owner_alias)
    session = new_owner.session
    link = new_owner.ownership_request_link

    response = fab_ui_confim_your_ownership.open(session, link)
    context.response = response
    if new_owner.has_sso_account:
        fab_ui_confim_your_ownership.should_be_here(response)
    else:
        reg_create_standalone_unverified_sso_account_from_sso_login_page(
            context, new_owner_alias
        )
        reg_should_get_verification_email(context, new_owner_alias)
        reg_open_email_confirmation_link(context, new_owner_alias)
        sso_new_onwer_confirm_email_address(context, new_owner_alias)
    logging.debug(
        "%s opened the transfer ownership request link from company %s",
        new_owner_alias,
        company_alias,
    )


def fab_confirm_account_ownership_request(
    context: Context, new_owner_alias: str, company_alias: str
):
    new_owner = context.get_actor(new_owner_alias)
    session = new_owner.session
    link = new_owner.ownership_request_link

    # Step 1 - confirm that Supplier is on SSO Confirm Your Email page
    fab_ui_confim_your_ownership.should_be_here(context.response)
    logging.debug(
        "New Owner %s is on the FAB Confirm your request for ownership page",
        new_owner_alias,
    )

    # Step 2 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(context.response)
    context.update_actor(new_owner_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(context.response)
    context.form_action_value = form_action_value

    # Step 3 - submit the form
    response = fab_ui_confim_your_ownership.confirm(session, token, link)
    context.response = response

    profile_edit_company_profile.should_be_here(response)

    context.update_actor(new_owner_alias, company_alias=company_alias)
    logging.debug(
        "%s confirmed that he/she wants to be added to the profile for %s",
        new_owner_alias,
        company_alias,
    )


def fab_transfer_ownership(
    context: Context,
    supplier_alias: str,
    company_alias: str,
    new_owner_alias: str,
):
    fab_send_transfer_ownership_request(
        context, supplier_alias, company_alias, new_owner_alias
    )
    fab_should_get_request_for_becoming_owner(
        context, new_owner_alias, company_alias
    )
    fab_open_transfer_ownership_request_link_and_create_sso_account_if_needed(
        context, new_owner_alias, company_alias
    )
    fab_confirm_account_ownership_request(
        context, new_owner_alias, company_alias
    )


def fab_remove_collaborators(
    context: Context,
    supplier_alias: str,
    collaborators_aliases: str,
    company_alias: str,
):
    aliases = [alias.strip() for alias in collaborators_aliases.split(",")]
    emails = [context.get_actor(alias).email for alias in aliases]
    supplier = context.get_actor(supplier_alias)
    company = context.get_company(company_alias)

    # Step 1: go to the remove collaborators page
    response = fab_ui_account_remove_collaborator.go_to(supplier.session)
    context.response = response

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 2: extract SSO IDs for users to remove
    emails_to_sso_id = fab_ui_account_remove_collaborator.extract_sso_ids(
        response
    )
    logging.debug("SSO IDs for specific actor: %s", emails_to_sso_id)
    sso_ids = [
        sso_id for email, sso_id in emails_to_sso_id.items() if email in emails
    ]
    logging.debug("List of SSO IDs to remove: %s", sso_ids)

    # Step 3: send the request with SSO IDs of users to remove
    response = fab_ui_account_remove_collaborator.remove(
        supplier.session, token, sso_ids
    )
    context.response = response

    profile_find_a_buyer.should_be_here(response, user_removed=True)
    collaborators = company.collaborators
    collaborators = [alias for alias in collaborators if alias not in aliases]
    context.set_company_details(company.alias, collaborators=collaborators)


def stannp_download_verification_letter_and_extract_text(
    context: Context, actor_alias: str
):
    with assertion_msg(
        "context.response does not contain response from StanNP!"
    ):
        assert "data" in context.response

    pdf_link = context.response["data"]["pdf"]
    pdf_path = get_pdf_from_stannp(pdf_link)
    pdf_text = extract_text_from_pdf(pdf_path)

    try:
        os.remove(pdf_path)
    except OSError:
        logging.error(
            "Something went wrong when trying to delete: %s", pdf_path)
    context.update_actor(actor_alias, verification_letter=pdf_text)


def enrol_enter_email_and_password(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    logging.debug("# 1) Go to Enter your email & password")
    response = profile_enter_your_email_and_password.go_to(actor.session)
    context.response = response
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor.alias, csrfmiddlewaretoken=token)

    logging.debug("# 2) submit the form")
    response = profile_enter_your_email_and_password.submit(actor)
    context.response = response
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor.alias, csrfmiddlewaretoken=token)
    profile_enter_email_verification_code.should_be_here(response)


def enrol_get_email_verification_code(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    logging.debug("# 3) get email verification code")
    code = get_email_verification_code(actor.email)
    assert code, f"Could not find email verification code for {actor.email}"
    context.update_actor(actor.alias, email_confirmation_code=code)


def enrol_enter_email_verification_code(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    logging.debug("# 4) submit email verification code")
    response = profile_enter_email_verification_code.submit(actor)
    context.response = response
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor.alias, csrfmiddlewaretoken=token)
    profile_enter_your_business_details.should_be_here(response)


def retry_if_assertion_error(exception):
    """Return True if we should retry on AssertionError, False otherwise"""
    return isinstance(exception, AssertionError)


def check_if_found_wrong_company(context: Context, actor_alias: str, company_alias: str):
    content = context.response.content.decode("UTF-8")
    actor = context.get_actor(actor_alias)
    company = context.get_company(company_alias)
    errors = {
        "Company not active":
            f"Found wrong company '{company.number} - {company.title}' is inactive",
        "74990":
            f"Found wrong company '{company.number} - {company.title}' has SIC=74990",
        "88100":
            f"Found wrong company '{company.number} - {company.title}' has SIC=88100",
    }
    for string, error in errors.items():
        if string in content:
            with assertion_msg(error):
                logging.debug(error)
                token = extract_csrf_middleware_token(context.response)
                context.update_actor(actor.alias, csrfmiddlewaretoken=token)
                find_unregistered_company(context, actor.alias, company.alias)
                assert string not in content


@retry(
    wait_fixed=500,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_assertion_error,
    wrap_exception=False,
)
def enrol_enter_company_name(context: Context, actor_alias: str, company_alias: str):
    actor = context.get_actor(actor_alias)
    company = context.get_company(company_alias)
    logging.debug("# 5) submit company details - 1st part")
    response = profile_enter_your_business_details.submit(actor, company)
    context.response = response

    check_if_found_wrong_company(context, actor_alias, company_alias)

    token = extract_csrf_middleware_token(response)
    context.update_actor(actor.alias, csrfmiddlewaretoken=token)
    profile_enter_your_business_details_part_2.should_be_here(response)


def enrol_enter_company_website_and_industry(context: Context, actor_alias: str, company_alias: str):
    actor = context.get_actor(actor_alias)
    company = context.get_company(company_alias)
    logging.debug("# 6) submit company details - 2nd part")
    if not company.website:
        words = ".".join(sentence().split())
        context.set_company_details(company.alias, website=f"https://{words}/")
    if not company.sector:
        industry, _ = random.choice(choices.INDUSTRIES)
        context.set_company_details(company.alias, sector=industry)
    if not company.no_employees:
        size = random.choice(NO_OF_EMPLOYEES)
        context.set_company_details(company.alias, no_employees=size)
    company = context.get_company(company.alias)
    response = profile_enter_your_business_details_part_2.submit(actor, company)
    context.response = response
    token = extract_csrf_middleware_token(response)
    context.update_actor(actor.alias, csrfmiddlewaretoken=token)
    profile_enter_your_personal_details.should_be_here(response)


def enrol_enter_personal_details(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    logging.debug("# 7) submit personal details")
    response = profile_enter_your_personal_details.submit(actor)
    context.response = response
    profile_enrolment_finished.should_be_here(response)


def enrol_user(context: Context, actor_alias: str, company_alias: str):
    enrol_enter_email_and_password(context, actor_alias)
    enrol_get_email_verification_code(context, actor_alias)
    enrol_enter_email_verification_code(context, actor_alias)
    enrol_enter_company_name(context, actor_alias, company_alias)
    enrol_enter_company_website_and_industry(context, actor_alias, company_alias)
    enrol_enter_personal_details(context, actor_alias)

    actor = context.get_actor(actor_alias)
    company = context.get_company(company_alias)
    logging.debug(
        f"'{actor.alias}' created an unverified Business Profile for "
        f"'{company.title} - {company.number}'"
    )
