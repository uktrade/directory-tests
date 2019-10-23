# -*- coding: utf-8 -*-
"""Various form autocomplete callbacks"""
import logging
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, assertion_msg, find_element, find_elements


def autocomplete_uk_region(driver: WebDriver, *, value):
    if isinstance(value, bool) and not value:
        logging.debug(f"Won't use autocomplete")
        return

    if isinstance(value, bool):
        logging.debug(f"Will select random region to type")
        options = find_elements(
            driver,
            Selector(
                By.CSS_SELECTOR,
                "#id_consumer-group-consumer_regions option",
                is_visible=False,
            ),
        )
        options_texts = [
            option.get_attribute("text")
            for option in options
            if option.get_attribute("text")
        ]
        logging.debug(f"Available region options: {options_texts}")
        with assertion_msg(f"Expected to find at least 1 region option to choose from"):
            assert options_texts

        value = random.choice(options_texts)

    logging.debug(f"Will select '{value}' from Region Autocomplete list")

    # enter text value into the input field with autocomplete
    input_selector = Selector(
        By.ID, "id_consumer-group-consumer_regions_autocomplete", is_visible=True
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
            By.ID,
            "id_consumer-group-consumer_regions_autocomplete__listbox",
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
