# -*- coding: utf-8 -*-
"""Then step implementations"""
import inspect
import logging
from collections import defaultdict
from statistics import median

from behave.model import Table
from behave.runner import Context
from requests import Response
from retrying import retry
from scrapy import Selector

from directory_tests_shared import URLs
from directory_tests_shared.constants import (
    FAS_LOGO_PLACEHOLDER_IMAGE,
    FAS_MESSAGE_FROM_BUYER_SUBJECT,
    PROFILE_INVITATION_MSG_SUBJECT,
    SEARCHABLE_CASE_STUDY_DETAILS,
)
from directory_tests_shared.enums import Language
from directory_tests_shared.gov_notify import (
    get_email_notification,
    get_notifications_by_subject,
    get_password_reset_link,
    get_verification_link,
)
from directory_tests_shared.utils import check_for_errors
from tests.functional.pages import (
    fab,
    fas,
    get_page_object,
    has_action,
    international,
    isd,
    profile,
    sso,
)
from tests.functional.steps.common import can_find_supplier_by_term
from tests.functional.utils.context_utils import (
    get_actor,
    get_company,
    reset_actor_session,
    set_company_logo_detail,
    update_actor,
)
from tests.functional.utils.generic import (
    assertion_msg,
    check_hash_of_remote_file,
    detect_page_language,
    extract_csrf_middleware_token,
    extract_logo_url,
    extract_page_contents,
    surround,
)


def reg_should_get_verification_email(
    context: Context, alias: str, *, subject: str = None
):
    """Will check if the Supplier received an email verification message."""
    logging.debug("Looking for an email verification message...")
    actor = get_actor(context, alias)
    link = get_verification_link(actor.email, subject=subject)
    update_actor(context, alias, email_confirmation_link=link)


def generic_should_get_email_notifications(context: Context, alias: str, subject: str):
    actor = get_actor(context, alias)
    notifications = get_notifications_by_subject(actor.email, subject=subject)
    update_actor(context, alias, notifications=notifications)


def prof_should_be_told_about_missing_description(
    response: Response, supplier_alias: str
):
    profile.edit_company_profile.should_see_missing_description(response)
    logging.debug("%s was told about missing description", supplier_alias)


def fas_should_be_on_profile_page(context, supplier_alias, company_alias):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    fas.profile.should_be_here(context.response, number=company.number)
    logging.debug("%s is on the %s company's FAS page", supplier_alias, company_alias)


def fas_check_profiles(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    # Step 1 - go to company's profile page on FAS
    response = fas.profile.go_to(actor.session, company.number)
    context.response = response
    fas.profile.should_be_here(response)
    # Step 2 - check if links to online profile are visible
    fas.profile.should_see_online_profiles(company, response)
    logging.debug(
        "%s can see all expected links to Online Profiles on "
        "FAS Company's Directory Profile Page",
        supplier_alias,
    )


def reg_supplier_has_to_verify_email_first(context: Context, supplier_alias: str):
    sso.verify_your_email.should_be_here(context.response)
    logging.debug(
        "%s was told that her/his email address has to be verified "
        "first before being able to Sign In",
        supplier_alias,
    )


def sso_should_be_signed_in_to_sso_account(context: Context, supplier_alias: str):
    response = context.response
    with assertion_msg(
        "Response doesn't contain 'Sign out' button. It looks "
        "like user is not logged in"
    ):
        assert "Sign out" in response.content.decode("utf-8")
    error = f"Missing response history in SSO login request!"
    assert response.history, error

    intermediate_headers = []
    for r in response.history:
        dev_session = r.cookies.get("directory_sso_dev_session", None)
        stage_session = r.cookies.get("sso_stage_session", None)
        sso_display_logged_in = r.cookies.get("sso_display_logged_in", None)
        cookies = {
            "url": r.url,
            "location": r.headers.get("location", None),
            "sso_session": dev_session or stage_session,
            "sso_display_logged_in": sso_display_logged_in,
        }
        intermediate_headers.append(cookies)
    logging.debug(f"SSO session cookie history: {intermediate_headers}")
    with assertion_msg(
        "Expected to see following SSO Session cookies to be set in intermediate "
        "responses: sso_display_logged_in=true and directory_sso_dev_session or "
        "sso_stage_session. It looks like user did not log in successfully!"
    ):
        assert all(
            cookies["sso_display_logged_in"] == "true"
            for cookies in intermediate_headers
        )
    logging.debug("%s is logged in to the SSO account", supplier_alias)


def sso_should_be_signed_out_from_sso_account(context: Context, supplier_alias: str):
    """Sign out from SSO."""
    actor = get_actor(context, supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign Out confirmation page
    next_param = URLs.PROFILE_LANDING.absolute
    response = sso.logout.go_to(session, next_param=next_param)
    context.response = response

    # Step 2 - check if Supplier is on Log Out page & extract CSRF token
    sso.logout.should_be_here(response)
    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)

    # Step 3 - log out
    next_param = URLs.PROFILE_LANDING.absolute
    response = sso.logout.logout(session, token, next_param=next_param)
    context.response = response

    # Step 4 - check if Supplier is on SSO landing page
    profile.about.should_be_here(response)
    profile.about.should_be_logged_out(response)

    # Step 5 - reset requests Session object
    reset_actor_session(context, supplier_alias)


def profile_should_be_told_about_invalid_links(context: Context, supplier_alias: str):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    profile.edit_online_profiles.should_see_errors(
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
    actor = get_actor(context, supplier_alias)
    case_studies = get_company(context, actor.company_alias).case_studies
    profile.edit_company_profile.should_see_case_studies(case_studies, context.response)


def fas_should_see_all_case_studies(context: Context, supplier_alias: str):
    """Check if Supplier can see all case studies on FAS profile page."""
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    response = fas.profile.go_to(actor.session, company.number)
    context.response = response
    fas.profile.should_be_here(response)
    case_studies = get_company(context, actor.company_alias).case_studies
    fas.profile.should_see_case_studies(case_studies, response)
    logging.debug(
        "%s can see all %d Case Studies on FAS Company's " "Directory Profile Page",
        supplier_alias,
        len(case_studies),
    )


def profile_should_see_logo_picture(context: Context, supplier_alias: str):
    """Will check if Company's Logo visible on FAB profile page is the same as
    the uploaded one.
    """
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    logo_url = company.logo_url
    logo_hash = company.logo_hash
    logo_picture = company.logo_picture

    logging.debug(
        "Fetching logo image visible on the %s's FAB profile page", company.title
    )
    check_hash_of_remote_file(logo_hash, logo_url)
    logging.debug(
        "The Logo visible on the %s's FAB profile page is the same " "as uploaded %s",
        company.title,
        logo_picture,
    )


def fas_should_see_png_logo_thumbnail(context: Context, supplier_alias: str):
    """Will check if Company's PNG thumbnail logo visible on FAS profile."""
    actor = get_actor(context, supplier_alias)
    session = actor.session
    company = get_company(context, actor.company_alias)

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas.profile.go_to(session, company.number)
    context.response = response
    fas.profile.should_be_here(response)
    visible_logo_url = extract_logo_url(response)
    placeholder = FAS_LOGO_PLACEHOLDER_IMAGE

    with assertion_msg(
        "Expected company logo but got image placeholder '%s'", visible_logo_url
    ):
        assert visible_logo_url != placeholder
    with assertion_msg("Expected PNG logo thumbnail, but got: %s", visible_logo_url):
        assert visible_logo_url.lower().endswith(".png")
    set_company_logo_detail(context, actor.company_alias, url=visible_logo_url)
    logging.debug("Set Company's logo URL to: %s", visible_logo_url)


def fas_should_see_different_png_logo_thumbnail(context: Context, actor_alias: str):
    """Will check if Company's Logo visible on FAS profile page is the same as
    the one uploaded on FAB.
    """
    actor = get_actor(context, actor_alias)
    session = actor.session
    company = get_company(context, actor.company_alias)
    fas_logo_url = company.logo_url

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas.profile.go_to(session, company.number)
    context.response = response
    fas.profile.should_be_here(response)
    visible_logo_url = extract_logo_url(response)
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
    with assertion_msg("Expected PNG logo thumbnail, but got: %s", visible_logo_url):
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
    logging.debug(f"All files of unsupported types uploaded by %s were rejected")


def profile_should_see_online_profiles(context: Context, supplier_alias: str):
    """Check if Supplier can see all online Profiles on FAB Profile page."""
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    response = context.response
    profile.edit_company_profile.should_see_online_profiles(company, response)


def profile_no_links_to_online_profiles_are_visible(
    context: Context, supplier_alias: str
):
    """Supplier should't see any links to Online Profiles on FAB Profile page.
    """
    response = context.response
    profile.edit_company_profile.should_not_see_links_to_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAB Profile page", supplier_alias
    )


def fas_no_links_to_online_profiles_are_visible(context: Context, supplier_alias: str):
    """Supplier should't see any links to Online Profiles on FAS Profile page.
    """
    response = context.response
    fas.profile.should_not_see_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAS Profile page", supplier_alias
    )


def profile_profile_is_published(context: Context, supplier_alias: str):
    """Check if Supplier was told that Company's profile is verified."""
    response = context.response
    profile.edit_company_profile.should_see_profile_is_published(response)
    logging.debug("%s was told that the profile is verified.", supplier_alias)


def profile_should_see_company_details(
    context: Context, supplier_alias: str, page_name: str
):
    actor = get_actor(context, supplier_alias)
    company = get_company(context, actor.company_alias)
    page = get_page_object(page_name)
    has_action(page, "go_to")
    has_action(page, "should_see_details")
    if "company_number" in inspect.getfullargspec(page.go_to).args:
        context.response = page.go_to(actor.session, company_number=company.number)
    else:
        context.response = page.go_to(actor.session)
    page.should_see_details(company, context.response, context.table)
    logging.debug(f"{supplier_alias} can see all expected details on {page_name}")


def profile_supplier_should_be_on_landing_page(context: Context, supplier_alias: str):
    """Check if Supplier is on Profile Landing page."""
    response = context.response
    profile.about.should_be_here(response)
    logging.debug("%s got to the SSO landing page.", supplier_alias)


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def fas_find_supplier_using_case_study_details(
    context: Context,
    buyer_alias: str,
    company_alias: str,
    case_alias: str,
    *,
    properties: Table = None,
    max_pages: int = 5,
):
    """Find Supplier on FAS using parts of the Case Study added by Supplier.

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the sought Company
    :param case_alias: alias of the Case Study used in the search
    :param properties: (optional) table containing the names of Case Study
                       parts that will be used search. If not provided, then
                       all parts will be used except 'alias'.
    :param max_pages: (optional) maximum number of search result pages to go
                      through
    """
    actor = get_actor(context, buyer_alias)
    session = actor.session
    company = get_company(context, company_alias)
    case_study = company.case_studies[case_alias]
    keys = SEARCHABLE_CASE_STUDY_DETAILS
    if properties:
        keys = [row["search using case study's"] for row in properties]
    search_terms = {}
    for key in keys:
        # if key == "keywords":
        #     for index, keyword in enumerate(case_study.keywords.split(", ")):
        #         search_terms[f"keyword #{index}"] = keyword
        # else:
        search_terms[key] = getattr(case_study, key.replace(" ", "_"))
    logging.debug(
        "Now %s will try to find '%s' using following search terms: %s",
        buyer_alias,
        company.title,
        search_terms,
    )

    search_results = defaultdict()
    for term_type in search_terms:
        term = search_terms[term_type]
        logging.debug(f"Looking for '{company.title}' using '{term_type}': '{term}'")
        profile_link, context.response = can_find_supplier_by_term(
            session, company.title, term, term_type, max_pages=max_pages
        )
        found = profile_link != ""
        search_results[term_type] = {"term": term, "found": found}

    logging.debug(f"Search results: {search_results}")
    not_found_by = {
        term_type: search_results
        for term_type, search_results in search_results.items()
        if not search_results["found"]
    }
    not_found_by_str = "; ".join(
        [f"{k} → {v['term']}" for k, v in not_found_by.items()]
    )
    with assertion_msg(
        f"Couldn't find '{company.title}' on FAS using following case study "
        f"details: {not_found_by_str}"
    ):
        assert not not_found_by
    logging.debug(
        f"{buyer_alias} was able to find company '{company.title} using all "
        f"case study details: {search_terms}"
    )


def fas_supplier_cannot_be_found_using_case_study_details(
    context: Context, buyer_alias: str, company_alias: str, case_alias: str
):
    actor = get_actor(context, buyer_alias)
    session = actor.session
    company = get_company(context, company_alias)
    case_study = company.case_studies[case_alias]
    keys = SEARCHABLE_CASE_STUDY_DETAILS
    search_terms = {}
    for key in keys:
        if key == "keywords":
            for index, keyword in enumerate(case_study.keywords.split(", ")):
                search_terms[f"keyword #{index}"] = keyword
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
            "Searching for '%s' using %s: %s", company.title, term_name, search_terms
        )
        response = fas.search.go_to(session, term=term)
        context.response = response
        fas.search.should_be_here(response)
        found = fas.search.should_not_see_company(response, company.title)
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
    company = get_company(context, company_alias)
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
    company = get_company(context, company_alias)
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


def generic_content_of_viewed_pages_should_in_selected_language(
    context: Context, language: str, *, page_part: str = None, probability: float = 0.9
):
    """Check if all viewed pages contain content in expected language

    NOTE:
    This requires all responses with page views to be stored in context.views

    :param context: behave `context` object
    :param language: expected language of the view FAS page content
    :param page_part: detect language of the whole page or just the main part
    :param probability: expected probability of expected language
    """
    with assertion_msg("Required dictionary with page views is missing"):
        assert hasattr(context, "views")
    views = context.views
    page_names = (
        [row["page"] for row in context.table] if context.table else views.keys()
    )

    if page_part:
        if page_part == "main":
            main = True
        elif page_part == "whole":
            main = False
        else:
            raise KeyError("Please select valid part of the page: main or whole")
    else:
        main = False

    if language.lower() == "chinese":
        expected_language_code = "zh-cn"
    elif language.lower() == "english":
        expected_language_code = "en"
    else:
        expected_language_code = Language[language.upper()].value

    results = defaultdict()
    for page_name in page_names:
        response = views[page_name]
        content = response.content.decode("utf-8")
        check_for_errors(content, response.url)
        logging.debug(f"Detecting the language of '{page_name}'' page {response.url}")
        lang_detect_results = detect_page_language(page_name, "", content, main=main)
        median_results = {
            language: median(probabilities)
            for language, probabilities in lang_detect_results.items()
        }

        results[page_name] = median_results

    undetected_languages = {
        page: medians
        for page, medians in results.items()
        if expected_language_code not in medians
    }
    with assertion_msg(
        f"Could not detect '{expected_language_code}' in page content on following pages: {undetected_languages}"
    ):
        assert not undetected_languages

    unmet_probabilities = {
        page: medians
        for page, medians in results.items()
        if medians[expected_language_code] < probability
    }
    with assertion_msg(
        f"Median '{expected_language_code}' language detection probability of "
        f"{probability} was not met on following pages: {unmet_probabilities}"
    ):
        assert not unmet_probabilities


def fas_should_find_all_sought_companies(context: Context, buyer_alias: str):
    """Check if Buyer was able to find Supplier using all provided terms."""
    with assertion_msg(
        "Context has no required `search_details` dict. Please check if "
        "one of previous steps sets it correctly."
    ):
        assert hasattr(context, "search_results")
    logging.debug(context.search_results)
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
    company = get_company(context, company_alias)
    fas.contact.should_see_that_message_has_been_sent(company, response)
    logging.debug(
        "%s was told that the message to '%s' (%s) has been sent",
        buyer_alias,
        company.title,
        company_alias,
    )


def fas_supplier_should_receive_message_from_buyer(
    context: Context, supplier_alias: str, buyer_alias: str
):
    buyer = get_actor(context, buyer_alias)
    supplier = get_actor(context, supplier_alias)
    context.response = get_email_notification(
        from_email=buyer.email,
        to_email=supplier.email,
        subject=FAS_MESSAGE_FROM_BUYER_SUBJECT,
    )
    logging.debug(
        f"{supplier_alias} received a notification about a message from {buyer_alias}"
    )


def profile_should_see_expected_error_messages(context: Context, supplier_alias: str):
    results = context.results
    assertion_results = []
    for company, response, error in results:
        if error not in response.content.decode("utf-8"):
            context.response = response
            logging.debug(f"Modified company's details: {company}")
            logging.debug(f"Expected error message: {error}")
            logging.debug(
                f"Response: {extract_page_contents(response.content.decode('utf-8'))}"
            )
            assertion_results.append((response, error))

    formatted_message = ";\n\n".join(
        [
            f"'{error}' in response from '{response.url}':\n"
            f"'{extract_page_contents(response.content.decode('utf-8'))}'"
            for response, error in assertion_results
        ]
    )
    with assertion_msg(
        f"Expected to see correct error messages, but couldn't find them in"
        f" following responses: {formatted_message}"
    ):
        assert not assertion_results
    logging.debug("%s has seen all expected form errors", supplier_alias)


def international_should_see_links_to_industry_pages(
    context: Context, actor_alias: str, language: str
):
    page_name = (
        f"{international.industries.SERVICE.value} - {international.industries.NAME}"
    )
    response = context.views[page_name]
    international.industries.should_see_links_to_industry_pages(response, language)
    logging.debug(
        f"{actor_alias} saw all links to industry pages available in '{language}'"
    )


def fas_should_see_filtered_search_results(context: Context, actor_alias: str):
    results = context.results
    sector_filters_selector = "#id_sectors input"
    for industry, result in results.items():
        context.response = result["response"]
        content = result["response"].content.decode("utf-8")
        filters = Selector(text=content).css(sector_filters_selector).extract()
        for filter in filters:
            sector = Selector(text=filter).css("input::attr(value)").extract()[0]
            input = Selector(text=filter).css("input::attr(checked)").extract()
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


def fas_should_see_unfiltered_search_results(context: Context, actor_alias: str):
    response = context.response
    content = response.content.decode("utf-8")
    sector_filters_selector = "#id_sectors input"
    filters = Selector(text=content).css(sector_filters_selector).extract()
    for filter in filters:
        sector = Selector(text=filter).css("input::attr(value)").extract()[0]
        selector = "input::attr(checked)"
        checked = True if Selector(text=filter).css(selector).extract() else False
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
    company = get_company(context, company_alias)
    results = context.results
    founds = [
        (page, result["found"]) for page, result in results.items() if result["found"]
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
    search_summaries_selector = "#companies-column div.width-full.details-container"
    summaries = Selector(text=content).css(search_summaries_selector).extract()
    tag = "em"
    keywords = [surround(keyword, tag) for keyword in search_term.split()]
    founds = []
    for summary in summaries:
        founds += [(keyword in summary) for keyword in keywords]

    with assertion_msg(
        f"Expected to see at least 1 search result with highlighted search "
        f"term: '{', '.join(keywords)}'"
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
    fab.verify_company.should_see_company_is_verified(response)
    logging.debug("%s saw that his company's FAB profile is verified", supplier_alias)


def profile_business_profile_should_be_ready_for_publishing(
    context: Context, supplier_alias: str
):
    response = context.response
    profile.edit_company_profile.should_see_profile_is_verified(response)
    logging.debug(
        f"{supplier_alias} saw that his company's Business Profile is ready to"
        f" be published on FAS"
    )


def fab_should_see_case_study_error_message(context: Context, supplier_alias: str):
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


def sso_should_be_told_about_password_reset(context: Context, supplier_alias: str):
    sso.password_reset.should_see_that_password_was_reset(context.response)
    logging.debug("%s was told that the password was reset", supplier_alias)


def sso_should_get_password_reset_email(context: Context, supplier_alias: str):
    """Will check if the Supplier received an email verification message."""
    logging.debug("Searching for a password reset email...")
    actor = get_actor(context, supplier_alias)
    link = get_password_reset_link(actor.email)
    update_actor(context, supplier_alias, password_reset_link=link)


def sso_should_see_invalid_password_reset_link_error(
    context: Context, supplier_alias: str
):
    sso.invalid_password_reset_link.should_be_here(context.response)
    logging.debug("%s was told about invalid password reset link", supplier_alias)


def should_be_at(context: Context, supplier_alias: str, page_name: str):
    response = context.response
    page = get_page_object(page_name.lower())
    has_action(page, "should_be_here")
    page.should_be_here(response)
    logging.debug("%s is on '%s' page", supplier_alias, page_name)


def should_see_selected_pages(context: Context, actor_alias: str):
    results = context.results
    for page_name, response in results.items():
        context.response = response
        page = get_page_object(page_name.lower())
        page.should_be_here(response)
        logging.debug("%s successfully got to '%s' page", actor_alias, page_name)


def should_be_taken_to_selected_page(
    context: Context, actor_alias: str, page_name: str
):
    page = get_page_object(page_name.lower())
    for _, response, _ in context.results:
        context.response = response
        page.should_be_here(response)
    logging.debug(
        f"{actor_alias} was successfully taken to '{page_name}' page for all "
        f"requests"
    )


def fab_should_be_asked_about_verification_form(context: Context, supplier_alias: str):
    fab.confirm_identity.should_be_here(context.response)
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


def should_not_see_message(context: Context, actor_alias: str, message: str):
    content = context.response.content.decode("utf-8")
    with assertion_msg(f"Response content contains unexpected message: '{message}'"):
        assert message not in content
    logging.debug(
        f"As expected {actor_alias} haven't seen unexpected message: '{message}'"
    )


def sso_should_get_request_for_collaboration_email(
    context: Context, actor_aliases: str, company_alias: str
):
    actor_aliases = [alias.strip() for alias in actor_aliases.split(",")]
    for actor_alias in actor_aliases:
        actor = get_actor(context, actor_alias)
        company = get_company(context, company_alias)
        subject = PROFILE_INVITATION_MSG_SUBJECT.format(
            company_title=company.title.upper()
        )
        link = get_verification_link(actor.email, subject=subject)
        update_actor(
            context,
            actor_alias,
            invitation_for_collaboration_link=link,
            company_alias=company_alias,
        )


def sud_should_see_options_to_manage_users(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    session = actor.session

    context.response = profile.business_profile.go_to(session)
    profile.business_profile.should_be_here(context.response)

    profile.business_profile.should_see_options_to_manage_users(context.response)
    logging.debug("%s can see options to control user accounts", actor_alias)


def sud_should_not_see_options_to_manage_users(context: Context, actor_alias: str):
    """
    Due to bug ED-2268 the first time you visit SUD pages by going directly
    to SUD "Find a Buyer" page, then you're redirected to SUD "About" page
    To circumvent this behaviour we have to go to the "About" page first, and
    then visit the SUD "Find a Buyer" page
    """
    actor = get_actor(context, actor_alias)
    session = actor.session
    context.response = profile.about.go_to(session, set_next_page=False)
    profile.about.should_be_here(context.response)

    context.response = profile.business_profile.go_to(session)
    profile.business_profile.should_be_here(context.response)

    profile.business_profile.should_not_see_options_to_manage_users(context.response)
    logging.debug("%s can't see options to control user accounts", actor_alias)


def profile_should_get_request_for_becoming_owner(
    context: Context, new_owner_alias: str, company_alias: str
):
    actor = get_actor(context, new_owner_alias)
    company = get_company(context, company_alias)
    subject = PROFILE_INVITATION_MSG_SUBJECT.format(company_title=company.title.upper())
    link = get_verification_link(actor.email, subject=subject)
    update_actor(
        context,
        new_owner_alias,
        ownership_request_link=link,
        company_alias=company_alias,
    )


def fab_should_not_see_collaborator(
    context: Context, supplier_alias: str, collaborators_aliases: str
):
    aliases = [alias.strip() for alias in collaborators_aliases.split(",")]
    supplier = get_actor(context, supplier_alias)
    response = fab.account_remove_collaborator.go_to(supplier.session)
    context.response = response

    for collaborator_alias in aliases:
        collaborator = get_actor(context, collaborator_alias)
        fab.account_remove_collaborator.should_not_see_collaborator(
            response, collaborator.email
        )


def should_not_be_able_to_access_page(
    context: Context, collaborator_alias: str, page_name: str
):
    collaborator = get_actor(context, collaborator_alias)
    page_object = get_page_object(page_name)
    response = page_object.go_to(collaborator.session)
    try:
        page_object.should_be_here(response)
        raise Exception("%s was able to access '%' page", collaborator_alias, page_name)
    except AssertionError:
        logging.debug(
            "As expected %s could not access '%s' page. Current URL is: %s",
            collaborator_alias,
            page_name,
            response.url,
        )


def isd_should_be_told_about_empty_search_results(context: Context, buyer_alias: str):
    isd.search.should_see_no_matches(context.response)
    logging.debug(
        "%s was told that the search did not match any UK trade profiles", buyer_alias
    )


def isd_should_see_unfiltered_search_results(context: Context, actor_alias: str):
    response = context.response
    content = response.content.decode("utf-8")
    sector_filters_selector = "#filter-column input[type=checkbox]"
    filters = Selector(text=content).css(sector_filters_selector).extract()
    with assertion_msg(f"Couldn't find filter checkboxes on {response.url}"):
        assert filters
    for filter in filters:
        sector = Selector(text=filter).css("input::attr(value)").extract()[0]
        selector = "input::attr(checked)"
        checked = True if Selector(text=filter).css(selector).extract() else False
        with assertion_msg(
            "Expected search results to be unfiltered but this "
            "filter was checked: '%s'",
            sector,
        ):
            assert not checked
    logging.debug("%s was shown with unfiltered search results", actor_alias)


def generic_page_language_should_be_set_to(context: Context, language: str):
    language_code = Language[language.upper()].value
    with assertion_msg("Required dictionary with page views is missing"):
        assert hasattr(context, "views")
    views = context.views
    page_names = (
        [row["page"] for row in context.table] if context.table else views.keys()
    )

    results = defaultdict()
    for page_name in page_names:
        response = views[page_name]
        content = response.content.decode("utf-8")
        check_for_errors(content, response.url)
        html_tag_language = Selector(text=content).css("html::attr(lang)").extract()[0]
        results[page_name] = html_tag_language

    logging.debug(f"HTML tag language attributes for: {dict(results)}")
    undetected_languages = {
        page: html_tag_lang
        for page, html_tag_lang in results.items()
        if language_code not in html_tag_lang
    }
    with assertion_msg(
        f"HTML document language was not set to '{language_code}' in following pages: {undetected_languages}"
    ):
        assert not undetected_languages


def generic_language_switcher_should_be_set_to(context: Context, language: str):
    language_code = Language[language.upper()].value
    with assertion_msg("Required dictionary with page views is missing"):
        assert hasattr(context, "views")
    views = context.views
    page_names = (
        [row["page"] for row in context.table] if context.table else views.keys()
    )

    results = defaultdict()
    for page_name in page_names:
        response = views[page_name]
        content = response.content.decode("utf-8")
        check_for_errors(content, response.url)
        selector = f"#great-header-language-select option[selected]::attr(value)"
        selected_language_switcher_option = (
            Selector(text=content).css(selector).extract()
        )
        error = f"Couldn't find language switcher on {response.url}"
        with assertion_msg(error):
            assert selected_language_switcher_option
        selected_language_switcher_option = selected_language_switcher_option[0]
        results[page_name] = selected_language_switcher_option

    logging.debug(f"Selected language in Language Switcher on: {dict(results)}")
    undetected_languages = {
        page: selected_language_switcher_option
        for page, selected_language_switcher_option in results.items()
        if language_code not in selected_language_switcher_option
    }
    with assertion_msg(
        f"'{language}' was not selected in Language Switcher for following pages: {undetected_languages}"
    ):
        assert not undetected_languages


def profile_should_not_see_options_to_manage_users(context: Context, actor_alias: str):
    profile.business_profile.should_not_see_options_to_manage_users(context.response)
    logging.debug("%s can't see options to control user accounts", actor_alias)
