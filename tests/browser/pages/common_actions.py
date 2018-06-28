# -*- coding: utf-8 -*-
"""Common PageObject actions."""
import logging

from selenium import webdriver
from utils import (
    assertion_msg,
    check_if_element_is_visible,
    clear_driver_cookies,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)

from pages import Selector


def go_to_url(
    driver: webdriver, url: str, page_name: str, *, first_time: bool = False
):
    """Go to the specified URL and take a screenshot afterwards.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param url: URL to open
    :param page_name: human friend page name used in screenshot name
    :param first_time: (optional) will delete all cookies if True
    """
    if first_time:
        clear_driver_cookies(driver)
    driver.get(url)
    take_screenshot(driver, page_name)


def check_url(
    driver: webdriver, expected_url: str, *, exact_match: bool = True
):
    """Check if current page URL matches the expected one.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param expected_url: expected page URL
    :param exact_match: (optional) if `True` then will do a `==` comparison.
                        If `False` then will do a `in` comparison.
                        Defaults to `True`.
    """
    with assertion_msg(
        "Expected page URL to be: '%s' but got '%s'",
        expected_url,
        driver.current_url,
    ):
        if exact_match:
            assert driver.current_url == expected_url
        else:
            assert (driver.current_url in expected_url) or (
                expected_url in driver.current_url
            )
    logging.debug("Current page URL matches expected '%s'", driver.current_url)


def check_title(
    driver: webdriver, expected_title: str, *, exact_match: bool = False
):
    """Check if current page title matches the expected one.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param expected_title: expected page title
    :param exact_match: (optional) if `True` then will do a `==` comparison.
                        If `False` then will do a `in` comparison.
                        Defaults to `False`.
    """
    with assertion_msg(
        "Expected page title to be: '%s' but got '%s'",
        expected_title,
        driver.title,
    ):
        if exact_match:
            assert expected_title.lower() == driver.title.lower()
        else:
            assert expected_title.lower() in driver.title.lower()
    logging.debug(
        "Page title on '%s' matches expected '%s'",
        driver.current_url,
        expected_title,
    )


def check_for_section(
    driver: webdriver, all_sections: dict, sought_section: str
):
    """Check if all page elements from sought section are visible.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param all_sections: a dict with page elements selectors grouped into page
                         sections.
    :param sought_section: section for which visibility check will be performed
    """
    section = all_sections[sought_section.lower()]
    for element_name, selector in section.items():
        element = find_element(
            driver, by_css=selector, element_name=element_name
        )
        with assertion_msg(
            "'%s' in '%s' is not displayed on: %s",
            element_name,
            sought_section,
            driver.current_url,
        ):
            assert element.is_displayed()
            logging.debug(
                "'%s' in '%s' is displayed", element_name, sought_section
            )


def check_for_expected_elements(
    driver: webdriver, elements: dict, *, wait_for_it: bool = True
):
    """Check if all page elements are visible.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param elements: a dict with page elements selectors. e.g.:
                     EXPECTED_ELEMENTS = {
                        "start now button": "<css_selector>",
                        "register link": "<css_selector>"
                        "sign-in link": "<css_selector>"
                     }
    """
    for element_name, element_selector in elements.items():
        element = find_element(
            driver,
            by_css=element_selector,
            element_name=element_name,
            wait_for_it=wait_for_it,
        )
        with assertion_msg(
            "It looks like '%s' element is not visible on %s",
            element_name,
            driver.current_url,
        ):
            assert element.is_displayed()
    logging.debug(
        "All expected elements are visible on '%s'", driver.current_url
    )


def check_for_expected_sections_elements(driver: webdriver, sections: dict):
    """Check if all elements in page sections are visible.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param sections: a dict with page elements selectors grouped into page
                     sections. e.g.:
                     SECTIONS = {
                        "start now": {
                            "start now button": "<css_selector>",
                            "register link": "<css_selector>"
                            "sign-in link": "<css_selector>"
                        }
                     }
    """
    for section in sections:
        for element_name, element_selector in sections[section].items():
            element = find_element(
                driver, by_css=element_selector, element_name=element_name
            )
            with assertion_msg(
                "It looks like '%s' element in '%s' section is not visible"
                " on %s",
                element_name,
                section,
                driver.current_url,
            ):
                assert element.is_displayed()
        logging.debug(
            "All expected elements are visible on '%s'", driver.current_url
        )


def find_and_click_on_page_element(
    driver: webdriver,
    sections: dict,
    element_name: str,
    *,
    wait_for_it: bool = True
):
    """Find page element in any page section selectors and click on it.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param sections: a dict with page elements selectors grouped into page
                     sections.
    :param element_name: name of the sought page element to click
    :param wait_for_it: (optional) Use `True` to wait for the element's
                        visibility or use `False` not to do so.
                        Defaults to `True`
    """
    found_selector = False
    for section_name, element_selectors in sections.items():
        if element_name.lower() in element_selectors:
            found_selector = True
            selector = element_selectors[element_name.lower()]
            if isinstance(selector, Selector):
                selector = selector.value
            logging.debug(
                "Found '%s' in '%s' section with following selector: '%s'",
                element_name,
                section_name,
                selector,
            )
            web_element = find_element(
                driver,
                by_css=selector,
                element_name=element_name,
                wait_for_it=wait_for_it,
            )
            check_if_element_is_visible(web_element, element_name)
            with wait_for_page_load_after_action(driver):
                web_element.click()
    with assertion_msg("Could not find '%s' in any section", element_name):
        assert found_selector
