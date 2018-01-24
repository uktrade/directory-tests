# -*- coding: utf-8 -*-
"""Common Language Selector on great pages"""
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from utils import (
    assertion_msg,
    check_if_element_is_not_visible,
    find_element,
    selenium_action,
    take_screenshot
)

NAME = "Language selector"

LANGUAGE_INDICATOR = "#header-bar span.lang"
LANGUAGE_SELECTOR_OPEN = "#header-bar a.LanguageSelectorDialog-Tracker"
LANGUAGE_SELECTOR_CLOSE = "#header-language-selector-close"
DOMESTIC_PAGE = "section.language-selector-dialog div.domestic-redirect > p > a"
ENGLISH = "#header-language-selector-en-gb"
CHINESE = "#header-language-selector-zh-hans"
GERMAN = "#header-language-selector-de"
JAPANESE = "#header-language-selector-ja"
SPANISH = "#header-language-selector-es"
PORTUGUESE = "#header-language-selector-pt"
ARABIC = "#header-language-selector-ar"
ELEMENTS_ON = {
    "home": {
        "itself": "section.language-selector-dialog",
        "title": "#great-languages-selector",
        "English": ENGLISH,
        "简体中文": CHINESE,
        "Deutsch": GERMAN,
        "日本語": JAPANESE,
        "Español": SPANISH,
        "Português": PORTUGUESE,
        "العربيّة": ARABIC,
        "close": LANGUAGE_SELECTOR_CLOSE
    },
    "international": {
        "itself": "section.language-selector-dialog",
        "title": "#great-languages-selector",
        "English (UK)": DOMESTIC_PAGE,
        "English": ENGLISH,
        "简体中文": CHINESE,
        "Deutsch": GERMAN,
        "日本語": JAPANESE,
        "Español": SPANISH,
        "Português": PORTUGUESE,
        "العربيّة": ARABIC,
        "close": LANGUAGE_SELECTOR_CLOSE
    }
}
KEYBOARD_NAVIGABLE_ELEMENTS = {
    "home": [
        ("English", ENGLISH),
        ("简体中文", CHINESE),
        ("Deutsch", GERMAN),
        ("日本語", JAPANESE),
        ("Español", SPANISH),
        ("Português", PORTUGUESE),
        ("العربيّة", ARABIC),
        ("close", LANGUAGE_SELECTOR_CLOSE)
    ],
    "international": [
        ("English", ENGLISH),
        ("简体中文", CHINESE),
        ("Deutsch", GERMAN),
        ("日本語", JAPANESE),
        ("Español", SPANISH),
        ("Português", PORTUGUESE),
        ("العربيّة", ARABIC),
        ("domestic page", DOMESTIC_PAGE),
        ("close", LANGUAGE_SELECTOR_CLOSE),
    ]
}
LANGUAGE_INDICATOR_VALUES = {
    "English": "en-gb",
    "English (UK)": "en-gb",
    "简体中文": "zh-hans",
    "Deutsch": "de",
    "日本語": "ja",
    "Español": "es",
    "Português": "pt",
    "العربيّة": "ar",
}


def close(driver: webdriver, *, with_keyboard: bool = False):
    close_language_selector_button = find_element(
        driver, by_css=LANGUAGE_SELECTOR_CLOSE)
    with assertion_msg("Close Language Selector button is not visible"):
        assert close_language_selector_button.is_displayed()
    if with_keyboard:
        close_language_selector_button.send_keys(Keys.ENTER)
    else:
        close_language_selector_button.click()


def open(driver: webdriver, *, with_keyboard: bool = False):
    language_selector = find_element(driver, by_css=LANGUAGE_SELECTOR_OPEN)
    with assertion_msg("Language Selector button is not visible"):
        assert language_selector.is_displayed()
    if with_keyboard:
        language_selector.send_keys(Keys.ENTER)
    else:
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
            driver, by_css=selector, element_name=key, wait_for_it=False)


def navigate_through_links_with_keyboard(driver: webdriver, page_name: str):
    for name, selector in KEYBOARD_NAVIGABLE_ELEMENTS[page_name.lower()]:
        element = find_element(driver, by_css=selector, element_name=name)
        with assertion_msg("Expected '%s' element to be in focus", name):
            assert element.id == driver.switch_to.active_element.id
            logging.debug("%s is focused, moving to the next one", name)
        element.send_keys(Keys.TAB)


def keyboard_should_be_trapped(driver: webdriver, page_name: str):
    number_of_navigation_iterations = 2
    for _ in range(number_of_navigation_iterations):
        navigate_through_links_with_keyboard(driver, page_name)


def change_to(
        driver: webdriver, page_name: str, language: str, *,
        with_keyboard: bool = False):
    language_selector = ELEMENTS_ON[page_name.lower()][language]
    language_button = find_element(driver, by_css=language_selector)
    if with_keyboard:
        language_button.send_keys(Keys.ENTER)
    else:
        language_button.click()


def check_page_language_is(driver: webdriver, expected_language: str):
    expected_language_code = LANGUAGE_INDICATOR_VALUES[expected_language]
    language_indicator = find_element(driver, by_css=LANGUAGE_INDICATOR)
    language_indicator_code = language_indicator.text.lower()
    with assertion_msg(
            "Expected to see page in '%s' but got '%s'",
            expected_language_code, language_indicator_code):
        assert language_indicator_code == expected_language_code
