# -*- coding: utf-8 -*-
"""ERP - Product detail"""
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import common_selectors
from pages.common_actions import check_for_sections, check_url

NAME = "Product detail"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_PRODUCT_DETAIL.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_PRODUCT_DETAIL.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_PRODUCT_DETAIL.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())
PAGE_TITLE = ""

SELECTORS = {}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_PRODUCT_DETAIL_FORM)
SELECTORS.update(common_selectors.ERP_SAVE_FOR_LATER)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
