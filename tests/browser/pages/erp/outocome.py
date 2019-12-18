# -*- coding: utf-8 -*-
"""ERP - What outcome are you seeking for"""
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
    check_form_choices,
    check_radio,
    check_url,
    pick_one_option_and_submit,
    submit_form,
)

NAME = "What outcome are you seeking for"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_OUTCOME.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_OUTCOME.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_OUTCOME.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "i want the tariff rate to increase": Selector(
            By.ID,
            "id_outcome-tariff_rate_0",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "i want the tariff rate to decrease": Selector(
            By.ID,
            "id_outcome-tariff_rate_1",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "i want the tariff rate to neither increase or decrease": Selector(
            By.ID,
            "id_outcome-tariff_rate_2",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "i want the tariff quota to increase": Selector(
            By.ID,
            "id_outcome-tariff_quota_0",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "i want the tariff quota to decrease": Selector(
            By.ID,
            "id_outcome-tariff_quota_1",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "i want the tariff quota to neither increase or decrease": Selector(
            By.ID,
            "id_outcome-tariff_quota_2",
            type=ElementType.RADIO,
            is_visible=False,
            alternative_visibility_check=True,
        ),
        "continue": Selector(
            By.CSS_SELECTOR,
            "#content > form button.govuk-button",
            type=ElementType.SUBMIT,
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


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(
        driver, SELECTORS["form"], name, submit_button_name="continue"
    )


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    rate_increase = [False] * 3
    quota_increase = [False] * 3
    rate_increase[randrange(0, 3)] = True
    quota_increase[randrange(0, 3)] = True
    result = {
        "i want the tariff rate to increase": rate_increase[0],
        "i want the tariff rate to decrease": rate_increase[1],
        "i want the tariff rate to neither increase or decrease": rate_increase[2],
        "i want the tariff quota to increase": quota_increase[0],
        "i want the tariff quota to decrease": quota_increase[1],
        "i want the tariff quota to neither increase or decrease": quota_increase[2],
    }

    if custom_details:
        result.update(custom_details)
    return result


def fill_out(driver: WebDriver, details: dict):
    check_radio(driver, SELECTORS["form"], details)


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
