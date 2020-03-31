# -*- coding: utf-8 -*-
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, check_if_element_is_not_visible, find_element

ALLOWED = {
    "google tag manager": Selector(
        By.CSS_SELECTOR, "script[src=^'https://www.googletagmanager.com/gtm.js?id=']"
    ),
    "google tag manager - no script": Selector(
        By.XPATH, "//noscript[contains(text(),'googletagmanager.com')]"
    ),
    "utm cookie domain": Selector(By.ID, "utmCookieDomain"),
}


NOT_ALLOWED = {
    "facebook tracking pixel": Selector(
        By.XPATH, "//script[contains(text(),'connect.facebook.net')]"
    ),
    "linkedin tracking pixel": Selector(
        By.XPATH, "//script[contains(text(),'linkedin.com')]"
    ),
}


def should_be_present(driver: WebDriver, name: str):
    find_element(driver, ALLOWED[name.lower()], element_name=name, wait_for_it=False)
    logging.debug("As expected '{}' is present".format(name))


def should_not_be_present(driver: WebDriver, name: str):
    check_if_element_is_not_visible(
        driver, NOT_ALLOWED[name.lower()], element_name=name, take_screenshot=False
    )
