# -*- coding: utf-8 -*-
"""Various form autocomplete callbacks"""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, find_element, find_elements


def enrol_autocomplete_company_name(driver: WebDriver, value: str = None):
    """Value is ignored as we want to choose random company name"""
    autocomplete = Selector(
        By.CSS_SELECTOR, "ul.SelectiveLookupDisplay", is_visible=True
    )
    find_element(driver, autocomplete, element_name="Autocomplete", wait_for_it=True)
    options = find_elements(driver, Selector(By.CSS_SELECTOR, "li[role='option']"))
    option = random.choice(options)
    logging.debug(
        f"Selected company: {option.get_attribute('data-value')} {option.text}"
    )
    option.click()
