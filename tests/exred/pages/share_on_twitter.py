# -*- coding: utf-8 -*-
"""Share on Twitter Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import check_for_expected_elements, check_title
from utils import assertion_msg, find_element, take_screenshot

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
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


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
