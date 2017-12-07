# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from utils import (
    assertion_msg,
    find_element,
    take_screenshot,
    wait_for_visibility
)

NAME = "ExRed Header"
URL = None


HOME_LINK = "#menu > ul > li:nth-child(1) > a"
REGISTRATION_LINK = "#header-bar a.register"
SIGN_IN_LINK = "#header-bar a.signin"
SECTIONS = {
    "export readiness": {
        "menu": "#export-readiness-links",
        "new": "#export-readiness-links-list a[href='/new']",
        'occasional': "#export-readiness-links-list a[href='/occasional']",
        "regular": "#export-readiness-links-list a[href='/regular']",
        "i'm new to exporting": "#export-readiness-links-list a[href='/new']",
        'i export occasionally': "#export-readiness-links-list a[href='/occasional']",
        "i'm a regular exporter": "#export-readiness-links-list a[href='/regular']"
    },
    "guidance": {
        "menu": "#guidance-links",
        "market research": "#guidance-links-list a[href='/market-research']",
        "customer insight": "#guidance-links-list a[href='/customer-insight']",
        "finance": "#guidance-links-list a[href='/finance']",
        "business planning": "#guidance-links-list a[href='/business-planning']",
        "getting paid": "#guidance-links-list a[href='/getting-paid']",
        "operations and compliance": "#guidance-links-list a[href='/operations-and-compliance']"
    },
    "services": {
        "menu": "#services-links",
        "find a buyer": "#services-links-list > li:nth-child(1) > a",
        "selling online overseas": "#services-links-list > li:nth-child(2) > a",
        "export opportunities": "#services-links-list > li:nth-child(3) > a",
        "get finance": "#services-links-list > li:nth-child(4) > a",
        "events": "#services-links-list > li:nth-child(5) > a"
    },
    "government links": {
        "part of great.gov.uk": "#header-bar p.government-links > a"
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
            element = find_element(driver, by_css=element_selector)
            wait_for_visibility(driver, by_css=element_selector)
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
        logging.debug("Open the menu by sending 'Right Arrow' key")
        menu_selector = SECTIONS[section.lower()]["menu"]
        menu = find_element(driver, by_css=menu_selector)
        if "firefox" in driver.capabilities["browserName"].lower():
            logging.debug("Opening '%s' menu under Firefox", section)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(menu)
            action_chains.send_keys(Keys.ENTER)
            action_chains.perform()
        else:
            menu.send_keys(Keys.ENTER)
    menu_item = find_element(driver, by_css=item_selector)
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
        if "firefox" in driver.capabilities["browserName"].lower():
            logging.debug("Opening '%s' menu under Firefox", group)
            action_chains = ActionChains(driver)
            action_chains.move_to_element(menu)
            action_chains.send_keys(Keys.ENTER)
            action_chains.perform()
        else:
            menu.send_keys(Keys.ENTER)
    menu_item_selector = SECTIONS[group.lower()][element.lower()]
    menu_item = find_element(driver, by_css=menu_item_selector)
    wait_for_visibility(driver, by_css=menu_item_selector)
    with assertion_msg("%s menu item: '%s' is not visible", group, element):
        assert menu_item.is_displayed()
    menu_item.click()
    take_screenshot(
        driver, NAME + " after clicking on: {} link".format(element))


def go_to_registration(driver: webdriver):
    registration_link = find_element(driver, by_css=REGISTRATION_LINK)
    registration_link.click()


def go_to_sign_in(driver: webdriver):
    registration_link = find_element(driver, by_css=SIGN_IN_LINK)
    registration_link.click()
