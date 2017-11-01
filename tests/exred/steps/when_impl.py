# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random

from behave.runner import Context

from pages import (
    footer,
    header,
    home,
    personalised_journey,
    triage_are_you_registered_with_companies_house,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_result,
    triage_what_is_your_sector
)
from registry.pages import get_page_object
from utils import add_actor, get_actor, unauthenticated_actor, update_actor


def visit_page(
        context: Context, actor_name: str, page_name: str, *,
        first_time: bool = False):
    context.current_page = get_page_object(page_name)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_name, page_name,
        context.current_page.URL)
    context.current_page.visit(context.driver, first_time=first_time)


def finish_triage_as(context: Context, actor_alias: str):
    """Will finish triage with randomly selected exporting status."""
    exporter_status = random.choice(["new", "occasional", "regular"])
    triage_classify_as(context, actor_alias, exporter_status)


def actor_classifies_himself_as(
        context: Context, actor_alias: str, exporter_status: str):
    actor = unauthenticated_actor(
        actor_alias, self_classification=exporter_status)
    add_actor(context, actor)


def open_group_element(
        context: Context, group: str, element: str, location: str):
    driver = context.driver
    if location == "home page":
        home.open(driver, group, element)
    elif location == "header menu":
        header.open(driver, group, element)
    elif location == "footer links":
        footer.open(driver, group, element)


def guidance_open_category(
        context: Context, actor: str, category: str, location: str):
    home.visit(driver=context.driver)
    logging.debug(
        "%s is about to open Guidance '%s' category from %s",
        actor, category, location)
    open_group_element(
        context, group="guidance", element=category, location=location)


def start_triage(context: Context, actor_alias: str):
    home.start_exporting_journey(context.driver)
    logging.debug("%s started triage process", actor_alias)


def triage_select_sector(context: Context, *, sector: str = None):
    driver = context.driver
    triage_what_is_your_sector.select_sector(driver, sector)
    triage_what_is_your_sector.submit(driver)
    triage_have_you_exported.should_be_here(driver)


def triage_say_you_exported_before(context: Context):
    driver = context.driver
    triage_have_you_exported.select_yes(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_regular_exporter.should_be_here(driver)


def triage_say_you_are_registered_with_companies_house(context: Context):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_yes(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_company_name.should_be_here(driver)


def triage_say_you_are_not_registered_with_companies_house(context: Context):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_no(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_result.should_be_here(driver)


def triage_say_you_never_exported_before(context: Context):
    driver = context.driver
    triage_have_you_exported.select_no(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)


def triage_say_you_export_regularly(context: Context):
    driver = context.driver
    triage_are_you_regular_exporter.select_yes(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)


def triage_say_you_do_not_export_regularly(context: Context):
    driver = context.driver
    triage_are_you_regular_exporter.select_no(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_do_you_use_online_marketplaces.should_be_here(driver)


def triage_say_you_use_online_marketplaces(context: Context):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_yes(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)


def triage_say_you_do_not_use_online_marketplaces(context: Context):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_no(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)


def triage_enter_company_name(context: Context):
    driver = context.driver
    triage_company_name.enter_company_name(driver)
    triage_company_name.submit(driver)
    triage_result.should_be_here(driver)


def triage_should_be_classified_as_new(context: Context):
    triage_result.should_be_classified_as_new(context.driver)


def triage_should_be_classified_as_occasional(context: Context):
    triage_result.should_be_classified_as_occasional(context.driver)


def triage_should_be_classified_as_regular(context: Context):
    triage_result.should_be_classified_as_regular(context.driver)


def triage_create_exporting_journey(context: Context):
    triage_result.create_exporting_journey(context.driver)


def triage_classify_as_new(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_never_exported_before(context)
    if random.choice([True, False]):
        triage_say_you_are_registered_with_companies_house(context)
        triage_enter_company_name(context)
    else:
        triage_say_you_are_not_registered_with_companies_house(context)
    triage_should_be_classified_as_new(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="new")


def triage_classify_as_occasional(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_exported_before(context)
    triage_say_you_do_not_export_regularly(context)
    if random.choice([True, False]):
        triage_say_you_use_online_marketplaces(context)
    else:
        triage_say_you_do_not_use_online_marketplaces(context)
    if random.choice([True, False]):
        triage_say_you_are_registered_with_companies_house(context)
        triage_enter_company_name(context)
    else:
        triage_say_you_are_not_registered_with_companies_house(context)
    triage_should_be_classified_as_occasional(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="occasional")


def triage_classify_as_regular(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_exported_before(context)
    triage_say_you_export_regularly(context)
    if random.choice([True, False]):
        triage_say_you_are_registered_with_companies_house(context)
        triage_enter_company_name(context)
    else:
        triage_say_you_are_not_registered_with_companies_house(context)
    triage_should_be_classified_as_regular(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="regular")


def triage_classify_as(
        context: Context, actor_alias: str, exporter_status: str):
    classifications = {
        "new": triage_classify_as_new,
        "occasional": triage_classify_as_occasional,
        "regular": triage_classify_as_regular
    }
    visit_page(context, actor_alias, "home")
    step = classifications[exporter_status.lower()]
    logging.debug(
        "%s decided to classify himself/herself as %s Exporter", actor_alias,
        exporter_status)
    step(context, actor_alias)


def personalised_journey_create_page(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    export_status = actor.self_classification
    triage_classify_as(context, actor_alias, export_status)
    personalised_journey.should_be_here(context.driver)
