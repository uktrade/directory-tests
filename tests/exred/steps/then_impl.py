# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context

from tests.exred.registry import get_page_object


def should_see_sections(context: Context, actor_name: str, sections: str):
    section_names = sections.lower().split(", ")
    page = context.current_page
    page.should_see_sections(context.driver, section_names)
    logging.debug(
        "%s saw all expected sections on '%s' page", actor_name,
        context.current_page.NAME)


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    page.should_be_here(context.driver)
    logging.debug("%s is on %s page", actor_alias, page_name)
