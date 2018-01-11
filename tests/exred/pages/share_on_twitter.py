# -*- coding: utf-8 -*-
"""Share on Twitter Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from utils import (
    assertion_msg,
    find_element,
    take_screenshot
)

NAME = "Share on Twitter page"
URL = urljoin("https://twitter.com/", "intent/tweet?text=")
PAGE_TITLE = "Post a Tweet on Twitter"

MESSAGE_BOX = "#status"
EXPECTED_ELEMENTS = {
    "logo": "#header > div > h1 > a",
    "message_box": MESSAGE_BOX
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


def check_if_populated(driver: webdriver, shared_url: str):
    status_update_message = find_element(driver, by_css=MESSAGE_BOX)
    with assertion_msg(
            "Expected to see article URL '%s' in LinkedIn's status update "
            "textbox, but couldn't find it in : %s", shared_url,
            status_update_message.text):
        assert shared_url in status_update_message.text


def close_all_windows_except_first(driver: webdriver):
    """This action works only locally, and doesn't work on BrowserStack :("""
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        logging.debug(
            "Closing window: %s opened with URL %s", driver.window_handles[1],
            driver.current_url)
        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
