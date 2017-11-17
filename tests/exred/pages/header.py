# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Header"
URL = None


HOME_LINK = "#menu > ul > li:nth-child(1) > a"
SECTIONS = {
    "export readiness": {
        "menu": "#nav-export-readiness",
        "new": "#nav-export-readiness-list a[href='/new']",
        'occasional': "#nav-export-readiness-list a[href='/occasional']",
        "regular": "#nav-export-readiness-list a[href='/regular']",
        "i'm new to exporting": "#nav-export-readiness-list a[href='/new']",
        'i export occasionally': "#nav-export-readiness-list a[href='/occasional']",
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


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    if section.lower() in ["export readiness", "guidance", "services"]:
        # Open the menu by sending "Down Arrow" key
        menu_selector = SECTIONS[section.lower()]["menu"]
        menu = driver.find_element_by_css_selector(menu_selector)
        menu.send_keys(Keys.DOWN)
    with selenium_action(
            driver, "Could not find '%s' using '%s'", item_name,
            item_selector):
        menu_item = driver.find_element_by_css_selector(item_selector)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


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
        # Open the menu by sending "Down Arrow" key
        menu_selector = SECTIONS[group.lower()]["menu"]
        menu = driver.find_element_by_css_selector(menu_selector)
        menu.send_keys(Keys.DOWN)
    menu_item_selector = SECTIONS[group.lower()][element.lower()]
    with selenium_action(
            driver, "Could not find %s element in %s group with '%s' selector",
            element, group, menu_item_selector):
        menu_item = driver.find_element_by_css_selector(menu_item_selector)
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              menu_item_selector)))
    with assertion_msg("%s menu item: '%s' is not visible", group, element):
        assert menu_item.is_displayed()
    menu_item.click()
    take_screenshot(
        driver, NAME + " after clicking on: {} link".format(element))
