# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import os
import re
from random import choice, randrange
from string import ascii_letters, digits
from urllib.parse import parse_qsl, quote, urljoin, urlsplit

from behave.model import Table
from behave.runner import Context
from requests import Response, Session
from scrapy import Selector
from tests import get_absolute_url
from tests.functional.common import DETAILS, PROFILES
from tests.functional.pages import (
    fab_ui_account_add_collaborator,
    fab_ui_account_confrim_password,
    fab_ui_account_remove_collaborator,
    fab_ui_account_transfer_ownership,
    fab_ui_build_profile_basic,
    fab_ui_build_profile_sector,
    fab_ui_build_profile_verification_letter,
    fab_ui_case_study_basic,
    fab_ui_case_study_images,
    fab_ui_confim_your_collaboration,
    fab_ui_confim_your_ownership,
    fab_ui_confirm_company,
    fab_ui_confirm_export_status,
    fab_ui_confirm_identity,
    fab_ui_confirm_identity_letter,
    fab_ui_edit_description,
    fab_ui_edit_details,
    fab_ui_edit_online_profiles,
    fab_ui_edit_sector,
    fab_ui_landing,
    fab_ui_profile,
    fab_ui_upload_logo,
    fab_ui_verify_company,
    fas_ui_contact,
    fas_ui_feedback,
    fas_ui_find_supplier,
    fas_ui_profile,
    profile_ui_find_a_buyer,
    profile_ui_landing,
    sso_ui_change_password,
    sso_ui_confim_your_email,
    sso_ui_login,
    sso_ui_logout,
    sso_ui_password_reset,
    sso_ui_register,
    sso_ui_verify_your_email,
    sud_ui_landing,
)
from tests.functional.registry import get_fabs_page_object, get_fabs_page_url
from tests.functional.steps.fab_then_impl import (
    fab_should_get_request_for_becoming_owner,
    reg_should_get_verification_email,
)
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import (
    assertion_msg,
    escape_html,
    extract_and_set_csrf_middleware_token,
    extract_csrf_middleware_token,
    extract_form_action,
    extract_logo_url,
    extract_registration_page_link,
    extract_text_from_pdf,
    get_absolute_path_of_file,
    get_active_company_without_fas_profile,
    get_language_code,
    get_md5_hash_of_file,
    get_number_of_search_result_pages,
    get_pdf_from_stannp,
    get_verification_code,
    is_already_registered,
    is_inactive,
    random_case_study_data,
    random_chars,
    random_feedback_data,
    random_message_data,
    rare_word,
    sentence,
)
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

    # Submit SSO Registration form with Supplier's & Company's required details
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
    title = "{} {}".format(company.title, sentence())
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


def bp_verify_identity_with_letter(context: Context, supplier_alias: str):
    """Build Profile - verify identity with a physical letter."""
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Choose to verify with a letter
    response = fab_ui_confirm_identity.confirm_with_letter(actor)
    context.response = response

    # Step 2 - check if Supplier is on the We've sent you a verification letter
    fab_ui_confirm_identity_letter.should_be_here(response)
    logging.debug(
        "Supplier is on the 'Your company address' letter verification page"
    )

    # Step 3 - extract & store CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 4 - check if Supplier is on the We've sent you a verification letter
    fab_ui_confirm_identity_letter.submit(actor)
    context.response = response

    # Step 5 - Click on the "View or amend your company profile" link
    # use previous url as the referer link
    response = fab_ui_build_profile_verification_letter.go_to_profile(session)
    context.response = response

    # Step 6 - check if Supplier is on the FAB profile page
    fab_ui_profile.should_see_missing_description(response)


def prof_set_company_description(context: Context, supplier_alias: str):
    """Edit Profile - Will set company description.

    This is quasi-mandatory (*) step before Supplier can verify the company
    with the code sent in a letter.

    (*) it's quasi mandatory, because Supplier can actually go to the company
    verification page using the link provided in the letter without the need
    to set company description.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - go to the "Set Company Description" page
    response = fab_ui_edit_description.go_to(session)

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)
    logging.debug("Supplier is on the Set Company Description page")

    # Step 2 - Submit company description
    summary = sentence()
    description = sentence()
    response = fab_ui_edit_description.submit(
        session, token, summary, description
    )
    context.response = response

    # Step 3 - check if Supplier is on Profile page
    fab_ui_profile.should_see_profile_is_not_verified(response)

    # Step 4 - update company details in Scenario Data
    context.set_company_details(
        actor.company_alias, summary=summary, description=description
    )
    logging.debug("Supplier is back to the Profile Page")


def prof_verify_company(context: Context, supplier_alias: str):
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
    response = fab_ui_verify_company.view_or_amend_profile(session)
    context.response = response

    # STEP 6 - check if Supplier is on Verified Profile Page
    fab_ui_profile.should_see_profile_is_verified(response)


def prof_view_published_profile(context: Context, supplier_alias: str):
    """Whilst being of FAB company profile page it will `click` on
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


def prof_attempt_to_sign_in_to_fab(context: Context, supplier_alias: str):
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


def prof_sign_out_from_fab(context: Context, supplier_alias: str):
    """Sign out from Find a Buyer."""
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign Out confirmation page
    response = sso_ui_logout.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on Log Out page & extract CSRF token
    sso_ui_logout.should_be_here(response)
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - log out
    response = sso_ui_logout.logout(session, token)
    context.response = response

    # Step 4 - check if Supplier is on FAB Landing page & is logged out
    fab_ui_landing.should_be_here(response)
    fab_ui_landing.should_be_logged_out(response)

    # Step 5 - reset requests Session object
    context.reset_actor_session(supplier_alias)


def prof_sign_in_to_fab(context: Context, supplier_alias: str):
    """Sign in to Find a Buyer."""
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign In page
    response = sso_ui_login.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on the SSO Login page
    sso_ui_login.should_be_here(response)
    with assertion_msg(
        "It looks like user is still logged in, as the "
        "sso_display_logged_in cookie is not equal to False"
    ):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 3 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 4 - submit the login form
    response = sso_ui_login.login(actor)
    context.response = response

    # Step 5 - check if Supplier is on the FAB profile page
    fab_ui_profile.should_be_here(response)
    with assertion_msg(
        "Found sso_display_logged_in cookie in the response. Maybe user is"
        " still logged in?"
    ):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
        "Found directory_sso_dev_session cookie in the response. Maybe "
        "user is still logged in?"
    ):
        assert "directory_sso_dev_session" not in response.cookies


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
    profile_ui_landing.should_be_here(response)

    # STEP 3 - Update Actor's data
    context.update_actor(supplier_alias, has_sso_account=True)


def sso_go_to_create_trade_profile(context: Context, supplier_alias: str):
    """Follow the 'Create a trade profile' button on the "Find a Buyer" tab.

    NOTE:
    It's assumed that Supplier already has a standalone SSO/great.gov.uk
    account
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Go to "Find a Buyer" tab
    response = profile_ui_find_a_buyer.go_to(session)
    context.response = response
    profile_ui_find_a_buyer.should_be_here(response)
    profile_ui_find_a_buyer.should_see_get_a_trade_profile(response)

    # Step 2 - Click on "Create a trade profile" button
    response = profile_ui_find_a_buyer.go_to_create_a_trade_profile(session)
    context.response = response
    fab_ui_landing.should_be_here(response)


def prof_upload_logo(context: Context, supplier_alias: str, picture: str):
    """Upload Company's logo & extract newly uploaded logo image URL.

    NOTE:
    picture must represent file stored in ./tests/functional/files

    :param picture: name of the picture file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    file_path = get_absolute_path_of_file(picture)

    # Step 1 - Upload company's logo
    response = fab_ui_upload_logo.upload(session, token, file_path)
    context.response = response

    # Step 2 - check if Supplier is on the FAB profile page
    fab_ui_profile.should_be_here(response)
    logging.debug("Successfully uploaded logo picture: %s", picture)

    # Step 3 - Keep logo details in Company's scenario data
    logo_url = extract_logo_url(response)
    md5_hash = get_md5_hash_of_file(file_path)
    context.set_company_logo_detail(
        actor.company_alias, picture=picture, hash=md5_hash, url=logo_url
    )


def prof_upload_unsupported_file_as_logo(
    context: Context, supplier_alias: str, file: str
):
    """Try to upload unsupported file type as Company's logo.

    NOTE:
    file must exist in ./tests/functional/files

    :param file: name of the file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    file_path = get_absolute_path_of_file(file)

    logging.debug("Attempting to upload %s as company logo", file)
    # Step 1 - Try to upload a file of unsupported type as company's logo
    response = fab_ui_upload_logo.upload(session, token, file_path)
    context.response = response

    # Step 2 - check if upload was rejected
    rejected = fab_ui_upload_logo.was_upload_rejected(response)

    # There are 2 different error message that you can get, depending of the
    # type of uploaded file.
    # Here, we're checking if `any` of these 2 message is visible.
    if rejected:
        logging.debug("%s was rejected", file)
    else:
        logging.error("%s was accepted", file)
    return rejected


def prof_supplier_uploads_logo(
    context: Context, supplier_alias: str, picture: str
):
    """Upload a picture and set it as Company's logo.

    :param picture: name of the picture file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - go to Upload Logo page
    response = fab_ui_upload_logo.go_to(session)
    context.response = response

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - upload the logo
    prof_upload_logo(context, supplier_alias, picture)


def prof_to_upload_unsupported_logos(
    context: Context, supplier_alias: str, table: Table
):
    """Upload a picture and set it as Company's logo."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    files = [row["file"] for row in table]
    rejections = []
    for file in files:
        fab_ui_upload_logo.go_to(session)
        rejected = prof_upload_unsupported_file_as_logo(
            context, supplier_alias, file
        )
        rejections.append(rejected)
    context.rejections = rejections


def prof_update_company_details(
    context: Context, supplier_alias: str, table_of_details: Table
):
    """Update selected Company's details.

    NOTE:
    `table_of_details` contains names of details to update.
    Passing `table_of_details` can be avoided as we already have access to
    `context` object, yet in order to be more explicit, we're making it
    a mandatory argument.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # Step 0 - prepare company's details to update
    details_to_update = [row["detail"] for row in table_of_details]
    title = DETAILS["TITLE"] in details_to_update
    keywords = DETAILS["KEYWORDS"] in details_to_update
    website = DETAILS["WEBSITE"] in details_to_update
    size = DETAILS["SIZE"] in details_to_update
    sector = DETAILS["SECTOR"] in details_to_update
    exported_before = DETAILS["HAS_EXPORTED_BEFORE"] in details_to_update
    countries = DETAILS["COUNTRIES"] in details_to_update

    # Steps 1 - Go to the FAB Edit Company's details page
    response = fab_ui_edit_details.go_to(session)
    context.response = response
    fab_ui_edit_details.should_be_here(response)

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - Update company's details
    response, new_details = fab_ui_edit_details.update_details(
        actor,
        company,
        title=title,
        keywords=keywords,
        website=website,
        size=size,
    )
    context.response = response

    # Step 4 - Supplier should be on Edit Profile page
    fab_ui_profile.should_be_here(response)

    # Step 5 - Go to the Edit Sector page
    response = fab_ui_edit_sector.go_to(session)
    context.response = response
    fab_ui_edit_sector.should_be_here(response)

    # Step 5 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 6 - Update company's sector
    response, new_sector, new_countries, has_exported_before = fab_ui_edit_sector.update(
        actor, company, update_sector=sector, update_countries=countries,
        update_has_exported_before=exported_before
    )
    context.response = response

    # Step 7 - Check if Supplier is on FAB Profile page
    fab_ui_profile.should_be_here(response)

    # Step 7 - update company's details stored in context.scenario_data
    context.set_company_details(
        actor.company_alias,
        title=new_details.title,
        website=new_details.website,
        keywords=new_details.keywords,
        no_employees=new_details.no_employees,
        sector=new_sector,
        export_to_countries=new_countries,
        has_exported_before=has_exported_before,
    )
    logging.debug(
        "%s successfully updated basic Company's details: title=%s, "
        "website=%s, keywords=%s, number of employees=%s, sector=%s, "
        "countries=%s, has_exported_before=%s",
        supplier_alias,
        new_details.title,
        new_details.website,
        new_details.keywords,
        new_details.no_employees,
        new_sector,
        new_countries,
        has_exported_before,
    )


def prof_add_online_profiles(
    context: Context, supplier_alias: str, online_profiles: Table
):
    """Update links to Company's Online Profiles."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    profiles = [row["online profile"] for row in online_profiles]
    facebook = PROFILES["FACEBOOK"] in profiles
    linkedin = PROFILES["LINKEDIN"] in profiles
    twitter = PROFILES["TWITTER"] in profiles

    # Step 1 - Go to the FAB Edit Online Profiles page
    response = fab_ui_edit_online_profiles.go_to(session)
    context.response = response
    fab_ui_edit_online_profiles.should_be_here(response)

    # Step 2 - Extract CSRF token
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)

    # Step 3 - Update links to Online Profiles
    response, new_details = fab_ui_edit_online_profiles.update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )
    context.response = response

    # Step 4 - Check if Supplier is on FAB Profile page
    fab_ui_profile.should_be_here(response)

    # Step 5 - Update company's details stored in context.scenario_data
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


def prof_add_invalid_online_profiles(
    context: Context, supplier_alias: str, online_profiles: Table
):
    """Attempt to update links to Company's Online Profiles using invalid URLs.
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
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

    # Step 1 - Go to the Edit Online Profiles page
    response = fab_ui_edit_online_profiles.go_to(session)
    context.response = response
    fab_ui_edit_online_profiles.should_be_here(response)

    # Step 2 - Extract CSRF token
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)

    # Step 3 - update links to Online Profiles
    logging.debug(
        "Will use following invalid URLs to Online Profiles: %s %s %s",
        facebook_url if facebook else "",
        linkedin_url if linkedin else "",
        twitter_url if twitter else "",
    )
    response, _ = fab_ui_edit_online_profiles.update_profiles(
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


def prof_remove_links_to_online_profiles(
    context: Context, supplier_alias: str
):
    """Will remove links to existing Online Profiles."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    response = fab_ui_edit_online_profiles.remove_links(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter
    )
    context.response = response


def prof_add_case_study(
    context: Context, supplier_alias: str, case_alias: str
):
    """Will add a complete case study (all fields will be filled out)."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    case_study = random_case_study_data(case_alias)

    # Step 1 - go to "Add case study" form & extract CSRF token
    response = fab_ui_case_study_basic.go_to(session)
    context.response = response
    fab_ui_case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 2 - submit the "basic case study data" form & extract CSRF token
    response = fab_ui_case_study_basic.submit_form(session, token, case_study)
    context.response = response
    fab_ui_case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "case study images" form
    response = fab_ui_case_study_images.submit_form(session, token, case_study)
    context.response = response

    # Step 4 - check if we're on the FAB Profile page
    fab_ui_profile.should_be_here(response)

    # Step 5 - Store Case Study data in Scenario Data
    context.add_case_study(actor.company_alias, case_alias, case_study)


def fab_update_case_study(
    context: Context, supplier_alias: str, case_alias: str
):
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    # get content from last response (which contains FAB Profile Page)
    content = context.response.content.decode("utf-8")

    # Step 0 - extract links to Case Studies and do a crude mapping to
    # Case Study titles.
    css_titles = ".company-profile-module-container h4::text"
    css_links = "div.ed-company-profile-sector-case-study-inner a::attr(href)"
    titles = Selector(text=content).css(css_titles).extract()
    links = Selector(text=content).css(css_links).extract()
    case_link_mappings = {k: v for (k, v) in zip(titles, links)}
    current = company.case_studies[case_alias]
    current_link = case_link_mappings[current.title]
    index_of_case_id_in_url = -2
    current_number = int(current_link.split("/")[index_of_case_id_in_url])
    logging.debug(
        "Extracted link for case study: %s is: %s", case_alias, current_link
    )

    # Step 1 - generate new case study data
    new_case = random_case_study_data(case_alias)
    logging.debug("Now will replace case study data with: %s", new_case)

    # Step 2 - go to specific "Case study" page form & extract CSRF token
    response = fab_ui_case_study_basic.go_to(
        session, case_number=current_number
    )
    context.response = response
    fab_ui_case_study_basic.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 3 - submit the "basic case study data" form & extract CSRF token
    response = fab_ui_case_study_basic.submit_form(session, token, new_case)
    context.response = response
    fab_ui_case_study_images.should_be_here(response)
    token = extract_csrf_middleware_token(response)

    # Step 4 - submit the "case study images" form
    response = fab_ui_case_study_images.submit_form(session, token, new_case)
    context.response = response

    # Step 5 - check if we're on the FAB Profile page
    fab_ui_profile.should_be_here(response)

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
                search_terms["keyword #{}".format(index)] = keyword
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


def fas_view_pages_in_selected_language(
    context: Context, buyer_alias: str, pages_table: Table, language: str
):
    """View specific FAS pages in selected language.

    NOTE:
    This will store a dict with all page views responses in context.views
    """
    pages = [row["page"] for row in pages_table]
    views = {}
    for page_name in pages:
        actor = context.get_actor(buyer_alias)
        session = actor.session
        language_code = get_language_code(language)
        page_url = get_fabs_page_url(page_name, language_code=language_code)
        response = make_request(Method.GET, page_url, session=session)
        views[page_name] = response
    context.views = views


def fas_view_page(context: Context, actor_alias: str, page_name: str):
    actor = context.get_actor(actor_alias)
    session = actor.session
    page_object = get_fabs_page_object(page_name)
    context.response = page_object.go_to(session)


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
    referer_url = get_fabs_page_url(page_name)

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
    links_to_profiles_selector = "#ed-search-list-container a"
    href_selector = "a::attr(href)"
    links_to_profiles = (
        Selector(text=content).css(links_to_profiles_selector).extract()
    )
    profile_url = None
    for link in links_to_profiles:
        if escape_html(name).lower() in escape_html(link).lower():
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
    response = fas_ui_contact.go_to(
        session, company_number=company.number, company_name=company.title
    )
    context.response = response
    fas_ui_contact.should_be_here(response)

    # Step 3 - submit the form with the message data
    response = fas_ui_contact.submit(session, message, company.number)
    context.response = response


def fab_provide_company_details(
    context: Context, supplier_alias: str, table: Table
):
    """Submit company details with specific values in order to verify data
     validation.

    NOTE:
    This will store a list of `results` tuples in context. Each tuple will
    contain:
    * Company namedtuple (with details used in the request)
    * response object
    * expected error message
    """
    actor = context.get_actor(supplier_alias)
    original_details = context.get_company(actor.company_alias)
    results = []
    for row in table:
        if row["company name"] == "unchanged":
            title = original_details.title
        elif row["company name"] == "empty string":
            title = ""
        elif row["company name"].endswith(" characters"):
            number = [
                int(word)
                for word in row["company name"].split()
                if word.isdigit()
            ][0]
            title = random_chars(number)
        else:
            title = original_details.title

        if row["website"] == "empty string":
            website = ""
        elif row["website"] == "valid http":
            website = "http://{}.{}".format(rare_word(), rare_word())
        elif row["website"] == "valid https":
            website = "https://{}.{}".format(rare_word(), rare_word())
        elif row["website"] == "invalid http":
            website = "http:{}.{}".format(rare_word(), rare_word())
        elif row["website"] == "invalid https":
            website = "https:{}.{}".format(rare_word(), rare_word())
        elif row["website"].endswith(" characters"):
            number = [
                int(word) for word in row["website"].split() if word.isdigit()
            ][0]
            website = random_chars(number)

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

        if row["size"] == "unset":
            size = ""
        else:
            size = row["size"]

        new_details = Company(
            title=title, website=website, keywords=keywords, no_employees=size
        )

        response = fab_ui_build_profile_basic.submit(actor, new_details)
        results.append((new_details, response, row["error"]))

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


def fab_go_to_letter_verification(
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


def fab_attempt_to_add_case_study(
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

        response = fab_ui_case_study_basic.go_to(session)
        context.response = response
        fab_ui_case_study_basic.should_be_here(response)

        token = extract_csrf_middleware_token(response)

        if field in page_1_fields:
            response = fab_ui_case_study_basic.submit_form(
                session, token, case_study
            )
            context.response = response
        elif field in page_2_fields:
            response = fab_ui_case_study_basic.submit_form(
                session, token, case_study
            )
            context.response = response
            token = extract_csrf_middleware_token(response)
            response = fab_ui_case_study_images.submit_form(
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
        next_param = get_fabs_page_url(page_name="sud about")
    else:
        next_param = get_fabs_page_url(page_name="fab landing")

    response = sso_ui_password_reset.go_to(
        actor.session, next_param=next_param
    )
    context.response = response

    sso_ui_password_reset.should_be_here(response)

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    response = sso_ui_password_reset.reset(actor, token, next_param=next_param)
    context.response = response


def sso_sign_in(context: Context, supplier_alias: str):
    """Sign in to standalone SSO account."""
    actor = context.get_actor(supplier_alias)
    next_param = get_absolute_url("profile:about")
    referer = get_absolute_url("profile:about")
    response = sso_ui_login.go_to(
        actor.session, next_param=next_param, referer=referer
    )
    context.response = response

    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    context.response = sso_ui_login.login(
        actor, next_param=next_param, referer=referer
    )


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
    url = get_fabs_page_url(page_name)
    context.response = make_request(Method.GET, url, session=actor.session)


def go_to_pages(context: Context, actor_alias: str, table: Table):
    actor = context.get_actor(actor_alias)
    results = {}
    for row in table:
        page_name = row["page name"]
        url = get_fabs_page_url(page_name)
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


def fab_add_collaborator(
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

        profile_ui_find_a_buyer.should_be_here(response)
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


def fab_collaborator_create_sso_account_and_confirm_email(
    context: Context, collaborator_alias: str, company_alias: str
):
    fab_open_collaboration_request_link(
        context, collaborator_alias, company_alias
    )
    sso_ui_login.should_be_here(context.response)
    reg_create_standalone_unverified_sso_account_from_sso_login_page(
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

    context.response = sud_ui_landing.go_to(
        supplier.session, set_next_page=False
    )
    sud_ui_landing.should_be_here(context.response)

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

    profile_ui_find_a_buyer.should_be_here(response, owner_transferred=True)

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

    fab_ui_profile.should_be_here(response)

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

    profile_ui_find_a_buyer.should_be_here(response, user_removed=True)
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
            "Something went wrong when trying to delete: {}".format(pdf_path)
        )
    context.update_actor(actor_alias, verification_letter=pdf_text)
