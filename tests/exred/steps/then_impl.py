# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context

from pages import (
    article_common,
    case_studies_common,
    export_readiness_common,
    get_finance,
    guidance_common,
    header,
    home,
    language_selector,
    personalised_journey,
    triage_summary
)
from registry.articles import get_article, get_articles
from registry.pages import get_page_object
from steps.when_impl import (
    triage_should_be_classified_as_new,
    triage_should_be_classified_as_occasional,
    triage_should_be_classified_as_regular
)
from utils import assertion_msg, clear_driver_cookies, get_actor


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    assert hasattr(page, "should_be_here")
    page.should_be_here(context.driver)
    logging.debug("%s is on %s page", actor_alias, page_name)


def guidance_ribbon_should_be_visible(context: Context, actor_alias: str):
    driver = context.driver
    guidance_common.ribbon_should_be_visible(driver)
    logging.debug(
        "%s can see Guidance Ribbon on %s", actor_alias, driver.current_url)


def guidance_tile_should_be_highlighted(
        context: Context, actor_alias: str, tile: str):
    driver = context.driver
    guidance_common.ribbon_tile_should_be_highlighted(driver, tile)
    logging.debug(
        "%s can see highlighted Guidance Ribbon '%s' tile on %s",
        actor_alias, tile, driver.current_url)


def guidance_should_see_article_read_counter(
        context: Context, actor_alias: str, category: str, expected: int):
    guidance_common.correct_article_read_counter(
        context.driver, category, expected)
    logging.debug(
        "%s can see correct Guidance Read Counter equal to %d on %s",
        actor_alias, expected, category)


def guidance_should_see_total_number_of_articles(
        context: Context, actor_alias: str, category: str):
    guidance_common.correct_total_number_of_articles(context.driver, category)
    logging.debug(
        "%s can see Total Number of Articles for Guidance '%s' category",
        actor_alias, category)


def guidance_should_see_articles(
        context: Context, actor_alias: str, category: str):
    guidance_common.check_if_correct_articles_are_displayed(
        context.driver, category)
    logging.debug(
        "%s can see correct Articles for Guidance '%s' category and link to "
        "the next category wherever possible", actor_alias, category)


def guidance_check_if_link_to_next_category_is_displayed(
        context: Context, actor_alias: str, next_category: str):
    guidance_common.check_if_link_to_next_category_is_displayed(
        context.driver, next_category)
    logging.debug(
        "%s was able to see the link to the next category '%s' wherever"
        " expected", actor_alias, next_category)


def guidance_expected_page_elements_should_be_visible(
        context: Context, actor_alias: str, elements: list):
    guidance_common.check_elements_are_visible(context.driver, elements)
    logging.debug(
        "%s can see all expected page elements: '%s' on current Guidance "
        "Articles page: %s", actor_alias, elements, context.driver.current_url)


def personalised_journey_should_see_read_counter(
        context: Context, actor_alias: str, exporter_status: str):
    personalised_journey.should_see_read_counter(
        context.driver, exporter_status=exporter_status)
    logging.debug(
        "%s can see Guidance Article Read Counter on the Personalised Journey "
        "page: %s", actor_alias, context.driver.current_url)


def triage_should_be_classified_as(
        context: Context, actor_alias: str, classification: str):
    if classification == "new":
        triage_should_be_classified_as_new(context)
    elif classification == "occasional":
        triage_should_be_classified_as_occasional(context)
    elif classification == "regular":
        triage_should_be_classified_as_regular(context)
    else:
        raise KeyError(
            "Couldn't recognize: '%s'. Please use: new, occasional or regular",
            classification)
    logging.debug(
        "%s was properly classified as %s exporter", actor_alias,
        classification)


def personalised_should_see_layout_for(
        context: Context, actor_alias: str, classification: str):
    actor = get_actor(context, actor_alias)
    incorporated = actor.are_you_incorporated
    online_marketplaces = actor.do_you_use_online_marketplaces
    code, _ = actor.what_do_you_want_to_export
    if classification.lower() == "new":
        personalised_journey.layout_for_new_exporter(
            context.driver, incorporated=incorporated, sector_code=code)
    elif classification.lower() == "occasional":
        personalised_journey.layout_for_occasional_exporter(
            context.driver, incorporated=incorporated,
            use_online_marketplaces=online_marketplaces, sector_code=code)
    elif classification.lower() == "regular":
        personalised_journey.layout_for_regular_exporter(
            context.driver, incorporated=incorporated, sector_code=code)
    else:
        raise KeyError(
            "Could not recognise '%s'. Please use: new, occasional or "
            "regular" % classification)
    logging.debug(
        "%s saw Personalised Journey page layout tailored for %s exporter",
        actor_alias, classification)


def export_readiness_should_see_articles(
        context: Context, actor_alias: str, category: str):
    export_readiness_common.check_if_correct_articles_are_displayed(
        context.driver, category)
    logging.debug(
        "%s can see correct Articles for Guidance '%s' category and link to "
        "the next category wherever possible", actor_alias, category)


def export_readiness_expected_page_elements_should_be_visible(
        context: Context, actor_alias: str, elements: list):
    export_readiness_common.check_elements_are_visible(
        context.driver, elements)
    logging.debug(
        "%s can see all expected page elements: '%s' on current Guidance "
        "Articles page: %s", actor_alias, elements, context.driver.current_url)


def should_see_sections(
        context: Context, actor_alias: str, sections: list, page_name: str):
    page = get_page_object(page_name)
    assert hasattr(page, "should_see_section")
    for section in sections:
        page.should_see_section(context.driver, section)
        logging.debug(
            "%s can see '%s' section on %s page", actor_alias, section,
            page_name)


def should_not_see_sections(
        context: Context, actor_alias: str, sections: list, page_name: str):
    page = get_page_object(page_name)
    assert hasattr(page, "should_not_see_section")
    for section in sections:
        page.should_not_see_section(context.driver, section)
        logging.debug(
            "As expected %s cannot see '%s' section on %s page", actor_alias,
            section, page_name)


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
                "viewed it as %d", group, category, title,
                expected_article.index, actor_alias, index):
            assert expected_article.index == index
        logging.debug(
            "%s saw '%s' '%s' article '%s' at correct position %d",
            actor_alias, group, category, title, index)


def articles_should_not_see_link_to_next_article(
        context: Context, actor_alias: str):
    article_common.should_not_see_link_to_next_article(context.driver)
    logging.debug(
        "As expected %s didn't see link to the next article", actor_alias)


def articles_should_not_see_personas_end_page(
        context: Context, actor_alias: str):
    article_common.should_not_see_personas_end_page(context.driver)


def articles_should_see_link_to_first_article_from_next_category(
        context: Context, actor_alias: str, next_category: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    first_article = get_articles(group, next_category)[0]
    article_common.check_if_link_to_next_article_is_displayed(
        driver, first_article.title)
    logging.debug(
        "%s can see link to the first article '%s' from '%s' category",
        actor_alias, first_article.title, next_category)
    logging.debug("%s wasn't presented with Personas end page", actor_alias)


def articles_should_see_article_as_read(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_article = actor.visited_articles[0]
    article_common.should_see_article_as_read(
        context.driver, visited_article.title)
    logging.debug(
        "%s can see that '%s' articles is marked as read", actor_alias,
        visited_article.title)


def articles_should_see_read_counter_increase(
        context: Context, actor_alias: str, increase: int):
    actor = get_actor(context, actor_alias)
    previous_read_counter = actor.article_list_read_counter
    current_read_counter = article_common.get_read_counter(context.driver)
    difference = current_read_counter - previous_read_counter
    with assertion_msg(
            "Expected the Read Counter to increase by '%s', but it increased"
            " by '%s'", increase, difference):
        assert difference == increase


def articles_should_see_time_to_complete_decrease(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    previous_time_to_complete = actor.article_list_time_to_complete
    current_time_to_complete = article_common.get_time_to_complete(
        context.driver)
    visited_article = actor.visited_articles[0]
    difference = current_time_to_complete - previous_time_to_complete
    logging.debug(
        "Time to Complete remaining Articles changed by %d mins after reading"
        " %s", difference, visited_article.title)
    with assertion_msg(
            "Expected the Time to Complete reading remaining Articles to "
            "decrease or remain unchanged after reading '%s', but it actually "
            "increased by %d. Expected time to read in seconds: %d",
            visited_article.title, difference, visited_article.time_to_read):
        assert difference <= 0


def articles_should_not_see_feedback_widget(context: Context):
    article_common.should_not_see_feedback_widget(context.driver)
    logging.debug("Feedback widget is not visible any more")


def articles_should_be_thanked_for_feedback(context, actor_alias):
    article_common.should_see_feedback_result(context.driver)
    logging.debug("%s was thanked for the feedback", actor_alias)


def articles_total_number_of_articles_should_not_change(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    driver = context.driver
    previous_total_articles = actor.articles_total_number
    current_total_articles = article_common.get_total_articles(driver)
    with assertion_msg(
            "Expected Total Number of Articles to Read to be: %d but got "
            "%d", previous_total_articles, current_total_articles):
        assert current_total_articles == previous_total_articles


def expected_page_elements_should_not_be_visible_on_get_finance(
        context: Context, actor_alias: str, elements: list):
    get_finance.check_elements_are_not_visible(context.driver, elements)
    logging.debug(
        "%s cannot see all expected page elements: '%s' on current page %s",
        actor_alias, elements, context.driver.current_url)


def case_studies_should_see_case_study(
        context: Context, actor_alias: str, case_study_number: str):
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    number = case_study_numbers[case_study_number.lower()]
    case_study_title = get_actor(context, actor_alias).case_study_title
    case_studies_common.should_be_here(
        context.driver, number, title=case_study_title)


def should_see_share_widget(context: Context, actor_alias: str):
    driver = context.driver
    case_studies_common.should_see_share_widget(driver)
    logging.debug(
        "%s can see Share Widget on %s", actor_alias, driver.current_url)


def should_see_links_to_services(
        context: Context, actor_alias: str, services: list, location: str):
    page_object = get_page_object(location)
    assert hasattr(page_object, "should_see_link_to")
    for service in services:
        page_object.should_see_link_to(context.driver, "services", service)
        logging.debug(
            "%s can see link to '%s' in '%s'", actor_alias, service, location)


def personalised_journey_should_not_see_banner_and_top_10_table(
        context: Context, actor_alias: str):
    personalised_journey.should_not_see_banner_and_top_10_table(context.driver)
    actor = get_actor(context, actor_alias)
    code, sector = actor.what_do_you_want_to_export
    logging.debug(
        "As expected %s can't see Top Importer banner and Top 10 Importers "
        "table on personalised page for '%s - %s' sector", actor_alias, code,
        sector)


def personalised_journey_should_see_banner_and_top_10_table(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    code, sector = actor.what_do_you_want_to_export
    personalised_journey.should_see_banner_and_top_10_table(
        context.driver, sector)
    logging.debug(
        "As expected %s can see Top Importer banner and Top 10 Importers "
        "table on personalised page for '%s - %s' sector", actor_alias, code,
        sector)


def articles_should_see_read_counter_set_to(
        context: Context, actor_alias: str, expected_value: int):
    current_read_counter = article_common.get_read_counter(context.driver)
    with assertion_msg(
            "Expected to see Read Counter set to %d but got %s",
            expected_value, current_read_counter):
        assert current_read_counter == expected_value
    logging.debug(
        "%s saw Reading Counter set to expected value of: %d", actor_alias,
        expected_value)


def articles_read_counter_same_as_before_registration(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    preregistration_value = actor.articles_read_counter
    articles_should_see_read_counter_set_to(
        context, actor_alias, preregistration_value)


def articles_should_not_see_link_to_sign_in(
        context: Context, actor_alias: str, page_name: str):
    page_object = get_page_object(page_name)
    assert hasattr(page_object, "should_not_see_link_to_sign_in")
    page_object.should_not_see_link_to_sign_in(context.driver)
    logging.debug(
        "As expected %s did not see 'Sign In' link on the '%s' page",
        actor_alias, page_name)


def articles_should_not_see_link_to_register(
        context: Context, actor_alias: str, page_name: str):
    page_object = get_page_object(page_name)
    assert hasattr(page_object, "should_not_see_link_to_register")
    page_object.should_not_see_link_to_register(context.driver)
    logging.debug(
        "As expected %s did not see 'Register' link on the '%s' page",
        actor_alias, page_name)


def articles_read_counter_should_be_merged(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_articles = actor.visited_articles
    current_read_counter = article_common.get_read_counter(context.driver)
    number_of_visited_articles = len(set(visited_articles))
    with assertion_msg(
            "%s expected to see current article reading counter to be %d but "
            "got %d", actor_alias, number_of_visited_articles,
            current_read_counter):
        assert current_read_counter == number_of_visited_articles


def articles_should_be_on_share_page(
        context: Context, actor_alias: str, social_media: str):
    page_name = "share on {}".format(social_media.lower())
    social_media_page = get_page_object(page_name)
    assert hasattr(social_media_page, "should_be_here")
    social_media_page.should_be_here(context.driver)
    logging.debug("%s is on the '%s' share page", actor_alias, social_media)


def share_page_should_be_prepopulated(
        context: Context, actor_alias: str, social_media: str):
    page_name = "share on {}".format(social_media.lower())
    social_media_page = get_page_object(page_name)
    assert hasattr(social_media_page, "check_if_populated")
    shared_url = context.article_url
    social_media_page.check_if_populated(context.driver, shared_url)
    clear_driver_cookies(driver=context.driver)
    logging.debug(
        "%s saw '%s' share page populated with appropriate data", actor_alias,
        social_media)


def share_page_via_email_should_have_article_details(
        context: Context, actor_alias: str):
    driver = context.driver
    body = driver.current_url
    subject = article_common.get_article_name(driver)
    article_common.check_share_via_email_link_details(driver, subject, body)
    logging.debug(
        "%s checked that the 'share via email' link contain correct subject: "
        "'%s' and message body: '%s'", actor_alias, subject, body)


def triage_should_see_change_your_answers_link(
        context: Context, actor_alias: str):
    triage_summary.should_see_change_your_answers_link(context.driver)
    logging.debug("%s can see 'change your answers' link", actor_alias)


def promo_video_check_watch_time(
        context: Context, actor_alias: str, expected_watch_time: int):
    watch_time = home.get_video_watch_time(context.driver)
    with assertion_msg(
            "%s expected to watch at least first '%d' seconds of the video but"
            " got '%d'", actor_alias, expected_watch_time, watch_time):
        assert watch_time >= expected_watch_time
    logging.debug("%s was able to watch see at least first '%d' seconds of the"
                  " promotional video", actor_alias, expected_watch_time)


def promo_video_should_not_see_modal_window(
        context: Context, actor_alias: str):
    home.should_not_see_video_modal_window(context.driver)
    logging.debug(
        "As expected %s can't see promotional video modal window", actor_alias)


def header_check_dit_logo(context, actor_alias):
    header.check_dit_logo(context.driver)
    logging.debug("As expected %s can see correct DIT logo", actor_alias)


def header_check_favicon(context: Context, actor_alias: str):
    header.check_dit_favicon(context.driver)
    logging.debug("As expected %s can see correct DIT favicon", actor_alias)


def language_selector_should_see_it(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    language_selector.should_see_it_on(context.driver, page_name=visited_page)
    logging.debug("As expected %s can see language selector", actor_alias)


def language_selector_should_not_see_it(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    language_selector.should_not_see_it_on(
        context.driver, page_name=visited_page)
    logging.debug("As expected %s cannot see language selector", actor_alias)


def language_selector_keyboard_should_be_trapped(
        context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    language_selector.keyboard_should_be_trapped(
        context.driver, page_name=visited_page)


def should_see_page_in_preferred_language(
        context: Context, actor_alias: str, preferred_language: str):
    language_selector.check_page_language_is(
        context.driver, preferred_language)
    logging.debug(
        "%s can see '%' page in '%s", actor_alias, context.current_url,
        preferred_language)
