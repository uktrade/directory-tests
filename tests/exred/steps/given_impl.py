# -*- coding: utf-8 -*-
"""Given step definitions."""
import logging

from behave.runner import Context

from tests.exred.registry import get_page_object


def visit_page(
        context: Context, actor_name: str, page_name: str, *,
        first_time: bool = False):
    logging.debug("%s will visit '%s' page", actor_name, page_name)
    context.current_page = get_page_object(page_name)
    context.current_page.visit(context.driver, first_time=first_time)
