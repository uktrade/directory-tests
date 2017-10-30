# -*- coding: utf-8 -*-
"""ExRed Common Guidance Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Common Guidance"
URL = None


RIBBON = {
    "itself": ".navigation-ribbon",
    "market research": ".navigation-ribbon a[href='/market-research']",
    "customer insight": ".navigation-ribbon a[href='/customer-insight']",
    "finance": ".navigation-ribbon a[href='/finance']",
    "business planning": ".navigation-ribbon a[href='/business-planning']",
    "getting paid": ".navigation-ribbon a[href='/getting-paid']",
    "operations and compliance": ".navigation-ribbon a[href='/operations-and-compliance']"
}


def ribbon_should_be_visible(driver: webdriver):
    for element_name, element_selector in RIBBON.items():
        logging.debug(
            "Looking for Ribbon '%s' element with '%s' selector",
            element_name, element_selector)
        with selenium_action(
                driver, "Could not find '%s' using '%s'", element_name,
                element_selector):
            element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' is not visible", element_name):
            assert element.is_displayed()
    take_screenshot(driver, NAME + " Ribbon")
