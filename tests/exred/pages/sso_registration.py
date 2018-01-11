# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import DIRECTORY_UI_SSO_URL
from utils import assertion_msg, find_element, take_screenshot

NAME = "SSO Registration page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/signup/")

EMAIL_INPUT = "#id_email"
EMAIL_CONFIRMATION_INPUT = "#id_email2"
PASSWORD_INPUT = "#id_password1"
PASSWORD_CONFIRMATION_INPUT = "#id_password2"
T_AND_C_BUTTON = "div.form-field > input"
SIGN_UP_BUTTON = "#signup_form > button"
EXPECTED_ELEMENTS = {
    "title": "#profile-register-intro > h1",
    "email input": EMAIL_INPUT,
    "email confirmation input": EMAIL_CONFIRMATION_INPUT,
    "password input": PASSWORD_INPUT,
    "password confirmation input": PASSWORD_CONFIRMATION_INPUT,
    "sign up button": SIGN_UP_BUTTON,
}


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
    email_confirmation_input = find_element(
        driver, by_css=EMAIL_CONFIRMATION_INPUT)
    password_input = find_element(driver, by_css=PASSWORD_INPUT)
    password_confirmation_input = find_element(
        driver, by_css=PASSWORD_CONFIRMATION_INPUT)
    t_and_c = find_element(driver, by_css=T_AND_C_BUTTON, wait_for_it=False)
    email_input.clear()
    email_input.send_keys(email)
    email_confirmation_input.clear()
    email_confirmation_input.send_keys(email)
    password_input.clear()
    password_input.send_keys(password)
    password_confirmation_input.clear()
    password_confirmation_input.send_keys(password)
    t_and_c.click()
    take_screenshot(driver, NAME + "after filling out the form")


def submit(driver: webdriver):
    sign_up_button = find_element(driver, by_css=SIGN_UP_BUTTON)
    sign_up_button.click()
