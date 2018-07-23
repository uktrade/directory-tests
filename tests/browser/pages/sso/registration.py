# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_title,
    check_url,
    find_element,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import DIRECTORY_UI_SSO_URL

NAME = "Registration"
SERVICE = "Single Sign-On"
TYPE = "registration"
URL = urljoin(DIRECTORY_UI_SSO_URL, "accounts/signup/")
PAGE_TITLE = "Register - great.gov.uk"

EMAIL_INPUT = Selector(By.ID, "id_email")
EMAIL_CONFIRMATION_INPUT = Selector(By.ID, "id_email2")
PASSWORD_INPUT = Selector(By.ID, "id_password1")
PASSWORD_CONFIRMATION_INPUT = Selector(By.ID, "id_password2")
T_AND_C_BUTTON = Selector(By.ID, "id_terms_agreed-label")
SIGN_UP_BUTTON = Selector(By.CSS_SELECTOR, "#signup_form > button")
SELECTORS = {
    "general": {
        "title": Selector(By.CSS_SELECTOR, "#profile-register-intro > h1"),
        "email input": EMAIL_INPUT,
        "email confirmation input": EMAIL_CONFIRMATION_INPUT,
        "password input": PASSWORD_INPUT,
        "password confirmation input": PASSWORD_CONFIRMATION_INPUT,
        "sign up button": SIGN_UP_BUTTON,
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_expected_sections_elements(driver, SELECTORS)


def fill_out(driver: WebDriver, email: str, password: str):
    email_input = find_element(driver, EMAIL_INPUT)
    email_confirmation_input = find_element(driver, EMAIL_CONFIRMATION_INPUT)
    password_input = find_element(driver, PASSWORD_INPUT)
    password_confirmation_input = find_element(driver, PASSWORD_CONFIRMATION_INPUT)
    t_and_c = find_element(driver, T_AND_C_BUTTON, wait_for_it=False)
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


def submit(driver: WebDriver):
    sign_up_button = find_element(driver, SIGN_UP_BUTTON)
    with wait_for_page_load_after_action(driver):
        sign_up_button.click()
