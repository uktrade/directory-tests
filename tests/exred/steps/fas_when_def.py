# -*- coding: utf-8 -*-
# flake8: noqa
"""When step definitions."""
from behave import when
from behave.runner import Context

from steps.fas_when_impl import (
    fas_landing_page_search_for_companies
)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword in "{sector}" sector on "{page_alias}" page')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str, sector: str,
        page_alias: str):
    fas_landing_page_search_for_companies(
        context, actor_alias, keyword, sector, page_alias)
