# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from pages.common_actions import (
    assertion_msg,
    check_hash_of_remote_file,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIT_FAVICON_MD5_CHECKSUM, DIT_LOGO_MD5_CHECKSUM

NAME = "ExRed Header"
URL = None


FAVICON = "link[rel='shortcut icon']"
EXOPPS_FAVICON = "link[rel='icon']"
LOGO = "#header-dit-logo > img"
HOME_LINK = "#header-home-link"
YOUR_EXPORT_JOURNEY = "#header-custom-page-link"
REGISTRATION_LINK = "#header-register-link"
SIGN_IN_LINK = "#header-sign-in-link"
PROFILE_LINK = "#header-profile-link"
SIGN_OUT_LINK = "#header-sign-out-link"
LANGUAGE_SELECTOR = "#header-bar .LanguageSelectorDialog-Tracker"
SECTIONS = {
    "export readiness": {
        "menu": "#export-readiness-links",
        "new": "#header-export-readiness-new",
        "occasional": "#header-export-readiness-occasional",
        "regular": "#header-export-readiness-regular",
        "i'm new to exporting": "#header-export-readiness-new",
        "i export occasionally": "#header-export-readiness-occasional",
        "i'm a regular exporter": "#header-export-readiness-regular",
    },
    "guidance": {
        "menu": "#header-guidance-links",
        "market research": "#header-guidance-market-research",
        "customer insight": "#header-guidance-customer-insight",
        "finance": "#header-guidance-finance",
        "business planning": "#header-guidance-business-planning",
        "getting paid": "#header-guidance-getting-paid",
        "operations and compliance": "#header-guidance-operations-and-compliance",
    },
    "services": {
        "menu": "#header-services-links",
        "find a buyer": "#header-services-find-a-buyer",
        "selling online overseas": "#header-services-",
        "export opportunities": "#header-services-export-opportunities",
        "get finance": "#header-services-get-finance",
        "events": "#header-services-events",
    },
    "general": {
        "logo": LOGO,
        "home": HOME_LINK,
        "your export journey": YOUR_EXPORT_JOURNEY,
    },
    "account links": {"register": REGISTRATION_LINK, "sign in": SIGN_IN_LINK},
}


def should_see_all_links(driver: webdriver):
    for section in SECTIONS:
        for element_name, element_selector in SECTIONS[section].items():
            logging.debug(
                "Looking for '%s' element in '%s' section with '%s' selector",
                element_name,
                section,
                element_selector,
            )
            element = find_element(driver, by_css=element_selector)
            with assertion_msg(
                "It looks like '%s' in '%s' section is not visible",
                element_name,
                section,
            ):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section)
    logging.debug("All expected sections on %s are visible", NAME)


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    if section.lower() in ["export readiness", "guidance", "services"]:
        logging.debug("Open the menu by sending 'Right Arrow' key")
        menu_selector = SECTIONS[section.lower()]["menu"]
        menu = find_element(driver, by_css=menu_selector)
        menu.send_keys(Keys.ENTER)
    menu_item = find_element(driver, by_css=item_selector)
    with assertion_msg(
        "It looks like '%s' in '%s' section is not visible", item_name, section
    ):
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
        # Open the menu by sending "Enter" key
        menu_selector = SECTIONS[group.lower()]["menu"]
        menu = find_element(
            driver,
            by_css=menu_selector,
            element_name="Header menu {}".format(group),
            wait_for_it=False,
        )
        menu.send_keys(Keys.ENTER)
    menu_item_selector = SECTIONS[group.lower()][element.lower()]
    menu_item = find_element(driver, by_css=menu_item_selector)
    with assertion_msg("%s menu item: '%s' is not visible", group, element):
        assert menu_item.is_displayed()
    with wait_for_page_load_after_action(driver):
        menu_item.click()
    take_screenshot(driver, NAME + " after clicking on: {} link".format(element))


def go_to_registration(driver: webdriver):
    registration_link = find_element(
        driver, by_css=REGISTRATION_LINK, wait_for_it=False
    )
    with wait_for_page_load_after_action(driver):
        registration_link.click()


def go_to_sign_in(driver: webdriver):
    sign_in = find_element(driver, by_css=SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        sign_in.click()


def go_to_profile(driver: webdriver):
    profile_link = find_element(driver, by_css=PROFILE_LINK)
    with wait_for_page_load_after_action(driver):
        profile_link.click()


def go_to_sign_out(driver: webdriver):
    sign_out_link = find_element(driver, by_css=SIGN_OUT_LINK)
    with wait_for_page_load_after_action(driver):
        sign_out_link.click()


def check_dit_logo(driver: webdriver):
    old = "#header-bar > div:nth-child(2) > a > img"
    try:
        logo = find_element(driver, by_css=LOGO)
    except NoSuchElementException:
        try:
            logo = find_element(driver, by_css=old)
        except NoSuchElementException:
            raise
    src = logo.get_attribute("src")
    check_hash_of_remote_file(DIT_LOGO_MD5_CHECKSUM, src)
    logging.debug("%s has correct MD5sum %s", src, DIT_LOGO_MD5_CHECKSUM)


def check_dit_favicon(driver: webdriver):
    try:
        favicon = find_element(
            driver, by_css=FAVICON, element_name="Favicon", wait_for_it=False
        )
    except NoSuchElementException:
        try:
            favicon = find_element(
                driver, by_css=EXOPPS_FAVICON, element_name="Favicon", wait_for_it=False
            )
        except NoSuchElementException:
            raise
    src = favicon.get_attribute("href")
    check_hash_of_remote_file(DIT_FAVICON_MD5_CHECKSUM, src)
    logging.debug("Favicon %s has correct MD5sum %s", src, DIT_FAVICON_MD5_CHECKSUM)


def click_on_page_element(driver: webdriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
