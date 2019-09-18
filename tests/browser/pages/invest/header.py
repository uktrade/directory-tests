# -*- coding: utf-8 -*-
"""Invest - Page Header."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services, common_selectors
from pages.common_actions import (
    Selector,
    check_hash_of_remote_file,
    find_and_click_on_page_element,
    find_element,
    scroll_to,
    take_screenshot,
)
from settings import MD5_CHECKSUM_INVEST_IN_GREAT

NAME = "Header"
URL = None
SERVICE = Services.INVEST
TYPE = "header"
HEADER_LOGO = Selector(By.CSS_SELECTOR, "#great-header-logo > img")
SELECTORS = {}
SELECTORS.update(common_selectors.HEADER_INVEST)
SELECTORS.update(common_selectors.BETA_BAR)


def click_on_page_element(driver: WebDriver, element: str):
    """Open specific element that belongs to the group."""
    find_and_click_on_page_element(driver, SELECTORS, element)
    take_screenshot(driver, NAME + " after clicking on: {} link".format(element))


def check_logo(driver: WebDriver):
    logo = find_element(driver, HEADER_LOGO)
    scroll_to(driver, logo)
    src = logo.get_attribute("src")
    check_hash_of_remote_file(MD5_CHECKSUM_INVEST_IN_GREAT, src)
    logging.debug("%s has correct MD5sum %s", src, MD5_CHECKSUM_INVEST_IN_GREAT)
