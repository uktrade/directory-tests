# -*- coding: utf-8 -*-
"""Share on Facebook Page Object."""
from urllib import parse as urlparse
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    take_screenshot,
)

NAME = "Share on Facebook"
SERVICE = "facebook"
TYPE = "share"
URL = urljoin("https://www.facebook.com/", "share.php?u=")
PAGE_TITLE = "Facebook"

SELECTORS = {"header": "#homelink"}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_elements(driver, SELECTORS)


def extract_shared_url(url: str) -> str:
    parsed_initial_url = urlparse.urlparse(url)
    initial_url_query_parameters = urlparse.parse_qs(parsed_initial_url.query)
    next_parameter = initial_url_query_parameters["next"][0]
    parsed_next_url = urlparse.urlparse(next_parameter)
    next_url_query_parameters = urlparse.parse_qs(parsed_next_url.query)
    shared_url = next_url_query_parameters["u"][0]
    return shared_url


def check_if_populated(driver: webdriver, shared_url: str):
    found_shared_url = extract_shared_url(driver.current_url)
    with assertion_msg(
        "Expected to find link to Article '%s' in the Facebook share page "
        "URL, but got '%s' instead",
        shared_url,
        found_shared_url,
    ):
        assert shared_url == found_shared_url
