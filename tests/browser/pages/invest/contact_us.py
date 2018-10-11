# -*- coding: utf-8 -*-
"""Invest in Great - Contact us Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    AssertionExecutor,
    check_for_sections,
    check_title,
    check_url,
    Executor,
    fill_out_input_fields,
    fill_out_textarea_fields,
    find_element,
    pick_option,
    Selector,
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
        "full name": Selector(By.ID, "id_name", type=ElementType.INPUT),
        "job title": Selector(By.ID, "id_job_title", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "company name": Selector(
            By.ID, "id_company_name", type=ElementType.INPUT
        ),
        "website url": Selector(
            By.ID, "id_company_website", type=ElementType.INPUT
        ),
        "country": Selector(
            By.CSS_SELECTOR,
            "select[name='country']",
            type=ElementType.SELECT,
            is_visible=False,
        ),
        "organisation size": Selector(
            By.ID, "id_staff_number", type=ElementType.SELECT, is_visible=False
        ),
        "your plans": Selector(
            By.ID, "id_description", type=ElementType.TEXTAREA
        ),
        "captcha": Selector(
            By.CSS_SELECTOR, "#form-container iframe", type=ElementType.IFRAME
        ),
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


def generate_form_details(actor: Actor) -> dict:
    details = {
        "full name": actor.company_name or "Automated test",
        "job title": "QA @ DIT",
        "email": actor.email,
        "phone": "0123456789",
        "company name": actor.company_name or "Automated test - company name",
        "website url": "https://example.com",
        "country": None,
        "organisation size": None,
        "your plans": "This is a test message sent via automated tests",
    }
    return details


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]

    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    pick_option(driver, form_selectors, details)
    tick_captcha_checkbox(driver)

    take_screenshot(driver, "After filling out the contact us form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the contact us form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the contact us form")
