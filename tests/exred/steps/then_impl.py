# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context

from pages import guidance_common, home, personalised_journey
from registry.pages import get_page_object


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
