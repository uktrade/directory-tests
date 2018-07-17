# -*- coding: utf-8 -*-
"""SSO Sign In Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Log in"
SERVICE = "Single sign-on"
TYPE = "log in"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/login/")
PAGE_TITLE = "Sign in - great.gov.uk"

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
SELECTORS = {}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


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
    with wait_for_page_load_after_action(driver):
        sign_up_button.click()
    take_screenshot(driver, NAME + "after signing in")
