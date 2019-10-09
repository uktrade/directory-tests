# -*- coding: utf-8 -*-
"""Common Actions for Domestic Page Objects"""
import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.constants import MD5_CHECKSUM_DIT_FAVICON
from pages.common_actions import (
    check_hash_of_remote_file,
    find_element,
    find_selector_by_name,
    wait_for_page_load_after_action,
)
from pages.common_selectors import EXOPPS_FAVICON, FAVICON, HEADER, LOGOS


def search(driver: WebDriver, phrase: str):
    search_input = find_element(driver, find_selector_by_name(HEADER, "search box"))
    search_button = find_element(driver, find_selector_by_name(HEADER, "search button"))
    search_input.clear()
    search_input.send_keys(phrase)
    search_button.click()


def go_to_sign_out(driver: WebDriver):
    sign_out_link = find_element(driver, find_selector_by_name(HEADER, "sign out"))
    with wait_for_page_load_after_action(driver):
        sign_out_link.click()


def check_logo(driver: WebDriver, logo_name: str):
    logo = LOGOS[logo_name.lower()]
    logo_element = find_element(driver, logo["selector"], wait_for_it=False)
    src = logo_element.get_attribute("src")
    if not src:
        logging.debug(f"IMG SRC is empty will try to use 'data-src' for {logo}")
        src = logo_element.get_attribute("data-src")
    check_hash_of_remote_file(logo["md5"], src)
    logging.debug(f"{src} has correct MD5sum {logo['md5']}")


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
    check_hash_of_remote_file(MD5_CHECKSUM_DIT_FAVICON, src)
    logging.debug("Favicon %s has correct MD5sum %s", src, MD5_CHECKSUM_DIT_FAVICON)
