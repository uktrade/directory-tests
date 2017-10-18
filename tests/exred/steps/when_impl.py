# -*- coding: utf-8 -*-
"""When step implementations."""
import logging

from behave.runner import Context

from pages import (
    home,
    triage_1st_question,
    triage_2nd_question,
    triage_3rd_question,
    triage_4th_question,
    triage_result
)


def start_triage(context: Context, actor_alias: str):
    home.start_exporting_journey(context.driver)
    logging.debug("%s started triage process", actor_alias)


def triage_select_sector(context: Context, *, sector: str = None):
    driver = context.driver
    triage_1st_question.select_sector(driver, sector)
    triage_1st_question.submit(driver)
    triage_2nd_question.should_be_here(driver)


def triage_say_you_exported_before(context: Context):
    driver = context.driver
    triage_2nd_question.select_yes(driver)
    triage_2nd_question.submit(driver)
    triage_3rd_question.should_be_here(driver)


def triage_say_you_never_exported_before(context: Context):
    driver = context.driver
    triage_2nd_question.select_no(driver)
    triage_2nd_question.submit(driver)
    triage_4th_question.should_be_here(driver)


def triage_say_you_export_regularly(context: Context):
    driver = context.driver
    triage_3rd_question.select_yes(driver)
    triage_3rd_question.submit(driver)
    triage_4th_question.should_be_here(driver)


def triage_say_you_do_not_export_regularly(context: Context):
    driver = context.driver
    triage_3rd_question.select_no(driver)
    triage_3rd_question.submit(driver)
    triage_4th_question.should_be_here(driver)


def triage_enter_company_name(context: Context):
    driver = context.driver
    triage_4th_question.enter_company_name(driver)
    triage_4th_question.submit(driver)
    triage_result.should_be_here(driver)


def triage_should_be_classified_as_new(context: Context):
    triage_result.should_be_classified_as_new(context.driver)


def triage_should_be_classified_as_occasional(context: Context):
    triage_result.should_be_classified_as_occasional(context.driver)


def triage_should_be_classified_as_regular(context: Context):
    triage_result.should_be_classified_as_regular(context.driver)


def triage_create_exporting_journey(context: Context):
    triage_result.create_exporting_journey(context.driver)
