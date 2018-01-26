# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    find_and_click_on_page_element
)
from utils import assertion_msg, find_element, take_screenshot

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
        "operations and compliance":
            "#footer-guidance-operations-and-compliance"
    },
    "services": {
        "label": "#footer-services-links",
        "find a buyer": "#footer-services-find-a-buyer",
        "selling online overseas": "#footer-services-selling-online-overseas",
        "export opportunities": "#footer-services-export-opportunities",
        "get finance": "#footer-services-get-finance",
        "events": "#footer-services-events"
    },
    "general": {
        "your export journey": "#footer-custom-page-link",
        "about": "#footer-site-links-about",
        "contact us": "#footer-site-links-contact-us",
        "privacy and cookies": "#footer-site-links-privacy-and-cookies",
        "terms and conditions": "#footer-site-links-t-and-c",
        "department for international trade": "#footer-site-links-dit",
        "copyright": "#footer-copyright"
    }
}


def should_see_all_menus(driver: webdriver):
    check_for_expected_sections_elements(driver, SECTIONS)


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    menu_item = find_element(
        driver, by_css=item_selector, element_name=item_name)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = find_element(
        driver, by_css=link, element_name=element, wait_for_it=False)
    button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
