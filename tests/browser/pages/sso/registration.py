# -*- coding: utf-8 -*-
"""SSO Registration Page Object."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import common_selectors
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
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
