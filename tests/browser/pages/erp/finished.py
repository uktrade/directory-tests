# -*- coding: utf-8 -*-
"""ERP - Finished"""
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import extract_by_css
from pages import common_selectors
from pages.common_actions import Selector, check_for_sections, check_url, find_element

NAME = "Finished"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_FINISHED.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_FINISHED.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_FINISHED.absolute,
    f"{NAME} (UK consumer)": URLs.ERP_CONSUMER_FINISHED.absolute,
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())

SELECTORS = {
    "form submitted": {
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "print a copy now": Selector(By.PARTIAL_LINK_TEXT, "print a copy now"),
        "submit another form": Selector(By.PARTIAL_LINK_TEXT, "Submit another form"),
        "return to gov.uk": Selector(By.PARTIAL_LINK_TEXT, "Return to Gov.uk"),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_FOOTER)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_be_able_to_print(driver: WebDriver):
    print_link_selector = Selector(By.PARTIAL_LINK_TEXT, "print a copy now")
    print_link = find_element(driver, print_link_selector)
    onclick = print_link.get_attribute("onclick")
    error = f"Expected 'window.print()' got '{onclick}' on {driver.current_url}"
    assert onclick == "window.print()", error

    print_only_selector = "div.print-only *::text"
    raw_to_print = extract_by_css(driver.page_source, print_only_selector, first=False)
    clean_to_print = [
        text
        for text in raw_to_print
        if "\n" not in text and "Change" not in text and "answer" not in text
    ]
    to_print = "\n".join(clean_to_print)
    error = (
        f"Could not find expected values in content to print: {to_print} on "
        f"{driver.current_url}"
    )
    assert "Feedback form details" in to_print, error
