# -*- coding: utf-8 -*-
"""Export Readiness - First page of Long Contact us form"""
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
from pages.exread import contact_us_triage_domestic
from settings import EXRED_UI_URL

NAME = "Short contact form (Tell us how we can help)"
NAMES = [
    "Short contact form (Tell us how we can help)",
    "Short contact form (Events)",
    "Short contact form (Defence and Security Organisation (DSO))",
    "Short contact form (Buying from the UK)",
    "Short contact form (Other)",
]
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/domestic/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "first name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "uk private or public limited company": Selector(By.ID, "id_company_type_0", type=ElementType.CHECKBOX),
        "other type of uk organisation": Selector(By.ID, "id_company_type_1", type=ElementType.CHECKBOX),
        "organisation name": Selector(By.ID, "id_organisation_name", type=ElementType.INPUT),
        "postcode": Selector(By.ID, "id_postcode", type=ElementType.INPUT),
        "terms and conditions": Selector(By.ID, "id_terms_agreed", type=ElementType.CHECKBOX),
        "submit": SUBMIT_BUTTON,
    }
}

URLs = {
    "short contact form (tell us how we can help)":
        URL,
    "short contact form (events)":
        urljoin(URL, "/contact/events/"),
    "short contact form (defence and security organisation (dso))":
        urljoin(URL, "/contact/defence-and-security-organisation/"),
    "short contact form (other)":
        URL,
    "short contact form (buying from the uk)":
        urljoin(URL, "/contact/find-uk-companies/"),
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_triage_domestic
