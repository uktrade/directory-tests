# -*- coding: utf-8 -*-
"""Domestic - First page of Long Contact us form"""
from types import ModuleType
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_url,
    fill_out_textarea_fields,
    go_to_url,
    submit_form,
    take_screenshot,
)
from pages.domestic import contact_us_long_export_advice_personal

NAME = "Long (Export Advice Comment)"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTACT_US
URL = URLs.CONTACT_US_EXPORT_ADVICE_COMMENT.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#lede form"),
        "comment": Selector(By.ID, "id_comment-comment", type=ElementType.TEXTAREA),
        "submit": Selector(
            By.CSS_SELECTOR,
            "div.exred-triage-form button",
            type=ElementType.SUBMIT,
            next_page=contact_us_long_export_advice_personal,
        ),
    }
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {"comment": f"Submitted by automated tests {actor.alias}"}
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_textarea_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
