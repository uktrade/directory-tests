# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random
import re
import uuid
from random import choice, randrange
from string import ascii_letters, digits
from typing import Tuple
from urllib.parse import parse_qsl, quote, urljoin, urlsplit

from behave.model import Table
from behave.runner import Context
from requests import Response, Session
from retrying import retry
from scrapy import Selector

from directory_constants import choices
from directory_constants.expertise import (
    BUSINESS_SUPPORT,
    FINANCIAL,
    HUMAN_RESOURCES,
    LEGAL,
    MANAGEMENT_CONSULTING,
    PUBLICITY,
)
from directory_tests_shared import URLs
from directory_tests_shared.constants import SECTORS, SEPARATORS, BMPs, JP2s, WEBPs
from directory_tests_shared.enums import Account, BusinessType, Language
from directory_tests_shared.gov_notify import get_email_verification_code
from directory_tests_shared.settings import TEST_EMAIL_DOMAIN
from directory_tests_shared.utils import check_for_errors, rare_word, sentence
from tests.functional.common import DETAILS, PROFILES
from tests.functional.pages import (
    fab,
    fas,
    get_page_object,
    has_action,
    isd,
    profile,
    sso,
)
from tests.functional.steps.common import can_find_supplier_by_term
from tests.functional.steps.then_impl import (
    profile_should_get_request_for_becoming_owner,
    reg_should_get_verification_email,
    sso_should_be_told_about_password_reset,
    sso_should_get_password_reset_email,
)
from tests.functional.utils.context_utils import (
    Actor,
    Company,
    add_actor,
    add_case_study,
    add_company,
    get_actor,
    get_company,
    set_company_logo_detail,
    update_actor,
    update_case_study,
    update_company,
)
from tests.functional.utils.generic import (
    assert_that_captcha_is_in_dev_mode,
    assertion_msg,
    create_test_isd_company,
    escape_html,
    extract_and_set_csrf_middleware_token,
    extract_csrf_middleware_token,
    extract_form_action,
    extract_logo_url,
    filter_out_legacy_industries,
    get_absolute_path_of_file,
    get_company_by_id_or_title,
    get_md5_hash_of_file,
    get_number_of_search_result_pages,
    get_published_companies,
    get_published_companies_with_n_sectors,
    get_verification_code,
    is_verification_letter_sent,
    random_case_study_data,
    random_chars,
    random_feedback_data,
    random_message_data,
    verify_non_ch_company,
)
from tests.functional.utils.request import Method, check_response, make_request

INDUSTRIES_FOR_PRODUCTS_AND_SERVICES = {
    "financial": FINANCIAL,
    "management-consulting": MANAGEMENT_CONSULTING,
    "human-resources": HUMAN_RESOURCES,
    "legal": LEGAL,
    "publicity-and-communication": PUBLICITY,
    "business-support": BUSINESS_SUPPORT,
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
        f"test+{supplier_alias}{str(uuid.uuid4())}@{TEST_EMAIL_DOMAIN}".replace("-", "")
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
        f"test+buyer_{buyer_alias}{str(uuid.uuid4())}@{TEST_EMAIL_DOMAIN}".replace(
            "-", ""
        )
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


def go_to_page(context: Context, supplier_alias: str, page_name: str):
    actor = get_actor(context, supplier_alias)
    page = get_page_object(page_name)
    has_action(page, "go_to")

    if hasattr(page, "SUB_URLs"):
        page_name = page_name.split(" - ")[1]
        specific_url = page.SUB_URLs[page_name.lower()]
        logging.debug(
            f"{supplier_alias} will visit '{page_name}' using page specific URL"
            f": {specific_url} not the general one: {page.URL}"
        )
        response = page.go_to(actor.session, page_name=page_name)
    else:
        response = page.go_to(actor.session)

    context.response = response


@retry(wait_fixed=2000, stop_max_attempt_number=5)
def fas_find_company_by_name(context: Context, buyer_alias: str, company_alias: str):
    buyer = get_actor(context, buyer_alias)
    session = buyer.session
    company = get_company(context, company_alias)
    profile_link, context.response = can_find_supplier_by_term(
        session=session,
        company_title=company.title,
        term=company.title,
        term_type="company title",
    )
    with assertion_msg(
        f"{buyer_alias} could not find FAS company '{company.title}' using its title"
    ):
        assert profile_link
    update_company(context, company_alias, fas_profile_endpoint=profile_link)


@retry(wait_fixed=3000, stop_max_attempt_number=5)
def fab_find_published_company(
    context: Context,
    actor_alias: str,
    company_alias: str,
    *,
    min_number_sectors: int = None,
):
    if min_number_sectors:
        companies = get_published_companies_with_n_sectors(context, min_number_sectors)
    else:
        companies = get_published_companies(context)

    with assertion_msg("Expected to find at least 1 published company but got none!"):
        assert len(companies) > 0
    filtered_companies = [
        c for c in companies if f"@{TEST_EMAIL_DOMAIN}" not in c["company_email"]
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
    update_actor(context, actor_alias, company_alias=company_alias)
    add_company(context, company)
    logging.debug("%s found a published company: %s", actor_alias, company)


def fas_get_company_slug(context: Context, actor_alias: str, company_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session
    company = get_company(context, company_alias)
    response = fas.profile.go_to(session, company_number=company.number)
    context.response = response
    fas.profile.should_be_here(response)
    url = response.request.url
    last_item_idx = -1
    slash_idx = 1
    slug = urlsplit(url).path.split(company.number)[last_item_idx][
        slash_idx:last_item_idx
    ]
    logging.debug(f"{actor_alias} got company's slug: {slug}")
    update_company(context, company_alias, slug=slug)


def reg_should_get_verification_letter(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    sent = is_verification_letter_sent(context, company.number)

    with assertion_msg("Verification letter wasn't sent"):
        assert sent

    verification_code = get_verification_code(context, company.number)
    update_company(context, company.alias, verification_code=verification_code)

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
            actor = get_actor(context, actor_alias)
            account = Account("verified Individual")
            profile_enrol_individual(context, actor, account=account)
        else:
            supplier = unauthenticated_supplier(actor_alias)
            add_actor(context, supplier)


def reg_create_sso_account(context: Context, supplier_alias: str, company_alias: str):
    """Will create a SSO account for selected company.

    NOTE:
    Will use credentials randomly generated at Actor's initialization.
    It will also store final response in `context`
    """
    actor = get_actor(context, supplier_alias)
    company = get_company(context, company_alias)

    logging.debug(
        "Submit SSO Registration form with Supplier's & Company's required details"
    )
    context.response = sso.register.submit(actor, company)


def reg_open_email_confirmation_link(context: Context, supplier_alias: str):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.
    """
    actor = get_actor(context, supplier_alias)
    session = actor.session
    link = actor.email_confirmation_link

    # Step 1 - open confirmation link
    response = sso.confirm_your_email.open_confirmation_link(session, link)
    context.response = response

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    sso.confirm_your_email.should_be_here(response)
    logging.debug("Supplier is on the SSO Confirm your email address page")

    # Step 4 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(response)
    context.form_action_value = form_action_value


def reg_supplier_confirms_email_address(context: Context, supplier_alias: str):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.
    """
    actor = get_actor(context, supplier_alias)
    form_action_value = context.form_action_value

    response = sso.confirm_your_email.confirm(actor, form_action_value)
    context.response = response


def fab_decide_to_verify_profile_with_letter(context: Context, supplier_alias: str):
    """Build Profile - verify identity with a physical letter."""
    actor = get_actor(context, supplier_alias)

    # Step 1 - go to page where you choose to verify with a letter
    response = fab.confirm_identity_letter.go_to(actor.session)
    context.response = response
    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    # Step 2 - Choose to verify with a letter
    context.response = fab.confirm_identity_letter.submit(actor)

    # Step 2 - check if Supplier is on the We've sent you a verification letter
    fab.confirm_identity_letter.should_be_here(context.response)
    logging.debug("Supplier is on the 'Your company address' letter verification page")


def profile_add_business_description(
    context: Context, supplier_alias: str, *, ch_company: bool = True
):
    """Edit Profile - Will set company description.

    This is quasi-mandatory (*) step before Supplier can verify the company
    with the code sent in a letter.

    (*) it's quasi mandatory, because Supplier can actually go to the company
    verification page using the link provided in the letter without the need
    to set company description.
    """
    actor = get_actor(context, supplier_alias)
    session = actor.session

    # Step 1 - Submit company description
    summary = sentence()
    description = sentence()
    response = profile.edit_company_description.submit(session, summary, description)
    context.response = response

    # Step 3 - check if Supplier is on Profile page
    profile.edit_company_profile.should_see_profile_is_not_verified(
        response, ch_company=ch_company
    )

    # Step 4 - update company details in Scenario Data
    update_company(
        context, actor.company_alias, summary=summary, description=description
    )
    logging.debug("Supplier is back to the Profile Page")


def profile_verify_company_profile(context: Context, supplier_alias: str):
    """Will verify the company by submitting the verification code that is sent
    by post to the company's address.
    """
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    session = actor.session

    # STEP 0 - get the verification code from DB
    verification_code = get_verification_code(context, company.number)
    update_company(context, company.alias, verification_code=verification_code)

    # STEP 1 - go to the "Verify your company" page
    context.response = fab.verify_company.go_to(session)

    # STEP 2 - extract CSRF token
    token = extract_csrf_middleware_token(context.response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    # STEP 3 - Submit the verification code
    context.response = fab.verify_company.submit(session, token, verification_code)

    # STEP 4 - check if code was accepted
    fab.verify_company.should_see_company_is_verified(context.response)

    # STEP 5 - click on the "View or amend your company profile" link
    context.response = profile.edit_company_profile.go_to(session)

    # STEP 6 - check if Supplier is on Verified Profile Page
    profile.edit_company_profile.should_see_profile_is_verified(context.response)


def profile_publish_profile_to_fas(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    context.response = profile.publish_company_profile.submit(actor.session)
    profile.edit_company_profile.should_see_profile_is_published(context.response)


def profile_unpublish_profile_from_fas(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    context.response = profile.publish_company_profile.submit(
        actor.session, unpublish=True
    )
    profile.edit_company_profile.should_see_profile_is_verified(context.response)


@retry(wait_fixed=3000, stop_max_attempt_number=3)
def profile_view_published_profile(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    session = actor.session
    company = get_company(context, actor.company_alias)
    context.response = fas.profile.go_to(session, company.number)
    fas.profile.should_be_here(context.response)
    logging.debug("Supplier is on the company's FAS page")


def profile_view_unpublished_profile(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    context.response = fas.profile.go_to(actor.session, company.number)


def prof_attempt_to_sign_in_to_sso(context: Context, supplier_alias: str):
    """Try to sign in to FAB as a Supplier without verified email address."""
    actor = get_actor(context, supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign In page
    response = sso.login.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on SSO Login page & extract CSRF token
    sso.login.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"
    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - submit the login form
    context.response = sso.login.login(actor)


def sso_collaborator_confirm_email_address(context: Context, supplier_alias: str):
    """Given that invited collaborator has clicked on the email confirmation
     link, he/she has to confirm that the provided email address is the
      correct one.
    """
    actor = get_actor(context, supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso.confirm_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if Supplier if on SSO Profile Landing page
    profile.confirm_your_collaboration.should_be_here(response)

    # STEP 3 - Update Actor's data
    update_actor(context, supplier_alias, has_sso_account=True)


def sso_new_owner_confirm_email_address(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso.confirm_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if new account owner is on the correct page
    fab.confirm_your_ownership.should_be_here(response)

    # STEP 3 - Update Actor's data
    update_actor(context, supplier_alias, has_sso_account=True)


def sso_supplier_confirms_email_address(context: Context, supplier_alias: str):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.
    """
    actor = get_actor(context, supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso.confirm_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if Supplier if on SSO Profile Landing page
    profile.about.should_be_here(response)

    # STEP 3 - Update Actor's data
    update_actor(context, supplier_alias, has_sso_account=True)


def profile_upload_unsupported_file_as_logo(
    context: Context, supplier_alias: str, file: str
) -> bool:
    """Try to upload unsupported file type as Company's logo.

    NOTE:
    file must exist in ./tests/functional/files

    :param file: name of the file stored in ./tests/functional/files
    """
    actor = get_actor(context, supplier_alias)
    session = actor.session
    file_path = get_absolute_path_of_file(file)

    logging.debug("Attempting to upload %s as company logo", file)
    # Step 1 - Try to upload a file of unsupported type as company's logo
    response = profile.upload_logo.upload(session, file_path)
    context.response = response

    # Step 2 - check if upload was rejected
    rejected = profile.upload_logo.was_upload_rejected(response)

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


def profile_supplier_uploads_logo(context: Context, supplier_alias: str, picture: str):
    """Upload a picture and set it as Company's logo.

    :param picture: name of the picture file stored in ./tests/files
    """
    actor = get_actor(context, supplier_alias)
    session = actor.session
    file_path = get_absolute_path_of_file(picture)

    # Step 1 - upload the logo
    response = profile.upload_logo.upload(session, file_path)
    context.response = response

    # Step 2 - check if Supplier is on the FAB profile page
    profile.edit_company_profile.should_be_here(response)
    logging.debug("Successfully uploaded logo picture: %s", picture)

    # Step 3 - Keep logo details in Company's scenario data
    logo_url = extract_logo_url(response)
    md5_hash = get_md5_hash_of_file(file_path)
    set_company_logo_detail(
        context, actor.company_alias, picture=picture, hash=md5_hash, url=logo_url
    )


def profile_update_company_details(
    context: Context, supplier_alias: str, table_of_details: Table
):
    """Update selected Company's details."""
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)

    # Step 0 - prepare company's details to update
    details_to_update = [row["detail"] for row in table_of_details]
    change_name = DETAILS["NAME"] in details_to_update
    change_website = DETAILS["WEBSITE"] in details_to_update
    change_size = DETAILS["SIZE"] in details_to_update
    change_sector = DETAILS["SECTOR"] in details_to_update
    change_keywords = DETAILS["KEYWORDS"] in details_to_update
    change_other_keywords = DETAILS["OTHER_KEYWORDS"] in details_to_update
    if change_other_keywords:
        change_keywords = True

    # Step 1 - Update company's details
    if any([change_name, change_website, change_size, change_sector]):
        response, new_details = profile.edit_company_business_details.submit(
            actor,
            company,
            change_name=change_name,
            change_website=change_website,
            change_size=change_size,
            change_sector=change_sector,
        )
        context.response = response

        # Step 2 - Supplier should be on Edit Profile page
        profile.edit_company_profile.should_be_here(response)

        # Step 3 - update company's details stored in context.scenario_data
        update_company(
            context,
            actor.company_alias,
            title=new_details.title,
            website=new_details.website,
            no_employees=new_details.no_employees,
            sector=new_details.sector,
        )

    # Step 3 - Go to the Edit Sector page
    industries = INDUSTRIES_FOR_PRODUCTS_AND_SERVICES
    if change_keywords:
        if change_other_keywords:
            industry = "other"
        else:
            industry = random.choice(list(industries.keys()))
        response = profile.edit_products_and_services_industry.submit(
            actor.session, industry=industry
        )
        context.response = response
        profile.edit_products_and_services_keywords.should_be_here(
            response, industry=industry
        )

        number_of_keywords = random.randint(1, len(industries[industry]))
        keywords = list(
            set(random.choice(industries[industry]) for _ in range(number_of_keywords))
        )
        response = profile.edit_products_and_services_keywords.submit(
            actor.session,
            industry=industry,
            keywords=keywords,
            separator="," if change_other_keywords else "|",
        )
        context.response = response

        # Step 3 - Check if Supplier is back on the "Add products and services" page
        profile.edit_products_and_services_industry.should_be_here(response)

        # Step 4 - update company's details stored in context.scenario_data
        update_company(
            context,
            actor.company_alias,
            industry=industry,
            keywords=", ".join(keywords),
        )


def profile_add_online_profiles(
    context: Context, supplier_alias: str, online_profiles: Table
):
    """Update links to Company's Online Profiles."""
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    profiles = [row["online profile"] for row in online_profiles]
    facebook = PROFILES["FACEBOOK"] in profiles
    linkedin = PROFILES["LINKEDIN"] in profiles
    twitter = PROFILES["TWITTER"] in profiles

    # Step 1 - Update links to Online Profiles
    response, new_details = profile.edit_online_profiles.update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )
    context.response = response

    # Step 2 - Check if Supplier is on FAB Profile page
    profile.edit_company_profile.should_be_here(response)

    # Step 3 - Update company's details stored in context.scenario_data
    update_company(
        context,
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
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
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
    response, _ = profile.edit_online_profiles.update_profiles(
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


def profile_remove_links_to_online_profiles(context: Context, supplier_alias: str):
    """Will remove links to existing Online Profiles."""
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    context.response = profile.edit_online_profiles.remove_links(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )

    # Update company's details stored in context.scenario_data
    update_company(context, company.alias, facebook=None, linkedin=None, twitter=None)


def profile_add_case_study(context: Context, supplier_alias: str, case_alias: str):
    """Will add a complete case study (all fields will be filled out)."""
    actor = get_actor(context, supplier_alias)
    session = actor.session
    case_study = random_case_study_data(case_alias)

    # Step 1 - go to "Add case study" form & extract CSRF token
    response = profile.case_study_basic.go_to(session)
    context.response = response
    profile.case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 2 - submit the "basic case study data" form & extract CSRF token
    response = profile.case_study_basic.submit(session, token, case_study)
    context.response = response
    profile.case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "case study images" form
    response = profile.case_study_images.submit(session, token, case_study)
    context.response = response

    # Step 4 - check if we're on the FAB Profile page
    profile.edit_company_profile.should_be_here(response)

    # Step 5 - Store Case Study data in Scenario Data
    add_case_study(context, actor.company_alias, case_alias, case_study)


def profile_update_case_study(context: Context, supplier_alias: str, case_alias: str):
    actor = get_actor(context, supplier_alias)
    session = actor.session
    company = get_company(context, actor.company_alias)
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
    logging.debug("Extracted link for case study: %s is: %s", case_alias, current_link)

    # Step 1 - generate new case study data
    new_case = random_case_study_data(case_alias)
    logging.debug("Now will replace case study data with: %s", new_case)

    # Step 2 - go to specific "Case study" page form & extract CSRF token
    response = profile.case_study_basic.go_to(session, case_number=current_number)
    context.response = response
    profile.case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "basic case study data" form & extract CSRF token
    response = profile.case_study_basic.submit(session, token, new_case)
    context.response = response
    profile.case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 4 - submit the "case study images" form
    response = profile.case_study_images.submit(session, token, new_case)
    context.response = response

    # Step 5 - check if we're on the FAB Profile page
    profile.edit_company_profile.should_be_here(response)

    # Step 5 - Store new Case Study data in Scenario Data
    # `add_case_study` apart from adding will replace existing case study.
    add_case_study(context, actor.company_alias, case_alias, new_case)
    logging.debug(
        "Successfully updated details of case study: '%s', title:'%s', link:" "'%s'",
        case_alias,
        current.title,
        current_link,
    )


def fas_search_using_company_details(
    context: Context,
    buyer_alias: str,
    company_alias: str,
    *,
    table_of_details: Table = None,
):
    """Search for Company on FAS using it's all or selected details."""
    actor = get_actor(context, buyer_alias)
    session = actor.session
    company = get_company(context, company_alias)
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
        profile_link, response = can_find_supplier_by_term(
            session, company.title, term, term_name
        )
        found = profile_link != ""
        search_results[term_name] = found
        search_responses[term_name] = response
        if found:
            continue

    context.search_results = search_results
    context.search_responses = search_responses


@retry(wait_fixed=2000, stop_max_attempt_number=5)
def generic_view_pages_in_selected_language(
    context: Context,
    buyer_alias: str,
    pages_table: Table,
    language: str,
    language_argument: str = "lang",
):
    """View specific FAS pages in selected language.

    NOTE:
    This will store a dict with all page views responses in context.views
    """
    language_code = Language[language.upper()].value
    pages = [row["page"] for row in pages_table]
    views = {}
    actor = get_actor(context, buyer_alias)
    session = actor.session
    for page_name in pages:
        page = get_page_object(page_name)
        if hasattr(page, "SUB_URLs"):
            name = page_name.split(" - ")[1]
            page_url = page.SUB_URLs[name.lower()]
        else:
            page_url = get_page_object(page_name).URL
        page_url += f"?{language_argument}={language_code}"
        response = make_request(Method.GET, page_url, session=session)
        views[page_name] = response
    context.views = views


def fas_search_with_empty_query(context: Context, buyer_alias: str):
    actor = get_actor(context, buyer_alias)
    session = actor.session
    context.response = fas.search.go_to(session, term="")
    fas.search.should_be_here(context.response)


def fas_should_be_told_about_empty_search_results(context: Context, buyer_alias: str):
    fas.search.should_see_no_matches(context.response)
    logging.debug(
        "%s was told that the search did not match any UK trade profiles", buyer_alias
    )


def fas_should_be_told_to_enter_search_term_or_use_filters(
    context: Context, buyer_alias: str
):
    fas.search.should_see_no_results(context.response)
    logging.debug("%s was told to use a search term or use the filters", buyer_alias)


def fas_send_feedback_request(context: Context, buyer_alias: str, page_name: str):
    actor = get_actor(context, buyer_alias)
    # Step 0: get csrf token
    context.response = fas.feedback.go_to(actor.session)
    assert_that_captcha_is_in_dev_mode(context.response)
    token = extract_csrf_middleware_token(context.response)
    update_actor(context, buyer_alias, csrfmiddlewaretoken=token)

    actor = get_actor(context, buyer_alias)
    referer_url = get_page_object(page_name).URL
    # Step 1: generate random form data for our Buyer
    feedback = random_feedback_data(email=actor.email)

    # Step 2: submit the form
    context.response = fas.feedback.submit(actor, feedback, referer=referer_url)
    logging.debug("%s submitted the feedback request", buyer_alias)


def fas_feedback_request_should_be_submitted(context: Context, buyer_alias: str):
    response = context.response
    fas.feedback.should_see_feedback_submission_confirmation(response)
    logging.debug(
        "%s was told that the feedback request has been submitted", buyer_alias
    )


def fas_get_company_profile_url(response: Response, name: str) -> str:
    content = response.content.decode("utf-8")
    links_to_profiles_selector = "#companies-column > ul > li > a"
    href_selector = "a::attr(href)"
    links_to_profiles = Selector(text=content).css(links_to_profiles_selector).extract()
    profile_url = None
    clean_name = escape_html(name.replace("  ", " ")).lower()
    for link in links_to_profiles:
        # try to find Profile URL by escaping html chars or not in found link
        if (clean_name in link.lower()) or (clean_name in escape_html(link).lower()):
            profile_url = Selector(text=link).css(href_selector).extract()[0]
    with assertion_msg(
        f"Couldn't find link to '{name}' company profile page on {response.url}"
    ):
        assert profile_url
    logging.debug(f"Found link to '{name}'s profile: {profile_url}")
    return profile_url


def fas_search_with_product_service_keyword(
    context: Context, buyer_alias: str, search_table: Table
):
    """Search for Suppliers with one of the following:
    * Product name
    * Service name
    * keyword

    NOTE: this will add a dictionary `search_results` to `context`
    """
    actor = get_actor(context, buyer_alias)
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
            profile_link, response = can_find_supplier_by_term(
                session, company, term, term_type
            )
            found = profile_link != ""
            search_term["found"] = found
            search_term["response"] = response

    context.search_results = search_results


def fas_send_message_to_supplier(
    context: Context, buyer_alias: str, company_alias: str
):
    buyer = get_actor(context, buyer_alias)
    session = buyer.session
    company = get_company(context, company_alias)
    endpoint = company.fas_profile_endpoint
    with assertion_msg("Company '%s' doesn't have FAS profile URL set", company.title):
        assert endpoint
    # Step 0 - generate message data
    message = random_message_data(
        family_name=buyer.alias,
        given_name="AUTOMATED TESTS",
        company_name=buyer.company_alias,
        email_address=buyer.email,
        subject="CONTACT SUPPLIER - AUTOMATED TESTS",
    )

    # Step 1 - go to Company's profile page
    context.response = fas.profile.go_to_endpoint(session, endpoint)
    fas.profile.should_be_here(context.response, number=company.number)

    # Step 2 - go to the "email company" form
    context.response = fas.contact.go_to(session, company_number=company.number)
    fas.contact.should_be_here(context.response)
    assert_that_captcha_is_in_dev_mode(context.response)

    # Step 3 - submit the form with the message data
    context.response = fas.contact.submit(session, message, company.number)


def profile_provide_business_details(
    context: Context, supplier_alias: str, table: Table
):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
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
                int(word) for word in row["trading name"].split() if word.isdigit()
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
            new_website = f"http://{rare_word()}.{rare_word()}"
            change_website = True
        elif row["website"] == "valid https":
            new_website = f"https://{rare_word()}.{rare_word()}"
            change_website = True
        elif row["website"] == "invalid http":
            new_website = "http"
            change_website = True
        elif row["website"] == "invalid https":
            new_website = "https"
            change_website = True
        elif row["website"].endswith(" characters"):
            number = [int(word) for word in row["website"].split() if word.isdigit()][0]
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
            title=new_name,
            website=new_website,
            no_employees=new_size,
            sector=new_sector,
        )

        logging.debug(f"Details to update: {modified_details}")
        response, new_details = profile.edit_company_business_details.submit(
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

        if row["error"] == "no error":
            # update company's details if no error was expected
            update_company(
                context,
                actor.company_alias,
                title=new_details.title,
                website=new_details.website,
                no_employees=new_details.no_employees,
                sector=new_details.sector,
            )

    context.results = results


def profile_provide_products_and_services(
    context: Context, supplier_alias: str, table: Table
):
    actor = get_actor(context, supplier_alias)
    results = []
    industries = INDUSTRIES_FOR_PRODUCTS_AND_SERVICES
    for row in table:
        send_as_files = True
        send_as_data = False
        industry = random.choice(list(industries.keys()))
        response = profile.edit_products_and_services_industry.submit(
            actor.session, industry=industry
        )
        context.response = response
        profile.edit_products_and_services_keywords.should_be_here(
            response, industry=industry
        )

        separator = "|"
        if row["keywords"] == "empty string":
            keywords = [""]
        elif row["keywords"].endswith(" characters"):
            number = [int(word) for word in row["keywords"].split() if word.isdigit()][
                0
            ]
            keywords = [random_chars(number)]
            send_as_files = False
            send_as_data = True
        else:
            keywords = row["keywords"]
            keywords = keywords.split(", ")
            if row["separator"] == "pipe":
                separator = "|"
            elif row["separator"] == "semi-colon":
                separator = ";"
            elif row["separator"] == "colon":
                separator = ":"
            elif row["separator"] == "full stop":
                separator = "."

        modified_details = Company(keywords=keywords)
        logging.debug(
            f"Add products & services keywords: '{keywords}' to '{industry}' "
            f"using '{separator}' as separator"
        )
        response = profile.edit_products_and_services_keywords.submit(
            actor.session,
            industry=industry,
            keywords=keywords,
            separator=separator,
            send_as_data=send_as_data,
            send_as_files=send_as_files,
        )
        results.append((modified_details, response, row["error"]))

    context.results = results


def fas_follow_case_study_links_to_related_sectors(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
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
    fas_url = URLs.FAS_LANDING.absolute
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
        results[industry] = {"url": url, "sectors": sectors, "response": response}
    context.results = results


def fas_browse_suppliers_using_every_sector_filter(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session

    response = fas.search.go_to(session, term="")
    context.response = response
    fas.search.should_be_here(response)

    sector_filters_selector = "#checkbox-industry-expertise input::attr(value)"
    content = response.content.decode("utf-8")
    sector_filters = Selector(text=content).css(sector_filters_selector).extract()
    results = {}
    for sector in sector_filters:
        logging.debug(
            "%s will browse Suppliers by Industry sector filter '%s'",
            actor_alias,
            sector,
        )
        response = fas.search.go_to(session, sectors=[sector])
        fas.search.should_be_here(response)
        results[sector] = {
            "url": response.request.url,
            "sectors": [sector],
            "response": response,
        }
    context.results = results


def fas_browse_suppliers_by_multiple_sectors(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session

    response = fas.search.go_to(session, term="")
    context.response = response
    fas.search.should_be_here(response)

    sector_selector = "#checkbox-industry-expertise input::attr(value)"
    content = response.content.decode("utf-8")
    filters = Selector(text=content).css(sector_selector).extract()

    sectors = list(set(choice(filters) for _ in range(randrange(1, len(filters)))))
    results = {}
    logging.debug(
        "%s will browse Suppliers by multiple Industry sector filters '%s'",
        actor_alias,
        ", ".join(sectors),
    )
    response = fas.search.go_to(session, sectors=sectors)
    fas.search.should_be_here(response)
    results["multiple choice"] = {
        "url": response.request.url,
        "sectors": sectors,
        "response": response,
    }
    context.results = results


def fas_browse_suppliers_by_invalid_sectors(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session

    response = fas.search.go_to(session, term="")
    context.response = response
    fas.search.should_be_here(response)

    sector_selector = "#checkbox-industry-expertise input::attr(value)"
    content = response.content.decode("utf-8")
    filters = Selector(text=content).css(sector_selector).extract()

    sectors = list(set(choice(filters) for _ in range(randrange(1, len(filters)))))

    sectors.append("this_is_an_invalid_sector_filter")
    logging.debug(
        "%s will browse Suppliers by multiple Industry sector filters and will"
        " inject an invalid filter: '%s'",
        actor_alias,
        ", ".join(sectors),
    )
    context.response = fas.search.go_to(session, sectors=sectors)


def fas_clear_search_filters(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session

    logging.debug("%s will clear the search filter", actor_alias)
    response = fas.search.go_to(session, term="")
    context.response = response
    fas.search.should_be_here(response)


def fas_browse_suppliers_by_company_sectors(
    context: Context, actor_alias: str, company_alias: str, pages_to_scan: int
):
    actor = get_actor(context, actor_alias)
    session = actor.session
    company = get_company(context, company_alias)
    sectors = company.sector
    results = {}

    response = fas.search.go_to(session, sectors=sectors)
    context.response = response
    fas.search.should_be_here(response)

    profile_link = fas.search.find_profile_link(response, company.title)
    found = profile_link != ""

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
            response = fas.search.go_to(session, page=page_number, sectors=sectors)
            profile_link = fas.search.find_profile_link(response, company.title)
            found = profile_link != ""
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


def fas_get_case_study_slug(context: Context, actor_alias: str, case_alias: str):
    result = None
    actor = get_actor(context, actor_alias)
    company = get_company(context, actor.company_alias)
    case = get_company(context, actor.company_alias).case_studies[case_alias]

    response = fas.profile.go_to(actor.session, company.number)
    context.response = response
    fas.profile.should_be_here(response)

    case_studies_details = fas.profile.get_case_studies_details(response)
    for title, summary, href, slug in case_studies_details:
        if title == case.title:
            result = slug

    with assertion_msg("Could not find slug for case study '%s'", case_alias):
        assert result is not None

    update_case_study(context, company.alias, case_alias, slug=result)
    logging.debug("%s got case study '%s' slug: '%s'", actor_alias, case_alias, result)


def fas_search_with_term(context: Context, actor_alias: str, search_term: str):
    actor = get_actor(context, actor_alias)
    session = actor.session
    context.response = fas.search.go_to(session, term=search_term)
    fas.search.should_be_here(context.response)


def profile_go_to_letter_verification(
    context: Context, supplier_alias: str, logged_in: bool
):
    actor = get_actor(context, supplier_alias)
    response = fab.confirm_identity.go_to(actor.session)
    context.response = response

    if logged_in:
        fab.verify_company.should_be_here(response)
    else:
        sso.login.should_be_here(response)

        token = extract_csrf_middleware_token(response)
        update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

        sso_login_url = URLs.SSO_LOGIN.absolute
        fab_verify_url = quote(URLs.FAB_CONFIRM_IDENTITY.absolute)
        referer = f"{sso_login_url}?next={fab_verify_url}"
        next = URLs.FAB_CONFIRM_IDENTITY.absolute
        logging.debug(
            "After successful login %s should be redirected to: %s",
            supplier_alias,
            referer,
        )
        response = sso.login.login(actor, referer=referer, next_param=next)
        context.response = response

        fab.verify_company.should_be_here(response)


def fab_choose_to_verify_with_code(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    referer = URLs.FAB_CONFIRM_IDENTITY.absolute
    response = fab.verify_company.go_to(actor.session, referer=referer)
    context.response = response
    fab.verify_company.should_be_here(response)


def fab_submit_verification_code(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    verification_code = company.verification_code
    referer = URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute
    response = fab.verify_company.submit(
        actor.session, actor.csrfmiddlewaretoken, verification_code, referer=referer
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
        ("valid http", f"http://{rare_word()}.{rare_word()}"),
        ("valid https", f"https://{rare_word()}.{rare_word()}"),
        ("invalid http", f"http:{rare_word()}.{rare_word()}"),
        ("invalid https", f"https:{rare_word()}.{rare_word()}"),
        ("invalid sector", "this is an invalid sector"),
        ("no image", None),
        ("invalid image", choice(BMPs + JP2s + WEBPs)),
        (" characters$", get_n_chars(get_number_from_key(key))),
        (" words$", get_n_words(get_number_from_key(key))),
        (" predefined countries$", get_n_country_codes(get_number_from_key(key))),
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
    actor = get_actor(context, supplier_alias)
    session = actor.session

    page_1_fields = ["title", "summary", "description", "sector", "website", "keywords"]
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
        logging.debug(
            f"Trying to add a case study with: field='{field}'; "
            f"value type='{value_type}'; separator='{separator}'; error='{error}'"
        )

        value = get_form_value(value_type)

        if field == "keywords":
            separator = SEPARATORS.get(separator, ",")
            value = "{} ".format(separator).join(value.split())

        case_study = case_study._replace(**{field: value})

        response = profile.case_study_basic.go_to(session)
        context.response = response
        profile.case_study_basic.should_be_here(response)

        token = extract_csrf_middleware_token(response)

        logging.debug(f"Case study details: {case_study}")
        if field in page_1_fields:
            response = profile.case_study_basic.submit(session, token, case_study)
            context.response = response
            check_response(response, 200)
        elif field in page_2_fields:
            response = profile.case_study_basic.submit(session, token, case_study)
            context.response = response
            token = extract_csrf_middleware_token(response)
            response = profile.case_study_images.submit(session, token, case_study)
            context.response = response
            check_response(response, 200)
        else:
            raise KeyError("Could not recognize field '{}' as valid case study field")

        results.append((field, value_type, case_study, response, error))

    context.results = results


def sso_request_password_reset(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    if actor.company_alias is None:
        next_param = get_page_object("profile - about").URL
    else:
        next_param = get_page_object("find a buyer - landing").URL

    response = sso.password_reset.go_to(actor.session, next_param=next_param)
    context.response = response

    sso.password_reset.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    response = sso.password_reset.reset(actor, token, next_param=next_param)
    context.response = response


def sso_sign_in(context: Context, supplier_alias: str, *, from_page: str = None):
    """Sign in to standalone SSO account."""
    actor = get_actor(context, supplier_alias)
    from_page = get_page_object(from_page).URL if from_page else None
    next_param = from_page or URLs.PROFILE_ABOUT.absolute
    referer = from_page or URLs.PROFILE_ABOUT.absolute
    response = sso.login.go_to(actor.session, next_param=next_param, referer=referer)
    context.response = response

    sso.login.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    context.response = sso.login.login(actor, next_param=next_param, referer=referer)
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
    letters_only: bool = False,
):
    actor = get_actor(context, supplier_alias)
    session = actor.session
    link = actor.password_reset_link

    response = sso.password_reset.open_link(session, link)
    context.response = response

    sso.change_password.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)
    action = extract_form_action(response)

    password = None
    password_again = None

    if new:
        password_length = 15
        if letters_only:
            password = "".join(choice(ascii_letters) for _ in range(password_length))
        else:
            password = "".join(
                choice(ascii_letters) + choice(digits) for _ in range(password_length)
            )
        update_actor(context, supplier_alias, password=password)
    if same:
        password = actor.password
    if mismatch:
        password = "first password"
        password_again = "this password does not match"

    actor = get_actor(context, supplier_alias)

    response = sso.change_password.submit(
        actor, action, password=password, password_again=password_again
    )
    context.response = response


def sso_open_password_reset_link(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    session = actor.session
    link = actor.password_reset_link
    context.response = sso.password_reset.open_link(session, link)


def go_to_pages(context: Context, actor_alias: str, table: Table):
    actor = get_actor(context, actor_alias)
    results = {}
    for row in table:
        page_name = row["page name"]
        url = get_page_object(page_name).URL
        response = make_request(Method.GET, url, session=actor.session)
        context.response = response
        results[page_name] = response

    context.results = results


def profile_add_collaborator(
    context: Context, supplier_alias: str, collaborator_aliases: str, role: str
):

    aliases = [alias.strip() for alias in collaborator_aliases.split(",")]

    for collaborator_alias in aliases:
        supplier = get_actor(context, supplier_alias)
        company = get_company(context, supplier.company_alias)
        collaborator = get_actor(context, collaborator_alias)
        response = fab.account_add_collaborator.go_to(supplier.session)
        context.response = response

        fab.account_add_collaborator.should_be_here(response)

        response = fab.account_add_collaborator.add_collaborator(
            supplier.session, collaborator.email, role
        )
        context.response = response

        fab.account_add_collaborator.should_be_here(response, invitation_sent=True)
        collaborators = company.collaborators
        if collaborators:
            collaborators.append(collaborator_alias)
        else:
            collaborators = [collaborator_alias]
        update_company(context, company.alias, collaborators=collaborators)


def profile_confirm_collaboration_request(
    context: Context, collaborator_alias: str, company_alias: str
):
    collaborator = get_actor(context, collaborator_alias)
    session = collaborator.session
    link = collaborator.invitation_for_collaboration_link

    # Step 1 - open confirmation link
    context.response = profile.confirm_your_collaboration.open(session, link)

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    profile.confirm_your_collaboration.should_be_here(context.response)
    logging.debug(
        "Collaborator %s is on the FAB Confirm your collaboration page",
        collaborator_alias,
    )

    # Step 4 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(context.response)
    update_actor(context, collaborator_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(context.response)
    context.form_action_value = form_action_value

    # Step 5 - submit the form
    response = profile.confirm_your_collaboration.confirm(session, token, link)
    context.response = response
    update_actor(context, collaborator_alias, company_alias=company_alias)
    logging.debug(
        "%s confirmed that he/she wants to be added to the profile for %s",
        collaborator_alias,
        company_alias,
    )


def fab_open_collaboration_request_link(
    context: Context, collaborator_alias: str, company_alias: str
):
    collaborator = get_actor(context, collaborator_alias)
    session = collaborator.session
    link = collaborator.invitation_for_collaboration_link

    response = profile.confirm_your_collaboration.open(session, link)
    context.response = response
    logging.debug(
        "%s opened the collaboration request link from company %s",
        collaborator_alias,
        company_alias,
    )


def sso_create_standalone_unverified_sso_account_from_collaboration_request(
    context: Context, actor_alias: str, *, next_link: str = None
):
    """Create a standalone SSO/great.gov.uk account."""
    actor = get_actor(context, actor_alias)
    next = next_link or actor.invitation_for_collaboration_link

    # Step 1: Go to the SSO/great.gov.uk registration page
    referer = URLs.SSO_SIGNUP.absolute + f"?next={next}"
    response = sso.register.go_to(actor.session, next=next, referer=referer)
    context.response = response

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    update_actor(context, actor_alias, csrfmiddlewaretoken=token)

    # Step 3: Check if User is not logged in
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 4: POST SSO accounts/signup/
    response = sso.register.submit_no_company(actor, next=next, referer=referer)
    context.response = response

    # Step 8: Check if Supplier is on Verify your email page & is not logged in
    sso.verify_your_email.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"


def fab_collaborator_create_sso_account_and_confirm_email(
    context: Context, collaborator_alias: str, company_alias: str
):
    fab_open_collaboration_request_link(context, collaborator_alias, company_alias)
    sso.login.should_be_here(context.response)
    sso_create_standalone_unverified_sso_account_from_collaboration_request(
        context, collaborator_alias
    )
    reg_should_get_verification_email(context, collaborator_alias)
    reg_open_email_confirmation_link(context, collaborator_alias)
    sso_collaborator_confirm_email_address(context, collaborator_alias)
    profile_confirm_collaboration_request(context, collaborator_alias, company_alias)


def profile_send_transfer_ownership_request(
    context: Context, supplier_alias: str, company_alias: str, new_owner_alias: str
):
    """
    Due to bug ED-2268 the first time you visit SUD pages by going directly
    to SUD "Find a Buyer" page, then you're redirected to SUD "About" page
    To circumvent this behaviour we have to go to the "About" page first, and
    then visit the SUD "Find a Buyer" page
    """
    supplier = get_actor(context, supplier_alias)
    company = get_company(context, company_alias)
    new_owner = get_actor(context, new_owner_alias)

    context.response = profile.admin_transfer_ownership.submit(
        supplier.session, new_owner.email
    )
    profile.admin.should_be_here(context.response)

    update_actor(context, supplier_alias, ex_owner=True)
    update_actor(context, new_owner_alias, company_alias=company_alias)
    update_company(
        context, company.alias, owner=new_owner_alias, owner_email=new_owner.email
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
    new_owner = get_actor(context, new_owner_alias)
    session = new_owner.session
    link = new_owner.ownership_request_link

    response = fab.confirm_your_ownership.open(session, link)
    context.response = response
    if new_owner.has_sso_account:
        fab.confirm_your_ownership.should_be_here(response)
    else:
        sso_create_standalone_unverified_sso_account_from_collaboration_request(
            context, new_owner_alias, next_link=link
        )
        reg_should_get_verification_email(context, new_owner_alias)
        reg_open_email_confirmation_link(context, new_owner_alias)
        sso_new_owner_confirm_email_address(context, new_owner_alias)
    logging.debug(
        "%s opened the transfer ownership request link from company %s",
        new_owner_alias,
        company_alias,
    )


def fab_confirm_account_ownership_request(
    context: Context, new_owner_alias: str, company_alias: str
):
    new_owner = get_actor(context, new_owner_alias)
    session = new_owner.session
    link = new_owner.ownership_request_link

    # Step 1 - confirm that Supplier is on SSO Confirm Your Email page
    fab.confirm_your_ownership.should_be_here(context.response)
    logging.debug(
        "New Owner %s is on the FAB Confirm your request for ownership page",
        new_owner_alias,
    )

    # Step 2 - extract & store CSRF token & form action value
    # Form Action Value is required to successfully confirm email
    token = extract_csrf_middleware_token(context.response)
    update_actor(context, new_owner_alias, csrfmiddlewaretoken=token)
    form_action_value = extract_form_action(context.response)
    context.form_action_value = form_action_value

    # Step 3 - submit the form
    response = fab.confirm_your_ownership.confirm(session, token, link)
    context.response = response

    profile.edit_company_profile.should_be_here(response)

    update_actor(context, new_owner_alias, company_alias=company_alias)
    logging.debug(
        "%s confirmed that he/she wants to be added to the profile for %s",
        new_owner_alias,
        company_alias,
    )


def fab_transfer_ownership(
    context: Context, supplier_alias: str, company_alias: str, new_owner_alias: str
):
    profile_send_transfer_ownership_request(
        context, supplier_alias, company_alias, new_owner_alias
    )
    profile_should_get_request_for_becoming_owner(
        context, new_owner_alias, company_alias
    )
    fab_open_transfer_ownership_request_link_and_create_sso_account_if_needed(
        context, new_owner_alias, company_alias
    )
    fab_confirm_account_ownership_request(context, new_owner_alias, company_alias)


def fab_remove_collaborators(
    context: Context,
    supplier_alias: str,
    collaborators_aliases: str,
    company_alias: str,
):
    aliases = [alias.strip() for alias in collaborators_aliases.split(",")]
    emails = [get_actor(context, alias).email for alias in aliases]
    supplier = get_actor(context, supplier_alias)
    company = get_company(context, company_alias)

    # Step 1: go to the remove collaborators page
    response = fab.account_remove_collaborator.go_to(supplier.session)
    context.response = response

    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    # Step 2: extract SSO IDs for users to remove
    emails_to_sso_id = fab.account_remove_collaborator.extract_sso_ids(response)
    logging.debug("SSO IDs for specific actor: %s", emails_to_sso_id)
    sso_ids = [sso_id for email, sso_id in emails_to_sso_id.items() if email in emails]
    logging.debug("List of SSO IDs to remove: %s", sso_ids)

    # Step 3: send the request with SSO IDs of users to remove
    response = fab.account_remove_collaborator.remove(supplier.session, token, sso_ids)
    context.response = response

    profile.business_profile.should_be_here(response, user_removed=True)
    collaborators = company.collaborators
    collaborators = [alias for alias in collaborators if alias not in aliases]
    update_company(context, company.alias, collaborators=collaborators)


def enrol_get_email_verification_code(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    logging.debug("Get email verification code")
    code = get_email_verification_code(actor.email)
    assert code, f"Could not find email verification code for {actor.email}"
    if code.startswith("0"):
        logging.warning(f"TT-2089 Got a code that starts with 0: {code}")
    update_actor(context, actor.alias, email_confirmation_code=code)


def find_ch_company(alias: str, *, term: str = None, active: bool = True):
    search_terms = [
        "food",
        "sell",
        "office",
        "fruits",
        "music",
        "group",
        "digital",
        "open",
        "world",
        "finance",
        "accounting",
        "consulting",
        "health",
        "access",
        "supply",
        "suppliers",
        "safety",
        "discount",
        "energy",
        "media",
        "impact",
        "solutions",
        "market",
        "green",
        "price",
        "social",
        "soft",
        "software",
        "fashion",
        "british",
        "farm",
        "innovations",
        "furniture",
        "light",
        "power",
        "care",
        "metal",
        "building",
        "society",
    ]
    term = term or random.choice(search_terms)

    headers = {"Accept": "application/json"}
    url = URLs.PROFILE_API_COMPANIES_HOUSE_SEARCH.absolute_template.format(term=term)
    response = make_request(Method.GET, url, headers=headers)
    assert response.status_code == 200
    logging.debug(f"Found {len(response.json())} companies for term: '{term}'")

    unfiltered = response.json()

    ch_companies = [
        company
        for company in unfiltered
        if company["company_number"]
        and len(
            company["company_name"]
            .lower()
            .replace("ltd", "")
            .replace("limited", "")
            .split()
        )
        > 2
    ]

    active_statuses = ["active", "voluntary-arrangement"]
    if active:
        by_status = [
            company
            for company in ch_companies
            if company["company_status"] in active_statuses
        ]
    else:
        by_status = [
            company
            for company in ch_companies
            if company["company_status"] not in active_statuses
        ]

    accepted_types = [
        "ltd",
        "charitable-incorporated-organisation",
        "uk-establishment",
        "limited-partnership",
        "private-limited-guarant-nsc-limited-exemption",
        "private-limited-guarant-nsc",
        "registered-society-non-jurisdictional",
        "industrial-and-provident-society",
    ]
    by_type = [
        company for company in by_status if company["company_type"] in accepted_types
    ]
    logging.debug(f"Found {len(by_type)} CH companies filtered by status & type")

    ch_company_details = random.choice(by_type)
    logging.debug(f"SEARCH: Selected CH company: {ch_company_details}")

    details_mapping = {
        "alias": alias,
        "title": ch_company_details["title"],
        "number": ch_company_details["company_number"],
        "companies_house_details": ch_company_details,
        "case_studies": {},
    }
    return Company(**details_mapping)


def should_skip_company(response: Response) -> Tuple[bool, str]:
    content = response.content.decode("UTF-8")
    errors = {
        "Company not active": "Inactive company",
        "74990": "Company with unsupported SIC=74990",
        "88100": "Company with unsupported SIC=88100",
        "Good news, a Business Profile already exists for this company": "A business profile already exists",
    }
    for string, error in errors.items():
        if string in content:
            return True, error
    return False, "No problems were found with selected company"


def profile_enrol_companies_house_registered_company(
    context: Context, actor: Actor, account: Account
):
    context.response = profile.select_business_type.submit(actor, account.business_type)
    profile.enter_your_email_and_password.should_be_here(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.enter_your_email_and_password.submit(actor)
    profile.enter_email_verification_code.should_be_here(context.response)

    if not account.verify_email:
        logging.debug(
            f"Won't verify email address for '{actor.alias}' as '{account.description}' was requested"
        )
        return
    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    enrol_get_email_verification_code(context, actor.alias)
    actor = get_actor(context, actor.alias)
    assert actor.session
    context.response = profile.enter_email_verification_code.submit(actor)
    profile.enter_your_business_details.should_be_here(context.response)

    max_attempt = 10
    attempt_counter = 1
    skip_company = True
    while skip_company and attempt_counter < max_attempt:
        company = find_ch_company(actor.company_alias)
        extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
        context.response = profile.enter_your_business_details.submit(actor, company)
        skip_company, error = should_skip_company(context.response)
        logging.debug(f"'{company.title}': {error}")
        attempt_counter += 1
    error = f"Could not find unregistered CH company after {attempt_counter} attempts"
    assert not skip_company, error
    add_company(context, company)
    update_company(
        context, alias=actor.company_alias, business_type=account.business_type
    )
    profile.enter_your_business_details_part_2.should_be_here(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.enter_your_business_details_part_2.submit(actor, company)
    profile.enter_your_personal_details.should_be_here(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    if "Tick this box to accept" in context.response.content.decode("UTF-8"):
        logging.warning(f"User was asked to accept T&Cs on: {context.response.url}")
        context.response = profile.enter_your_personal_details.submit(
            actor, tick_t_and_c=True
        )
    else:
        context.response = profile.enter_your_personal_details.submit(actor)
    profile.enrolment_finished.should_be_here(context.response)

    if not account.verify:
        logging.debug(
            f"Won't verify account for '{actor.alias}' as '{account.description}' account was requested"
        )
        return
    profile_add_business_description(context, actor.alias)
    fab_decide_to_verify_profile_with_letter(context, actor.alias)
    profile_verify_company_profile(context, actor.alias)

    if not account.publish:
        logging.debug(
            f"Won't publish account for '{actor.alias}' as '{account.description}' account was requested"
        )
        return
    profile_publish_profile_to_fas(context, actor.alias)


def profile_enrol_sole_trader(context: Context, actor: Actor, account: Account):
    context.response = profile.select_business_type.submit(actor, account.business_type)
    profile.non_ch_company_enter_your_email_and_password.should_be_here(
        context.response
    )

    assert_that_captcha_is_in_dev_mode(context.response)
    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.non_ch_company_enter_your_email_and_password.submit(
        actor
    )
    profile.enter_email_verification_code.should_be_here(context.response)

    if not account.verify_email:
        logging.debug(
            f"Won't verify email address for '{actor.alias}' as '{account.description}' was requested"
        )
        return
    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    enrol_get_email_verification_code(context, actor.alias)
    actor = get_actor(context, actor.alias)
    assert actor.session
    context.response = profile.non_ch_company_enter_email_verification_code.submit(
        actor
    )

    profile.non_ch_company_enter_your_business_details.should_be_here(context.response)
    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    company = Company(
        alias=actor.company_alias,
        title=f"DIT AUTOMATED TESTS {uuid.uuid4()}",
        business_type=account.business_type,
        companies_house_details={},
    )
    add_company(context, company)
    context.response = profile.non_ch_company_enter_your_business_details.submit(
        actor, company
    )
    profile.non_ch_company_enter_your_personal_details.should_be_here(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.non_ch_company_enter_your_personal_details.submit(actor)
    profile.non_ch_company_enrolment_finished.should_be_here(context.response)

    if not account.verify:
        logging.debug(
            f"Won't verify account for '{actor.alias}' as '{account.description}' account was requested"
        )
        return
    profile_add_business_description(context, actor.alias, ch_company=False)
    profile.non_ch_company_request_to_verify.submit(actor)
    verify_non_ch_company(context, company)
    company_number = get_company_by_id_or_title(company.title)["number"]
    update_company(context, company.alias, number=company_number)

    if not account.publish:
        logging.debug(
            f"Won't publish account for '{actor.alias}' as '{account.description}' account was requested"
        )
        return
    profile_publish_profile_to_fas(context, actor.alias)


def profile_enrol_individual(context: Context, actor: Actor, account: Account):
    context.response = profile.enrol.go_to(actor.session)
    context.response = profile.select_business_type.go_to(actor.session)

    context.response = profile.select_business_type.submit(actor, account.business_type)
    profile.individual_enter_your_email_and_password.should_be_here(context.response)
    assert_that_captcha_is_in_dev_mode(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.individual_enter_your_email_and_password.submit(actor)
    profile.individual_enter_email_verification_code.should_be_here(context.response)

    if not account.verify_email:
        logging.debug(
            f"Won't verify email address for '{actor.alias}' as '{account.description}'"
            f" was requested"
        )
        return
    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    enrol_get_email_verification_code(context, actor.alias)
    actor = get_actor(context, actor.alias)
    assert actor.session
    context.response = profile.individual_enter_email_verification_code.submit(actor)
    profile.individual_enter_your_personal_details.should_be_here(context.response)

    extract_and_set_csrf_middleware_token(context, context.response, actor.alias)
    context.response = profile.individual_enter_your_personal_details.submit(actor)
    profile.individual_enrolment_finished.should_be_here(context.response)


def profile_enrol_overseas_company(context: Context, actor: Actor, account: Account):
    context.response = profile.select_business_type.submit(actor, account.business_type)


def profile_create_isd_profile(context: Context, actor: Actor, account: Account):
    pass


def profile_enrol_user(
    context: Context,
    actor_alias: str,
    account_description: str,
    *,
    company_alias: str = None,
):
    account = Account(account_description)
    logging.debug(f"Account was identified as: {account}")

    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_supplier(actor_alias))
    if company_alias:
        update_actor(context, actor_alias, company_alias=company_alias)
    actor = get_actor(context, actor_alias)
    logging.debug(f"Found matching account type: {account}")

    if account.business_type is BusinessType.COMPANIES_HOUSE:
        profile_enrol_companies_house_registered_company(context, actor, account)
    if account.business_type in [
        BusinessType.SOLE_TRADER,
        BusinessType.CHARITY,
        BusinessType.PARTNERSHIP,
        BusinessType.OTHER,
    ]:
        profile_enrol_sole_trader(context, actor, account)
    if account.business_type is BusinessType.INDIVIDUAL:
        profile_enrol_individual(context, actor, account)
    if account.business_type is BusinessType.OVERSEAS_COMPANY:
        profile_enrol_overseas_company(context, actor, account)
    if account.business_type in [
        BusinessType.ISD_ONLY,
        BusinessType.ISD_AND_TRADE,
        BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE,
    ]:
        profile_create_isd_profile(context, actor, account)


def isd_enrol_user(context: Context, actor_alias: str, company_alias: str):
    pass


def isd_publish_profile(context: Context, supplier_alias: str):
    pass


def isd_create_unregistered_company(
    context: Context, supplier_alias: str, company_alias: str
):
    company_dict = create_test_isd_company(context)
    company = Company(
        alias=company_alias,
        title=company_dict["name"],
        number=company_dict["number"],
        sector=company_dict["sectors"],
        description=company_dict["description"],
        summary=company_dict["summary"],
        no_employees=company_dict["employees"],
        keywords=company_dict["keywords"],
        website=company_dict["website"],
        facebook=company_dict["facebook_url"],
        twitter=company_dict["twitter_url"],
        linkedin=company_dict["linkedin_url"],
        is_uk_isd_company=company_dict["is_uk_isd_company"],
        slug=company_dict["slug"],
        expertise_industries=company_dict["expertise_industries"],
        export_destinations=company_dict["export_destinations"],
        export_destinations_other=company_dict["export_destinations_other"],
    )
    update_actor(context, supplier_alias, company_alias=company_alias)
    add_company(context, company)
    logging.debug(f"A test ISD company was successfully created:\n{company}")


def isd_create_unverified_business_profile(
    context: Context, supplier_alias: str, company_alias: str
):
    if not get_actor(context, supplier_alias):
        add_actor(context, unauthenticated_supplier(supplier_alias))
    isd_create_unregistered_company(context, supplier_alias, company_alias)
    isd_enrol_user(context, supplier_alias, company_alias)
    update_actor(context, supplier_alias, has_sso_account=True)


def isd_create_verified_and_published_business_profile(
    context: Context, supplier_alias: str, company_alias: str
):
    """Create a verified ISD Business profile and publish it to ISD"""
    logging.debug("1 - find unregistered ISD company & enrol user for that company")
    isd_create_unverified_business_profile(context, supplier_alias, company_alias)
    logging.debug("2 - Publish ISD business profile")
    isd_publish_profile(context, supplier_alias)


def isd_search(context: Context, buyer_alias: str, term: str):
    actor = get_actor(context, buyer_alias)
    session = actor.session
    context.response = isd.search.go_to(session, term=term)
    isd.search.should_be_here(context.response)


def profile_request_to_verify(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    profile_add_business_description(context, actor.alias, ch_company=False)
    response = profile.non_ch_company_request_to_verify.submit(actor)
    check_for_errors(response.content.decode("UTF-8"), response.url)
