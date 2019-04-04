# -*- coding: utf-8 -*-
"""Export Readiness - Feedback Contact us form"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import Selector, check_url, go_to_url, take_screenshot
from settings import EXRED_UI_URL

NAME = "Feedback"
SERVICE = "Export Readiness"
TYPE = "Contact us"
URL = urljoin(EXRED_UI_URL, "contact/feedback/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "feedback": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX
        ),
        "submit": SUBMIT_BUTTON,
    }
}
OTHER_SELECTORS = {
    "other": Selector(By.ID, "id_company_type_other", type=ElementType.SELECT)
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
