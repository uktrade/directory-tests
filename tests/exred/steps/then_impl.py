# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context


def should_see_sections(context: Context, actor_name: str, sections: str):
    section_names = sections.lower().split(", ")
    page = context.current_page
    page.should_see_sections(context.driver, section_names)
    logging.debug(
        "%s saw all expected sections on '%s' page", actor_name,
        context.current_page.NAME)
