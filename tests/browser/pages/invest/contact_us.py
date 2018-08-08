# -*- coding: utf-8 -*-
"""Invest in Great - Contact us Page Object."""
import logging
import random
import time
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Executor,
    Selector,
    check_for_sections,
    check_title,
    check_url,
    find_element,
    take_screenshot,
    tick_captcha_checkbox,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Contact us"
SERVICE = "Invest"
TYPE = "contact"
URL = urljoin(INVEST_UI_URL, "contact/")
PAGE_TITLE = ""

IM_NOT_A_ROBOT = Selector(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "#content form button.button")
SELECTORS = {
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.hero"),
        "heading": Selector(By.CSS_SELECTOR, "section.hero h1"),
    },
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "full name": Selector(By.ID, "id_name"),
        "job title": Selector(By.ID, "id_job_title"),
        "email": Selector(By.ID, "id_email"),
        "phone": Selector(By.ID, "id_phone_number"),
        "company name": Selector(By.ID, "id_company_name"),
        "website url": Selector(By.ID, "id_company_website"),
        "country": Selector(By.CSS_SELECTOR, "select[name='country']"),
        "organisation size": Selector(By.ID, "id_staff_number"),
        "your plans": Selector(By.ID, "id_description"),
        "captcha": Selector(By.ID, "recaptcha-accessible-status"),
        "i'm not a robot": IM_NOT_A_ROBOT,
        "hint": Selector(By.CSS_SELECTOR, "#content form div.form-hint"),
        "submit": SUBMIT_BUTTON,
    },
}


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=False)
    check_url(executor, URL, exact_match=False)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def fill_out(driver: WebDriver, details: dict):
    input_fields = [
        "full name",
        "job title",
        "email",
        "phone",
        "company name",
        "website url",
        "your plans",
    ]
    dropdown_menus = ["country", "organisation size"]

    for field_name in input_fields:
        value = details[field_name]
        field = find_element(
            driver,
            SELECTORS["form"][field_name],
            element_name=field_name,
            wait_for_it=False,
        )
        field.send_keys(value)

    for menu_name in dropdown_menus:
        selector = SELECTORS["form"][menu_name]
        dropdown = find_element(
            driver,
            selector,
            element_name="{} dropdown menu".format(menu_name),
            wait_for_it=False,
        )
        if details[menu_name]:
            option = details[menu_name]
        else:
            options = dropdown.find_elements_by_css_selector("option")
            values = [option.get_property("value") for option in options]
            logging.debug("OPTIONS: {}".format(values))
            option = random.choice(values)
            logging.debug("OPTION: {}".format(option))
        if menu_name == "country":
            js_field_selector = Selector(By.ID, "js-country-select")
            js_field = find_element(driver, js_field_selector)
            js_field.click()
            js_field.clear()
            js_field.send_keys(option)
        else:
            option_value_selector = "option[value='{}']".format(option)
            option_element = dropdown.find_element_by_css_selector(
                option_value_selector
            )
            option_element.click()

    tick_captcha_checkbox(driver)

    take_screenshot(driver, "After filling out the contact us form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the contact us form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the contact us form")
