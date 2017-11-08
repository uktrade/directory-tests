# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context

from pages import (
    export_readiness_common,
    guidance_common,
    home,
    personalised_journey
)
from registry.pages import get_page_object
from steps.when_impl import (
    triage_should_be_classified_as_new,
    triage_should_be_classified_as_occasional,
    triage_should_be_classified_as_regular
)
from utils import get_actor


def should_see_sections_on_home_page(
        context: Context, actor_name: str, sections: str):
    section_names = sections.lower().split(", ")
    home.should_see_sections(context.driver, section_names)
    logging.debug(
        "%s saw all expected sections on '%s' page", actor_name,
        context.current_page.NAME)


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
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
        "%s was able t see the link to the next category wherever expected",
        actor_alias, next_category)


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
        raise KeyError("Could not recognize: '%s'. Please use: ")
    logging.debug(
        "%s was properly classified as %s exporter", actor_alias,
        classification)


def personalised_should_see_layout_for(
        context: Context, actor_alias: str, classification: str):
    actor = get_actor(context, actor_alias)
    incorporated = actor.are_you_incorporated
    online_marketplaces = actor.do_you_use_online_marketplaces
    code, _ = actor.what_do_you_want_to_export
    if classification == "new":
        personalised_journey.layout_for_new_exporter(
            context.driver, incorporated=incorporated, sector_code=code)
    elif classification == "occasional":
        personalised_journey.layout_for_occasional_exporter(
            context.driver, incorporated=incorporated,
            use_online_marketplaces=online_marketplaces, sector_code=code)
    elif classification == "regular":
        personalised_journey.layout_for_regular_exporter(
            context.driver, incorporated=incorporated, sector_code=code)
    else:
        raise KeyError(
            "Could not recognise '%s'. Please use: new, occasional or "
            "regular" % classification)
    logging.debug(
        "%s saw Personalised Journey page layout tailored for %s exporter",
        actor_alias, classification)


def exred_should_see_articles(
        context: Context, actor_alias: str, category: str):
    export_readiness_common.check_if_correct_articles_are_displayed(
        context.driver, category)
    logging.debug(
        "%s can see correct Articles for Guidance '%s' category and link to "
        "the next category wherever possible", actor_alias, category)
