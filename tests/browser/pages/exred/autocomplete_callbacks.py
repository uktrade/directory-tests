"""Various form autocomplete callbacks"""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, find_element, find_elements


def autocomplete_company_name(driver: WebDriver):
    autocomplete = Selector(
        By.CSS_SELECTOR, "ul.SelectiveLookupDisplay", is_visible=True
    )
    find_element(driver, autocomplete, element_name="Autocomplete", wait_for_it=True)
    options = find_elements(
        driver, Selector(By.CSS_SELECTOR, "li[role='option']", is_visible=True)
    )
    option = random.choice(options)
    logging.debug(
        f"Autocomplete selected country name: {option.get_attribute('data-value')} {option.text}"
    )
    option.click()
