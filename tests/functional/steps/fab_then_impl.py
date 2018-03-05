# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
import logging
from statistics import median

from behave.model import Table
from behave.runner import Context
from requests import Response
from retrying import retry
from scrapy import Selector

from tests import get_absolute_url
from tests.functional.pages import (
    fab_ui_build_profile_basic,
    fab_ui_confirm_identity,
    fab_ui_edit_online_profiles,
    fab_ui_profile,
    fab_ui_try_other_services,
    fab_ui_verify_company,
    fas_ui_contact,
    fas_ui_find_supplier,
    fas_ui_industries,
    fas_ui_profile,
    profile_ui_landing,
    sso_ui_invalid_password_reset_link,
    sso_ui_logout,
    sso_ui_password_reset,
    sso_ui_verify_your_email
)
from tests.functional.registry import get_fabs_page_object
from tests.functional.utils.generic import (
    MailGunEvent,
    MailGunService,
    assertion_msg,
    check_hash_of_remote_file,
    detect_page_language,
    extract_csrf_middleware_token,
    extract_logo_url,
    find_mail_gun_events,
    get_language_code,
    get_number_of_search_result_pages,
    surround
)
from tests.functional.utils.gov_notify import (
    get_verification_link,
    get_password_reset_link
)
from tests.settings import (
    FAS_LOGO_PLACEHOLDER_IMAGE,
    FAS_MESSAGE_FROM_BUYER_SUBJECT,
    SEARCHABLE_CASE_STUDY_DETAILS,
    FAB_CONFIRM_COLLABORATION_SUBJECT
)


def reg_sso_account_should_be_created(response: Response, supplier_alias: str):
    """Will verify if SSO account was successfully created.

    Note:
    It's a very crude check, as it will only check if the response body
    contains selected phrases.

    :param response: response object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    sso_ui_verify_your_email.should_be_here(response)
    logging.debug("Successfully created new SSO account for %s", supplier_alias)


def reg_should_get_verification_email(context: Context, alias: str):
    """Will check if the Supplier received an email verification message.

    :param context: behave `context` object
    :param alias: alias of the Actor used in the scope of the scenario
    """
    logging.debug("Searching for an email verification message...")
    actor = context.get_actor(alias)
    link = get_verification_link(actor.email)
    context.update_actor(alias, email_confirmation_link=link)


def bp_should_be_prompted_to_build_your_profile(
        context: Context, supplier_alias: str):
    fab_ui_build_profile_basic.should_be_here(context.response)
    logging.debug(
        "%s is on the 'Build and improve your profile' page", supplier_alias)
    token = extract_csrf_middleware_token(context.response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)


def prof_should_be_on_profile_page(response: Response, supplier_alias: str):
    fab_ui_profile.should_be_here(response)
    logging.debug("%s is on the company profile page", supplier_alias)


def prof_should_be_told_about_missing_description(
        response: Response, supplier_alias: str):
    fab_ui_profile.should_see_missing_description(response)
    logging.debug("%s was told about missing description", supplier_alias)


def fas_should_be_on_profile_page(context, supplier_alias, company_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    fas_ui_profile.should_be_here(context.response, number=company.number)
    logging.debug(
        "%s is on the %s company's FAS page", supplier_alias, company_alias)


def fas_check_profiles(context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    # Step 1 - go to company's profile page on FAS
    response = fas_ui_profile.go_to(actor.session, company.number)
    context.response = response
    # Step 2 - check if links to online profile are visible
    fas_ui_profile.should_see_online_profiles(company, response)
    logging.debug("%s can see all expected links to Online Profiles on "
                  "FAS Company's Directory Profile Page", supplier_alias)


def reg_supplier_is_not_appropriate_for_fab(
        context: Context, supplier_alias: str):
    fab_ui_try_other_services.should_be_here(context.response)
    logging.debug("%s was told that her/his business is not appropriate "
                  "to feature in the Find a Buyer service", supplier_alias)


def reg_supplier_has_to_verify_email_first(
        context: Context, supplier_alias: str):
    sso_ui_verify_your_email.should_be_here(context.response)
    logging.debug("%s was told that her/his email address has to be verified "
                  "first before being able to Sign In", supplier_alias)


def sso_should_be_signed_in_to_sso_account(
        context: Context, supplier_alias: str):
    response = context.response
    with assertion_msg("Expected sessionid cookie to be set. It looks like "
                       "user is not logged in"):
        assert response.cookies.get("sessionid") is not None
    with assertion_msg("Response doesn't contain 'Sign out' button. It looks "
                       "like user is not logged in"):
        assert "Sign out" in response.content.decode("utf-8")
    logging.debug("%s is logged in to the SSO account", supplier_alias)


def sso_should_be_signed_out_from_sso_account(
        context: Context, supplier_alias: str):
    """Sign out from SSO.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Get to the Sign Out confirmation page
    next_param = get_absolute_url("profile:about")
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


def prof_should_be_told_about_invalid_links(
        context: Context, supplier_alias: str):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    fab_ui_edit_online_profiles.should_see_errors(
        context.response, facebook=facebook, linkedin=linkedin,
        twitter=twitter)
    logging.debug(
        "%s was not able to set Company's Online Profile links using invalid "
        "URLs to: %s %s %s", supplier_alias, "Facebook" if facebook else "",
        "LinkedIn" if linkedin else "", "Twitter" if twitter else "")


def fab_should_see_all_case_studies(context: Context, supplier_alias: str):
    """Check if Supplier can see all case studies on FAB profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    case_studies = context.get_company(actor.company_alias).case_studies
    fab_ui_profile.should_see_case_studies(case_studies, context.response)


def fas_should_see_all_case_studies(context: Context, supplier_alias: str):
    """Check if Supplier can see all case studies on FAS profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    response = fas_ui_profile.go_to(actor.session, company.number)
    context.response = response
    case_studies = context.get_company(actor.company_alias).case_studies
    fas_ui_profile.should_see_case_studies(case_studies, response)
    logging.debug("%s can see all %d Case Studies on FAS Company's "
                  "Directory Profile Page", supplier_alias, len(case_studies))


def prof_should_see_logo_picture(context: Context, supplier_alias: str):
    """Will check if Company's Logo visible on FAB profile page is the same as
    the uploaded one.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    logo_url = company.logo_url
    logo_hash = company.logo_hash
    logo_picture = company.logo_picture

    logging.debug("Fetching logo image visible on the %s's FAB profile page",
                  company.title)
    check_hash_of_remote_file(logo_hash, logo_url)
    logging.debug("The Logo visible on the %s's FAB profile page is the same "
                  "as uploaded %s", company.title, logo_picture)


def fas_should_see_png_logo_thumbnail(context: Context, supplier_alias: str):
    """Will check if Company's PNG thumbnail logo visible on FAS profile.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    visible_logo_url = extract_logo_url(response, fas=True)
    placeholder = FAS_LOGO_PLACEHOLDER_IMAGE

    with assertion_msg(
            "Expected company logo but got image placeholder '%s'",
            visible_logo_url):
        assert visible_logo_url != placeholder
    with assertion_msg(
            "Expected PNG logo thumbnail, but got: %s", visible_logo_url):
        assert visible_logo_url.lower().endswith(".png")
    context.set_company_logo_detail(
        actor.company_alias, url=visible_logo_url)
    logging.debug("Set Company's logo URL to: %s", visible_logo_url)


def fas_should_see_different_png_logo_thumbnail(context, actor_alias):
    """Will check if Company's Logo visible on FAS profile page is the same as
    the one uploaded on FAB.

    :param context: behave `context` object
    :param actor_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(actor_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    fas_logo_url = company.logo_url

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response
    visible_logo_url = extract_logo_url(response, fas=True)
    placeholder = FAS_LOGO_PLACEHOLDER_IMAGE

    with assertion_msg(
            "Expected company logo but got image placeholder",
            visible_logo_url):
        assert visible_logo_url != placeholder
    with assertion_msg(
            "Expected to see other logo thumbnail than the previous one '%s'.",
            visible_logo_url):
        assert visible_logo_url != fas_logo_url
    with assertion_msg(
            "Expected PNG logo thumbnail, but got: %s", visible_logo_url):
        assert visible_logo_url.lower().endswith(".png")


def prof_all_unsupported_files_should_be_rejected(
        context: Context, supplier_alias: str):
    """Check if all unsupported files were rejected upon upload as company logo.

    NOTE:
    This require `context.rejections` to be set.
    It should be a list of bool values.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    assert hasattr(context, "rejections")
    with assertion_msg(
            "Some of the uploaded files that should be marked as unsupported "
            "were actually accepted. Please check the logs for more details"):
        assert all(context.rejections)
    logging.debug("All files of unsupported types uploaded by %s were rejected"
                  .format(supplier_alias))


def fab_should_see_online_profiles(context: Context, supplier_alias: str):
    """Check if Supplier can see all online Profiles on FAB Profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    response = context.response
    fab_ui_profile.should_see_online_profiles(company, response)


def fab_no_links_to_online_profiles_are_visible(
        context: Context, supplier_alias: str):
    """Supplier should't see any links to Online Profiles on FAB Profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    response = context.response
    fab_ui_profile.should_not_see_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAB Profile page",
        supplier_alias)


def fas_no_links_to_online_profiles_are_visible(
        context: Context, supplier_alias: str):
    """Supplier should't see any links to Online Profiles on FAS Profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    response = context.response
    fas_ui_profile.should_not_see_online_profiles(response)
    logging.debug(
        "%s cannot see links to Online Profiles on FAS Profile page",
        supplier_alias)


def fab_profile_is_verified(context: Context, supplier_alias: str):
    """Check if Supplier was told that Company's profile is verified.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    response = context.response
    fab_ui_profile.should_see_profile_is_verified(response)
    logging.debug("%s was told that the profile is verified.", supplier_alias)


def fab_should_see_company_details(context: Context, supplier_alias: str):
    """Supplier should see all expected Company details of FAB profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    response = context.response
    fab_ui_profile.should_see_details(company, response, context.table)
    logging.debug("%s can see all expected details are visible of FAB "
                  "Company's Directory Profile Page", supplier_alias)


def profile_supplier_should_be_on_landing_page(
        context: Context, supplier_alias: str):
    """Check if Supplier is on Profile Landing page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    response = context.response
    profile_ui_landing.should_be_here(response)
    logging.debug("%s got to the SSO landing page.", supplier_alias)


def fas_should_see_company_details(context: Context, supplier_alias: str):
    """Supplier should see all expected Company details of FAS profile page.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session

    # Step 1 - Go to the FAS profile page & extract URL of visible logo image
    response = fas_ui_profile.go_to(session, company.number)
    context.response = response

    # Step 2 - Check if all details are visible on FAS
    fas_ui_profile.should_see_details(company, response, context.table)
    logging.debug("%s can see all expected details are visible of FAS "
                  "Company's Directory Profile Page", supplier_alias)


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def fas_find_supplier_using_case_study_details(
        context: Context, buyer_alias: str, company_alias: str, case_alias: str,
        *, properties: Table = None):
    """Find Supplier on FAS using parts of the Case Study added by Supplier.

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the sought Company
    :param case_alias: alias of the Case Study used in the search
    :param properties: (optional) table containing the names of Case Study parts
                       that will be used search. If not provided, then all parts
                       will be used except 'alias'.
    """
    actor = context.get_actor(buyer_alias)
    session = actor.session
    company = context.get_company(company_alias)
    case_study = company.case_studies[case_alias]
    keys = SEARCHABLE_CASE_STUDY_DETAILS
    if properties:
        keys = [row['search using case study\'s'] for row in properties]
    search_terms = {}
    for key in keys:
        if key == "keywords":
            for index, keyword in enumerate(case_study.keywords.split(", ")):
                search_terms["keyword #{}".format(index)] = keyword
        else:
            search_terms[key] = getattr(case_study, key.replace(" ", "_"))
    logging.debug(
        "Now %s will try to find '%s' using following search terms: %s",
        buyer_alias, company.title, search_terms)
    for term_name in search_terms:
        term = search_terms[term_name]
        response = fas_ui_find_supplier.go_to(session, term=term)
        context.response = response
        found = fas_ui_find_supplier.should_see_company(response, company.title)
        if found:
            logging.debug(
                "Found Supplier '%s' using '%s' : '%s' on 1st result page",
                company.title, term_name, term)
        else:
            number_of_pages = get_number_of_search_result_pages(response)
            if number_of_pages > 1:
                for page_number in range(2, number_of_pages + 1):
                    response = fas_ui_find_supplier.go_to(
                        session, term=term, page=page_number)
                    context.response = response
                    found = fas_ui_find_supplier.should_see_company(
                        response, company.title)
                    if found:
                        break
            else:
                with assertion_msg(
                        "Couldn't find '%s' using '%s': '%s' on the only "
                        "available search result page", company.title,
                        term_name, term):
                    assert False

        with assertion_msg(
                "Buyer could not find Supplier '%s' on FAS using %s: %s",
                company.title, term_name, term):
            assert found
        logging.debug(
            "Buyer found Supplier '%s' on FAS using %s: %s", company.title,
            term_name, term)


def fas_supplier_cannot_be_found_using_case_study_details(
        context: Context, buyer_alias: str, company_alias: str, case_alias: str):
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
        buyer_alias, company.title, search_terms)
    for term_name in search_terms:
        term = search_terms[term_name]
        logging.debug(
            "Searching for '%s' using %s: %s", buyer_alias, company.title,
            term_name, search_terms)
        response = fas_ui_find_supplier.go_to(session, term=term)
        context.response = response
        found = fas_ui_find_supplier.should_not_see_company(response, company.title)
        with assertion_msg(
                "Buyer found Supplier '%s' on FAS using %s: %s", company.title,
                term_name, term):
            assert found
        logging.debug(
            "Buyer was not able to find unverified Supplier '%s' on FAS using "
            "%s: %s", company.title, term_name, term)


def fas_should_find_with_company_details(
        context: Context, buyer_alias: str, company_alias: str):
    """Check if Buyer was able to find Supplier using all selected search terms.

    NOTE:
    This step requires the search_results dict to be stored in context

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    :param company_alias: alias of the Company used in the scope of the scenario
    """
    assert hasattr(context, "search_results")
    company = context.get_company(company_alias)
    for result in context.search_results:
        # get response for specific search request. This helps to debug
        context.response = context.search_responses[result]
        with assertion_msg(
                "%s wasn't able to find '%s' (alias: %s) using %s", buyer_alias,
                company.title, company_alias, result):
            assert context.search_results[result]


def fas_pages_should_be_in_selected_language(
        context, pages_table: Table, language, *, page_part: str = None,
        probability: float = 0.9):
    """Check if all viewed pages contain content in expected language

    NOTE:
    This requires all responses with page views to be stored in context.views

    :param context: behave `context` object
    :param pages_table: a table with viewed FAS pages
    :param language: expected language of the view FAS page content
    :param page_part: detect language of the whole page or just the main part
    :param probability: expected probability of expected language to be detected
    """
    with assertion_msg("Required dictionary with page views is missing"):
        assert hasattr(context, "views")
    pages = [row['page'] for row in pages_table]
    views = context.views

    if page_part:
        if page_part == "main":
            main = True
        elif page_part == "whole":
            main = False
        else:
            raise KeyError(
                "Please select valid part of the page: main or whole")

    for page_name in pages:
        response = views[page_name]
        # store currently processed response in context, so that it can be
        # printed out to the console in case of a failing assertion
        context.response = response
        content = response.content.decode("utf-8")
        expected_language = get_language_code(language)
        logging.debug("Detecting the language of FAS %s page", page_name)
        results = detect_page_language(content=content, main=main)
        detected = set(lang.lang for idx in results for lang in results[idx])
        logging.debug("`langdetect` detected FAS %s page to be in %s", detected)

        error_msg = ""
        for lang_code in detected:
            probabilities = [lang.prob
                             for idx in results
                             for lang in results[idx]
                             if lang.lang == lang_code]
            error_msg += ("With median probability {} the text is in {}\n"
                          .format(median(probabilities), lang_code))

        with assertion_msg(error_msg):
            assert all(lang.prob > probability
                       for idx in results
                       for lang in results[idx]
                       if lang.lang == expected_language)


def fas_should_find_all_sought_companies(context: Context, buyer_alias: str):
    """Check if all Buyer was able to find Supplier using all provided terms.

    :param context: behave `context` object
    :param buyer_alias: alias of the Actor used in the scope of the scenario
    """
    with assertion_msg(
            "Context has no required `search_details` dict. Please check if "
            "one of previous steps sets it correctly."):
        assert hasattr(context, "search_results")
    for company, results in context.search_results.items():
        for result in results:
            term = result["term"]
            term_type = result["type"]
            context.response = result["response"]
            with assertion_msg(
                    "%s could not find Supplier '%s' using '%s' term '%s'",
                    buyer_alias, company, term_type, term):
                assert result["found"]


def fas_should_be_told_that_message_has_been_sent(
        context: Context, buyer_alias: str, company_alias: str):
    response = context.response
    company = context.get_company(company_alias)
    fas_ui_contact.should_see_that_message_has_been_sent(company, response)
    logging.debug("%s was told that the message to '%s' (%s) has been sent",
                  buyer_alias, company.title, company_alias)


def fas_supplier_should_receive_message_from_buyer(
        context: Context, supplier_alias: str, buyer_alias: str):
    supplier = context.get_actor(supplier_alias)
    response = find_mail_gun_events(
        context, service=MailGunService.DIRECTORY, recipient=supplier.email,
        event=MailGunEvent.ACCEPTED, subject=FAS_MESSAGE_FROM_BUYER_SUBJECT)
    context.response = response


def fab_should_see_expected_error_messages(context, supplier_alias):
    results = context.results
    logging.debug(results)
    for company, response, error in results:
        context.response = response
        with assertion_msg(
                "Could not find expected error message: '%s' in the response, "
                "after submitting the form with following company details: "
                "title='%s' website='%s' keywords='%s' number of employees="
                "'%s'", error, company.title, company.website,
                company.keywords, company.no_employees):
            assert error in response.content.decode("utf-8")
    logging.debug("%s has seen all expected form errors", supplier_alias)


def fas_should_be_on_selected_page(context, actor_alias, page_name):
    response = context.response
    page_object = get_fabs_page_object(page_name)
    page_object.should_be_here(response)
    logging.debug(
        "%s successfully got to the %s FAS page", actor_alias, page_name)


def fas_should_see_promoted_industries(context, actor_alias, table):
    industries = [row['industry'].lower() for row in table]
    response = context.response
    for industry in industries:
        fas_ui_industries.should_see_industry_section(response, industry)
    logging.debug(
        "%s can see all expected industry sections '%s'", actor_alias,
        industries)


def fas_should_see_filtered_search_results(context, actor_alias):
    results = context.results
    sector_filters_selector = "#id_sectors input"
    for industry, result in results.items():
        context.response = result["response"]
        content = result["response"].content.decode("utf-8")
        filters = Selector(text=content).css(sector_filters_selector).extract()
        for fil in filters:
            sector = Selector(text=fil).css("input::attr(value)").extract()[0]
            checked = True if Selector(text=fil).css("input::attr(checked)").extract() else False
            if sector in result["sectors"]:
                with assertion_msg(
                        "Expected search results to be filtered by '%s' sector"
                        " but this filter was not checked!"):
                    assert checked
            else:
                with assertion_msg(
                        "Expected search results to be filtered only by "
                        "following sectors '%s', but they are also filtered "
                        "by '%s'!", ", ".join(result['sectors']), sector):
                    assert not checked
        logging.debug(
            "%s was presented with '%s' industry search results correctly "
            "filtered by following sectors: '%s'", actor_alias, industry,
            ", ".join(result['sectors']))


def fas_should_see_unfiltered_search_results(context, actor_alias):
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
                "filter was checked: '%s'", sector):
            assert not checked
    logging.debug("%s was shown with unfiltered search results", actor_alias)


def fas_should_see_company_once_in_search_results(
        context: Context, actor_alias: str, company_alias: str):
    company = context.get_company(company_alias)
    results = context.results
    founds = [(page, result['found'])
              for page, result in results.items()
              if result['found']]
    with assertion_msg(
            "Expected to see company '%s' only once on first %d search result "
            "pages but found it %d times. On pages: %s", company.title,
            len(results), len(founds), founds):
        assert len(founds) == 1
    logging.debug(
        "As expected %s found company '%s' (%s) only once on first %d search "
        "result pages", actor_alias, company.title, company_alias,
        len(results) + 1)


def fas_should_see_highlighted_search_term(context, actor_alias, search_term):
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
            "term: '%s'".format(", ".join(keywords))):
        assert any(founds)

    logging.debug(
        "{alias} found highlighted search {term}: '{keywords}' {founds} {times}"
        " in {results} search results".format(
            alias=actor_alias, term="terms" if len(keywords) > 1 else "term",
            keywords=", ".join(keywords), founds=len([f for f in founds if f]),
            times="times" if len([f for f in founds if f]) > 1 else "time",
            results=len(summaries)))


def fab_company_should_be_verified(context, supplier_alias):
    response = context.response
    fab_ui_verify_company.should_see_company_is_verified(response)


def fab_should_see_case_study_error_message(context, supplier_alias):
    results = context.results
    logging.debug(results)
    for field, value_type, case_study, response, error in results:
        context.response = response
        with assertion_msg(
                "Could not find expected error message: '%s' in the response, "
                "after submitting the add case study form with '%s' value being"
                " '%s' following and other details: '%s'", error, field,
                value_type, case_study):
            assert error in response.content.decode("utf-8")
    logging.debug("%s has seen all expected case study errors", supplier_alias)


def sso_should_be_told_about_password_reset(
        context: Context, supplier_alias: str):
    sso_ui_password_reset.should_see_that_password_was_reset(context.response)
    logging.debug("%s was told that the password was reset", supplier_alias)


def sso_should_get_password_reset_email(context: Context, supplier_alias: str):
    """Will check if the Supplier received an email verification message.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    logging.debug("Searching for a password reset email...")
    actor = context.get_actor(supplier_alias)
    link = get_password_reset_link(actor.email)
    context.update_actor(supplier_alias, password_reset_link=link)


def sso_should_see_invalid_password_reset_link_error(
        context: Context, supplier_alias: str):
    sso_ui_invalid_password_reset_link.should_be_here(context.response)
    logging.debug(
        "%s was told about invalid password reset link", supplier_alias)


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
        logging.debug("%s successfully got to '%s' page", actor_alias, page_name)


def fab_should_be_asked_about_verification_form(
        context: Context, supplier_alias: str):
    fab_ui_confirm_identity.should_be_here(context.response)
    logging.debug(
        "%s was asked about the form of identity verification", supplier_alias)


def should_see_message(context: Context, actor_alias: str, message: str):
    content = context.response.content.decode("utf-8")
    with assertion_msg(
            "Response content doesn't contain expected message: '%s'", message):
        assert message in content
    logging.debug("%s saw expected message: '%s'", actor_alias, message)


def sso_should_get_request_for_collaboration_email(
        context: Context, actor_alias: str, company_alias: str):
    actor = context.get_actor(actor_alias)
    company = context.get_company(company_alias)
    logging.debug(
        "Trying to find email with a request for collaboration with company: "
        "%s", company.title)
    subject = FAB_CONFIRM_COLLABORATION_SUBJECT.format(company.title)
    response = find_mail_gun_events(
        context, service=MailGunService.DIRECTORY, recipient=actor.email,
        event=MailGunEvent.ACCEPTED, subject=subject)
    context.response = response
    with assertion_msg(
            "Expected to find an email with a request for collaboration with "
            "company: '%s'", company_alias):
        assert response.status_code == 200
