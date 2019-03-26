# -*- coding: utf-8 -*-
"""SSO Sign In Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Sign in"
SERVICE = "Single Sign-On"
TYPE = "log in"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/login/")
PAGE_TITLE = "Sign in - great.gov.uk"

EMAIL_INPUT = Selector(By.ID, "id_login")
PASSWORD_INPUT = Selector(By.ID, "id_login")
SIGN_IN_BUTTON = Selector(By.CSS_SELECTOR, "form button")
REGISTER_BUTTON = Selector(
    By.CSS_SELECTOR,
    "#login-form-container > div:nth-child(2) > section > a",
    type=ElementType.LINK,
)
RESET_YOUR_PASSWORD_LINK = Selector(By.CSS_SELECTOR, "form > a")
SELECTORS = {
    "returning user": {
        "title": Selector(By.CSS_SELECTOR, "#content h1.heading-xlarge"),
        "email input": EMAIL_INPUT,
        "password input": PASSWORD_INPUT,
        "sign in": SIGN_IN_BUTTON,
        "forgotten password?": RESET_YOUR_PASSWORD_LINK,
    },
    "register for an account": {"register": REGISTER_BUTTON},
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def fill_out(driver: WebDriver, email: str, password: str):
    email_input = find_element(driver, EMAIL_INPUT)
    password_input = find_element(driver, PASSWORD_INPUT)
    email_input.clear()
    email_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)
    take_screenshot(driver, NAME + "after filling out the form")


def submit(driver: WebDriver):
    sign_up_button = find_element(driver, SIGN_IN_BUTTON)
    with wait_for_page_load_after_action(driver):
        sign_up_button.click()
    take_screenshot(driver, NAME + "after signing in")
