# -*- coding: utf-8 -*-
"""ExRed Common Case Study Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Common Case Study"
URL = None


SHARE_WIDGET = "#top > ul.sharing-links"
CASE_STUDIES = {
    1: {
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    },
    2: {
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    },
    3: {
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    }
}


def should_be_here(driver: webdriver, case_study_number: int):
    for element_name, element_selector in CASE_STUDIES[case_study_number].items():
        with selenium_action(
                driver, "Could not find '%s' using '%s'", element_name,
                element_selector):
            element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_share_widget(driver: webdriver):
    with selenium_action(
            driver, "Could not find Share Widget with '%s'", SHARE_WIDGET):
        share_widget = driver.find_element_by_css_selector(SHARE_WIDGET)
    with assertion_msg(
            "Share widget is not visible on: %s", driver.current_url):
        assert share_widget.is_displayed()
