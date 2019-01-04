# -*- coding: utf-8 -*-
"""Export Readiness - Sort Domestic Contact us form"""
import logging
import random
from types import ModuleType
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_radio,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    find_element,
    go_to_url,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes,
    pick_option
)
from pages.exread import contact_us_short_domestic_thank_you
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

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "form button[type=submit]", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "first name": Selector(By.ID, "id_given_name", type=ElementType.INPUT),
        "last name": Selector(By.ID, "id_family_name", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "uk private or public limited company": Selector(
            By.ID, "id_company_type_0", type=ElementType.RADIO
        ),
        "other type of uk organisation": Selector(
            By.ID, "id_company_type_1", type=ElementType.RADIO
        ),
        "organisation name": Selector(
            By.ID, "id_organisation_name", type=ElementType.INPUT
        ),
        "postcode": Selector(By.ID, "id_postcode", type=ElementType.INPUT),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.CHECKBOX
        ),
        "submit": SUBMIT_BUTTON,
    }
}
OTHER_SELECTORS = {
    "other": Selector(By.ID, "id_company_type_other", type=ElementType.SELECT),
}

URLs = {
    "short contact form (tell us how we can help)": URL,
    "short contact form (events)": urljoin(URL, "/contact/events/"),
    "short contact form (defence and security organisation (dso))": urljoin(
        URL, "/contact/defence-and-security-organisation/"
    ),
    "short contact form (other)": URL,
    "short contact form (buying from the uk)": urljoin(
        URL, "/contact/find-uk-companies/"
    ),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)


def generate_form_details(actor: Actor) -> dict:
    is_company = random.choice([True, False])
    result = {
        "comment": f"Submitted by automated test {actor.alias}",
        "first name": f"send by {actor.alias} - automated tests",
        "last name": actor.alias,
        "email": actor.email,
        "uk private or public limited company": is_company,
        "other type of uk organisation": not is_company,
        "organisation name": "automated tests",
        "postcode": "SW1H 0TL",
        "terms and conditions": True,
    }
    if is_company:
        # In order to avoid situation when previous scenario example modified
        # SELECTORS we have to remove OTHER_SELECTORS that were then added
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(OTHER_SELECTORS.items())
        )
    else:
        SELECTORS["form"].update(OTHER_SELECTORS)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_textarea_fields(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    check_radio(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_captcha_checkbox(driver)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_short_domestic_thank_you
