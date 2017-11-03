# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random

from behave.runner import Context
from retrying import retry

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
    triage_what_do_you_want_to_export
)
from registry.pages import get_page_object
from utils import add_actor, get_actor, unauthenticated_actor, update_actor


@retry(wait_fixed=31000, stop_max_attempt_number=3)
def visit_page(
        context: Context, actor_alias: str, page_name: str, *,
        first_time: bool = False):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    context.current_page = get_page_object(page_name)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page_name,
        context.current_page.URL)
    context.current_page.visit(context.driver, first_time=first_time)


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
    elif location == "personalised journey":
        personalised_journey.open(driver, group, element)


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


def triage_say_what_do_you_want_to_export(
        context: Context, actor_alias: str, *, sector: str = None):
    driver = context.driver
    final_sector = triage_what_do_you_want_to_export.enter(driver, sector)
    triage_what_do_you_want_to_export.submit(driver)
    triage_have_you_exported.should_be_here(driver)
    update_actor(context, actor_alias, what_do_you_want_to_export=final_sector)


def triage_say_you_exported_before(context: Context, actor_alias: str):
    driver = context.driver
    triage_have_you_exported.select_yes(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_regular_exporter.should_be_here(driver)
    update_actor(context, actor_alias, have_you_exported_before=True)


def triage_say_you_never_exported_before(context: Context, actor_alias: str):
    driver = context.driver
    triage_have_you_exported.select_no(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, have_you_exported_before=False)


def triage_have_you_exported_before(context, actor_alias, has_or_has_never):
    if has_or_has_never == "has":
        triage_say_you_exported_before(context, actor_alias)
    elif has_or_has_never == "has never":
        triage_say_you_never_exported_before(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'has' or 'has never'" %
            has_or_has_never)


def triage_say_you_are_incorporated(
        context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_yes(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_company_name.should_be_here(driver)
    update_actor(context, actor_alias, are_you_incorporated=True)


def triage_say_you_are_not_incorporated(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_no(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_result.should_be_here(driver)
    update_actor(context, actor_alias, are_you_incorporated=False)


def triage_are_you_incorporated(context, actor_alias, is_or_not):
    if is_or_not == "is":
        triage_say_you_are_incorporated(context, actor_alias)
    elif is_or_not == "is not":
        triage_say_you_are_not_incorporated(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'is' or 'is not'" % is_or_not)


def triage_say_you_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_yes(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=True)


def triage_say_you_do_not_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_no(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_do_you_use_online_marketplaces.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=False)


def triage_do_you_export_regularly(context, actor_alias, regular_or_not):
    if regular_or_not == "a regular":
        triage_say_you_export_regularly(context, actor_alias)
    elif regular_or_not == "not a regular":
        triage_say_you_do_not_export_regularly(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'a regular' or "
            "'not a regular'" % regular_or_not)


def triage_say_you_use_online_marketplaces(context: Context, actor_alias: str):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_yes(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=True)


def triage_say_you_do_not_use_online_marketplaces(
        context: Context, actor_alias: str):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_no(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=False)


def triage_enter_company_name(
        context: Context, actor_alias: str, use_suggestions: bool, *,
        company_name: str = None):
    driver = context.driver
    triage_company_name.enter_company_name(driver, company_name)
    if use_suggestions:
        triage_company_name.click_on_first_suggestion(driver)
    else:
        triage_company_name.hide_suggestions(driver)
    final_company_name = triage_company_name.get_company_name(driver)
    triage_company_name.submit(driver)
    triage_result.should_be_here(driver)
    update_actor(context, actor_alias, company_name=final_company_name)


def triage_do_not_enter_company_name(context: Context, actor_alias: str):
    driver = context.driver
    triage_company_name.submit(driver)
    triage_result.should_be_here(driver)
    update_actor(context, actor_alias, company_name=None)


def triage_what_is_your_company_name(context, actor_alias, decision):
    if decision == "types in":
        triage_enter_company_name(context, actor_alias, use_suggestions=False)
    elif decision == "does not provide":
        triage_do_not_enter_company_name(context, actor_alias)
    elif decision == "types in and selects":
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'types in', "
            "'does not provide' or 'types in and selects'" % decision)


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
    triage_what_do_you_want_to_export(context, actor_alias)
    triage_say_you_never_exported_before(context, actor_alias)
    if random.choice([True, False]):
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_new(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="new")


def triage_classify_as_occasional(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_what_do_you_want_to_export(context, actor_alias)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_do_not_export_regularly(context, actor_alias)
    if random.choice([True, False]):
        triage_say_you_use_online_marketplaces(context, actor_alias)
    else:
        triage_say_you_do_not_use_online_marketplaces(context, actor_alias)
    if random.choice([True, False]):
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_occasional(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="occasional")


def triage_classify_as_regular(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_what_do_you_want_to_export(context, actor_alias)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_export_regularly(context, actor_alias)
    if random.choice([True, False]):
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_regular(context)
    triage_create_exporting_journey(context)
    update_actor(context, alias=actor_alias, triage_classification="regular")


def triage_classify_as(
        context: Context, actor_alias: str, *, exporter_status: str = None):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    classifications = {
        "new": triage_classify_as_new,
        "occasional": triage_classify_as_occasional,
        "regular": triage_classify_as_regular
    }
    exporter_status = exporter_status or random.choice(list(classifications))
    visit_page(context, actor_alias, "home")
    step = classifications[exporter_status.lower()]
    logging.debug(
        "%s decided to classify himself/herself as %s Exporter", actor_alias,
        exporter_status)
    step(context, actor_alias)


def triage_should_see_answers_to_questions(context, actor_alias):
    actor = get_actor(context, actor_alias)
    q_and_a = triage_result.get_questions_and_answers(context.driver)
    if actor.what_do_you_want_to_export is not None:
        what = actor.what_do_you_want_to_export
        assert q_and_a["What do you want to export?"] == what
    if actor.company_name is not None:
        name = actor.company_name
        assert q_and_a["Company name"] == name
    if actor.have_you_exported_before is not None:
        exported_before = "Yes" if actor.have_you_exported_before else "No"
        assert q_and_a["Have you exported before?"] == exported_before
    if actor.do_you_export_regularly is not None:
        export_regularly = "Yes" if actor.do_you_export_regularly else "No"
        assert q_and_a["Is exporting a regular part of your business activities?"] == export_regularly
    # if actor.are_you_incorporated is not None:
    #     incorporated = "Yes" if actor.are_you_incorporated else "No"
    #     assert q_and_a["Is your company incorporated in the UK?"] == incorporated
    if actor.do_you_use_online_marketplaces is not None:
        sell_online = "Yes" if actor.do_you_use_online_marketplaces else "No"
        assert q_and_a["Do you use online marketplaces to sell your products?"] == sell_online


def personalised_journey_create_page(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    exporter_status = actor.self_classification
    triage_classify_as(context, actor_alias, exporter_status=exporter_status)
    personalised_journey.should_be_here(context.driver)
