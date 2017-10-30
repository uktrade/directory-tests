# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Header"
URL = None


HOME_LINK = "#menu > ul > li:nth-child(1) > a"
SECTIONS = {
    "export readiness": {
        "menu": "#nav-export-readiness",
        "i'm new to exporting": "#nav-export-readiness-list a[href='/new']",
        "i export occasionally": "#nav-export-readiness-list a[href='/occasional']",
        "i'm a regular exporter": "#nav-export-readiness-list a[href='/regular']"
    },
    "guidance": {
        "menu": "#nav-guidance",
        "market research": "#nav-guidance-list  a[href='/market-research']",
        "customer insight": "#nav-guidance-list  a[href='/customer-insight']",
        "finance": "#nav-guidance-list  a[href='/finance']",
        "business planning": "#nav-guidance-list  a[href='/business-planning']",
        "getting paid": "#nav-guidance-list  a[href='/getting-paid']",
        "operations and compliance": "#nav-guidance-list  a[href='/operations-and-compliance']"
    },
    "services": {
        "menu": "#nav-services",
        "find a buyer": "#nav-services-list > li:nth-child(1) > a",
        "selling online overseas": "#nav-services-list > li:nth-child(2) > a",
        "export opportunities": "#nav-services-list > li:nth-child(3) > a",
        "get finance": "#nav-services-list > li:nth-child(4) > a",
        "events": "#nav-services-list > li:nth-child(5) > a"
    },
    "government links": {
        "part of great.gov.uk": "#header-bar > div > p > a"
    },
    "account links": {
        "register": "#header-bar .account-links li:nth-child(1) > a",
        "sign in": "#header-bar .account-links li:nth-child(2) > a"
    }
}


def should_see_all_links(driver: webdriver):
    for section in SECTIONS:
        for element_name, element_selector in SECTIONS[section].items():
            logging.debug(
                "Looking for '%s' element in '%s' section with '%s' selector",
                element_name, section, element_selector)
            with selenium_action(
                    driver, "Could not find '%s' using '%s'", element_name,
                    element_selector):
                element = driver.find_element_by_css_selector(element_selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible",
                    element_name, section):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section)
    logging.debug(
        "All expected sections on %s are visible", NAME)


def open(driver: webdriver, group: str, element: str):
    if "menu" in SECTIONS[group.lower()]:
        menu_selector = SECTIONS[group.lower()]["menu"]
        menu = driver.find_element_by_css_selector(menu_selector)
        menu.is_displayed()
        menu.click()
        take_screenshot(
            driver, NAME + " after clicking on '%s' menu".format(group))
    link_selector = SECTIONS[group.lower()][element.lower()]
    with selenium_action(
            driver, "Could not find '%s' menu '%s' link", group, element):
        link = driver.find_element_by_css_selector(link_selector)
    assert link.is_displayed()
    link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
