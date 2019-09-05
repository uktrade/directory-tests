# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging
from collections import defaultdict
from time import sleep
from typing import List, Union
from urllib.parse import urlparse

import requests
from behave.model import Table
from behave.runner import Context
from datadiff import diff
from retrying import retry
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from pages import (
    common_language_selector,
    domestic,
    fas,
    get_page_object,
    international,
    invest,
    profile,
)
from pages.common_actions import (
    assertion_msg,
    avoid_browser_stack_idle_timeout_exception,
    clear_driver_cookies,
    get_actor,
    get_last_visited_page,
    update_actor,
)
from pages.domestic import contact_us_office_finder_search_results
from settings import (
    FORMS_API_MAILBOXES,
    HPO_AGENT_EMAIL_ADDRESS,
    HPO_AGENT_EMAIL_SUBJECT,
    HPO_ENQUIRY_CONFIRMATION_SUBJECT,
    HPO_PDF_URLS,
)
from steps import has_action
from steps.when_impl import generic_set_basic_auth_creds

from utils.forms_api import (
    find_form_submissions,
    find_form_submissions_by_subject_and_action,
    find_form_submissions_for_dit_office
)
from utils.gov_notify import (
    get_email_confirmation_notification,
    get_email_confirmations_with_matching_string,
)
from utils.gtm import (
    get_gtm_data_layer_events,
    get_gtm_data_layer_properties,
    replace_string_representations,
)
from utils.pdf import extract_text_from_pdf_bytes


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    if "Access denied" in context.driver.page_source:
        logging.debug(f"Trying to re-authenticate on '{page_name}'' {page.URL}")
        generic_set_basic_auth_creds(context, page_name)
        context.driver.get(page.URL)
        error = f"Got blocked again on {context.driver.current_url}"
        assert "Access denied" not in context.driver.page_source, error

    source = context.driver.page_source
    url = context.driver.current_url
    error = f"'{page_name}' does not exist. Got 404 on {url}"
    assert "404 Not Found: Requested route" not in source, error
    error = f"Looks like following page: {url} cannot be found"
    assert "This page cannot be found" not in source, error
    error = f"Got 500 ISE on {url}"
    assert "HTTP 500 Error Code" not in source, error

    has_action(page, "should_be_here")
    if hasattr(page, "URLs"):
        special_page_name = page_name.split(" - ")[1]
        page.should_be_here(context.driver, page_name=special_page_name)
    else:
        page.should_be_here(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(
        f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> " f"{page}"
    )


def should_be_on_page_or_international_page(
    context: Context, actor_alias: str, page_name: str
):
    try:
        should_be_on_page(context, actor_alias, page_name)
    except AssertionError:
        international.landing.should_be_here(context.driver)
        logging.debug("%s was redirected to the International page", actor_alias)


def should_be_on_page_or_be_redirected_to_page(
        context: Context, actor_alias: str, page_name: str, redirect_page: str
):
    try:
        should_be_on_page(context, actor_alias, page_name)
    except AssertionError:
        should_be_on_page(context, actor_alias, redirect_page)
        logging.debug(f"{actor_alias} was redirected to '{redirect_page}' page")


def should_see_sections(
    context: Context,
    actor_alias: str,
    sections_table: Table = None,
    *,
    sections_list: list = None,
):
    sections = sections_list or [row[0] for row in sections_table]
    logging.debug(
        "%s will look for following sections: '%s' on %s",
        actor_alias,
        sections,
        context.driver.current_url,
    )
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_sections")
    page.should_see_sections(context.driver, sections)


def should_not_see_sections(
    context: Context, actor_alias: str, sections_table: Table = None
):
    sections = [row[0] for row in sections_table]
    logging.debug(f"sections {sections}")
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_not_see_section")
    for section in sections:
        page.should_not_see_section(context.driver, section)
        logging.debug(
            "As expected %s cannot see '%s' section on %s page",
            actor_alias,
            section,
            page.NAME,
        )


def case_studies_should_see_case_study(
    context: Context, actor_alias: str, case_study_number: str
):
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    number = case_study_numbers[case_study_number.lower()]
    case_study_title = get_actor(context, actor_alias).case_study_title
    domestic.case_studies_common.should_be_here(
        context.driver, number, title=case_study_title
    )


def should_see_share_widget(context: Context, actor_alias: str):
    driver = context.driver
    domestic.case_studies_common.should_see_share_widget(driver)
    logging.debug("%s can see Share Widget on %s", actor_alias, driver.current_url)


def should_see_links_in_specific_location(
    context: Context,
    actor_alias: str,
    section: str,
    links: Union[list, Table],
    location: str,
):
    page = get_page_object(location)
    has_action(page, "should_see_link_to")
    if isinstance(links, Table):
        links = [row[0] for row in links]
    for link in links:
        page.should_see_link_to(context.driver, section, link)
        logging.debug("%s can see link to '%s' in '%s'", actor_alias, link, location)


def articles_should_be_on_share_page(
    context: Context, actor_alias: str, social_media: str
):
    page_name = f"{social_media} - share on {social_media}"
    social_media_page = get_page_object(page_name)
    has_action(social_media_page, "should_be_here")
    social_media_page.should_be_here(context.driver)
    logging.debug("%s is on the '%s' share page", actor_alias, social_media)


def share_page_should_be_prepopulated(
    context: Context, actor_alias: str, social_media: str
):
    page_name = f"{social_media} - share on {social_media}"
    page = get_page_object(page_name)
    has_action(page, "check_if_populated")
    shared_url = context.article_url
    page.check_if_populated(context.driver, shared_url)
    clear_driver_cookies(driver=context.driver)
    logging.debug(
        "%s saw '%s' share page populated with appropriate data",
        actor_alias,
        social_media,
    )


def share_page_via_email_should_have_article_details(
    context: Context, actor_alias: str
):
    driver = context.driver
    body = driver.current_url
    subject = domestic.advice_article.get_article_name(driver)
    domestic.advice_article.check_share_via_email_link_details(driver, subject, body)
    logging.debug(
        "%s checked that the 'share via email' link contain correct subject: "
        "'%s' and message body: '%s'",
        actor_alias,
        subject,
        body,
    )


def promo_video_check_watch_time(
    context: Context, actor_alias: str, expected_watch_time: int
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "get_video_watch_time")
    watch_time = page.get_video_watch_time(context.driver)
    with assertion_msg(
        "%s expected to watch at least first '%d' seconds of the video but" " got '%d'",
        actor_alias,
        expected_watch_time,
        watch_time,
    ):
        assert watch_time >= expected_watch_time
    logging.debug(
        "%s was able to watch see at least first '%d' seconds of the"
        " promotional video",
        actor_alias,
        expected_watch_time,
    )


def promo_video_should_not_see_modal_window(context: Context, actor_alias: str):
    domestic.home.should_not_see_video_modal_window(context.driver)
    logging.debug(
        "As expected %s can't see promotional video modal window", actor_alias
    )


def header_check_logo(context: Context, actor_alias: str, logo_name: str):
    domestic.actions.check_logo(context.driver, logo_name)
    logging.debug(f"As expected {actor_alias} can see correct {logo_name} logo")


def header_check_favicon(context: Context, actor_alias: str):
    domestic.actions.check_dit_favicon(context.driver)
    logging.debug("As expected %s can see correct DIT favicon", actor_alias)


def language_selector_should_see_it(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.should_see_it_on(context.driver, page=page)
    logging.debug("As expected %s can see language selector", actor_alias)


def should_see_page_in_preferred_language(
    context: Context, actor_alias: str, preferred_language: str
):
    common_language_selector.check_page_language_is(context.driver, preferred_language)
    logging.debug(
        f"{actor_alias} can see '{context.driver.current_url}' page in "
        f"'{preferred_language}"
    )


def fas_search_results_filtered_by_industries(
    context: Context, actor_alias: str, industry_names: List[str]
):
    fas.search_results.should_see_filtered_results(context.driver, industry_names)
    logging.debug(
        "%s can see results filtered by %s (%s)",
        actor_alias,
        industry_names,
        context.driver.current_url,
    )


def generic_should_see_expected_page_content(
    context: Context, actor_alias: str, expected_page_name: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_content_for")
    page.should_see_content_for(context.driver, expected_page_name)
    logging.debug(
        "%s found content specific to %s on %s",
        actor_alias,
        expected_page_name,
        context.driver.current_url,
    )


def stats_and_tracking_elements_should_be_present(context: Context, names: Table):
    element_names = [row[0] for row in names]

    for name in element_names:
        invest.pixels.should_be_present(context.driver, name)


def stats_and_tracking_elements_should_not_be_present(context: Context, names: Table):
    element_names = [row[0] for row in names]

    for name in element_names:
        invest.pixels.should_not_be_present(context.driver, name)


def invest_should_see_uk_gov_logo(context: Context, actor_alias: str, section: str):
    if section.lower() == "header":
        invest.header.check_logo(context.driver)
    else:
        invest.footer.check_logo(context.driver)
    logging.debug(
        "%s can see correct UK GOV logo in page %s on %s",
        actor_alias,
        section,
        context.driver.current_url,
    )


def hpo_should_receive_enquiry_confirmation_email(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=actor.email,
        subject=HPO_ENQUIRY_CONFIRMATION_SUBJECT,
        strings=HPO_PDF_URLS,
    )


def hpo_agent_should_receive_enquiry_email(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=HPO_AGENT_EMAIL_ADDRESS,
        subject=HPO_AGENT_EMAIL_SUBJECT,
        strings=[actor.email] + HPO_PDF_URLS,
    )


def form_check_state_of_element(
    context: Context, actor_alias: str, element: str, state: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "check_state_of_form_element")
    page.check_state_of_form_element(context.driver, element, state)
    logging.debug(
        f"{actor_alias} saw {element} in expected {state} state on "
        f"{context.driver.current_url}"
    )


def pdf_check_expected_details(
    context: Context, actor_alias: str, details_table: Table
):
    pdfs = context.pdfs
    pdf_texts = [(pdf["href"], extract_text_from_pdf_bytes(pdf["pdf"])) for pdf in pdfs]
    details = {
        item[0].split(" = ")[0]: item[0].split(" = ")[1] for item in details_table
    }
    for href, text in pdf_texts:
        for name, value in details.items():
            error_message = (
                f"Could not find {name}: {value} in PDF text downloaded from " f"{href}"
            )
            assert value in text, error_message
            logging.debug(
                f"{actor_alias} saw correct {name} in the PDF downloaded from "
                f"{href}"
            )
    context.pdf_texts = pdf_texts


def pdf_check_for_dead_links(context: Context):
    pdf_texts = context.pdf_texts
    links = set(
        [
            word
            for _, text in pdf_texts
            for word in text.split()
            if any(item in word for item in ["http", "https", "www"])
        ]
    )
    logging.debug(f"Links found in PDFs: {links}")
    for link in links:
        parsed = urlparse(link)
        if not parsed.netloc:
            link = f"http://{link}"
        response = requests.get(link)
        error_message = (
            f"Expected 200 from {link} but got {response.status_code} instead"
        )
        assert response.status_code == 200, error_message
    logging.debug("All links in PDFs returned 200 OK")


def form_should_see_error_messages(
    context: Context, actor_alias: str, message: str = "This field is required"
):
    page_source = context.driver.page_source
    assertion_error = f"Expected error message '{message}' is not present"
    assert message in page_source, assertion_error
    logging.debug(f"{actor_alias} saw expected error message '{message}'")


def should_see_articles_filtered_by_tag(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    tag = actor.last_tag
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "is_filtered_by_tag")
    page.is_filtered_by_tag(context.driver, tag)


# BrowserStack times out after 60s of inactivity
# https://www.browserstack.com/automate/timeouts
@retry(wait_fixed=10000, stop_max_attempt_number=5, wrap_exception=False)
def generic_contact_us_should_receive_confirmation_email(
    context: Context, actor_alias: str, subject: str
):
    avoid_browser_stack_idle_timeout_exception(context.driver)
    actor = get_actor(context, actor_alias)
    confirmation = get_email_confirmation_notification(
        email=actor.email, subject=subject
    )
    assert confirmation


@retry(wait_fixed=5000, stop_max_attempt_number=15)
def generic_a_notification_should_be_sent(
        context: Context, actor_alias: str, action: str, subject: str
):
    actor = get_actor(context, actor_alias)
    submissions = find_form_submissions_by_subject_and_action(
        email=actor.email, subject=subject, action=action
    )
    logging.debug(
        f"Email submissions from '{actor.email}': {submissions}"
    )
    error = (
        f"Expected to find 1 '{action}' notification entitled '{subject}' sent to "
        f"'{actor.email}', but found {len(submissions)}"
    )
    assert len(submissions) == 1, error

    error = (
        f"A '{action}' notification entitled '{subject}' was NOT sent to "
        f"'{actor.email}'!"
    )
    assert submissions[0]["is_sent"], error


@retry(wait_fixed=5000, stop_max_attempt_number=3)
def generic_a_notification_should_be_sent_to_specific_dit_office(
        context: Context, actor_alias: str, mailbox_name: str
):
    actor = get_actor(context, actor_alias)
    mailbox_email = FORMS_API_MAILBOXES[mailbox_name]
    submissions = find_form_submissions_for_dit_office(
        mailbox=mailbox_email,
        sender=actor.email,
    )
    logging.debug(
        f"Email submissions from '{actor.email}' to '{mailbox_email}': {submissions}"
    )
    error = (
        f"Expected to find 1 notification sent to '{mailbox_email}' about contact "
        f"enquiry from {actor.email}, but found {len(submissions)}"
    )
    assert len(submissions) == 1, error

    error = (
        f"A notification about enquiry from '{actor.email}' was NOT sent to "
        f"{mailbox_name} mailbox: '{mailbox_email}'!"
    )
    assert submissions[0]["is_sent"], error
    logging.debug(
        f"A notification about enquiry from {actor.email} was successfully sent to "
        f"{mailbox_name} mailbox: {mailbox_email}")


def generic_a_notification_should_not_be_sent_to_specific_dit_office(
        context: Context, actor_alias: str, mailbox_name: str
):
    actor = get_actor(context, actor_alias)
    forms_data = actor.forms_data
    uuid = None
    for data in forms_data.values():
        if "full name" in data:
            uuid = data["full name"]
            break
        if "family name" in data:
            uuid = data["family name"]
            break
        if "last name" in data:
            uuid = data["last name"]
            break
        if "lastname" in data:
            uuid = data["lastname"]
            break
    assert uuid, f"Could not find last name UUID in user's form data: {forms_data}"
    mailbox_email = FORMS_API_MAILBOXES[mailbox_name]
    submissions = find_form_submissions_for_dit_office(
        mailbox=mailbox_email,
        sender=actor.email,
        uuid=uuid,
    )
    logging.debug(
        f"Email submissions from '{actor.email}' to '{mailbox_email}': {submissions}"
    )
    error = (
        f"Expected to find at least 1 notification sent to '{mailbox_email}' about "
        f"contact enquiry from blocked email address: {actor.email}, but found "
        f"{len(submissions)}"
    )
    assert len(submissions) >= 1, error

    error = (
        f"An unnecessary notification about enquiry from '{actor.email}' was sent to "
        f"'{mailbox_name}': '{mailbox_email}'!"
    )
    assert not submissions[0]["is_sent"], error
    logging.debug(
        f"Unfortunately a notification about enquiry from {actor.email} was sent to "
        f"{mailbox_name} mailbox: {mailbox_email}")


def generic_should_see_form_choices(
    context: Context, actor_alias: str, option_names: Table
):
    option_names = [row[0] for row in option_names]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_form_choices")
    page.should_see_form_choices(context.driver, option_names)


def office_finder_should_see_correct_office_details(
    context: Context, actor_alias: str, trade_office: str, city: str
):
    contact_us_office_finder_search_results.should_see_office_details(
        context.driver, trade_office, city
    )
    logging.debug(
        f"{actor_alias} found contact details for trade '{trade_office}' office"
        f" in '{city}'"
    )


@retry(wait_fixed=5000, stop_max_attempt_number=3, wrap_exception=False)
def forms_confirmation_email_should_not_be_sent(context: Context, actor_alias: str):
    avoid_browser_stack_idle_timeout_exception(context.driver)
    actor = get_actor(context, actor_alias)
    submissions = find_form_submissions(actor.email)
    assert submissions, f"No form submissions found for {actor_alias}"
    error = (
        f"Expected to find an unsent submission for {actor_alias} but found a sent"
        f" one. Check spam filters"
    )
    assert not submissions[0]["is_sent"], error


def marketplace_finder_should_see_marketplaces(
    context: Context, actor_alias: str, country: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_marketplaces")
    page.should_see_marketplaces(context.driver, country)


def domestic_search_finder_should_see_page_number(
    context: Context, actor_alias: str, page_num: int
):
    should_be_on_page(
        context,
        actor_alias,
        f"{domestic.search_results.SERVICE} - {domestic.search_results.NAME}",
    )
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_page_number")
    page.should_see_page_number(context.driver, page_num)


def generic_should_be_on_one_of_the_pages(
    context: Context, actor_alias: str, expected_pages: str
):
    expected_pages = [page.strip() for page in expected_pages.split(",")]
    results = defaultdict()
    for page_name in expected_pages:
        try:
            should_be_on_page(context, actor_alias, page_name)
            results[page_name] = True
        except AssertionError:
            results[page_name] = False

    with assertion_msg(
        f"{actor_alias} didn't see any of expected pages, instead it's on {context.driver.current_url}"
    ):
        assert any(list(results.values()))


def soo_contact_form_should_be_prepopulated(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)

    form_po = profile.enrol_enter_your_business_details_step_2
    form_data_key = f"{form_po.SERVICE} - {form_po.NAME} - {form_po.TYPE}"
    form_data = actor.forms_data[form_data_key]

    has_action(page, "check_if_populated")
    page.check_if_populated(context.driver, form_data)


def generic_check_gtm_datalayer_properties(context: Context, table: Table):
    row_names = [
        "businessUnit",
        "loginStatus",
        "siteLanguage",
        "siteSection",
        "siteSubsection",
        "userId",
    ]
    table.require_columns(row_names)
    raw_properties = {name: row.get(name) for name in row_names for row in table}
    expected_properties = replace_string_representations(raw_properties)
    found_properties = get_gtm_data_layer_properties(context.driver)

    with assertion_msg(
        f"Expected to see following GTM data layer properties:\n"
        f"'{expected_properties}'\n but got:\n'{found_properties}'\non: "
        f"{context.driver.current_url}\ndiff:\n"
        f"{diff(expected_properties, found_properties)}"
    ):
        assert expected_properties == found_properties


def table_to_list_of_dicts(table: Table) -> List[dict]:
    """Convert behave's table to a list of dictionaries"""
    result = []
    for row in table:
        result.append({name: row.get(name) for name in table.headings})
    return result


def generic_check_gtm_events(context: Context):
    required_columns = ["action", "element", "event", "type", "value"]
    context.table.require_columns(required_columns)
    expected_gtm_events = table_to_list_of_dicts(context.table)

    for event in expected_gtm_events:
        if event["type"] == "Empty string":
            event["type"] = ""
        if event["value"] == "Empty string":
            event["value"] = ""
        if event["type"] == "Not present":
            event.pop("type")
        if event["value"] == "Not present":
            event.pop("value")
    logging.debug(f"Expected GTM events: {expected_gtm_events}")
    registered_gtm_events = get_gtm_data_layer_events(context.driver)

    missing_events = [
        event
        for event in expected_gtm_events
        if event not in registered_gtm_events
    ]
    with assertion_msg(
            f"Could not find following GTM events:\n{missing_events}\n"
            f"among following GTM events:\n{registered_gtm_events}\n"
            f"registered on: {context.driver.current_url}\n"
            f"Diff:\n{diff(expected_gtm_events, registered_gtm_events)}"
    ):
        assert not missing_events

    with assertion_msg(
            f"Expected to find {len(expected_gtm_events)} registered GTM event(s) but "
            f"found {len(registered_gtm_events)} instead: "
            f"{registered_gtm_events}"
    ):
        assert len(expected_gtm_events) == len(registered_gtm_events)


def menu_items_should_be_visible(context: Context):
    ids = [
        'great-header-nav-mobile',
        'great-header-mobile-nav',
        'great-header-nav',
    ]
    for value in ids:
        try:
            element = context.driver.find_element(by=By.ID, value=value)
            break
        except NoSuchElementException as error:
            continue
    else:
        raise error

    assert element.is_displayed()
