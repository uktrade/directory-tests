# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random

from behave.model import Table
from behave.runner import Context
from requests import Response, Session
from scrapy import Selector

from tests.functional.features.pages import (
    fab_ui_build_profile_address,
    fab_ui_build_profile_basic,
    fab_ui_build_profile_sector,
    fab_ui_build_profile_verification_letter,
    fab_ui_case_study_basic,
    fab_ui_case_study_images,
    fab_ui_confirm_company,
    fab_ui_confirm_export_status,
    fab_ui_edit_description,
    fab_ui_edit_details,
    fab_ui_edit_online_profiles,
    fab_ui_edit_sector,
    fab_ui_landing,
    fab_ui_profile,
    fab_ui_upload_logo,
    fab_ui_verify_company,
    fas_ui_feedback,
    fas_ui_find_supplier,
    fas_ui_profile,
    profile_ui_find_a_buyer,
    profile_ui_landing,
    sso_ui_confim_your_email,
    sso_ui_login,
    sso_ui_logout,
    sso_ui_register,
    sso_ui_verify_your_email
)
from tests.functional.features.pages.common import DETAILS, PROFILES
from tests.functional.features.pages.utils import (
    extract_and_set_csrf_middleware_token,
    get_active_company_without_fas_profile,
    get_fas_page_url,
    get_language_code,
    get_number_of_search_result_pages,
    is_already_registered,
    is_inactive,
    random_case_study_data,
    random_feedback_data,
    rare_word,
    sentence
)
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    check_response,
    extract_confirm_email_form_action,
    extract_csrf_middleware_token,
    extract_logo_url,
    get_absolute_path_of_file,
    get_md5_hash_of_file,
    get_verification_code,
    make_request
)
from tests.settings import COUNTRIES, NO_OF_EMPLOYEES, SECTORS


def select_random_company(
        context: Context, supplier_alias: str, company_alias: str):
    """Will try to find an active company that doesn't have a FAS profile.

    Steps (repeat until successful):
        1 - generate a random Companies House Number
        2 - check if there's a FAS profile for it
        3 - check if such company is registered at Companies House & is active

    Once a matching company is found, then it's data will be stored in:
        context.scenario_data.companies[]

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the company used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    while True:
        # Step 1 - find an active company without a FAS profile
        company = get_active_company_without_fas_profile(company_alias)

        # Step 2 - Go to the Confirm Company page
        response = fab_ui_confirm_company.go_to(session, company)
        registered = is_already_registered(response)
        inactive = is_inactive(response)
        if registered or inactive:
            logging.warning(
                "Company '%s' is already registered or inactive, will use "
                "a different one", company.title)
            continue
        else:
            logging.warning(
                "Company '%s' is active and not registered with FAB",
                company.title)
            context.response = response
            break

    # Step 3 - check if we're on the Confirm Company page
    fab_ui_confirm_company.should_be_here(response, company)

    # Step 4 - store Company, CSRF token & associate Actor with Company
    context.add_company(company)
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    context.set_company_for_actor(supplier_alias, company_alias)


def reg_confirm_company_selection(
        context: Context, supplier_alias: str, company_alias: str):
    """Will confirm that the selected company is the right one.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the company used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    token = actor.csrfmiddlewaretoken
    has_sso_account = actor.has_sso_account
    session = actor.session
    company = context.get_company(company_alias)

    # Step 1 - confirm the selection of the company
    response = fab_ui_confirm_company.confirm_company_selection(
        session, company, token)
    context.response = response

    # Step 2 - check if we're on the Confirm Export Status page
    fab_ui_confirm_export_status.should_be_here(response)
    if not has_sso_account:
        fab_ui_confirm_export_status.should_see_info_about_sso_account(response)

    logging.debug("Confirmed selection of Company: %s", company.number)

    # Step 3 - extract & store CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def reg_supplier_is_not_ready_to_export(context, supplier_alias):
    """Supplier decides that her/his company is not ready to export.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    # Step 1 - Submit the form with No Intention to Export
    response = fab_ui_confirm_export_status.submit(
        session, token, exported=False)

    # Step 2 - store response & check it
    context.response = response
    check_response(response, 200)


def reg_confirm_export_status(
        context: Context, supplier_alias: str, exported: bool):
    """Will confirm the current export status of selected unregistered company.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param exported: True is exported in the past, False if not
    """
    actor = context.get_actor(supplier_alias)
    has_sso_account = actor.has_sso_account
    session = actor.session
    token = actor.csrfmiddlewaretoken
    context.exported = exported

    response = fab_ui_confirm_export_status.submit(session, token, exported)
    context.response = response

    if has_sso_account:
        logging.debug("Supplier already has a SSO account")
        fab_ui_build_profile_basic.should_be_here(response)
    else:
        logging.debug("Supplier doesn't have a SSO account")
        sso_ui_register.should_be_here(response)
        token = extract_csrf_middleware_token(response)
        context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def reg_create_sso_account(context, supplier_alias, alias):
    """Will create a SSO account for selected company.

    NOTE:
    Will use credentials randomly generated at Actor's initialization.
    It will also store final response in `context`

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(alias)
    exported = context.exported

    # Submit SSO Registration form with Supplier's & Company's required details
    context.response = sso_ui_register.submit(actor, company, exported)


def reg_open_email_confirmation_link(context, supplier_alias):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
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
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    form_action_value = extract_confirm_email_form_action(response)
    context.form_action_value = form_action_value


def reg_supplier_confirms_email_address(context, supplier_alias):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response


def bp_provide_company_details(context, supplier_alias):
    """Build Profile - Provide company details: website (optional), keywords
    and number of employees.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    company_alias = company.alias

    # Step 0 - generate random details & update Company matching details
    # Need to get Company details after updating it in the Scenario Data
    size = random.choice(NO_OF_EMPLOYEES)
    website = "http://{}.{}".format(rare_word(min_length=15), rare_word())
    keywords = ", ".join(sentence().split())
    context.set_company_details(
        company_alias, no_employees=size, website=website, keywords=keywords
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
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def bp_select_random_sector_and_export_to_country(context, supplier_alias):
    """Build Profile - Randomly select one of available sectors our company is
    interested in working in.

    NOTE:
    This will set `context.details` which will contain company details extracted
    from the page displayed after Supplier selects the sector.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    sector = random.choice(SECTORS)
    country = COUNTRIES[random.choice(list(COUNTRIES))]
    other = ""

    # Step 1 - Submit the Choose Your Sector form
    response = fab_ui_build_profile_sector.submit(actor, sector, country, other)
    context.response = response

    # Step 2 - check if Supplier is on Confirm Address page
    fab_ui_build_profile_address.should_be_here(response)
    logging.debug("Supplier is on the Your company address page")

    # Step 3 - extract & store CSRF token and company's address details
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def bp_provide_full_name(context, supplier_alias):
    """Build Profile - Provide Supplier's full name, which will be use when
    sending verification letter.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Submit Supplier's Full Name
    response = fab_ui_build_profile_address.submit(actor)
    context.response = response

    # Step 2 - check if Supplier is on the We've sent you a verification letter
    fab_ui_build_profile_verification_letter.should_be_here(response)
    logging.debug("Supplier is on the We've sent you verification letter page")

    # STEP 3 - Click on the "View or amend your company profile" link
    # use previous url as the referer link
    response = fab_ui_build_profile_verification_letter.go_to_profile(session)
    context.response = response

    # Step 4 - check if Supplier is on the FAB profile page
    fab_ui_profile.should_see_missing_description(response)


def prof_set_company_description(context, supplier_alias):
    """Edit Profile - Will set company description.

    This is quasi-mandatory (*) step before Supplier can verify the company with
    the code sent in a letter.

    (*) it's quasi mandatory, because Supplier can actually go to the company
    verification page using the link provided in the letter without the need
    to set company description.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - go to the "Set Company Description" page
    response = fab_ui_edit_description.go_to(session)

    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    logging.debug("Supplier is on the Set Company Description page")

    # Step 2 - Submit company description
    summary = sentence()
    description = sentence()
    response = fab_ui_edit_description.submit(
        session, token, summary, description)
    context.response = response

    # Step 3 - check if Supplier is on Profile page
    fab_ui_profile.should_see_profile_is_not_verified(response)

    # Step 4 - update company details in Scenario Data
    context.set_company_details(
        actor.company_alias, summary=summary, description=description)
    logging.debug("Supplier is back to the Profile Page")


def prof_verify_company(context, supplier_alias):
    """Will verify the company by submitting the verification code that is sent
    by post to the company's address.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session

    # STEP 0 - get the verification code from DB
    verification_code = get_verification_code(company.number)

    # STEP 1 - go to the "Verify your company" page
    response = fab_ui_verify_company.go_to(session)
    context.response = response

    # STEP 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

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


def prof_view_published_profile(context, supplier_alias):
    """Whilst being of FAB company profile page it will `click` on
    the `View published profile` link.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # STEP 1 - go to the "View published profile" page
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    logging.debug("Supplier is on the company's FAS page")


def prof_attempt_to_sign_in_to_fab(context, supplier_alias):
    """Try to sign in to FAB as a Supplier without verified email address.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign In page
    response = sso_ui_login.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on SSO Login page & extract CSRF token
    sso_ui_login.should_be_here(response)
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"):
        assert response.cookies.get("sso_display_logged_in") == "false"
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 3 - submit the login form
    response = sso_ui_login.login(actor, token)
    context.response = response


def prof_sign_out_from_fab(context, supplier_alias):
    """Sign out from Find a Buyer.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign Out confirmation page
    response = sso_ui_logout.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on Log Out page & extract CSRF token
    sso_ui_logout.should_be_here(response)
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 3 - log out
    response = sso_ui_logout.logout(session, token)
    context.response = response

    # Step 4 - check if Supplier is on FAB Landing page & is logged out
    fab_ui_landing.should_be_here(response)
    fab_ui_landing.should_be_logged_out(response)


def prof_sign_in_to_fab(context, supplier_alias):
    """Sign in to Find a Buyer.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign In page
    response = sso_ui_login.go_to(session)
    context.response = response

    # Step 2 - check if Supplier is on the SSO Login page
    sso_ui_login.should_be_here(response)
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 3 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 4 - submit the login form
    response = sso_ui_login.login(actor, token)
    context.response = response

    # Step 5 - check if Supplier is on the FAB profile page
    fab_ui_profile.should_be_here(response)
    with assertion_msg(
            "Found sso_display_logged_in cookie in the response. Maybe user is "
            "still logged in?"):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
            "Found directory_sso_dev_session cookie in the response. Maybe user"
            " is still logged in?"):
        assert "directory_sso_dev_session" not in response.cookies


def reg_create_standalone_sso_account(context: Context, supplier_alias: str):
    """Will create a standalone SSO/great.gov.uk account.

    NOTE:
    There will be no association between this account and any company.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1: Go to the SSO/great.gov.uk registration page
    response = sso_ui_register.go_to(session)
    context.response = response

    # Step 2: Check if User is not logged in
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"):
        assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 3: POST SSO accounts/signup/
    response = sso_ui_register.submit_no_company(actor)
    context.response = response

    # Step 3: Check if Supplier is on Verify your email page & is not logged in
    sso_ui_verify_your_email.should_be_here(response)
    with assertion_msg(
            "It looks like user is still logged in, as the "
            "sso_display_logged_in cookie is not equal to False"):
        assert response.cookies.get("sso_display_logged_in") == "false"


def sso_supplier_confirms_email_address(context, supplier_alias):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    form_action_value = context.form_action_value

    # STEP 1 - Submit "Confirm your email address" form
    response = sso_ui_confim_your_email.confirm(actor, form_action_value)
    context.response = response

    # STEP 2 - Check if Supplier if on SSO Profile Landing page
    profile_ui_landing.should_be_here(response)

    # STEP 3 - Update Actor's data
    context.set_actor_has_sso_account(supplier_alias, True)


def sso_go_to_create_trade_profile(context, supplier_alias):
    """Follow the 'Create a trade profile' button on the "Find a Buyer" tab.

    NOTE:
    It's assumed that Supplier already has a standalone SSO/great.gov.uk account

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Go to "Find a Buyer" tab
    response = profile_ui_find_a_buyer.go_to(session)
    context.response = response
    profile_ui_find_a_buyer.should_see_get_a_trade_profile(response)

    # Step 2 - Click on "Create a trade profile" button
    response = profile_ui_find_a_buyer.go_to_create_a_trade_profile(session)
    context.response = response
    fab_ui_landing.should_be_here(response)


def prof_upload_logo(context, supplier_alias, picture: str):
    """Upload Company's logo & extract newly uploaded logo image URL.

    NOTE:
    picture must represent file stored in ./tests/functional/files

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param picture: name of the picture file stored in ./tests/functional/files
    :type  picture: str
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
        actor.company_alias, picture=picture, hash=md5_hash, url=logo_url)


def prof_upload_unsupported_file_as_logo(context, supplier_alias, file):
    """Try to upload unsupported file type as Company's logo.

    NOTE:
    file must exist in ./tests/functional/files

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param file: name of the file stored in ./tests/functional/files
    :type  file: str
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


def prof_supplier_uploads_logo(context, supplier_alias, picture):
    """Upload a picture and set it as Company's logo.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param picture: name of the picture file stored in ./tests/functional/files
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - go to Upload Logo page
    response = fab_ui_upload_logo.go_to(session)
    context.response = response

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 3 - upload the logo
    prof_upload_logo(context, supplier_alias, picture)


def prof_to_upload_unsupported_logos(
        context: Context, supplier_alias: str, table: Table):
    """Upload a picture and set it as Company's logo.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param table: context.table containing data table
                  see: https://pythonhosted.org/behave/gherkin.html#table
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    files = [row['file'] for row in table]
    rejections = []
    for file in files:
        fab_ui_upload_logo.go_to(session)
        rejected = prof_upload_unsupported_file_as_logo(
            context, supplier_alias, file)
        rejections.append(rejected)
    context.rejections = rejections


def prof_update_company_details(
        context: Context, supplier_alias: str, table_of_details: Table):
    """Update selected Company's details.

    NOTE:
    `table_of_details` contains names of details to update.
    Passing `table_of_details` can be avoided as we already have access to
    `context` object, yet in order to be more explicit, we're making it
    a mandatory argument.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param table_of_details: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
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
    countries = DETAILS["COUNTRIES"] in details_to_update

    # Steps 1 - Go to the FAB Edit Company's details page
    response = fab_ui_edit_details.go_to(session)
    context.response = response

    # Step 2 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 3 - Update company's details
    response, new_details = fab_ui_edit_details.update_details(
        actor, company, title=title, keywords=keywords,
        website=website, size=size)
    context.response = response

    # Step 4 - Supplier should be on Edit Profile page
    fab_ui_profile.should_be_here(response)

    # Step 5 - Go to the Edit Sector page
    response = fab_ui_edit_sector.go_to(session)
    context.response = response

    # Step 5 - extract CSRF token
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 6 - Update company's sector
    response, new_sector, new_countries = fab_ui_edit_sector.update(
        actor, company, update_sector=sector, update_countries=countries)
    context.response = response

    # Step 7 - Check if Supplier is on FAB Profile page
    fab_ui_profile.should_be_here(response)

    # Step 7 - update company's details stored in context.scenario_data
    context.set_company_details(
        actor.company_alias, title=new_details.title,
        website=new_details.website, keywords=new_details.keywords,
        no_employees=new_details.no_employees, sector=new_sector,
        export_to_countries=new_countries)
    logging.debug(
        "%s successfully updated basic Company's details: title=%s, website=%s,"
        " keywords=%s, number of employees=%s, sector=%s, countries=%s",
        supplier_alias, new_details.title, new_details.website,
        new_details.keywords, new_details.no_employees, new_sector,
        new_countries)


def prof_add_online_profiles(
        context: Context, supplier_alias: str, online_profiles: Table):
    """Update links to Company's Online Profiles.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param online_profiles: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
    """
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

    # Step 2 - Extract CSRF token
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)

    # Step 3 - Update links to Online Profiles
    response, new_details = fab_ui_edit_online_profiles.update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter)
    context.response = response

    # Step 4 - Check if Supplier is on FAB Profile page
    fab_ui_profile.should_be_here(response)

    # Step 5 - Update company's details stored in context.scenario_data
    context.set_company_details(
        company.alias, facebook=new_details.facebook,
        linkedin=new_details.linkedin, twitter=new_details.twitter)
    logging.debug(
        "%s set Company's Online Profile links to: Facebook=%s, LinkedId=%s, "
        "Twitter=%s", supplier_alias, new_details.facebook,
        new_details.linkedin, new_details.twitter)


def prof_add_invalid_online_profiles(
        context: Context, supplier_alias: str, online_profiles: Table):
    """Attempt to update links to Company's Online Profiles using invalid URLs.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param online_profiles: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
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

    # Step 2 - Extract CSRF token
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)

    # Step 3 - update links to Online Profiles
    logging.debug(
        "Will use following invalid URLs to Online Profiles: %s %s %s",
        facebook_url if facebook else "", linkedin_url if linkedin else "",
        twitter_url if twitter else "")
    response, _ = fab_ui_edit_online_profiles.update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin,
        twitter=twitter, specific_facebook=facebook_url,
        specific_linkedin=linkedin_url, specific_twitter=twitter_url)
    context.response = response


def prof_remove_links_to_online_profiles(context, supplier_alias):
    """Will remove links to existing Online Profiles.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    response = fab_ui_edit_online_profiles.remove_links(
        actor, company, facebook=facebook, linkedin=linkedin, twitter=twitter)
    context.response = response


def prof_add_case_study(context, supplier_alias, case_alias):
    """Will add a complete case study (all fields will be filled out).

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param case_alias: alias of the Case Study used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    case_study = random_case_study_data(case_alias)

    # Step 1 - go to "Add case study" form & extract CSRF token
    response = fab_ui_case_study_basic.go_to(session)
    context.response = response
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
        context: Context, supplier_alias: str, case_alias: str):
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    # get content from last response (which contains FAB Profile Page)
    content = context.response.content.decode("utf-8")

    # Step 0 - extract links to Case Studies and do a crude mapping to
    # Case Study titles.
    css_selector_titles = ("div.ed-company-profile-sector-case-study-container"
                           ".company-profile-module-container h4::text")
    css_selector = ("div.row-fluid.ed-company-profile-sector-case-study-inner "
                    "p + a::attr(href)")
    titles = Selector(text=content).css(css_selector_titles).extract()
    links = Selector(text=content).css(css_selector).extract()
    case_link_mappings = {k: v for (k, v) in zip(titles, links)}
    current = company.case_studies[case_alias]
    current_link = case_link_mappings[current.title]
    current_number = int(current_link.split('/')[-1])
    logging.debug(
        "Extracted link for case study: %s is: %s", case_alias, current_link)

    # Step 1 - generate new case study data
    new_case = random_case_study_data(case_alias)
    logging.debug("Now will replace case study data with: %s", new_case)

    # Step 2 - go to specific "Case study" page form & extract CSRF token
    response = fab_ui_case_study_basic.go_to(
        session, case_number=current_number)
    context.response = response
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
        "'%s'", case_alias, current.title, current_link)


def fas_search_using_company_details(
        context: Context, buyer_alias: str, company_alias: str, *,
        table_of_details: Table = None):
    """Search for Company on FAS using it's all or selected details.

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the Company used in the scope of the scenario
    :param table_of_details: (optional) a table with selected company details
                             which will be used in search
    """
    actor = context.get_actor(buyer_alias)
    session = actor.session
    company = context.get_company(company_alias)
    keys = [
        'title', 'number', 'summary', 'description', 'website', 'keywords',
        'facebook', 'linkedin', 'twitter'
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
        buyer_alias, company.title, search_terms)
    for term_name in search_terms:
        term = search_terms[term_name]
        response = fas_ui_find_supplier.go_to(session, term=term)
        context.response = response
        number_of_pages = get_number_of_search_result_pages(response)
        for page_number in range(1, number_of_pages + 1):
            search_responses[term_name] = response
            found = fas_ui_find_supplier.should_see_company(
                response, company.title)
            search_results[term_name] = found
            if found:
                logging.debug(
                    "Found Supplier '%s' on FAS using '%s' : '%s' on %d page "
                    "out of %d", company.title, term_name, term, page_number,
                    number_of_pages)
                break
            else:
                logging.debug(
                    "Couldn't find Supplier '%s' on the %d page out of %d of "
                    "FAS search results. Search was done using '%s' : '%s'",
                    company.title, page_number, number_of_pages, term_name,
                    term)
                next_page = page_number + 1
                if next_page <= number_of_pages:
                    response = fas_ui_find_supplier.go_to(
                        session, term=term, page=next_page)
                else:
                    logging.debug("Couldn't find the Supplier even on the last "
                                  "page of the search results")
    context.search_results = search_results
    context.search_responses = search_responses


def fas_view_pages_in_selected_language(
        context: Context, buyer_alias: str, pages_table: Table, language: str):
    """View specific FAS pages in selected language.

    NOTE:
    This will store a dict with all page views responses in context.views

    :param context: behave `context` object
    :param buyer_alias: alias of the Buyer Actor
    :param pages_table: a table with FAS pages to view
    :param language: expected language of the view FAS page content
    """
    pages = [row['page'] for row in pages_table]
    views = {}
    for page_name in pages:
        actor = context.get_actor(buyer_alias)
        session = actor.session
        language_code = get_language_code(language)
        page_url = get_fas_page_url(page_name, language_code=language_code)
        response = make_request(Method.GET, page_url, session=session)
        views[page_name] = response
    context.views = views


def fas_search_with_empty_query(context, buyer_alias):
    actor = context.get_actor(buyer_alias)
    session = actor.session
    context.response = fas_ui_find_supplier.go_to(session, term="")


def fas_should_be_told_about_empty_search_results(context, buyer_alias):
    fas_ui_find_supplier.should_see_no_matches(context.response)
    logging.debug(
        "%s was told that the search did not match any UK trade profiles",
        buyer_alias)


def fas_send_feedback_request(
        context: Context, buyer_alias: str, page_name: str):
    actor = context.get_actor(buyer_alias)
    session = actor.session
    referer_url = get_fas_page_url(page_name)

    # Step 1: generate random form data for our Buyer
    feedback = random_feedback_data(email=actor.email)

    # Step 2: submit the form
    response = fas_ui_feedback.submit(session, feedback, referer=referer_url)
    context.response = response
    logging.debug("% submitted the feedback request", buyer_alias)


def fas_feedback_request_should_be_submitted(
        context: Context, buyer_alias: str):
    response = context.response
    fas_ui_feedback.should_see_feedback_submission_confirmation(response)
    logging.debug(
        "% was told that the feedback request has been submitted", buyer_alias)


def can_find_supplier_by_term(
        session: Session, name: str, term: str, term_type: str) \
        -> (bool, Response):
    """

    :param session: Buyer's session object
    :param name: sought Supplier name
    :param term: a text used to find the Supplier
    :param term_type: type of the term, e.g.: product, service, keyword etc.
    :return: a tuple with search result (True/False) and last search Response
    """
    found = False
    response = fas_ui_find_supplier.go_to(session, term=term)
    number_of_pages = get_number_of_search_result_pages(response)
    if number_of_pages == 0:
        return found, response
    for page_number in range(1, number_of_pages + 1):
        found = fas_ui_find_supplier.should_see_company(response, name)
        if found:
            break
        else:
            logging.debug(
                "Couldn't find Supplier '%s' on the %d page out of %d of "
                "FAS search results. Search was done using '%s' : '%s'",
                name, page_number, number_of_pages, term_type, term)
            next_page = page_number + 1
            if next_page <= number_of_pages:
                response = fas_ui_find_supplier.go_to(
                    session, term=term, page=next_page)
            else:
                logging.debug(
                    "Couldn't find the Supplier even on the last page of the "
                    "search results")
    return found, response


def fas_search_with_product_service_keyword(
        context: Context, buyer_alias: str, search_table: Table):
    """Search for Suppliers with one of the following:
    * Product name
    * Service name
    * keyword

    NOTE: this will add a dictionary `search_results` to `context`

    :param context: behave `context` object
    :param buyer_alias: alias of the Buyer Actor
    :param search_table: a table with FAS pages to view
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
            term_type = search_term['type']
            term = search_term['term']
            logging.debug(
                "%s is searching for company '%s' using %s term '%s'",
                buyer_alias, company, term_type, term)
            found, response = can_find_supplier_by_term(
                session, company, term, term_type)
            search_term['found'] = found
            search_term['response'] = response

    context.search_results = search_results
