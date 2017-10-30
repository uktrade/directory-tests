# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver import ActionChains

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Header"
URL = None


HOME_LINK = "#menu > ul > li:nth-child(1) > a"
# some sections contain an OrderedDict, this is because of the quirky browser
# behaviour when dealing with JS menus. Please refer to open() for more details
SECTIONS = {
    "export readiness": OrderedDict([
        ("menu", "#nav-export-readiness"),
        ("i'm new to exporting", "#nav-export-readiness-list a[href='/new']"),
        ('i export occasionally', "#nav-export-readiness-list a[href='/occasional']"),
        ("i'm a regular exporter", "#nav-export-readiness-list a[href='/regular']")
    ]),
    "guidance": OrderedDict([
        ("menu", "#nav-guidance"),
        ("market research", "#nav-guidance-list  a[href='/market-research']"),
        ("customer insight", "#nav-guidance-list  a[href='/customer-insight']"),
        ("finance", "#nav-guidance-list  a[href='/finance']"),
        ("business planning", "#nav-guidance-list  a[href='/business-planning']"),
        ("getting paid", "#nav-guidance-list  a[href='/getting-paid']"),
        ("operations and compliance", "#nav-guidance-list  a[href='/operations-and-compliance']")
    ]),
    "services": OrderedDict([
        ("menu", "#nav-services"),
        ("find a buyer", "#nav-services-list > li:nth-child(1) > a"),
        ("selling online overseas", "#nav-services-list > li:nth-child(2) > a"),
        ("export opportunities", "#nav-services-list > li:nth-child(3) > a"),
        ("get finance", "#nav-services-list > li:nth-child(4) > a"),
        ("events", "#nav-services-list > li:nth-child(5) > a)")
    ]),
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
    """Open specific element that belongs to the group.

    NOTE:
    Some browsers (Firefox & IE) can cause problems when dealing with JS menus.
    In order to move the cursor to the correct menu element before clicking on
    it, the driver needs to be instructed to move the cursor to a visible menu
    element that is not diagonally positioned in respect to the main menu.
    It's because "moving" the cursor diagonally can cause driver to "lose"
    the focus of the menu and which will make menu to fold.
    """
    if "menu" in SECTIONS[group.lower()]:
        menu_selector = SECTIONS[group.lower()]["menu"]
        menu = driver.find_element_by_css_selector(menu_selector)

        last_menu_item_name = next(reversed(SECTIONS[group.lower()]))
        last_menu_selector = SECTIONS[group.lower()][last_menu_item_name]
        last_menu_item = driver.find_element_by_css_selector(last_menu_selector)

        menu_item_selector = SECTIONS[group.lower()][element.lower()]
        menu_item = driver.find_element_by_css_selector(menu_item_selector)

        actions = ActionChains(driver)
        actions.move_to_element(menu)
        if menu_item_selector != last_menu_selector:
            actions.move_to_element(last_menu_item)
        actions.click(menu_item)
        actions.perform()
    else:
        menu_item_selector = SECTIONS[group.lower()][element.lower()]
        menu_item = driver.find_element_by_css_selector(menu_item_selector)
        assert menu_item.is_displayed()
        menu_item.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
