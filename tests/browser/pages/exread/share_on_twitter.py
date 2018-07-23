# -*- coding: utf-8 -*-
"""Share on Twitter Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    check_title,
    find_element,
    take_screenshot,
)

NAME = "Share on Twitter"
SERVICE = "twitter"
TYPE = "share"
URL = urljoin("https://twitter.com/", "intent/tweet?text=")
PAGE_TITLE = "Post a Tweet on Twitter"

MESSAGE_BOX = Selector(By.ID, "status")
SELECTORS = {
    "general": {
        "logo": Selector(By.CSS_SELECTOR, "#header > div > h1 > a"),
        "message_box": MESSAGE_BOX,
    }
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)


def check_if_populated(driver: WebDriver, shared_url: str):
    status_update_message = find_element(driver, MESSAGE_BOX)
    with assertion_msg(
        "Expected to see article URL '%s' in LinkedIn's status update "
        "textbox, but couldn't find it in : %s",
        shared_url,
        status_update_message.text,
    ):
        assert shared_url in status_update_message.text
