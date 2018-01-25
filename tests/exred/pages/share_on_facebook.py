# -*- coding: utf-8 -*-
"""Share on Facebook Page Object."""
import logging
from urllib import parse as urlparse
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_for_expected_elements, check_title
from utils import assertion_msg, take_screenshot

NAME = "Share on Facebook page"
URL = urljoin("https://www.facebook.com/", "share.php?u=")
PAGE_TITLE = "Facebook"

EXPECTED_ELEMENTS = {
    "header": "#homelink",
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def extract_shared_url(url: str) -> str:
    parsed_initial_url = urlparse.urlparse(url)
    initial_url_query_parameters = urlparse.parse_qs(parsed_initial_url.query)
    next_parameter = initial_url_query_parameters['next'][0]
    parsed_next_url = urlparse.urlparse(next_parameter)
    next_url_query_parameters = urlparse.parse_qs(parsed_next_url.query)
    shared_url = next_url_query_parameters['u'][0]
    return shared_url


def check_if_populated(driver: webdriver, shared_url: str):
    found_shared_url = extract_shared_url(driver.current_url)
    with assertion_msg(
            "Expected to find link to Article '%s' in the Facebook share page "
            "URL, but got '%s' instead", shared_url, found_shared_url):
        assert shared_url == found_shared_url


def close_all_windows_except_first(driver: webdriver):
    """This action works only locally, and doesn't work on BrowserStack :("""
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        logging.debug(
            "Closing window: %s opened with URL %s", driver.window_handles[1],
            driver.current_url)
        driver.close()
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    driver.switch_to.window(driver.window_handles[0])
