# -*- coding: utf-8 -*-
"""Invest in Great - Thank you for your message Page Object."""
import logging
from urllib.parse import urljoin

from pages.common_actions import (
    Executor,
    check_title,
    check_url,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Thank you for your message"
SERVICE = "invest"
TYPE = "contact"
URL = urljoin(INVEST_UI_URL, "contact/success/")
PAGE_TITLE = ""
SELECTORS = {}


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=False)
    check_url(executor, URL, exact_match=False)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
