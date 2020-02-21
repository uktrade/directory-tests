# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging
from collections import defaultdict
from inspect import signature
from typing import List, Union
from urllib.parse import urlparse

import requests
from behave.model import Table
from behave.runner import Context
from datadiff import diff
from retrying import retry
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from directory_tests_shared.clients import DIRECTORY_TEST_API_CLIENT
from directory_tests_shared.constants import (
    EMAIL_ERP_PROGRESS_SAVED_MSG_SUBJECT,
    FORMS_API_MAILBOXES,
    HPO_AGENT_EMAIL_ADDRESS,
    HPO_AGENT_EMAIL_SUBJECT,
    HPO_ENQUIRY_CONFIRMATION_SUBJECT,
    HPO_PDF_URLS,
)
from directory_tests_shared.gov_notify import (
    get_email_confirmation_notification,
    get_email_confirmations_with_matching_string,
    get_verification_link,
)
from directory_tests_shared.pdf import extract_text_from_pdf
from directory_tests_shared.utils import blue, check_for_errors, get_comparison_details
from pages import (
    common_language_selector,
    domestic,
    erp,
    fas,
    get_page_object,
    invest,
    profile,
)
from pages.common_actions import (
    accept_all_cookies,
    assertion_msg,
    avoid_browser_stack_idle_timeout_exception,
    get_actor,
    get_full_page_name,
    get_last_visited_page,
    revisit_page_on_access_denied,
    selenium_action,
    take_screenshot,
    update_actor,
)
from pages.domestic import contact_us_office_finder_search_results
from steps import has_action
from utils.browser import clear_driver_cookies
from utils.forms_api import (
    find_form_submissions,
    find_form_submissions_by_subject_and_action,
    find_form_submissions_for_dit_office,
)
from utils.gtm import (
    get_gtm_data_layer_events,
    get_gtm_data_layer_properties,
    replace_string_representations,
)


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    page_source = context.driver.page_source
    revisit_page_on_access_denied(context.driver, page, page_name)
    check_for_errors(page_source, context.driver.current_url)
    accept_all_cookies(context.driver)
    take_screenshot(context.driver, page_name)
    has_action(page, "should_be_here")
    if hasattr(page, "SubURLs"):
        special_page_name = page_name.split(" - ")[1].lower()
        if signature(page.should_be_here).parameters.get("page_name"):
            page.should_be_here(context.driver, page_name=special_page_name)
        else:
            raise TypeError(
                f"{page.__name__}.should_be_here() doesn't accept 'page_name' keyword "
                f"argument but it should as this Page Object has 'SubURLs' attribute."
            )
    else:
        page.should_be_here(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(
        f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> " f"{page}"
    )


def should_be_on_working_page(context: Context, actor_alias: str):
    check_for_errors(context.driver.page_source, context.driver.current_url)
    logging.debug(f"{actor_alias} is on {context.driver.current_url}")


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


def hpo_should_receive_enquiry_confirmation_email(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=actor.email,
        subject=HPO_ENQUIRY_CONFIRMATION_SUBJECT,
        strings=HPO_PDF_URLS,
    )


def hpo_agent_should_receive_enquiry_email(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    logging.debug(
        f"Looking for a notification sent to HPO agent: {HPO_AGENT_EMAIL_ADDRESS}"
    )
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
    pdf_texts = [
        (pdf["href"], extract_text_from_pdf(pdf_bytes=pdf["pdf"])) for pdf in pdfs
    ]
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


def generic_should_see_message(context: Context, actor_alias: str, message: str = None):
    message = message or "This field is required"
    page_source = context.driver.page_source
    assertion_error = (
        f"Expected message '{message}' is not present on {context.driver.current_url}"
    )
    assert message in page_source, assertion_error
    logging.debug(
        f"{actor_alias} saw expected: '{message}' on {context.driver.current_url}"
    )


# BrowserStack times out after 60 seconds of inactivity
# https://www.browserstack.com/automate/timeouts
@retry(wait_fixed=5000, stop_max_attempt_number=7, wrap_exception=False)
def generic_contact_us_should_receive_confirmation_email(
    context: Context, actor_alias: str, subject: str, *, service: str = None
):
    avoid_browser_stack_idle_timeout_exception(context.driver)
    actor = get_actor(context, actor_alias)
    confirmation = get_email_confirmation_notification(
        email=actor.email, subject=subject, service=service
    )
    assert confirmation


def erp_should_receive_email_with_link_to_restore_saved_progress(
    context: Context, actor_alias: str
):
    avoid_browser_stack_idle_timeout_exception(context.driver)
    actor = get_actor(context, actor_alias)

    link = get_verification_link(
        actor.email, subject=EMAIL_ERP_PROGRESS_SAVED_MSG_SUBJECT
    )
    with assertion_msg(f"Could not find an email with link to restore saved progress"):
        assert link
    update_actor(context, actor_alias, saved_progress_link=link)


def generic_contact_us_should_receive_confirmation_email_containing_message(
    context: Context, actor_alias: str, subject: str, message: str
):
    actor = get_actor(context, actor_alias)
    confirmation = get_email_confirmations_with_matching_string(
        recipient_email=actor.email, subject=subject, strings=[message]
    )
    assert confirmation
    logging.debug(
        f"Found an email notification containing expected message: '{message}' send to "
        f"{actor.email}"
    )


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def generic_a_notification_should_be_sent(
    context: Context, actor_alias: str, action: str, subject: str
):
    actor = get_actor(context, actor_alias)
    submissions = find_form_submissions_by_subject_and_action(
        email=actor.email, subject=subject, action=action
    )
    logging.debug(f"Email submissions from '{actor.email}': {submissions}")
    error = (
        f"Expected to find 1 '{action}' notification entitled '{subject}' sent to "
        f"'{actor.email}', but found {len(submissions)}"
    )
    assert len(submissions) == 1, error

    if not submissions[0]["is_sent"]:
        message = (
            f"A '{action}' notification entitled '{subject}' was NOT sent to "
            f"'{actor.email}' yet!"
        )
        logging.warning(message)
        blue(message)


def generic_a_notification_should_be_sent_to_specific_dit_office(
    context: Context, actor_alias: str, mailbox_name: str
):
    actor = get_actor(context, actor_alias)
    mailbox_email = FORMS_API_MAILBOXES[mailbox_name]
    submissions = find_form_submissions_for_dit_office(
        mailbox=mailbox_email, sender=actor.email
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
        f"{mailbox_name} mailbox: {mailbox_email}"
    )


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
        mailbox=mailbox_email, sender=actor.email, uuid=uuid
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
        f"{mailbox_name} mailbox: {mailbox_email}"
    )


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
    urls = [get_page_object(name).URL for name in expected_pages]
    logging.debug(f"Will check {context.driver.current_url} against {urls}")
    results = defaultdict()
    for page_name in expected_pages:
        try:
            should_be_on_page(context, actor_alias, page_name)
            results[page_name] = True
            break
        except AssertionError:
            results[page_name] = False

    with assertion_msg(
        f"{actor_alias} expected to land on one of the following pages: {urls}, "
        f"instead we got to: {context.driver.current_url}"
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


def generic_should_see_prepopulated_fields(
    context: Context, actor_alias: str, table: Table
):
    table.require_columns(["form", "fields"])
    expected_form_fields = {
        row.get("form"): [
            field.strip() for field in row.get("fields").split(",") if field
        ]
        for row in table
    }
    error = f"Expected to check at least 1 list of form fields but got 0"
    assert expected_form_fields, error

    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)

    field_values_to_check = {}
    for form_name, fields in expected_form_fields.items():
        form_page_object = get_page_object(form_name)
        form_full_page_name = get_full_page_name(form_page_object)
        submitted_form_data = actor.forms_data[form_full_page_name]
        for field in fields:
            field_values_to_check[field] = submitted_form_data[field]

    logging.debug(
        f"Will check if form on '{get_full_page_name(page)}' is populated with "
        f"following values: {field_values_to_check}"
    )
    has_action(page, "check_if_populated")
    page.check_if_populated(context.driver, field_values_to_check)


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
        event for event in expected_gtm_events if event not in registered_gtm_events
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
    ids = ["great-header-nav-mobile", "great-header-mobile-nav", "great-header-nav"]
    for value in ids:
        try:
            element = context.driver.find_element(by=By.ID, value=value)
            break
        except NoSuchElementException:
            continue
    else:
        raise
    with selenium_action(context.driver, f"Menu items should be visible"):
        assert element.is_displayed()


def generic_should_be_able_to_print(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_be_able_to_print")
    take_screenshot(context.driver, "should_be_able_to_print")
    page.should_be_able_to_print(context.driver)
    logging.debug(
        f"{actor_alias} is able to print out contents of: {context.driver.current_url}"
    )


def erp_should_see_number_of_product_codes_to_select(
    context: Context, actor_alias: str, comparison_description: str
):
    comparison_details = get_comparison_details(comparison_description)

    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_number_of_product_codes_to_select")
    take_screenshot(context.driver, "should_see_number_of_product_codes_to_select")
    page.should_see_number_of_product_codes_to_select(
        context.driver, comparison_details
    )
    logging.debug(
        f"{actor_alias} saw: {comparison_description} product code(s) to select"
    )


def erp_should_see_number_of_product_categories_to_expand(
    context: Context, actor_alias: str, comparison_description: str
):
    comparison_details = get_comparison_details(comparison_description)

    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_number_of_product_categories_to_expand")
    take_screenshot(context.driver, "should_see_number_of_product_categories_to_expand")
    page.should_see_number_of_product_categories_to_expand(
        context.driver, comparison_details
    )
    logging.debug(
        f"{actor_alias} saw: {comparison_description} product categories(s) to expand"
    )


def erp_should_see_correct_data_on_summary_page(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    take_screenshot(context.driver, "should_see_correct_data_on_summary_page")
    erp.summary.should_see_correct_data_on_summary_page(
        context.driver, actor.forms_data
    )
    logging.debug(f"{actor_alias} saw: all expected data on the ERP Summary page")


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def fas_buyer_should_be_signed_up_for_email_updates(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    response = DIRECTORY_TEST_API_CLIENT.get(f"testapi/buyer/{actor.email}/")
    with assertion_msg(
        f"Expected 200 OK but got {response.status_code} from {response.url}"
    ):
        assert response.status_code == 200
        assert response.json()["email"] == actor.email
        assert response.json()["name"] == actor.alias
        assert response.json()["company_name"] == "AUTOMATED TESTS"
    logging.debug(
        f"{actor_alias} successfully signed up for email updates. "
        f"Here's Buyer's data: {response.json()}"
    )
