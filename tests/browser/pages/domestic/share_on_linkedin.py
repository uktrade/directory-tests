# -*- coding: utf-8 -*-
"""Share on LinkedIn Page Object."""
import logging
from urllib import parse as urlparse
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_title,
    find_element,
    take_screenshot,
)

NAME = "Share on LinkedIn"
SERVICE = "linkedin"
TYPE = "share"
URL = urljoin("https://www.linkedin.com/", "shareArticle")
PAGE_TITLE = "LinkedIn"

LINKEDIN = Selector(By.ID, "share-linkedin")

SELECTORS = {}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_title(driver, PAGE_TITLE, exact_match=False)


def extract_shared_url(driver: WebDriver) -> str:
    link = find_element(driver, LINKEDIN, element_name="Share on LinkedIn link")
    url = link.get_attribute("href")
    parsed_url = urlparse.urlparse(url)
    query_parameters = urlparse.parse_qs(parsed_url.query)
    shared_url = query_parameters["url"][0]
    return shared_url


def check_if_populated(driver: WebDriver, shared_url: str):
    found_shared_url = extract_shared_url(driver)
    with assertion_msg(
        "Expected to find link to Article '%s' in the LinkedIn share page "
        "URL, but got '%s' instead",
        shared_url,
        found_shared_url,
    ):
        assert shared_url == found_shared_url
        logging.debug(f"Link to share page on LinkedIn contains expected {shared_url}")
