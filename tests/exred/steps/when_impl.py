# -*- coding: utf-8 -*-
"""When step implementations."""
import logging

from behave.runner import Context

from pages import exred_home


def start_triage(context: Context, actor_alias: str):
    exred_home.start_exporting_journey(context.driver)
    logging.debug("%s started triage process", actor_alias)
