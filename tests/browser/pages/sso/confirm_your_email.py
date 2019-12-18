# -*- coding: utf-8 -*-
"""SSO Confirm Your Email Address Page Object."""
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import Selector, check_url, submit_form

NAME = "Confirm your email address"
SERVICE = Service.SSO
TYPE = PageType.CONFIRMATION
URL = URLs.SSO_EMAIL_CONFIRM.absolute
PAGE_TITLE = "Confirm email Address"

SELECTORS = {
    "form": {
        "title": Selector(By.CSS_SELECTOR, "#content h1"),
        "confirm link": Selector(
            By.CSS_SELECTOR,
            "#content form > button[type=submit]",
            type=ElementType.SUBMIT,
        ),
    }
}


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
