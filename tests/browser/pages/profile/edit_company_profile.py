# -*- coding: utf-8 -*-
"""Profile - Edit Company Profile"""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import check_url, go_to_url, take_screenshot
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Edit Company Profile"
SERVICE = "Profile"
TYPE = "profile"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "find-a-buyer/")
PAGE_TITLE = "Business profile - great.gov.uk"

SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
