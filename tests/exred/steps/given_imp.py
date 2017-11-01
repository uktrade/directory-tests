# -*- coding: utf-8 -*-
"""Given step definitions."""
import logging
import random

from behave.runner import Context

from pages import footer, header, home
from registry import get_page_object
from steps.when_impl import (
    start_triage,
    triage_create_exporting_journey,
    triage_enter_company_name,
    triage_say_you_are_not_registered_with_companies_house,
    triage_say_you_are_registered_with_companies_house,
    triage_say_you_do_not_export_regularly,
    triage_say_you_do_not_use_online_marketplaces,
    triage_say_you_export_regularly,
    triage_say_you_exported_before,
    triage_say_you_never_exported_before,
    triage_say_you_use_online_marketplaces,
    triage_select_sector,
    triage_should_be_classified_as_new,
    triage_should_be_classified_as_occasional,
    triage_should_be_classified_as_regular
)
from utils import add_actor, unauthenticated_actor


def visit_page(
        context: Context, actor_name: str, page_name: str, *,
        first_time: bool = False):
    context.current_page = get_page_object(page_name)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_name, page_name,
        context.current_page.URL)
    context.current_page.visit(context.driver, first_time=first_time)


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
