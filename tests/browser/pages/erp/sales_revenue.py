# -*- coding: utf-8 -*-
"""ERP - Sales revenue"""
import logging
from random import randrange
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    submit_form,
)
from pages.erp import consumer_other_changes_after_brexit

NAME = "Sales revenue"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_SALES_REVENUE_BEFORE_BREXIT.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_SALES_REVENUE_BEFORE_BREXIT.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_SALES_REVENUE_BEFORE_BREXIT.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "form": {
        "selection form": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "step counter": Selector(
            By.CSS_SELECTOR, "form[method=post] span.govuk-caption-l"
        ),
        "heading": Selector(By.CSS_SELECTOR, "form[method=post] h1"),
        "q3 2019": Selector(
            By.ID,
            "id_sales-revenue-before-brexit-quarter_three_2019_sales_revenue",
            type=ElementType.INPUT,
        ),
        "q2 2019": Selector(
            By.ID,
            "id_sales-revenue-before-brexit-quarter_two_2019_sales_revenue",
            type=ElementType.INPUT,
        ),
        "q1 2019": Selector(
            By.ID,
            "id_sales-revenue-before-brexit-quarter_one_2019_sales_revenue",
            type=ElementType.INPUT,
        ),
        "q4 2018": Selector(
            By.ID,
            "id_sales-revenue-before-brexit-quarter_four_2018_sales_revenue",
            type=ElementType.INPUT,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
            next_page=consumer_other_changes_after_brexit,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    result = {
        "q3 2019": str(randrange(-1000, 1000)),
        "q2 2019": str(randrange(-1000, 1000)),
        "q1 2019": str(randrange(-1000, 1000)),
        "q4 2018": str(randrange(-1000, 1000)),
    }

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
