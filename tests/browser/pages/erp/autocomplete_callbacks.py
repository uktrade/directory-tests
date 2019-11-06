# -*- coding: utf-8 -*-
"""Various form autocomplete callbacks"""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.utils import extract_by_css
from pages.common_actions import Selector, assertion_msg, find_element, find_elements


def autocomplete_uk_region(driver: WebDriver, *, value):
    if isinstance(value, bool) and not value:
        logging.debug(f"Won't use autocomplete")
        return

    if isinstance(value, bool):
        logging.debug(f"Will select random region to type")
        options = extract_by_css(
            driver.page_source, "select[id$=regions] option::text", first=False
        )
        logging.debug(f"Available country options: {options}")
        value = random.choice(options)

    logging.debug(f"Will select '{value}' from Region Autocomplete list")

    # enter text value into the input field with autocomplete
    input_selector = Selector(
        By.CSS_SELECTOR, "[id$=_regions_autocomplete]", is_visible=True
    )
    input = find_element(
        driver, input_selector, element_name="region input", wait_for_it=True
    )
    input.click()
    input.send_keys(value)

    logging.debug(f"Get list of options from autocomplete listbox")
    autocomplete_list = find_element(
        driver,
        Selector(
            By.CSS_SELECTOR, "[id$=regions_autocomplete__listbox]", is_visible=False
        ),
        wait_for_it=True,
    )
    autocomplete_list_options = autocomplete_list.find_elements(By.TAG_NAME, "li")
    with assertion_msg(f"Expected to find at least 1 region suggestion but got 0"):
        assert autocomplete_list_options

    logging.debug(f"Selecting random element from the autocomplete listbox")
    option = random.choice(autocomplete_list_options)
    option.click()


def autocomplete_industry(driver: WebDriver, *, value):
    if isinstance(value, bool) and not value:
        logging.debug(f"Won't use autocomplete")
        return

    if isinstance(value, bool):
        logging.debug(f"Will select random industry to type")
        options = extract_by_css(
            driver.page_source,
            "#id_imported-products-usage-imported_good_sector-select option::text",
            first=False,
        )
        logging.debug(f"Available country options: {options}")
        value = random.choice(options)

    logging.debug(f"Will select '{value}' from Industry Autocomplete list")

    # enter text value into the input field with autocomplete
    input_selector = Selector(
        By.ID, "id_imported-products-usage-imported_good_sector", is_visible=True
    )
    input = find_element(
        driver, input_selector, element_name="industry input", wait_for_it=True
    )
    input.click()
    input.send_keys(value)

    logging.debug(f"Get list of options from autocomplete listbox")
    autocomplete_list = find_element(
        driver,
        Selector(
            By.ID,
            "id_imported-products-usage-imported_good_sector__listbox",
            is_visible=False,
        ),
        wait_for_it=True,
    )
    autocomplete_list_options = autocomplete_list.find_elements(By.TAG_NAME, "li")
    with assertion_msg(f"Expected to find at least 1 region suggestion but got 0"):
        assert autocomplete_list_options

    logging.debug(f"Selecting random element from the autocomplete listbox")
    option = random.choice(autocomplete_list_options)
    option.click()


def autocomplete_country(driver: WebDriver, *, value):
    if isinstance(value, bool) and not value:
        logging.debug(f"Won't use autocomplete")
        return

    if isinstance(value, bool):
        logging.debug(f"Will select random country to type")
        options = extract_by_css(
            driver.page_source, "select[id^=id] option::text", first=False
        )
        logging.debug(f"Available country options: {options}")
        value = random.choice(options)

    logging.debug(f"Will select '{value}' from country autocomplete list")

    # enter text value into the input field with autocomplete
    input_selector = Selector(
        By.CSS_SELECTOR, "input.autocomplete__input", is_visible=True
    )
    input = find_element(
        driver, input_selector, element_name="country input", wait_for_it=False
    )
    input.click()
    input.send_keys(value)

    logging.debug(f"Get list of options from autocomplete listbox")
    autocomplete_list = find_elements(
        driver, Selector(By.CSS_SELECTOR, "ul[role=listbox] li", is_visible=True)
    )
    input.send_keys(Keys.DOWN)
    random.choice(autocomplete_list).send_keys(Keys.SPACE)
