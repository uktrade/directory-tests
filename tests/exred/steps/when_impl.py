# -*- coding: utf-8 -*-
"""When step implementations."""
import logging

from behave.runner import Context

from pages import (
    home,
    triage_are_you_regular_exporter,
    triage_company_name_or_sole_trader,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_result,
    triage_what_is_your_sector
)


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


def triage_say_you_never_exported_before(context: Context):
    driver = context.driver
    triage_have_you_exported.select_no(driver)
    triage_have_you_exported.submit(driver)
    triage_company_name_or_sole_trader.should_be_here(driver)


def triage_say_you_export_regularly(context: Context):
    driver = context.driver
    triage_are_you_regular_exporter.select_yes(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_company_name_or_sole_trader.should_be_here(driver)


def triage_say_you_do_not_export_regularly(context: Context):
    driver = context.driver
    triage_are_you_regular_exporter.select_no(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_do_you_use_online_marketplaces.should_be_here(driver)


def triage_enter_company_name(context: Context):
    driver = context.driver
    triage_company_name_or_sole_trader.enter_company_name(driver)
    triage_company_name_or_sole_trader.submit(driver)
    triage_result.should_be_here(driver)


def triage_should_be_classified_as_new(context: Context):
    triage_result.should_be_classified_as_new(context.driver)


def triage_should_be_classified_as_occasional(context: Context):
    triage_result.should_be_classified_as_occasional(context.driver)


def triage_should_be_classified_as_regular(context: Context):
    triage_result.should_be_classified_as_regular(context.driver)


def triage_create_exporting_journey(context: Context):
    triage_result.create_exporting_journey(context.driver)
