# -*- coding: utf-8 -*-
"""Contact Us - Feedback Page Object."""
import logging
from urllib.parse import urljoin

from pages.common_actions import (
    Executor,
    check_url,
    take_screenshot,
    visit_url,
)
from settings import DIRECTORY_CONTACT_US_UI_URL

NAME = "Feedback"
SERVICE = "invest"
TYPE = "contact"
URL = urljoin(DIRECTORY_CONTACT_US_UI_URL, "triage/location/")
PAGE_TITLE = "Contact us - great.gov.uk"
SELECTORS = {}


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    take_screenshot(executor, PAGE_TITLE)
    check_url(executor, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
