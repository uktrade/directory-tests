# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import visit as common_visit
from settings import DIRECTORY_UI_PROFILE_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Confirm your Email address page"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "about/")
PAGE_TITLE = "Exporting is Great Profile - GREAT.gov.uk"

EXPECTED_ELEMENTS = {
    "title": "#content > div:nth-child(1) > div > div.span8.sso-profile-toolbar-labels-container > h1",
    "welcome message": "#welcome-message > h2",
}


def visit(driver: webdriver, *, first_time: bool = False):
    common_visit(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)
