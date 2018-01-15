# -*- coding: utf-8 -*-
"""SSO Sign In Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import visit as common_visit
from settings import DIRECTORY_UI_SSO_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Sign in page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/login/")

EMAIL_INPUT = "#id_login"
PASSWORD_INPUT = "#id_password"
REMEMBER_ME_BUTTON = "#id_remember"
SIGN_IN_BUTTON = "#content > div > div > form > button"
RESET_YOUR_PASSWORD_LINK = "#content > div > div > form > a"
EXPECTED_ELEMENTS = {
    "title": "#content > div > div > h1",
    "email input": EMAIL_INPUT,
    "password input": PASSWORD_INPUT,
    "sign in button": SIGN_IN_BUTTON,
    "reset your password link": RESET_YOUR_PASSWORD_LINK,
}


def visit(driver: webdriver, *, first_time: bool = False):
    common_visit(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = find_element(driver, by_css=element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def fill_out(driver: webdriver, email: str, password: str):
    email_input = find_element(driver, by_css=EMAIL_INPUT)
    password_input = find_element(driver, by_css=PASSWORD_INPUT)
    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)
    take_screenshot(driver, NAME + "after filling out the form")


def submit(driver: webdriver):
    sign_up_button = find_element(driver, by_css=SIGN_IN_BUTTON)
    sign_up_button.click()
    take_screenshot(driver, NAME + "after signing in")
