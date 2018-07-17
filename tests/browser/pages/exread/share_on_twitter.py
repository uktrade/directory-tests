# -*- coding: utf-8 -*-
"""Share on Twitter Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    assertion_msg,
    check_for_expected_elements,
    check_title,
    find_element,
    take_screenshot,
)

NAME = "Share on Twitter page"
URL = urljoin("https://twitter.com/", "intent/tweet?text=")
PAGE_TITLE = "Post a Tweet on Twitter"

MESSAGE_BOX = "#status"
EXPECTED_ELEMENTS = {"logo": "#header > div > h1 > a", "message_box": MESSAGE_BOX}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


def check_if_populated(driver: webdriver, shared_url: str):
    status_update_message = find_element(driver, by_css=MESSAGE_BOX)
    with assertion_msg(
        "Expected to see article URL '%s' in LinkedIn's status update "
        "textbox, but couldn't find it in : %s",
        shared_url,
        status_update_message.text,
    ):
        assert shared_url in status_update_message.text
