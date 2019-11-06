# -*- coding: utf-8 -*-
"""SSO Sign In Page Object."""
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_element,
    go_to_url,
    submit_form,
    take_screenshot,
)

NAME = "Sign in"
SERVICE = Service.SSO
TYPE = PageType.FORM
URL = URLs.SSO_LOGIN.absolute
PAGE_TITLE = "Sign in - great.gov.uk"

EMAIL_INPUT = Selector(By.ID, "id_login")
PASSWORD_INPUT = Selector(By.ID, "id_password")
REGISTER_BUTTON = Selector(
    By.CSS_SELECTOR,
    "#login-form-container > div:nth-child(2) > section > a",
    type=ElementType.LINK,
)
RESET_YOUR_PASSWORD_LINK = Selector(By.CSS_SELECTOR, "form > a")
SELECTORS = {
    "form": {
        "title": Selector(By.CSS_SELECTOR, "#content h1.heading-xlarge"),
        "email input": EMAIL_INPUT,
        "password input": PASSWORD_INPUT,
        "sign in": (
            Selector(By.CSS_SELECTOR, "form button.button", type=ElementType.SUBMIT)
        ),
        "forgotten password?": RESET_YOUR_PASSWORD_LINK,
    },
    "create a great.gov.uk account": {"create account": REGISTER_BUTTON},
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def fill_out(driver: WebDriver, email: str, password: str):
    email_input = find_element(driver, EMAIL_INPUT)
    password_input = find_element(driver, PASSWORD_INPUT)
    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
