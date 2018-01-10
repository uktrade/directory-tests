# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Footer"
URL = None

SECTIONS = {
    "logos": {
        "dit logo": "#footer-dit-logo",
        "eig logo": "#footer-eig-logo"
    },
    "export readiness": {
        "label": "#footer-export-readiness-links",
        "new": "#footer-export-readiness-new",
        "occasional": "#footer-export-readiness-occasional",
        "regular": "#footer-export-readiness-regular",
        "i'm new to exporting": "#footer-export-readiness-new",
        "i export occasionally": "#footer-export-readiness-occasional",
        "i'm a regular exporter": "#footer-export-readiness-regular"
    },
    "guidance": {
        "label": "#footer-guidance-links",
        "market research": "#footer-guidance-market-research",
        "customer insight": "#footer-guidance-customer-insight",
        "finance": "#footer-guidance-finance",
        "business planning": "#footer-guidance-business-planning",
        "getting paid": "#footer-guidance-getting-paid",
        "operations and compliance": "#footer-guidance-operations-and-compliance"
    },
    "services": {
        "label": "#footer-services-links",
        "find a buyer": "#footer-services-find-a-buyer",
        "selling online overseas": "#footer-services-selling-online-overseas",
        "export opportunities": "#footer-services-export-opportunities",
        "get finance": "#footer-services-get-finance",
        "events": "#footer-services-events"
    },
    "general links": {
        "about": "#footer-site-links-about",
        "contact us": "#footer-site-links-contact-us",
        "privacy and cookies": "#footer-site-links-privacy-and-cookies",
        "terms and conditions": "#footer-site-links-t-and-c",
        "department for international trade": "#footer-site-links-dit",
        "copyright": "#footer-copyright"
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
