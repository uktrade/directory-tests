# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_elements,
    check_title,
    check_url,
    go_to_url
)
from settings import DIRECTORY_UI_SSO_URL
from utils import find_element, take_screenshot

NAME = "SSO Registration page"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/signup/")
PAGE_TITLE = "Register - great.gov.uk"

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


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_elements(driver, EXPECTED_ELEMENTS)


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
