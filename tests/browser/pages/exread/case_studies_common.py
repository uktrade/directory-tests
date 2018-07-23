# -*- coding: utf-8 -*-
"""ExRed Common Case Study Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_if_element_is_visible,
    find_element,
    take_screenshot,
)

NAME = "ExRed Common Case Study"
URL = None


SHARE_WIDGET = Selector(By.CSS_SELECTOR, "#top > ul.sharing-links")
CASE_STUDIES = {
    1: {
        "breadcrumb": Selector(
            By.CSS_SELECTOR, "#content > div > p.breadcrumbs > span.current"
        ),
        "title": Selector(By.CSS_SELECTOR, "#top h1"),
        "type": Selector(By.CSS_SELECTOR, "#top p.type"),
        "description": Selector(By.CSS_SELECTOR, "#top p.description"),
    },
    2: {
        "breadcrumb": Selector(
            By.CSS_SELECTOR, "#content > div > p.breadcrumbs > span.current"
        ),
        "title": Selector(By.CSS_SELECTOR, "#top h1"),
        "type": Selector(By.CSS_SELECTOR, "#top p.type"),
        "description": Selector(By.CSS_SELECTOR, "#top p.description"),
    },
    3: {
        "breadcrumb": Selector(
            By.CSS_SELECTOR, "#content > div > p.breadcrumbs > span.current"
        ),
        "title": Selector(By.CSS_SELECTOR, "#top h1"),
        "type": Selector(By.CSS_SELECTOR, "#top p.type"),
        "description": Selector(By.CSS_SELECTOR, "#top p.description"),
    },
}


def should_be_here(driver: WebDriver, case_study_number: int, *, title: str = None):
    take_screenshot(driver, NAME)
    for element_name, selector in CASE_STUDIES[case_study_number].items():
        element = find_element(driver, selector, element_name=element_name)
        check_if_element_is_visible(element, element_name)
        if title:
            if element_name in ["title", "breadcrumb"]:
                element = find_element(driver, selector, element_name=element_name)
                with assertion_msg(
                    "Expected case study %s to be '%s' but got '%s'",
                    element_name,
                    title,
                    element.text,
                ):
                    assert element.text.lower() == title.lower()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_share_widget(driver: WebDriver):
    share_widget = find_element(driver, SHARE_WIDGET, element_name="Share widget")
    check_if_element_is_visible(share_widget, element_name="share widget")
