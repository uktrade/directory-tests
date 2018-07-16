# -*- coding: utf-8 -*-
"""Invest - Page Footer."""
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import (
    check_hash_of_remote_file,
    find_element,
    scroll_to,
    take_screenshot,
)

from pages import Selector
from pages.common_actions import find_and_click_on_page_element
from settings import UK_GOV_MD5_CHECKSUM

NAME = "Footer"
URL = None
SERVICE = "Invest"
TYPE = "Footer"

UK_GOV_LOGO = Selector(By.CSS_SELECTOR, "#invest-footer img:nth-child(1)")
SELECTORS = {
    "logos": {
        "uk gov": UK_GOV_LOGO,
        "invest in great": Selector(
            By.CSS_SELECTOR, "#invest-footer img:nth-child(2)"
        ),
    },
    "links": {
        "home": Selector(By.CSS_SELECTOR, "#invest-footer a[href='/']"),
        "industries": Selector(
            By.CSS_SELECTOR, "#invest-footer a[href='/industries/']"
        ),
        "uk setup guide": Selector(
            By.CSS_SELECTOR, "#invest-footer a[href='/uk-setup-guide/']"
        ),
        "contact us": Selector(
            By.CSS_SELECTOR, "#invest-footer a[href='/contact/']"
        ),
        "part of great.gov.uk": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(1) a",
        ),
        "terms and conditions": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(2) a",
        ),
        "privacy and cookies": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(3) a",
        ),
        "department for international trade": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(4) a",
        ),
    },
}


def click_on_page_element(driver: webdriver, element: str):
    """Open specific element that belongs to the group."""
    find_and_click_on_page_element(driver, SELECTORS, element)
    take_screenshot(
        driver, NAME + " after clicking on: {} link".format(element)
    )


def check_logo(driver: webdriver):
    logo = find_element(driver, by_css=UK_GOV_LOGO)
    scroll_to(driver, logo)
    src = logo.get_attribute("src")
    check_hash_of_remote_file(UK_GOV_MD5_CHECKSUM, src)
    logging.debug("%s has correct MD5sum %s", src, UK_GOV_MD5_CHECKSUM)
