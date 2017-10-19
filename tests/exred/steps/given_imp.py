# -*- coding: utf-8 -*-
"""Given step definitions."""
import logging
import random

from behave.runner import Context

from registry import get_page_object
from steps.when_impl import (
    start_triage,
    triage_create_exporting_journey,
    triage_enter_company_name,
    triage_say_you_do_not_export_regularly,
    triage_say_you_export_regularly,
    triage_say_you_exported_before,
    triage_say_you_never_exported_before,
    triage_select_sector,
    triage_should_be_classified_as_new,
    triage_should_be_classified_as_occasional,
    triage_should_be_classified_as_regular
)


def visit_page(
        context: Context, actor_name: str, page_name: str, *,
        first_time: bool = False):
    logging.debug("%s will visit '%s' page", actor_name, page_name)
    context.current_page = get_page_object(page_name)
    context.current_page.visit(context.driver, first_time=first_time)


def classify_as_new(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_never_exported_before(context)
    triage_enter_company_name(context)
    triage_should_be_classified_as_new(context)
    triage_create_exporting_journey(context)


def classify_as_occasional(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_exported_before(context)
    triage_say_you_do_not_export_regularly(context)
    triage_enter_company_name(context)
    triage_should_be_classified_as_occasional(context)
    triage_create_exporting_journey(context)


def classify_as_regular(context: Context, actor_alias: str):
    start_triage(context, actor_alias)
    triage_select_sector(context)
    triage_say_you_exported_before(context)
    triage_say_you_export_regularly(context)
    triage_enter_company_name(context)
    triage_should_be_classified_as_regular(context)
    triage_create_exporting_journey(context)


def classify_as(context: Context, actor_alias: str, exporter_status: str):
    classifications = {
        "new": classify_as_new,
        "occasional": classify_as_occasional,
        "regular": classify_as_regular
    }
    visit_page(context, actor_alias, "home")
    step = classifications[exporter_status.lower()]
    logging.debug(
        "%s decided to classify himself/herself as %s Exporter", actor_alias,
        exporter_status)
    step(context, actor_alias)


def finish_triage(context: Context, actor_alias: str):
    """Will finish triage with randomly selected exporting status."""
    exporter_status = random.choice(["new", "occasional", "regular"])
    classify_as(context, actor_alias, exporter_status)
