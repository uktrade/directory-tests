# -*- coding: utf-8 -*-
"""Common Language Selector on great pages"""
import logging
import time

from selenium import webdriver

from utils import (
    assertion_msg,
    check_if_element_is_not_visible,
    find_element,
    selenium_action,
    take_screenshot
)

NAME = "Language selector"

LANGUAGE_SELECTOR_OPEN = "#header-bar a.LanguageSelectorDialog-Tracker"
LANGUAGE_SELECTOR_CLOSE = "#header-language-selector-close"
DOMESTIC_PAGE = "section.language-selector-dialog div.domestic-redirect > p > a"
ELEMENTS_ON = {
    "home": {
        "itself": "section.language-selector-dialog",
        "title": "#great-languages-selector",
        "English": "#header-language-selector-en-gb",
        "简体中文": "#header-language-selector-zh-hans",
        "Deutsch": "#header-language-selector-de",
        "日本語": "#header-language-selector-ja",
        "Español": "#header-language-selector-es",
        "Português": "#header-language-selector-pt",
        "العربيّة": "#header-language-selector-ar",
        "close": LANGUAGE_SELECTOR_CLOSE
    },
    "international": {
        "itself": "section.language-selector-dialog",
        "title": "#great-languages-selector",
        "domestic page": DOMESTIC_PAGE,
        "English": "#header-language-selector-en-gb",
        "简体中文": "#header-language-selector-zh-hans",
        "Deutsch": "#header-language-selector-de",
        "日本語": "#header-language-selector-ja",
        "Español": "#header-language-selector-es",
        "Português": "#header-language-selector-pt",
        "العربيّة": "#header-language-selector-ar",
        "close": LANGUAGE_SELECTOR_CLOSE
    }
}


def close(driver: webdriver):
    close_language_selector_button = find_element(
        driver, by_css=LANGUAGE_SELECTOR_CLOSE)
    with assertion_msg("Close Language Selector button is not visible"):
        assert close_language_selector_button.is_displayed()
    close_language_selector_button.click()


def open(driver: webdriver):
    language_selector = find_element(driver, by_css=LANGUAGE_SELECTOR_OPEN)
    with assertion_msg("Language Selector button is not visible"):
        assert language_selector.is_displayed()
    language_selector.click()


def should_see_it_on(driver: webdriver, page_name: str):
    take_screenshot(driver, NAME + page_name)
    section = ELEMENTS_ON[page_name.lower()]
    for key, selector in section.items():
        with selenium_action(
                driver, "Could not find: '%s' element on '%s' using "
                        "'%s' selector",
                key, page_name, selector):
            element = find_element(driver, by_css=selector)
        with assertion_msg(
                "'%s' on '%s' is not displayed", key, page_name):
            assert element.is_displayed()
            logging.debug("'%s' on '%s' is displayed", key, page_name)


def should_not_see_it_on(driver: webdriver, page_name: str):
    # wait a second before language selector modal window disappears
    time.sleep(1)
    take_screenshot(driver, NAME + page_name)
    page_elements = ELEMENTS_ON[page_name.lower()]
    for key, selector in page_elements.items():
        check_if_element_is_not_visible(
            driver, by_css=selector, element_name=key)
