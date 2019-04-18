# -*- coding: utf-8 -*-
"""International - Contact us form"""
from types import ModuleType
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
)
from pages.exred import contact_us_triage_domestic
from settings import EXRED_UI_URL

NAME = "Contact us"
SERVICE = "International"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/international/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "first name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "company": Selector(By.ID, "id_organisation_type_0", type=ElementType.CHECKBOX),
        "other type of organisation": Selector(
            By.ID, "id_organisation_type_1", type=ElementType.CHECKBOX
        ),
        "your organisation name": Selector(
            By.ID, "id_organisation_name", type=ElementType.INPUT
        ),
        "country": Selector(By.ID, "id_country_name", type=ElementType.SELECT),
        "city": Selector(By.ID, "id_city", type=ElementType.INPUT),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX
        ),
        "submit": SUBMIT_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_triage_domestic
