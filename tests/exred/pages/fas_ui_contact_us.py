# -*- coding: utf-8 -*-
"""Find a Supplier Landing Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_title,
    check_url,
    go_to_url,
)
from settings import DIRECTORY_UI_SUPPLIER_URL
from utils import take_screenshot, find_element

NAME = "Find a Supplier - Contact Us page"
URL = urljoin(DIRECTORY_UI_SUPPLIER_URL, "industries/contact/")
PAGE_TITLE = "Contact us - trade.great.gov.uk"

SUBMIT_BUTTON = "form input[type=submit]"
FULL_NAME = "#id_full_name"
EMAIL = "#id_email_address"
INDUSTRY = "#id_sector"
ORGANISATION = "#id_organisation_name"
ORGANISATION_SIZE = "#id_organisation_size"
COUNTRY = "#id_country"
BODY = "#id_body"
SOURCE = "#id_source"
ACCEPT_TC = "#id_terms_agreed-label"
SECTIONS = {
    "form": {
        "itself": "#lede form",
        "full name": FULL_NAME,
        "email": EMAIL,
        "industry": INDUSTRY,
        "organisation": ORGANISATION,
        "organisation size": ORGANISATION_SIZE,
        "country": COUNTRY,
        "body": BODY,
        "source": SOURCE,
        "accept t&c": ACCEPT_TC,
        "submit": SUBMIT_BUTTON
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SECTIONS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def fill_out(driver: webdriver, contact_us_details: dict):
    input_fields = ["full name", "email", "organisation", "country", "body"]
    dropdown_menus = ["industry", "organisation size", "source"]

    for field_name in input_fields:
        value = contact_us_details[field_name]
        field = find_element(
            driver, by_css=SECTIONS["form"][field_name],
            element_name=field_name, wait_for_it=False)
        field.send_keys(value)

    for menu_name in dropdown_menus:
        selector = SECTIONS["form"][menu_name]
        dropdown = find_element(
            driver, by_css=selector,
            element_name="{} dropdown menu".format(menu_name),
            wait_for_it=False)
        if contact_us_details[menu_name]:
            option = contact_us_details[menu_name].lower().replace(" ", "-")
        else:
            options = dropdown.find_elements_by_css_selector("option")
            values = [option.get_property("value") for option in options]
            logging.debug("OPTIONS: {}".format(values))
            option = random.choice(values)
            logging.debug("OPTION: {}".format(option))
        sector_value = "option[value='{}']".format(option)
        sector_option = dropdown.find_element_by_css_selector(sector_value)
        sector_option.click()

    if contact_us_details["accept t&c"]:
        checkbox = find_element(driver, by_css=ACCEPT_TC)
        checkbox.click()

    take_screenshot(driver, "After filling out the contact us form")


def submit(driver: webdriver):
    take_screenshot(driver, "Before submitting the contact us form")
    button = find_element(
        driver, by_css=SUBMIT_BUTTON, element_name="Submit button",
        wait_for_it=False)
    button.click()
    take_screenshot(driver, "After submitting the contact us form")
