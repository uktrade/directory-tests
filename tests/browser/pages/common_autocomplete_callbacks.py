# -*- coding: utf-8 -*-
"""Common callback for form fields with autocomplete functionality."""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.utils import extract_attributes_by_css
from pages.common_actions import Selector, find_element


def js_country_select(driver: WebDriver, *, value):
    """Select random country from an input field with JS autocompletion.

    This callback works on following pages:
        * HPO contact form - high-potential-opportunities/contact/
    """
    option_values = extract_attributes_by_css(
        driver.page_source,
        "#js-country-select-select option",
        attrs=["value"],
        text=True,
    )
    # ignore options with no value and flatten the dict to a list
    option_values = [item["text"] for item in option_values if item["value"]]
    logging.debug(f"Available countries: {option_values}")
    value = random.choice(option_values)
    logging.debug(f"Selected country: {value}")
    js_field = find_element(driver, Selector(By.ID, "js-country-select"))
    js_field.click()
    js_field.clear()
    js_field.send_keys(value)
    first_suggestion_selector = Selector(
        By.CSS_SELECTOR, "#js-country-select__listbox li:nth-child(1)"
    )
    first_suggestion = find_element(driver, first_suggestion_selector, wait_for_it=True)
    first_suggestion.click()
