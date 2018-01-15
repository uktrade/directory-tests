# -*- coding: utf-8 -*-
"""Share on Facebook Page Object."""
import logging
from urllib import parse as urlparse
from urllib.parse import urljoin

from selenium import webdriver

from utils import assertion_msg, find_element, take_screenshot

NAME = "Share on Facebook page"
URL = urljoin("https://www.facebook.com/", "share.php?u=")
PAGE_TITLE = "Facebook"

EXPECTED_ELEMENTS = {
    "header": "#homelink",
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    with assertion_msg(
            "Expected page title to be: '%s' but got '%s'", PAGE_TITLE,
            driver.title):
        assert driver.title.lower() == PAGE_TITLE.lower()
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


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
