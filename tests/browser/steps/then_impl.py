# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging
from time import sleep
from typing import List
from urllib.parse import urlparse

import requests
from behave.model import Table
from behave.runner import Context
from retrying import retry

from pages import common_language_selector, exred, fas, get_page_object, invest
from pages.common_actions import (
    assertion_msg,
    clear_driver_cookies,
    get_actor,
    get_last_visited_page,
    update_actor,
)
from pages.exred import contact_us_office_finder_search_results
from settings import (
    HPO_AGENT_EMAIL_ADDRESS,
    HPO_AGENT_EMAIL_SUBJECT,
    HPO_ENQUIRY_CONFIRMATION_SUBJECT,
    HPO_PDF_URLS,
    INVEST_AGENT_CONTACT_CONFIRMATION_SUBJECT,
    INVEST_MAILBOX_ADMIN_EMAIL,
)
from steps import has_action
from utils.gov_notify import (
    get_email_confirmation_notification,
    get_email_confirmations_with_matching_string,
)
from utils.mailgun import mailgun_invest_find_contact_confirmation_email
from utils.pdf import extract_text_from_pdf_bytes
from utils.zendesk import find_tickets


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    has_action(page, "should_be_here")
    if hasattr(page, "URLs"):
        special_page_name = page_name.split(" - ")[1]
        page.should_be_here(context.driver, page_name=special_page_name)
    else:
        page.should_be_here(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> {page}")


def should_be_on_page_or_international_page(
    context: Context, actor_alias: str, page_name: str
):
    page = get_page_object(page_name)
    has_action(page, "should_be_here")
    try:
        page.should_be_here(context.driver)
        update_actor(context, actor_alias, visited_page=page)
        logging.debug("%s is on %s page", actor_alias, page_name)
    except AssertionError:
        exred.international.should_be_here(context.driver)
        logging.debug(
            "%s was redirected to the International page", actor_alias
        )


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
    exred.case_studies_common.should_be_here(
        context.driver, number, title=case_study_title
    )


def should_see_share_widget(context: Context, actor_alias: str):
    driver = context.driver
    exred.case_studies_common.should_see_share_widget(driver)
    logging.debug(
        "%s can see Share Widget on %s", actor_alias, driver.current_url
    )


def should_see_links_to_services(
    context: Context, actor_alias: str, services: list, location: str
):
    page = get_page_object(location)
    has_action(page, "should_see_link_to")
    for service in services:
        page.should_see_link_to(context.driver, "services", service)
        logging.debug(
            "%s can see link to '%s' in '%s'", actor_alias, service, location
        )


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
    subject = exred.article_common.get_article_name(driver)
    exred.article_common.check_share_via_email_link_details(driver, subject, body)
    logging.debug(
        "%s checked that the 'share via email' link contain correct subject: "
        "'%s' and message body: '%s'",
        actor_alias,
        subject,
        body,
    )


def triage_should_see_change_your_answers_link(
    context: Context, actor_alias: str
):
    exred.triage_summary.should_see_change_your_answers_link(context.driver)
    logging.debug("%s can see 'change your answers' link", actor_alias)


def promo_video_check_watch_time(
    context: Context, actor_alias: str, expected_watch_time: int
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "get_video_watch_time")
    watch_time = page.get_video_watch_time(context.driver)
    with assertion_msg(
        "%s expected to watch at least first '%d' seconds of the video but"
        " got '%d'",
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


def promo_video_should_not_see_modal_window(
    context: Context, actor_alias: str
):
    exred.home.should_not_see_video_modal_window(context.driver)
    logging.debug(
        "As expected %s can't see promotional video modal window", actor_alias
    )


def header_check_dit_logo(context: Context, actor_alias: str):
    exred.header.check_dit_logo(context.driver)
    logging.debug("As expected %s can see correct DIT logo", actor_alias)


def header_check_favicon(context: Context, actor_alias: str):
    exred.header.check_dit_favicon(context.driver)
    logging.debug("As expected %s can see correct DIT favicon", actor_alias)


def language_selector_should_see_it(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.should_see_it_on(context.driver, page=page)
    logging.debug("As expected %s can see language selector", actor_alias)


def language_selector_should_not_see_it(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.should_not_see_it_on(
        context.driver, page=page
    )
    logging.debug("As expected %s cannot see language selector", actor_alias)


def language_selector_keyboard_should_be_trapped(
    context: Context, actor_alias: str
):
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.keyboard_should_be_trapped(
        context.driver, page=page
    )


def should_see_page_in_preferred_language(
    context: Context, actor_alias: str, preferred_language: str
):
    common_language_selector.check_page_language_is(
        context.driver, preferred_language
    )
    logging.debug(
        f"{actor_alias} can see '{context.driver.current_url}' page in "
        f"'{preferred_language}",
    )


def fas_search_results_filtered_by_industries(
    context: Context, actor_alias: str, industry_names: List[str]
):
    fas.search_results.should_see_filtered_results(
        context.driver, industry_names
    )
    logging.debug(
        "%s can see results filtered by %s (%s)",
        actor_alias,
        industry_names,
        context.driver.current_url,
    )


def invest_should_see_topic_contents(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_topic")
    for topic in actor.visited_articles:
        page.should_see_topic(context.driver, topic)
        logging.debug(
            "%s can see contents of '%s' topic on %s",
            actor_alias,
            topic,
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


def stats_and_tracking_elements_should_be_present(
    context: Context, names: Table
):
    element_names = [row[0] for row in names]

    for name in element_names:
        invest.pixels.should_be_present(context.driver, name)


def stats_and_tracking_elements_should_not_be_present(
    context: Context, names: Table
):
    element_names = [row[0] for row in names]

    for name in element_names:
        invest.pixels.should_not_be_present(context.driver, name)


def invest_should_see_uk_gov_logo(
        context: Context, actor_alias: str, section: str):
    if section.lower() == "header":
        invest.header.check_logo(context.driver)
    else:
        invest.footer.check_logo(context.driver)
    logging.debug(
        "%s can see correct UK GOV logo in page %s on %s", actor_alias,
        section, context.driver.current_url)


def invest_should_receive_contact_confirmation_email(
        context: Context, actor_alias: str, sender_email: str):
    actor = get_actor(context, actor_alias)
    sleep(5)
    mailgun_invest_find_contact_confirmation_email(
        context, sender_email, actor.email)


def invest_mailbox_admin_should_receive_contact_confirmation_email(
        context: Context, sender_email: str):
    mailgun_invest_find_contact_confirmation_email(
        context, sender_email, INVEST_MAILBOX_ADMIN_EMAIL,
        subject=INVEST_AGENT_CONTACT_CONFIRMATION_SUBJECT)


def hpo_should_receive_enquiry_confirmation_email(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=actor.email,
        subject=HPO_ENQUIRY_CONFIRMATION_SUBJECT,
        strings=HPO_PDF_URLS,
    )


def hpo_agent_should_receive_enquiry_email(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=HPO_AGENT_EMAIL_ADDRESS,
        subject=HPO_AGENT_EMAIL_SUBJECT,
        strings=[actor.email] + HPO_PDF_URLS,
    )


def form_check_state_of_element(
        context: Context, actor_alias: str, element: str, state: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "check_state_of_form_element")
    page.check_state_of_form_element(context.driver, element, state)
    logging.debug(
        f"{actor_alias} saw {element} in expected {state} state on "
        f"{context.driver.current_url}"
    )


def pdf_check_expected_details(
        context: Context, actor_alias: str, details_table: Table):
    pdfs = context.pdfs
    pdf_texts = [(pdf["href"], extract_text_from_pdf_bytes(pdf["pdf"]))
                  for pdf in pdfs]
    details = {
        item[0].split(" = ")[0]: item[0].split(" = ")[1]
        for item in details_table
    }
    for href, text in pdf_texts:
        for name, value in details.items():
            error_message = (
                f"Could not find {name}: {value} in PDF text downloaded from "
                f"{href}")
            assert value in text, error_message
            logging.debug(
                f"{actor_alias} saw correct {name} in the PDF downloaded from "
                f"{href}")
    context.pdf_texts = pdf_texts


def pdf_check_for_dead_links(context: Context):
    pdf_texts = context.pdf_texts
    links = set([word
                 for _, text in pdf_texts
                 for word in text.split()
                 if any(item in word for item in ["http", "https", "www"])])
    logging.debug(f"Links found in PDFs: {links}")
    for link in links:
        parsed = urlparse(link)
        if not parsed.netloc:
            link = f"http://{link}"
        response = requests.get(link)
        error_message = (
            f"Expected 200 from {link} but got {response.status_code} instead")
        assert response.status_code == 200, error_message
    logging.debug("All links in PDFs returned 200 OK")


def form_should_see_error_messages(
        context: Context, actor_alias: str,
        message: str = "This field is required"):
    page_source = context.driver.page_source
    assertion_error = f"Expected error message '{message}' is not present"
    assert message in page_source, assertion_error
    logging.debug(f"{actor_alias} saw expected error message '{message}'")


@retry(wait_fixed=10000, stop_max_attempt_number=6, wrap_exception=False)
def zendesk_should_receive_confirmation_email(
        context: Context, actor_alias: str, subject: str):
    actor = get_actor(context, actor_alias)
    email = actor.email
    tickets = find_tickets(email, subject)
    assert tickets, f"Expected to find at least 1 ticket for {email} but got 0"
    error_msg = (f"Expected to find only 1 '{subject}' ticket for {email} but "
                 f"found {len(tickets)} instead")
    assert len(tickets) == 1, error_msg
    logging.debug(f"{actor_alias} received '{subject}' email from Zendesk")


def should_see_articles_filtered_by_tag(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    tag = actor.last_tag
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "is_filtered_by_tag")
    page.is_filtered_by_tag(context.driver, tag)


@retry(wait_fixed=10000, stop_max_attempt_number=6, wrap_exception=False)
def eu_exit_contact_us_should_receive_confirmation_email(
        context: Context, actor_alias: str, subject: str):
    actor = get_actor(context, actor_alias)
    confirmation = get_email_confirmation_notification(
        email=actor.email,
        subject=subject,
    )
    assert confirmation


def generic_should_see_form_choices(
        context: Context, actor_alias: str, option_names: Table):
    option_names = [row[0] for row in option_names]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "should_see_form_choices")
    page.should_see_form_choices(context.driver, option_names)


def generic_article_counters_should_match(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    _, expected_article_counter = actor.element_details
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "article_counter_is_equal_to")
    page.article_counter_is_equal_to(context.driver, expected_article_counter)


def generic_article_counter_should_match_number_of_articles(context, actor_alias):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "article_counter_matches_number_of_articles")
    page.article_counter_matches_number_of_articles(context.driver)


def office_finder_should_see_correct_office_details(
        context: Context, actor_alias: str, trade_office: str, city: str):
    contact_us_office_finder_search_results.should_see_office_details(
        context.driver, trade_office, city)
    logging.debug(
        f"{actor_alias} found contact details for trade '{trade_office}' office"
        f" in '{city}'")
