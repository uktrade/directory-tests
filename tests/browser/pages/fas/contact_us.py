# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging

from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_for_section,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    tick_captcha_checkbox,
    fill_out_input_fields,
    fill_out_textarea_fields,
    pick_option,
    tick_checkboxes_by_labels,
)
from settings import DIRECTORY_UI_SUPPLIER_URL

NAME = "Contact Us"
SERVICE = "Find a Supplier"
TYPE = "contact"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/contact/sent/")
PAGE_TITLE = "Contact us - trade.great.gov.uk"

FULL_NAME = Selector(By.ID, "id_full_name", type=ElementType.INPUT)
EMAIL = Selector(By.ID, "id_email_address", type=ElementType.INPUT)
INDUSTRY = Selector(By.ID, "id_sector", type=ElementType.SELECT)
ORGANISATION = Selector(By.ID, "id_organisation_name", type=ElementType.INPUT)
ORGANISATION_SIZE = Selector(By.ID, "id_organisation_size", type=ElementType.SELECT)
COUNTRY = Selector(By.ID, "id_country", type=ElementType.INPUT)
BODY = Selector(By.ID, "id_body", type=ElementType.INPUT)
SOURCE = Selector(By.ID, "id_source", type=ElementType.SELECT)
ACCEPT_TC = Selector(By.ID, "id_terms_agreed", type=ElementType.LABEL, is_visible=False)
IM_NOT_A_ROBOT = Selector(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form input[type=submit]", type=ElementType.BUTTON)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "full name": FULL_NAME,
        "email": EMAIL,
        "industry": INDUSTRY,
        "organisation": ORGANISATION,
        "organisation size": ORGANISATION_SIZE,
        "country": COUNTRY,
        "body": BODY,
        "source": SOURCE,
        "accept t&c": ACCEPT_TC,
        "submit": SUBMIT_BUTTON,
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, SELECTORS, sought_section=name)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    company_name = actor.company_name or "Automated test"
    result = {
        "full name": actor.alias,
        "email": actor.email,
        "industry": None,
        "organisation": company_name,
        "organisation size": None,
        "country": "DIT QA TEAM",
        "body": "This is a test message sent via automated tests",
        "source": None,
        "accept t&c": True,
    }
    if custom_details:
        if custom_details.get("industry", None):
            custom_details["industry"] = custom_details["industry"].lower().replace(" ", "-")
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, contact_us_details: dict, *, captcha: bool = True):
    form_selectors = SELECTORS["form"]

    fill_out_input_fields(driver, form_selectors, contact_us_details)
    fill_out_textarea_fields(driver, form_selectors, contact_us_details)
    pick_option(driver, form_selectors, contact_us_details)
    tick_checkboxes_by_labels(driver, form_selectors, contact_us_details)

    if captcha:
        tick_captcha_checkbox(driver)

    take_screenshot(driver, "After filling out the contact us form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the contact us form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the contact us form")
