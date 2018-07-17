# -*- coding: utf-8 -*-
"""Invest - Page Header."""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.common_actions import (
    Selector,
    check_hash_of_remote_file,
    find_and_click_on_page_element,
    find_element,
    scroll_to,
    take_screenshot,
)
from settings import UK_GOV_MD5_CHECKSUM

NAME = "Header"
URL = None
SERVICE = "Invest"
TYPE = "header"
FAVICON = Selector(By.CSS_SELECTOR, "link[rel='shortcut icon']")
HEADER_LOGO = Selector(By.CSS_SELECTOR, "#invest-header img")
FOOTER_LOGO = Selector(By.CSS_SELECTOR, "#invest-footer img:nth-child(1)")
HOME_LINK = Selector(By.CSS_SELECTOR, "#invest-header a[href='/']")
INDUSTRIES_LINK = Selector(
    By.CSS_SELECTOR, "#invest-header a[href='/industries/']"
)
UK_SETUP_GUIDE_LINK = Selector(
    By.CSS_SELECTOR, "#invest-header a[href='/uk-setup-guide/']"
)
CONTACT_US_LINK = Selector(
    By.CSS_SELECTOR, "#invest-header a[href='/contact/']"
)
LANGUAGE_SELECTOR = Selector(
    By.CSS_SELECTOR, "#language-selector-activator > a"
)
SELECTORS = {
    "general": {
        "uk gov logo": HEADER_LOGO,
        "home": HOME_LINK,
        "industries": INDUSTRIES_LINK,
        "uk setup guide": UK_SETUP_GUIDE_LINK,
        "contact us": CONTACT_US_LINK,
        "language selector": LANGUAGE_SELECTOR,
    },
    "beta bar": {
        "itself": Selector(By.ID, "#header-beta-bar"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
}


def click_on_page_element(driver: webdriver, element: str):
    """Open specific element that belongs to the group."""
    find_and_click_on_page_element(driver, SELECTORS, element)
    take_screenshot(
        driver, NAME + " after clicking on: {} link".format(element)
    )


def check_logo(driver: webdriver):
    logo = find_element(driver, by_css=HEADER_LOGO)
    scroll_to(driver, logo)
    src = logo.get_attribute("src")
    check_hash_of_remote_file(UK_GOV_MD5_CHECKSUM, src)
    logging.debug("%s has correct MD5sum %s", src, UK_GOV_MD5_CHECKSUM)
