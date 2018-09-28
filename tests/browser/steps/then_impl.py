# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging
from typing import List

from behave.model import Table
from behave.runner import Context

from pages import common_language_selector, exread, fas, get_page_object, invest
from pages.common_actions import (
    assertion_msg,
    clear_driver_cookies,
    get_actor,
    get_last_visited_page,
    update_actor
)
from registry.articles import get_article, get_articles
from steps import has_action
from steps.when_impl import (
    triage_should_be_classified_as_new,
    triage_should_be_classified_as_occasional,
    triage_should_be_classified_as_regular,
)
from utils.mailgun import mailgun_invest_find_contact_confirmation_email


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    has_action(page, "should_be_here")
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
        exread.international.should_be_here(context.driver)
        logging.debug(
            "%s was redirected to the International page", actor_alias
        )


def guidance_ribbon_should_be_visible(context: Context, actor_alias: str):
    driver = context.driver
    exread.guidance_common.ribbon_should_be_visible(driver)
    logging.debug(
        "%s can see Guidance Ribbon on %s", actor_alias, driver.current_url
    )


def guidance_tile_should_be_highlighted(
    context: Context, actor_alias: str, tile: str
):
    driver = context.driver
    exread.guidance_common.ribbon_tile_should_be_highlighted(driver, tile)
    logging.debug(
        "%s can see highlighted Guidance Ribbon '%s' tile on %s",
        actor_alias,
        tile,
        driver.current_url,
    )


def guidance_should_see_article_read_counter(
    context: Context, actor_alias: str, category: str, expected: int
):
    exread.guidance_common.correct_article_read_counter(
        context.driver, category, expected
    )
    logging.debug(
        "%s can see correct Guidance Read Counter equal to %d on %s",
        actor_alias,
        expected,
        category,
    )


def guidance_should_see_total_number_of_articles(
    context: Context, actor_alias: str, category: str
):
    exread.guidance_common.correct_total_number_of_articles(context.driver, category)
    logging.debug(
        "%s can see Total Number of Articles for Guidance '%s' category",
        actor_alias,
        category,
    )


def guidance_should_see_articles(
    context: Context, actor_alias: str, category: str
):
    exread.guidance_common.check_if_correct_articles_are_displayed(
        context.driver, category
    )
    logging.debug(
        "%s can see correct Articles for Guidance '%s' category and link to "
        "the next category wherever possible",
        actor_alias,
        category,
    )


def guidance_check_if_link_to_next_category_is_displayed(
    context: Context, actor_alias: str, next_category: str
):
    exread.guidance_common.check_if_link_to_next_category_is_displayed(
        context.driver, next_category
    )
    logging.debug(
        "%s was able to see the link to the next category '%s' wherever"
        " expected",
        actor_alias,
        next_category,
    )


def guidance_expected_page_elements_should_be_visible(
    context: Context, actor_alias: str, elements: list
):
    exread.guidance_common.check_elements_are_visible(context.driver, elements)
    logging.debug(
        "%s can see all expected page elements: '%s' on current Guidance "
        "Articles page: %s",
        actor_alias,
        elements,
        context.driver.current_url,
    )


def personalised_journey_should_see_read_counter(
    context: Context, actor_alias: str, exporter_status: str
):
    exread.personalised_journey.should_see_read_counter(
        context.driver, exporter_status=exporter_status
    )
    logging.debug(
        "%s can see Guidance Article Read Counter on the Personalised Journey "
        "page: %s",
        actor_alias,
        context.driver.current_url,
    )


def triage_should_be_classified_as(
    context: Context, actor_alias: str, classification: str
):
    if classification == "new":
        triage_should_be_classified_as_new(context)
    elif classification == "occasional":
        triage_should_be_classified_as_occasional(context)
    elif classification == "regular":
        triage_should_be_classified_as_regular(context)
    else:
        raise KeyError(
            "Couldn't recognize: '%s'. Please use: new, occasional or regular",
            classification,
        )
    logging.debug(
        "%s was properly classified as %s exporter",
        actor_alias,
        classification,
    )


def personalised_should_see_layout_for(
    context: Context, actor_alias: str, classification: str
):
    actor = get_actor(context, actor_alias)
    incorporated = actor.are_you_incorporated
    online_marketplaces = actor.do_you_use_online_marketplaces
    code = None
    if actor.what_do_you_want_to_export:
        _, code, _ = actor.what_do_you_want_to_export
    exread.personalised_journey.should_be_here(context.driver)
    if classification.lower() == "new":
        exread.personalised_journey.layout_for_new_exporter(
            context.driver, incorporated=incorporated, sector_code=code
        )
    elif classification.lower() == "occasional":
        exread.personalised_journey.layout_for_occasional_exporter(
            context.driver,
            incorporated=incorporated,
            use_online_marketplaces=online_marketplaces,
            sector_code=code,
        )
    elif classification.lower() == "regular":
        exread.personalised_journey.layout_for_regular_exporter(
            context.driver, incorporated=incorporated, sector_code=code
        )
    else:
        raise KeyError(
            "Could not recognise '%s'. Please use: new, occasional or "
            "regular" % classification
        )
    logging.debug(
        "%s saw Personalised Journey page layout tailored for %s exporter",
        actor_alias,
        classification,
    )


def export_readiness_should_see_articles(
    context: Context, actor_alias: str, category: str
):
    exread.common.check_if_correct_articles_are_displayed(
        context.driver, category
    )
    logging.debug(
        "%s can see correct Articles for Guidance '%s' category and link to "
        "the next category wherever possible",
        actor_alias,
        category,
    )


def export_readiness_expected_page_elements_should_be_visible(
    context: Context, actor_alias: str, elements: List[str]
):
    exread.common.should_see_sections(context.driver, elements)
    logging.debug(
        "%s can see all expected page elements: '%s' on current Guidance "
        "Articles page: %s",
        actor_alias,
        elements,
        context.driver.current_url,
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


def articles_should_see_in_correct_order(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    visited_articles = actor.visited_articles
    for visited_article in visited_articles:
        index = visited_article.index
        title = visited_article.title
        expected_article = get_article(group, category, title)
        with assertion_msg(
            "Expected to see '%s' '%s' article '%s' on position %d but %s "
            "viewed it as %d",
            group,
            category,
            title,
            expected_article.index,
            actor_alias,
            index,
        ):
            assert expected_article.index == index
        logging.debug(
            "%s saw '%s' '%s' article '%s' at correct position %d",
            actor_alias,
            group,
            category,
            title,
            index,
        )


def articles_should_not_see_link_to_next_article(
    context: Context, actor_alias: str
):
    exread.article_common.should_not_see_link_to_next_article(context.driver)
    logging.debug(
        "As expected %s didn't see link to the next article", actor_alias
    )


def articles_should_not_see_personas_end_page(
    context: Context, actor_alias: str
):
    exread.article_common.should_be_here(context.driver)
    logging.debug(
        "As expected %s wasn't taken to the personas end page but remained on "
        "the last article page",
        actor_alias,
    )


def articles_should_see_link_to_first_article_from_next_category(
    context: Context, actor_alias: str, next_category: str
):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    first_article = get_articles(group, next_category)[0]
    exread.article_common.check_if_link_to_next_article_is_displayed(
        driver, first_article.title
    )
    logging.debug(
        "%s can see link to the first article '%s' from '%s' category",
        actor_alias,
        first_article.title,
        next_category,
    )
    logging.debug("%s wasn't presented with Personas end page", actor_alias)


def articles_should_see_article_as_read(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_article = actor.visited_articles[0]
    exread.article_common.should_see_article_as_read(
        context.driver, visited_article.title
    )
    logging.debug(
        "%s can see that '%s' articles is marked as read",
        actor_alias,
        visited_article.title,
    )


def articles_should_see_read_counter_increase(
    context: Context, actor_alias: str, increase: int
):
    actor = get_actor(context, actor_alias)
    previous_read_counter = actor.article_list_read_counter
    current_read_counter = exread.article_common.get_read_counter(context.driver)
    difference = current_read_counter - previous_read_counter
    with assertion_msg(
        "Expected the Read Counter to increase by '%s', but it increased"
        " by '%s'",
        increase,
        difference,
    ):
        assert difference == increase


def articles_should_see_time_to_complete_decrease(
    context: Context, actor_alias: str
):
    actor = get_actor(context, actor_alias)
    previous_time_to_complete = actor.article_list_time_to_complete
    current_time_to_complete = exread.article_common.get_time_to_complete(
        context.driver
    )
    visited_article = actor.visited_articles[0]
    difference = current_time_to_complete - previous_time_to_complete
    logging.debug(
        "Time to Complete remaining Articles changed by %d mins after reading"
        " %s",
        difference,
        visited_article.title,
    )
    with assertion_msg(
        "Expected the Time to Complete reading remaining Articles to "
        "decrease or remain unchanged after reading '%s', but it actually "
        "increased by %d. Expected time to read in seconds: %d",
        visited_article.title,
        difference,
        visited_article.time_to_read,
    ):
        assert difference <= 0


def articles_should_not_see_feedback_widget(context: Context):
    exread.article_common.should_not_see_feedback_widget(context.driver)
    logging.debug("Feedback widget is not visible any more")


def articles_should_be_thanked_for_feedback(
    context: Context, actor_alias: str
):
    exread.article_common.should_see_feedback_result(context.driver)
    logging.debug("%s was thanked for the feedback", actor_alias)


def articles_total_number_of_articles_should_not_change(
    context: Context, actor_alias: str
):
    actor = get_actor(context, actor_alias)
    driver = context.driver
    previous_total_articles = actor.articles_total_number
    current_total_articles = exread.article_common.get_total_articles(driver)
    with assertion_msg(
        "Expected Total Number of Articles to Read to be: %d but got " "%d",
        previous_total_articles,
        current_total_articles,
    ):
        assert current_total_articles == previous_total_articles


def expected_page_elements_should_not_be_visible_on_get_finance(
    context: Context, actor_alias: str, elements: list
):
    exread.get_finance.check_elements_are_not_visible(context.driver, elements)
    logging.debug(
        "%s cannot see all expected page elements: '%s' on current page %s",
        actor_alias,
        elements,
        context.driver.current_url,
    )


def case_studies_should_see_case_study(
    context: Context, actor_alias: str, case_study_number: str
):
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    number = case_study_numbers[case_study_number.lower()]
    case_study_title = get_actor(context, actor_alias).case_study_title
    exread.case_studies_common.should_be_here(
        context.driver, number, title=case_study_title
    )


def should_see_share_widget(context: Context, actor_alias: str):
    driver = context.driver
    exread.case_studies_common.should_see_share_widget(driver)
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


def personalised_journey_should_not_see_banner_and_top_10_table(
    context: Context, actor_alias: str
):
    exread.personalised_journey.should_not_see_banner_and_top_10_table(context.driver)
    actor = get_actor(context, actor_alias)
    _, code, sector = actor.what_do_you_want_to_export
    logging.debug(
        "As expected %s can't see Top Importer banner and Top 10 Importers "
        "table on personalised page for '%s - %s' sector",
        actor_alias,
        code,
        sector,
    )


def personalised_journey_should_see_banner_and_top_10_table(
    context: Context, actor_alias: str
):
    actor = get_actor(context, actor_alias)
    _, code, sector = actor.what_do_you_want_to_export
    exread.personalised_journey.should_see_banner_and_top_10_table(
        context.driver, sector
    )
    logging.debug(
        "As expected %s can see Top Importer banner and Top 10 Importers "
        "table on personalised page for '%s - %s' sector",
        actor_alias,
        code,
        sector,
    )


def articles_should_see_read_counter_set_to(
    context: Context, actor_alias: str, expected_value: int
):
    current_read_counter = exread.article_common.get_read_counter(context.driver)
    with assertion_msg(
        "Expected to see Read Counter set to %d but got %s",
        expected_value,
        current_read_counter,
    ):
        assert current_read_counter == expected_value
    logging.debug(
        "%s saw Reading Counter set to expected value of: %d",
        actor_alias,
        expected_value,
    )


def articles_read_counter_same_as_before_registration(
    context: Context, actor_alias: str
):
    actor = get_actor(context, actor_alias)
    preregistration_value = actor.articles_read_counter
    articles_should_see_read_counter_set_to(
        context, actor_alias, preregistration_value
    )


def articles_should_not_see_link_to_sign_in(
    context: Context, actor_alias: str, page_name: str
):
    page = get_page_object(page_name)
    has_action(page, "should_not_see_link_to_sign_in")
    page.should_not_see_link_to_sign_in(context.driver)
    logging.debug(
        "As expected %s did not see 'Sign In' link on the '%s' page",
        actor_alias,
        page_name,
    )


def articles_should_not_see_link_to_register(
    context: Context, actor_alias: str, page_name: str
):
    page = get_page_object(page_name)
    has_action(page, "should_not_see_link_to_register")
    page.should_not_see_link_to_register(context.driver)
    logging.debug(
        "As expected %s did not see 'Register' link on the '%s' page",
        actor_alias,
        page_name,
    )


def articles_read_counter_should_be_merged(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_articles = actor.visited_articles
    current_read_counter = exread.article_common.get_read_counter(context.driver)
    number_of_visited_articles = len(set(visited_articles))
    with assertion_msg(
        "%s expected to see current article reading counter to be %d but "
        "got %d",
        actor_alias,
        number_of_visited_articles,
        current_read_counter,
    ):
        assert current_read_counter == number_of_visited_articles


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
    subject = exread.article_common.get_article_name(driver)
    exread.article_common.check_share_via_email_link_details(driver, subject, body)
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
    exread.triage_summary.should_see_change_your_answers_link(context.driver)
    logging.debug("%s can see 'change your answers' link", actor_alias)


def promo_video_check_watch_time(
    context: Context, actor_alias: str, expected_watch_time: int
):
    watch_time = exread.home.get_video_watch_time(context.driver)
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
    exread.home.should_not_see_video_modal_window(context.driver)
    logging.debug(
        "As expected %s can't see promotional video modal window", actor_alias
    )


def header_check_dit_logo(context: Context, actor_alias: str):
    exread.header.check_dit_logo(context.driver)
    logging.debug("As expected %s can see correct DIT logo", actor_alias)


def header_check_favicon(context: Context, actor_alias: str):
    exread.header.check_dit_favicon(context.driver)
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
    mailgun_invest_find_contact_confirmation_email(
        context, sender_email, actor.email)


def hpo_should_receive_enquiry_confirmation_email(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    get_email_confirmations_with_matching_string(
        recipient_email=actor.email,
        subject=HPO_ENQUIRY_CONFIRMATION_SUBJECT,
        strings=HPO_PDF_URLS,
    )


