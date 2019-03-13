# -*- coding: utf-8 -*-
"""Various form autocomplete callbacks"""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, find_element, find_elements


def autocomplete_product_type(driver: WebDriver):
    autocomplete = Selector(
        By.CSS_SELECTOR, "ul#search-product-dropdown", is_visible=True
    )
    find_element(
        driver, autocomplete, element_name="Autocomplete", wait_for_it=True
    )
    options = find_elements(
        driver, Selector(By.CSS_SELECTOR, "li > a.form-dropdown-option")
    )
    option = random.choice(options)
    logging.debug(
        f"Autocomplete selected product type: {option.get_attribute('data-option-id')}"
    )
    option.click()


def autocomplete_country_name(driver: WebDriver):
    # wait for the response from Geography API
    import time

    time.sleep(1)
    autocomplete = Selector(
        By.CSS_SELECTOR, "ul#search-country-dropdown", is_visible=True
    )
    find_element(
        driver, autocomplete, element_name="Autocomplete", wait_for_it=True
    )
    options = find_elements(
        driver,
        Selector(
            By.CSS_SELECTOR, "li > a.form-dropdown-option", is_visible=True
        ),
    )
    option = random.choice(options)
    logging.debug(
        f"Autocomplete selected country name: {option.get_attribute('data-option-id')}"
    )
    option.click()
