# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit News Article page"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Updates for UK companies on EU Exit"
SERVICE = "Export Readiness"
TYPE = "Domestic"
URL = urljoin(EXRED_UI_URL, "news/")
PAGE_TITLE = "Welcome to great.gov.uk"


BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
SELECTORS = {
    "header bar": {"itself": Selector(By.ID, "header-bar")},
    "header-menu": {
        "itself": Selector(By.ID, "header-menu"),
        "logo": Selector(By.CSS_SELECTOR, "#header-dit-logo img"),
    },
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "#content > section.hero"),
        "heading": Selector(By.ID, "hero-heading"),
        "counter": Selector(By.CSS_SELECTOR, "section.hero p"),
    },
    "news list": {
        "itself": Selector(By.ID, "news-list-page"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "news": Selector(By.CSS_SELECTOR, "#news-list-page ul li"),
        "links": Selector(By.CSS_SELECTOR, "#news-list-page ul li a"),
        "last updated dates": Selector(
            By.CSS_SELECTOR, "#news-list-page ul li p"
        ),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
