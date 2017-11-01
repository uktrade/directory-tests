# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Footer"
URL = None

SECTIONS = {
    "export readiness": {
        "label": "#footer-links-2",
        "i'm new to exporting": "#footer-links-2  ~ ul > li:nth-child(1) > a",
        "i export occasionally": "#footer-links-2  ~ ul > li:nth-child(2) > a",
        "i'm a regular exporter": "#footer-links-2  ~ ul > li:nth-child(3) > a"
    },
    "guidance": {
        "label": "#footer-links-3",
        "market research": "#footer-links-3  ~ ul a[href='/market-research']",
        "customer insight": "#footer-links-3  ~ ul a[href='/customer-insight']",
        "finance": "#footer-links-3  ~ ul a[href='/finance']",
        "business planning": "#footer-links-3  ~ ul a[href='/business-planning']",
        "getting paid": "#footer-links-3  ~ ul a[href='/getting-paid']",
        "operations and compliance": "#footer-links-3  ~ ul a[href='/operations-and-compliance']"
    },
    "services": {
        "label": "#footer-links-4",
        "export opportunities": "#footer-links-4  ~ ul > li:nth-child(1) > a",
        "selling online overseas": "#footer-links-4  ~ ul > li:nth-child(2) > a",
        "find a buyer": "#footer-links-4  ~ ul > li:nth-child(3) > a",
        "get finance": "#footer-links-4  ~ ul > li:nth-child(4) > a",
        "events": "#footer-links-4  ~ ul > li:nth-child(5) > a"
    },
    "general links": {
        "part of great.gov.uk": "#footer > .site-links > ul > li:nth-child(1) > a",
        "about": "#footer > .site-links > ul > li:nth-child(2) > a",
        "contact us": "#footer > .site-links > ul > li:nth-child(3) > a",
        "privacy and cookies": "#footer > .site-links > ul > li:nth-child(4) > a",
        "terms and conditions": "#footer > .site-links > ul > li:nth-child(5) > a",
        "department for international trade": "#footer > .site-links > ul > li:nth-child(6) > a"
    }
}


def should_see_all_menus(driver: webdriver):
    for section in SECTIONS:
        for name, selector in SECTIONS[section].items():
            logging.debug(
                "Looking for '%s' link in '%s' section with '%s' selector",
                name, section, selector)
            with selenium_action(
                    driver, "Could not find '%s link' using '%s'",
                    name, selector):
                element = driver.find_element_by_css_selector(selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible",
                    name, section):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section)
    logging.debug(
        "All expected sections on %s are visible", NAME)


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = driver.find_element_by_css_selector(link)
    assert button.is_displayed()
    button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
