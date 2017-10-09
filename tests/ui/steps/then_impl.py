# -*- coding: utf-8 -*-
"""Given steps implementation."""

import logging

from behave.runner import Context


def should_see_directory_header(context: Context, actor_alias: str):
    assert 'New to exporting' in context.driver.page_source
    logging.debug(
        "%s was presented with standard Directory page header", actor_alias)
