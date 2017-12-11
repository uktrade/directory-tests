# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Footer"
URL = None

SECTIONS = {
    "export readiness": {
        "label": "#footer-export-readiness-links",
        "new": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(1) > a",
        "occasional": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(2) > a",
        "regular": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(3) > a",
        "i'm new to exporting": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(1) > a",
        "i export occasionally": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(2) > a",
        "i'm a regular exporter": "#footer ul[aria-labelledby='footer-export-readiness-links'] > li:nth-child(3) > a"
    },
    "guidance": {
        "label": "#footer-guidance-links",
        "market research": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(1) > a",
        "customer insight": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(2) > a",
        "finance": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(3) > a",
        "business planning": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(4) > a",
        "getting paid": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(5) > a",
        "operations and compliance": "#footer ul[aria-labelledby='footer-guidance-links'] > li:nth-child(6) > a"
    },
    "services": {
        "label": "footer-services-links",
        "find a buyer": "#footer ul[aria-labelledby='footer-services-links'] > li:nth-child(1) > a",
        "selling online overseas": "#footer ul[aria-labelledby='footer-services-links'] > li:nth-child(2) > a",
        "export opportunities": "#footer ul[aria-labelledby='footer-services-links'] > li:nth-child(3) > a",
        "get finance": "#footer ul[aria-labelledby='footer-services-links'] > li:nth-child(4) > a",
        "events": "#footer ul[aria-labelledby='footer-services-links'] > li:nth-child(5) > a"
    },
    "general links": {
        "about": "#footer > .site-links > ul > li:nth-child(1) > a",
        "contact us": "#footer > .site-links > ul > li:nth-child(2) > a",
        "privacy and cookies": "#footer > .site-links > ul > li:nth-child(3) > a",
        "terms and conditions": "#footer > .site-links > ul > li:nth-child(4) > a",
        "department for international trade": "#footer > .site-links > ul > li:nth-child(5) > a"
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


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    with selenium_action(
            driver, "Could not find '%s' using '%s'", item_name,
            item_selector):
        menu_item = driver.find_element_by_css_selector(item_selector)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = driver.find_element_by_css_selector(link)
    assert button.is_displayed()
    button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
