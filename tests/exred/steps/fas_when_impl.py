# -*- coding: utf-8 -*-
"""Then step implementations."""
import logging

from behave.runner import Context

from registry.pages import get_page_object


def fas_landing_page_search_for_companies(
        context: Context, actor_alias: str, keyword: str, sector: str,
        page_alias: str):
    page = get_page_object(page_alias)
    assert hasattr(page, "search")
    optional_param_keywords = ["n/a", "no", "empty", "without", "any"]
    if keyword.lower() in optional_param_keywords:
        keyword = None
    if sector.lower() in optional_param_keywords:
        sector = None
    page.search(context.driver, keyword=keyword, sector=sector)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page_alias,
        page.URL)
