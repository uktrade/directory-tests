# -*- coding: utf-8 -*-
"""ExRed Header Page Object."""
import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_hash_of_remote_file,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIT_FAVICON_MD5_CHECKSUM, DIT_LOGO_MD5_CHECKSUM

NAME = "Header"
SERVICE = "Export Readiness"
TYPE = "header"
URL = None


FAVICON = Selector(By.CSS_SELECTOR, "link[rel='shortcut icon']")
EXOPPS_FAVICON = Selector(By.CSS_SELECTOR, "link[rel='icon']")
LOGO = Selector(By.CSS_SELECTOR, "#header-dit-logo > img")
HOME_LINK = Selector(By.ID, "header-home-link")
YOUR_EXPORT_JOURNEY = Selector(By.ID, "header-custom-page-link")
REGISTRATION_LINK = Selector(By.ID, "header-register-link")
SIGN_IN_LINK = Selector(By.ID, "header-sign-in-link")
PROFILE_LINK = Selector(By.ID, "header-profile-link")
SIGN_OUT_LINK = Selector(By.ID, "header-sign-out-link")
LANGUAGE_SELECTOR = Selector(
    By.CSS_SELECTOR, "#header-bar .LanguageSelectorDialog-Tracker"
)
SELECTORS = {
    "export readiness": {
        "menu": Selector(By.ID, "export-readiness-links"),
        "new": Selector(By.ID, "header-export-readiness-new"),
        "occasional": Selector(By.ID, "header-export-readiness-occasional"),
        "regular": Selector(By.ID, "header-export-readiness-regular"),
        "i'm new to exporting": Selector(By.ID, "header-export-readiness-new"),
        "i export occasionally": Selector(By.ID, "header-export-readiness-occasional"),
        "i'm a regular exporter": Selector(By.ID, "header-export-readiness-regular"),
    },
    "advice": {
        "menu": Selector(By.ID, "header-advice-links"),
        "create an export plan":
            Selector(By.ID, "footer-advice-make-an-export-plan"),
        "find an export market":
            Selector(By.ID, "footer-advice-how-to-find-an-export-market"),
        "define route to market":
            Selector(By.ID, "footer-advice-how-to-enter-an-export-market"),
        "get export finance and funding":
            Selector(By.ID, "footer-advice-managing-finance"),
        "manage payment for export orders":
            Selector(By.ID, "footer-advice-managing-finance"),
        "prepare to do business in a foreign country":
            Selector(By.ID, "footer-advice-doing-business-overseas"),
        "manage legal and ethical compliance":
            Selector(By.ID, "footer-advice-legal-and-compliance"),
        "prepare for export procedures and logistics":
            Selector(By.ID, "footer-advice-legal-and-compliance"),
    },
    "services": {
        "menu": Selector(By.ID, "header-services-links"),
        "find a buyer": Selector(By.ID, "header-services-find-a-buyer"),
        "selling online overseas": Selector(By.ID, "header-services-selling-online-overseas"),
        "export opportunities": Selector(By.ID, "header-services-export-opportunities"),
        "get finance": Selector(By.ID, "header-services-get-finance"),
        "events": Selector(By.ID, "header-services-events"),
    },
    "general": {
        "logo": LOGO,
        "home": HOME_LINK,
        "your export journey": YOUR_EXPORT_JOURNEY,
    },
    "account links": {"register": REGISTRATION_LINK, "sign in": SIGN_IN_LINK},
}


def should_see_all_links(driver: WebDriver):
    for section in SELECTORS:
        for element_name, element_selector in SELECTORS[section].items():
            logging.debug(
                "Looking for '%s' element in '%s' section with '%s' selector",
                element_name,
                section,
                element_selector,
            )
            element = find_element(driver, element_selector)
            with assertion_msg(
                "It looks like '%s' in '%s' section is not visible",
                element_name,
                section,
            ):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section)
    logging.debug("All expected sections on %s are visible", NAME)


def should_see_link_to(driver: WebDriver, section: str, item_name: str):
    item_selector = SELECTORS[section.lower()][item_name.lower()]
    if section.lower() in ["export readiness", "advice", "services"]:
        logging.debug("Open the menu by sending 'Right Arrow' key")
        menu_selector = SELECTORS[section.lower()]["menu"]
        menu = find_element(driver, menu_selector)
        menu.send_keys(Keys.ENTER)
    menu_item = find_element(driver, item_selector)
    with assertion_msg(
        "It looks like '%s' in '%s' section is not visible", item_name, section
    ):
        assert menu_item.is_displayed()


def open(driver: WebDriver, group: str, element: str):
    """Open specific element that belongs to the group.

    NOTE:
    Some browsers (Firefox & IE) can cause problems when dealing with JS menus.
    In order to move the cursor to the correct menu element before clicking on
    it, the driver needs to be instructed to move the cursor to a visible menu
    element that is not diagonally positioned in respect to the main menu.
    It's because "moving" the cursor diagonally can cause driver to "lose"
    the focus of the menu and which will make menu to fold.
    """
    if "menu" in SELECTORS[group.lower()]:
        # Open the menu by sending "Enter" key
        menu_selector = SELECTORS[group.lower()]["menu"]
        menu = find_element(
            driver,
            menu_selector,
            element_name="Header menu {}".format(group),
            wait_for_it=False,
        )
        menu.send_keys(Keys.ENTER)
    menu_item_selector = SELECTORS[group.lower()][element.lower()]
    menu_item = find_element(driver, menu_item_selector)
    with assertion_msg("%s menu item: '%s' is not visible", group, element):
        assert menu_item.is_displayed()
    if menu_item.get_attribute("target") == "_blank":
        with wait_for_page_load_after_action(driver):
            href = menu_item.get_attribute("href")
            driver.get(href)
    else:
        with wait_for_page_load_after_action(driver):
            menu_item.click()
    take_screenshot(driver, NAME + " after clicking on: {} link".format(element))


def go_to_registration(driver: WebDriver):
    registration_link = find_element(driver, REGISTRATION_LINK, wait_for_it=False)
    with wait_for_page_load_after_action(driver):
        registration_link.click()


def go_to_sign_in(driver: WebDriver):
    sign_in = find_element(driver, SIGN_IN_LINK)
    with wait_for_page_load_after_action(driver):
        sign_in.click()


def go_to_profile(driver: WebDriver):
    profile_link = find_element(driver, PROFILE_LINK)
    with wait_for_page_load_after_action(driver):
        profile_link.click()


def go_to_sign_out(driver: WebDriver):
    sign_out_link = find_element(driver, SIGN_OUT_LINK)
    with wait_for_page_load_after_action(driver):
        sign_out_link.click()


def check_dit_logo(driver: WebDriver):
    old = "#header-bar > div:nth-child(2) > a > img"
    try:
        logo = find_element(driver, LOGO)
    except NoSuchElementException:
        try:
            logo = find_element(driver, old)
        except NoSuchElementException:
            raise
    src = logo.get_attribute("src")
    check_hash_of_remote_file(DIT_LOGO_MD5_CHECKSUM, src)
    logging.debug("%s has correct MD5sum %s", src, DIT_LOGO_MD5_CHECKSUM)


def check_dit_favicon(driver: WebDriver):
    try:
        favicon = find_element(
            driver, FAVICON, element_name="Favicon", wait_for_it=False
        )
    except NoSuchElementException:
        try:
            favicon = find_element(
                driver, EXOPPS_FAVICON, element_name="Favicon", wait_for_it=False
            )
        except NoSuchElementException:
            raise
    src = favicon.get_attribute("href")
    check_hash_of_remote_file(DIT_FAVICON_MD5_CHECKSUM, src)
    logging.debug("Favicon %s has correct MD5sum %s", src, DIT_FAVICON_MD5_CHECKSUM)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
