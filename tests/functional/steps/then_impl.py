# -*- coding: utf-8 -*-
"""Then step implementations"""
import email
import inspect
import logging
from collections import defaultdict
from statistics import median

from behave.model import Table
from behave.runner import Context
from requests import Response
from retrying import retry
from scrapy import Selector

from tests import get_absolute_url
from tests.functional.pages import (
    fas_ui_contact,
    fas_ui_find_supplier,
    fas_ui_industries,
    fas_ui_profile,
    profile_about,
    profile_edit_company_profile,
    profile_edit_online_profiles,
    profile_find_a_buyer,
    profile_ui_landing,
    sso_ui_invalid_password_reset_link,
    sso_ui_logout,
    sso_ui_password_reset,
    sso_ui_verify_your_email,
)
from tests.functional.pages.fab import (
    fab_ui_account_remove_collaborator,
    fab_ui_build_profile_basic,
    fab_ui_confirm_identity,
    fab_ui_verify_company,
)
from tests.functional.registry import get_fabs_page_object
from tests.functional.steps import has_action
from tests.functional.utils.generic import (
    MailGunEvent,
    MailGunService,
    assertion_msg,
    check_hash_of_remote_file,
    detect_page_language,
    extract_csrf_middleware_token,
    extract_link_with_invitation_for_collaboration,
    extract_link_with_ownership_transfer_request,
    extract_logo_url,
    extract_plain_text_payload,
    find_mail_gun_events,
    get_language_code,
    get_number_of_search_result_pages,
    mailgun_find_email_with_ownership_transfer_request,
    mailgun_find_email_with_request_for_collaboration,
    surround,
)
from tests.functional.utils.gov_notify import (
    get_password_reset_link,
    get_verification_link,
)
from tests.settings import (
    FAS_LOGO_PLACEHOLDER_IMAGE,
    FAS_MESSAGE_FROM_BUYER_SUBJECT,
    SEARCHABLE_CASE_STUDY_DETAILS,
)


def reg_sso_account_should_be_created(response: Response, supplier_alias: str):
    """Will verify if SSO account was successfully created.

    Note:
    It's a very crude check, as it will only check if the response body
    contains selected phrases.
    """
    sso_ui_verify_your_email.should_be_here(response)
    logging.debug(
        "Successfully created new SSO account for %s", supplier_alias
    )


def reg_should_get_verification_email(context: Context, alias: str):
    """Will check if the Supplier received an email verification message."""
    logging.debug("Searching for an email verification message...")
    actor = context.get_actor(alias)
    link = get_verification_link(actor.email)
    context.update_actor(alias, email_confirmation_link=link)


def bp_should_be_prompted_to_build_your_profile(
    context: Context, supplier_alias: str
):
    fab_ui_build_profile_basic.should_be_here(context.response)
    logging.debug(
        "%s is on the 'Build and improve your profile' page", supplier_alias
    )
    token = extract_csrf_middleware_token(context.response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)


def prof_should_be_told_about_missing_description(
    response: Response, supplier_alias: str
):
    profile_edit_company_profile.should_see_missing_description(response)
    logging.debug("%s was told about missing description", supplier_alias)


def fas_should_be_on_profile_page(context, supplier_alias, company_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    fas_ui_profile.should_be_here(context.response, number=company.number)
    logging.debug(
        "%s is on the %s company's FAS page", supplier_alias, company_alias
    )


def fas_check_profiles(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    # Step 1 - go to company's profile page on FAS
    response = fas_ui_profile.go_to(actor.session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    # Step 2 - check if links to online profile are visible
    fas_ui_profile.should_see_online_profiles(company, response)
    logging.debug(
        "%s can see all expected links to Online Profiles on "
        "FAS Company's Directory Profile Page",
        supplier_alias,
    )


def reg_supplier_has_to_verify_email_first(
    context: Context, supplier_alias: str
):
    sso_ui_verify_your_email.should_be_here(context.response)
    logging.debug(
        "%s was told that her/his email address has to be verified "
        "first before being able to Sign In",
        supplier_alias,
    )


def sso_should_be_signed_in_to_sso_account(
    context: Context, supplier_alias: str
):
    response = context.response
    with assertion_msg(
        "Expected profile_sessionid cookie to be set. It looks like "
        "user is not logged in"
    ):
        assert response.cookies.get("profile_sessionid") is not None
    with assertion_msg(
        "Response doesn't contain 'Sign out' button. It looks "
        "like user is not logged in"
    ):
        assert "Sign out" in response.content.decode("utf-8")
    logging.debug("%s is logged in to the SSO account", supplier_alias)


def sso_should_be_signed_out_from_sso_account(
    context: Context, supplier_alias: str
):
    """Sign out from SSO."""
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign Out confirmation page
    next_param = get_absolute_url("profile:landing")
    response = sso_ui_logout.go_to(session, next_param=next_param)
    context.response = response

    # Step 2 - check if Supplier is on Log Out page & extract CSRF token
    sso_ui_logout.should_be_here(response)
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - log out
    next_param = get_absolute_url("profile:landing")
    response = sso_ui_logout.logout(session, token, next_param=next_param)
    context.response = response

    # Step 4 - check if Supplier is on SSO landing page
    profile_ui_landing.should_be_here(response)
    profile_ui_landing.should_be_logged_out(response)

    # Step 5 - reset requests Session object
    context.reset_actor_session(supplier_alias)


def profile_should_be_told_about_invalid_links(
    context: Context, supplier_alias: str
):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    profile_edit_online_profiles.should_see_errors(
        context.response, facebook=facebook, linkedin=linkedin, twitter=twitter
    )
    logging.debug(
        "%s was not able to set Company's Online Profile links using invalid "
        "URLs to: %s %s %s",
        supplier_alias,
        "Facebook" if facebook else "",
        "LinkedIn" if linkedin else "",
        "Twitter" if twitter else "",
    )


def profile_should_see_all_case_studies(context: Context, supplier_alias: str):
    """Check if Supplier can see all case studies on FAB profile page."""
    actor = context.get_actor(supplier_alias)
    case_studies = context.get_company(actor.company_alias).case_studies
    profile_edit_company_profile.should_see_case_studies(case_studies, context.response)


def fas_should_see_all_case_studies(context: Context, supplier_alias: str):
    """Check if Supplier can see all case studies on FAS profile page."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    response = fas_ui_profile.go_to(actor.session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    case_studies = context.get_company(actor.company_alias).case_studies
    fas_ui_profile.should_see_case_studies(case_studies, response)
    logging.debug(
        "%s can see all %d Case Studies on FAS Company's "
        "Directory Profile Page",
        supplier_alias,
        len(case_studies),
    )


def profile_should_see_logo_picture(context: Context, supplier_alias: str):
    """Will check if Company's Logo visible on FAB profile page is the same as
    the uploaded one.
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    logo_url = company.logo_url
    logo_hash = company.logo_hash
    logo_picture = company.logo_picture

    logging.debug(
        "Fetching logo image visible on the %s's FAB profile page",
        company.title,
    )
    check_hash_of_remote_file(logo_hash, logo_url)
    logging.debug(
        "The Logo visible on the %s's FAB profile page is the same "
        "as uploaded %s",
        company.title,
        logo_picture,
    )


def fas_should_see_png_logo_thumbnail(context: Context, supplier_alias: str):
    """Will check if Company's PNG thumbnail logo visible on FAS profile."""
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    visible_logo_url = extract_logo_url(response, fas=True)
    placeholder = FAS_LOGO_PLACEHOLDER_IMAGE

    with assertion_msg(
        "Expected company logo but got image placeholder '%s'",
        visible_logo_url,
    ):
        assert visible_logo_url != placeholder
    with assertion_msg(
        "Expected PNG logo thumbnail, but got: %s", visible_logo_url
    ):
        assert visible_logo_url.lower().endswith(".png")
    context.set_company_logo_detail(actor.company_alias, url=visible_logo_url)
    logging.debug("Set Company's logo URL to: %s", visible_logo_url)


def fas_should_see_different_png_logo_thumbnail(
    context: Context, actor_alias: str
):
    """Will check if Company's Logo visible on FAS profile page is the same as
    the one uploaded on FAB.
    """
    actor = context.get_actor(actor_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    fas_logo_url = company.logo_url

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    fas_ui_profile.should_be_here(response)
    visible_logo_url = extract_logo_url(response, fas=True)
    placeholder = FAS_LOGO_PLACEHOLDER_IMAGE

    with assertion_msg(
        "Expected company logo but got image placeholder", visible_logo_url
    ):
        assert visible_logo_url != placeholder
    with assertion_msg(
        "Expected to see other logo thumbnail than the previous one '%s'.",
        visible_logo_url,
    ):
        assert visible_logo_url != fas_logo_url
    with assertion_msg(
        "Expected PNG logo thumbnail, but got: %s", visible_logo_url
    ):
        assert visible_logo_url.lower().endswith(".png")


def profile_all_unsupported_files_should_be_rejected(
    context: Context, supplier_alias: str
):
    """Check if all unsupported files were rejected upon upload as company logo

    NOTE:
    This require `context.rejections` to be set.
    It should be a list of bool values.
    """
    assert hasattr(context, "rejections")
    with assertion_msg(
        "Some of the uploaded files that should be marked as unsupported "
        "were actually accepted. Please check the logs for more details"
    ):
        assert all(context.rejections)
    logging.debug(
        "All files of unsupported types uploaded by %s were rejected".format(
            supplier_alias
        )
    )


def profile_should_see_online_profiles(context: Context, supplier_alias: str):
    """Check if Supplier can see all online Profiles on FAB Profile page."""
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    response = context.response
    profile_edit_company_profile.should_see_online_profiles(company, response)


def profile_no_links_to_online_profiles_are_visible(
    context: Context, supplier_alias: str
):
    """Supplier should't see any links to Online Profiles on FAB Profile page.
    """
    response = context.response
    profile_edit_company_profile.should_not_see_links_to_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAB Profile page",
        supplier_alias,
    )


def fas_no_links_to_online_profiles_are_visible(
    context: Context, supplier_alias: str
):
    """Supplier should't see any links to Online Profiles on FAS Profile page.
    """
    response = context.response
    fas_ui_profile.should_not_see_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAS Profile page",
        supplier_alias,
    )


def profile_profile_is_published(context: Context, supplier_alias: str):
    """Check if Supplier was told that Company's profile is verified."""
    response = context.response
    profile_edit_company_profile.should_see_profile_is_published(response)
    logging.debug("%s was told that the profile is verified.", supplier_alias)


def profile_should_see_company_details(
        context: Context, supplier_alias: str, page_name: str
):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    page = get_fabs_page_object(page_name)
    has_action(page, "go_to")
    has_action(page, "should_see_details")
    if "company_number" in inspect.getfullargspec(page.go_to).args:
        context.response = page.go_to(actor.session, company_number=company.number)
    else:
        context.response = page.go_to(actor.session)
    page.should_see_details(company, context.response, context.table)
    logging.debug(
        f"{supplier_alias} can see all expected details on {page_name}"
    )


def profile_supplier_should_be_on_landing_page(
    context: Context, supplier_alias: str
):
    """Check if Supplier is on Profile Landing page."""
    response = context.response
    profile_ui_landing.should_be_here(response)
    logging.debug("%s got to the SSO landing page.", supplier_alias)


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def fas_find_supplier_using_case_study_details(
    context: Context,
    buyer_alias: str,
    company_alias: str,
    case_alias: str,
    *,
    properties: Table = None
):
    """Find Supplier on FAS using parts of the Case Study added by Supplier.

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the sought Company
    :param case_alias: alias of the Case Study used in the search
    :param properties: (optional) table containing the names of Case Study
                       parts that will be used search. If not provided, then
                       all parts will be used except 'alias'.
    """
    actor = context.get_actor(buyer_alias)
    session = actor.session
    company = context.get_company(company_alias)
    case_study = company.case_studies[case_alias]
    keys = SEARCHABLE_CASE_STUDY_DETAILS
    if properties:
        keys = [row["search using case study's"] for row in properties]
    search_terms = {}
    for key in keys:
        if key == "keywords":
            for index, keyword in enumerate(case_study.keywords.split(", ")):
                search_terms["keyword #{}".format(index)] = keyword
        else:
            search_terms[key] = getattr(case_study, key.replace(" ", "_"))
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
        found = fas_ui_find_supplier.should_see_company(
            response, company.title
        )
        if found:
            logging.debug(
                "Found Supplier '%s' using '%s' : '%s' on 1st result page",
                company.title,
                term_name,
                term,
            )
        else:
            number_of_pages = get_number_of_search_result_pages(response)
            if number_of_pages > 1:
                for page_number in range(2, number_of_pages + 1):
                    response = fas_ui_find_supplier.go_to(
                        session, term=term, page=page_number
                    )
                    context.response = response
                    fas_ui_find_supplier.should_be_here(response)
                    found = fas_ui_find_supplier.should_see_company(
                        response, company.title
                    )
                    if found:
                        break
            else:
                with assertion_msg(
                    "Couldn't find '%s' using '%s': '%s' on the only "
                    "available search result page",
                    company.title,
                    term_name,
                    term,
                ):
                    assert False

        with assertion_msg(
            "Buyer could not find Supplier '%s' on FAS using %s: %s",
            company.title,
            term_name,
            term,
        ):
            assert found
        logging.debug(
            "Buyer found Supplier '%s' on FAS using %s: %s",
            company.title,
            term_name,
            term,
        )


def fas_supplier_cannot_be_found_using_case_study_details(
    context: Context, buyer_alias: str, company_alias: str, case_alias: str
):
    actor = context.get_actor(buyer_alias)
    session = actor.session
    company = context.get_company(company_alias)
    case_study = company.case_studies[case_alias]
    keys = SEARCHABLE_CASE_STUDY_DETAILS
    search_terms = {}
    for key in keys:
        if key == "keywords":
            for index, keyword in enumerate(case_study.keywords.split(", ")):
                search_terms["keyword #{}".format(index)] = keyword
        else:
            search_terms[key] = getattr(case_study, key)
    logging.debug(
        "Now %s will try to find '%s' using following search terms: %s",
        buyer_alias,
        company.title,
        search_terms,
    )
    for term_name in search_terms:
        term = search_terms[term_name]
        logging.debug(
            "Searching for '%s' using %s: %s",
            company.title,
            term_name,
            search_terms,
        )
        response = fas_ui_find_supplier.go_to(session, term=term)
        context.response = response
        fas_ui_find_supplier.should_be_here(response)
        found = fas_ui_find_supplier.should_not_see_company(
            response, company.title
        )
        with assertion_msg(
            "Buyer found Supplier '%s' on FAS using %s: %s",
            company.title,
            term_name,
            term,
        ):
            assert found
        logging.debug(
            "Buyer was not able to find unverified Supplier '%s' on FAS using "
            "%s: %s",
            company.title,
            term_name,
            term,
        )


def fas_should_not_find_with_company_details(
        context: Context, buyer_alias: str, company_alias: str
):
    """Check if Buyer wasn't able to find Supplier using all selected search terms

    NOTE:
    This step requires the search_results dict to be stored in context
    """
    assert hasattr(context, "search_results")
    company = context.get_company(company_alias)
    for result in context.search_results:
        # get response for specific search request. This helps to debug
        logging.debug(f"Search results: {context.search_results}")
        context.response = context.search_responses[result]
        with assertion_msg(
                "%s was able to find '%s' (alias: %s) using %s",
                buyer_alias,
                company.title,
                company_alias,
                result,
        ):
            assert not context.search_results[result]


def fas_should_find_with_company_details(
    context: Context, buyer_alias: str, company_alias: str
):
    """Check if Buyer was able to find Supplier using all selected search terms

    NOTE:
    This step requires the search_results dict to be stored in context
    """
    assert hasattr(context, "search_results")
    company = context.get_company(company_alias)
    for result in context.search_results:
        # get response for specific search request. This helps to debug
        logging.debug(f"Search results: {context.search_results}")
        context.response = context.search_responses[result]
        with assertion_msg(
            "%s wasn't able to find '%s' (alias: %s) using its '%s'",
            buyer_alias,
            company.title,
            company_alias,
            result,
        ):
            assert context.search_results[result]


def generic_pages_should_be_in_selected_language(
    context: Context,
    pages_table: Table,
    language: str,
    *,
    page_part: str = None,
    probability: float = 0.9
):
    """Check if all viewed pages contain content in expected language

    NOTE:
    This requires all responses with page views to be stored in context.views

    :param context: behave `context` object
    :param pages_table: a table with viewed FAS pages
    :param language: expected language of the view FAS page content
    :param page_part: detect language of the whole page or just the main part
    :param probability: expected probability of expected language
    """
    with assertion_msg("Required dictionary with page views is missing"):
        assert hasattr(context, "views")
    pages = [row["page"] for row in pages_table]
    views = context.views

    if page_part:
        if page_part == "main":
            main = True
        elif page_part == "whole":
            main = False
        else:
            raise KeyError(
                "Please select valid part of the page: main or whole"
            )
    else:
        main = False

    if language.lower() == "chinese":
        expected_language = "zh-cn"
    else:
        expected_language = get_language_code(language)

    results = defaultdict()
    for page_name in pages:
        response = views[page_name]
        content = response.content.decode("utf-8")
        logging.debug(
            "detecting the language of fas %s page %s", page_name, response.url
        )
        lang_detect_results = detect_page_language(content=content, main=main)
        median_results = {
            language: median(probabilities)
            for language, probabilities in lang_detect_results.items()
        }

        results[page_name] = median_results

    undetected_languages = {
        page: medians
        for page, medians in results.items()
        if expected_language not in medians
    }
    with assertion_msg(
        f"Could not detect '{expected_language}' in page content on following"
        f" pages: {undetected_languages}"
    ):
        assert not undetected_languages

    unmet_probabilities = {
        page: medians
        for page, medians in results.items()
        if medians[expected_language] < probability
    }
    with assertion_msg(
            f"Median '{expected_language}' language detection probability of "
            f"{probability} wasn't met on following pages: {unmet_probabilities}"
    ):
        assert not unmet_probabilities


def fas_should_find_all_sought_companies(context: Context, buyer_alias: str):
    """Check if Buyer was able to find Supplier using all provided terms."""
    with assertion_msg(
        "Context has no required `search_details` dict. Please check if "
        "one of previous steps sets it correctly."
    ):
        assert hasattr(context, "search_results")
    for company, results in context.search_results.items():
        for result in results:
            term = result["term"]
            term_type = result["type"]
            context.response = result["response"]
            with assertion_msg(
                "%s could not find Supplier '%s' using '%s' term '%s'",
                buyer_alias,
                company,
                term_type,
                term,
            ):
                assert result["found"]


def fas_should_be_told_that_message_has_been_sent(
    context: Context, buyer_alias: str, company_alias: str
):
    response = context.response
    company = context.get_company(company_alias)
    fas_ui_contact.should_see_that_message_has_been_sent(company, response)
    logging.debug(
        "%s was told that the message to '%s' (%s) has been sent",
        buyer_alias,
        company.title,
        company_alias,
    )


def fas_supplier_should_receive_message_from_buyer(
    context: Context, supplier_alias: str, buyer_alias: str
):
    supplier = context.get_actor(supplier_alias)
    context.response = find_mail_gun_events(
        context,
        service=MailGunService.DIRECTORY,
        to=supplier.email,
        event=MailGunEvent.ACCEPTED,
        subject=FAS_MESSAGE_FROM_BUYER_SUBJECT,
    )
    logging.debug("%s received message from %s", supplier_alias, buyer_alias)


def profile_should_see_expected_error_messages(
    context: Context, supplier_alias: str
):
    results = context.results
    for company, response, error in results:
        context.response = response
        logging.debug(f"Modified company's details: {company}")
        logging.debug(f"Response: {response}")
        logging.debug(f"Expected error message: {error}")
        with assertion_msg(
            f"Could not find expected error message: '{error}' in the response,"
            f" after submitting the form with following company details: "
            f"{company}",
        ):
            assert error in response.content.decode("utf-8")
    logging.debug("%s has seen all expected form errors", supplier_alias)


def fas_should_be_on_selected_page(
    context: Context, actor_alias: str, page_name: str
):
    response = context.response
    page_object = get_fabs_page_object(page_name)
    page_object.should_be_here(response)
    logging.debug(
        "%s successfully got to the %s FAS page", actor_alias, page_name
    )


def fas_should_see_promoted_industries(
    context: Context, actor_alias: str, table: Table
):
    industries = [row["industry"].lower() for row in table]
    response = context.response
    for industry in industries:
        fas_ui_industries.should_see_industry_section(response, industry)
    logging.debug(
        "%s can see all expected industry sections '%s'",
        actor_alias,
        industries,
    )


def fas_should_see_filtered_search_results(context: Context, actor_alias: str):
    results = context.results
    sector_filters_selector = "#id_sectors input"
    for industry, result in results.items():
        context.response = result["response"]
        content = result["response"].content.decode("utf-8")
        filters = Selector(text=content).css(sector_filters_selector).extract()
        for fil in filters:
            sector = Selector(text=fil).css("input::attr(value)").extract()[0]
            input = Selector(text=fil).css("input::attr(checked)").extract()
            checked = True if input else False
            if sector in result["sectors"]:
                with assertion_msg(
                    "Expected search results to be filtered by '%s' sector"
                    " but this filter was not checked!"
                ):
                    assert checked
            else:
                with assertion_msg(
                    "Expected search results to be filtered only by "
                    "following sectors '%s', but they are also filtered "
                    "by '%s'!",
                    ", ".join(result["sectors"]),
                    sector,
                ):
                    assert not checked
        logging.debug(
            "%s was presented with '%s' industry search results correctly "
            "filtered by following sectors: '%s'",
            actor_alias,
            industry,
            ", ".join(result["sectors"]),
        )


def fas_should_see_unfiltered_search_results(
    context: Context, actor_alias: str
):
    response = context.response
    content = response.content.decode("utf-8")
    sector_filters_selector = "#id_sectors input"
    filters = Selector(text=content).css(sector_filters_selector).extract()
    for fil in filters:
        sector = Selector(text=fil).css("input::attr(value)").extract()[0]
        selector = "input::attr(checked)"
        checked = True if Selector(text=fil).css(selector).extract() else False
        with assertion_msg(
            "Expected search results to be unfiltered but this "
            "filter was checked: '%s'",
            sector,
        ):
            assert not checked
    logging.debug("%s was shown with unfiltered search results", actor_alias)


def fas_should_see_company_once_in_search_results(
    context: Context, actor_alias: str, company_alias: str
):
    company = context.get_company(company_alias)
    results = context.results
    founds = [
        (page, result["found"])
        for page, result in results.items()
        if result["found"]
    ]
    with assertion_msg(
        "Expected to see company '%s' only once on first %d search result "
        "pages but found it %d times. On pages: %s",
        company.title,
        len(results),
        len(founds),
        founds,
    ):
        assert len(founds) == 1
    logging.debug(
        "As expected %s found company '%s' (%s) only once on first %d search "
        "result pages",
        actor_alias,
        company.title,
        company_alias,
        len(results) + 1,
    )


def fas_should_see_highlighted_search_term(
    context: Context, actor_alias: str, search_term: str
):
    response = context.response
    content = response.content.decode("utf-8")
    search_summaries_selector = ".ed-company-search-summary"
    summaries = Selector(text=content).css(search_summaries_selector).extract()
    tag = "em"
    keywords = [surround(keyword, tag) for keyword in search_term.split()]
    founds = []
    for summary in summaries:
        founds += [(keyword in summary) for keyword in keywords]

    with assertion_msg(
        "Expected to see at least 1 search result with highlighted search "
        "term: '%s'".format(", ".join(keywords))
    ):
        assert any(founds)

    logging.debug(
        "{alias} found highlighted search {term}: '{keywords}' {founds} "
        "{times} in {results} search results".format(
            alias=actor_alias,
            term="terms" if len(keywords) > 1 else "term",
            keywords=", ".join(keywords),
            founds=len([f for f in founds if f]),
            times="times" if len([f for f in founds if f]) > 1 else "time",
            results=len(summaries),
        )
    )


def fab_company_should_be_verified(context: Context, supplier_alias: str):
    response = context.response
    fab_ui_verify_company.should_see_company_is_verified(response)
    logging.debug(
        "%s saw that his company's FAB profile is verified", supplier_alias
    )


def profile_business_profile_should_be_ready_for_publishing(
        context: Context, supplier_alias: str
):
    response = context.response
    profile_edit_company_profile.should_see_profile_is_verified(response)
    logging.debug(
        f"{supplier_alias} saw that his company's Business Profile is ready to"
        f" be published on FAS",
    )


def fab_should_see_case_study_error_message(
    context: Context, supplier_alias: str
):
    results = context.results
    logging.debug(results)
    for field, value_type, case_study, response, error in results:
        context.response = response
        with assertion_msg(
            "Could not find expected error message: '%s' in the response, "
            "after submitting the add case study form with '%s' value "
            "being '%s' following and other details: '%s'",
            error,
            field,
            value_type,
            case_study,
        ):
            assert error in response.content.decode("utf-8")
    logging.debug("%s has seen all expected case study errors", supplier_alias)


def sso_should_be_told_about_password_reset(
    context: Context, supplier_alias: str
):
    sso_ui_password_reset.should_see_that_password_was_reset(context.response)
    logging.debug("%s was told that the password was reset", supplier_alias)


def sso_should_get_password_reset_email(context: Context, supplier_alias: str):
    """Will check if the Supplier received an email verification message."""
    logging.debug("Searching for a password reset email...")
    actor = context.get_actor(supplier_alias)
    link = get_password_reset_link(actor.email)
    context.update_actor(supplier_alias, password_reset_link=link)


def sso_should_see_invalid_password_reset_link_error(
    context: Context, supplier_alias: str
):
    sso_ui_invalid_password_reset_link.should_be_here(context.response)
    logging.debug(
        "%s was told about invalid password reset link", supplier_alias
    )


def should_be_at(context: Context, supplier_alias: str, page_name: str):
    response = context.response
    page = get_fabs_page_object(page_name.lower())
    page.should_be_here(response)
    logging.debug("%s is on '%s' page", supplier_alias, page_name)


def should_see_selected_pages(context: Context, actor_alias: str):
    results = context.results
    for page_name, response in results.items():
        context.response = response
        page = get_fabs_page_object(page_name.lower())
        page.should_be_here(response)
        logging.debug(
            "%s successfully got to '%s' page", actor_alias, page_name
        )


def fab_should_be_asked_about_verification_form(
    context: Context, supplier_alias: str
):
    fab_ui_confirm_identity.should_be_here(context.response)
    logging.debug(
        "%s was asked about the form of identity verification", supplier_alias
    )


def should_see_message(context: Context, actor_alias: str, message: str):
    content = context.response.content.decode("utf-8")
    with assertion_msg(
        "Response content doesn't contain expected message: '%s'", message
    ):
        assert message in content
    logging.debug("%s saw expected message: '%s'", actor_alias, message)


def sso_should_get_request_for_collaboration_email(
    context: Context, actor_aliases: str, company_alias: str
):
    actor_aliases = [alias.strip() for alias in actor_aliases.split(",")]
    for actor_alias in actor_aliases:
        actor = context.get_actor(actor_alias)
        company = context.get_company(company_alias)
        mailgun_response = mailgun_find_email_with_request_for_collaboration(
            context, actor, company
        )
        raw_message_payload = mailgun_response["body-mime"]
        email_message = email.message_from_string(raw_message_payload)
        payload = extract_plain_text_payload(email_message)
        link = extract_link_with_invitation_for_collaboration(payload)
        context.update_actor(
            actor_alias,
            invitation_for_collaboration_link=link,
            company_alias=company_alias,
        )


def sud_should_see_options_to_manage_users(context: Context, actor_alias: str):
    actor = context.get_actor(actor_alias)
    session = actor.session

    context.response = profile_find_a_buyer.go_to(session)
    profile_find_a_buyer.should_be_here(context.response)

    profile_find_a_buyer.should_see_options_to_manage_users(context.response)
    logging.debug("%s can see options to control user accounts", actor_alias)


def sud_should_not_see_options_to_manage_users(
    context: Context, actor_alias: str
):
    """
    Due to bug ED-2268 the first time you visit SUD pages by going directly
    to SUD "Find a Buyer" page, then you're redirected to SUD "About" page
    To circumvent this behaviour we have to go to the "About" page first, and
    then visit the SUD "Find a Buyer" page
    """
    actor = context.get_actor(actor_alias)
    session = actor.session
    context.response = profile_about.go_to(session, set_next_page=False)
    profile_about.should_be_here(context.response)

    context.response = profile_find_a_buyer.go_to(session)
    profile_find_a_buyer.should_be_here(context.response)

    profile_find_a_buyer.should_not_see_options_to_manage_users(
        context.response
    )
    logging.debug("%s can't see options to control user accounts", actor_alias)


def fab_should_get_request_for_becoming_owner(
    context: Context, new_owner_alias: str, company_alias: str
):
    actor = context.get_actor(new_owner_alias)
    company = context.get_company(company_alias)
    mailgun_response = mailgun_find_email_with_ownership_transfer_request(
        context, actor, company
    )
    raw_message_payload = mailgun_response["body-mime"]
    email_message = email.message_from_string(raw_message_payload)
    payload = extract_plain_text_payload(email_message)
    link = extract_link_with_ownership_transfer_request(payload)
    context.update_actor(
        new_owner_alias,
        ownership_request_link=link,
        company_alias=company_alias,
    )


def fab_should_not_see_collaborator(
    context: Context, supplier_alias: str, collaborators_aliases: str
):
    aliases = [alias.strip() for alias in collaborators_aliases.split(",")]
    supplier = context.get_actor(supplier_alias)
    response = fab_ui_account_remove_collaborator.go_to(supplier.session)
    context.response = response

    for collaborator_alias in aliases:
        collaborator = context.get_actor(collaborator_alias)
        fab_ui_account_remove_collaborator.should_not_see_collaborator(
            response, collaborator.email
        )


def should_not_be_able_to_access_page(
    context: Context, collaborator_alias: str, page_name: str
):
    collaborator = context.get_actor(collaborator_alias)
    page_object = get_fabs_page_object(page_name)
    response = page_object.go_to(collaborator.session)
    try:
        page_object.should_be_here(response)
        raise Exception(
            "%s was able to access '%' page", collaborator_alias, page_name
        )
    except AssertionError:
        logging.debug(
            "As expected %s could not access '%s' page. Current URL is: %s",
            collaborator_alias,
            page_name,
            response.url,
        )


def stannp_should_see_expected_details_in_verification_letter(
    context: Context, actor_alias: str, correct_details: Table
):
    actor = context.get_actor(actor_alias)
    company = context.get_company(actor.company_alias)
    letter = actor.verification_letter
    address = company.companies_house_details["address"]
    address_line_1 = address.get("address_line_1", "Fake address line 1")
    address_line_2 = address.get("address_line_2", "Fake address line 2")
    locality = address.get("address_line_2", "Fake locality")
    details_mapping = {
        "recipient name": actor.alias,
        "recipient postcode": address["postal_code"],
        "company name": company.title,
        "address line 1": address_line_1,
        "address line 2": address_line_2,
        "locality": locality,
        "verification code": company.verification_code,
        "verification link": "great.gov.uk/verify",
        "contact us link": "https://contact-us.export.great.gov.uk/",
    }
    expected_keys = [row["correct_details"] for row in correct_details]
    expected_details = {key: details_mapping[key] for key in expected_keys}
    with assertion_msg(
        "Could not find all expected details in the verification letter!:"
        "\nExpected details:\n{}\nVerification letter:\n{}".format(
            expected_details, letter
        )
    ):
        all(detail in letter for detail in expected_details.values())
    logging.debug(
        "All expected details are visible in the verification letter"
    )
