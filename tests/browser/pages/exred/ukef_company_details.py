# -*- coding: utf-8 -*-
"""ExRed UKEF Contact Us - Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    pick_option,
    take_screenshot,
    tick_checkboxes,
)
from settings import EXRED_UI_URL

NAME = "Company details"
SERVICE = "Export Readiness"
TYPE = "UKEF Contact us"
URL = urljoin(EXRED_UI_URL, "get-finance/company-details/")
PAGE_TITLE = "Welcome to great.gov.uk"

BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "div.breadcrumbs a")
SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "#content form button", type=ElementType.BUTTON
)
SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "div.breadcrumbs li[aria-current='page']"
        ),
        "links": BREADCRUMB_LINKS,
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "heading": Selector(By.CSS_SELECTOR, "#heading-container h2"),
        "trading name": Selector(
            By.ID, "id_company-details-trading_name", type=ElementType.INPUT
        ),
        "companies house number": Selector(
            By.ID, "id_company-details-company_number", type=ElementType.INPUT
        ),
        "not registered with companies house": Selector(
            By.ID,
            "id_company-details-not_companies_house",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "building and street first line": Selector(
            By.ID,
            "id_company-details-address_line_one",
            type=ElementType.INPUT,
        ),
        "building and street second line": Selector(
            By.ID,
            "id_company-details-address_line_two",
            type=ElementType.INPUT,
        ),
        "town or city": Selector(
            By.ID,
            "id_company-details-address_town_city",
            type=ElementType.INPUT,
        ),
        "county": Selector(
            By.ID, "id_company-details-address_county", type=ElementType.INPUT
        ),
        "postcode": Selector(
            By.ID,
            "id_company-details-address_post_code",
            type=ElementType.INPUT,
        ),
        "industry": Selector(
            By.ID, "id_company-details-industry", type=ElementType.SELECT
        ),
        "i have customers outside the uk": Selector(
            By.ID,
            "checkbox-multiple-i-have-customers-outside-the-uk",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "i supply uk companies that sell overseas": Selector(
            By.ID,
            "checkbox-multiple-i-supply-uk-companies-that-sell-overseas",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "i don't currently export or supply businesses that export": Selector(
            By.ID,
            "checkbox-multiple-i-dont-currently-export-or-supply-businesses-that-export",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "continue": SUBMIT_BUTTON,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "trading name": "automated tests",
        "companies house number": None,
        "not registered with companies house": True,
        "building and street first line": "automated tests",
        "building and street second line": "automated tests",
        "town or city": "automated tests",
        "county": "automated tests",
        "postcode": "automated tests",
        "industry": None,
        "i have customers outside the uk": True,
        "i supply uk companies that sell overseas": True,
        "i don't currently export or supply businesses that export": True,
    }
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
