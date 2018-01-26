# -*- coding: utf-8 -*-
"""Share on LinkedIn Page Object."""
from urllib import parse as urlparse
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_for_expected_elements, check_title
from utils import assertion_msg, take_screenshot

NAME = "Share on LinkedIn page"
URL = urljoin("https://www.linkedin.com/", "shareArticle")
PAGE_TITLE = "Sign Up | LinkedIn"

EXPECTED_ELEMENTS = {
    "logo": "#uno-reg-join > div > div > div > div.header-container > header",
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def extract_shared_url(url: str) -> str:
    parsed_initial_url = urlparse.urlparse(url)
    initial_url_query_parameters = urlparse.parse_qs(parsed_initial_url.query)
    session_redirect = initial_url_query_parameters['session_redirect'][0]
    parsed_next_url = urlparse.urlparse(session_redirect)
    next_url_query_parameters = urlparse.parse_qs(parsed_next_url.query)
    shared_url = next_url_query_parameters['url'][0]
    return shared_url


def check_if_populated(driver: webdriver, shared_url: str):
    found_shared_url = extract_shared_url(driver.current_url)
    with assertion_msg(
            "Expected to find link to Article '%s' in the LinkedIn share page "
            "URL, but got '%s' instead", shared_url, found_shared_url):
        assert shared_url == found_shared_url
