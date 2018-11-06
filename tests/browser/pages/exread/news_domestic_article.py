# -*- coding: utf-8 -*-
"""great.gov.uk Domestic EU Exit News Article page"""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    take_screenshot,
)
from settings import EXRED_UI_URL

NAME = "Domestic EU Exit news"
SERVICE = "Export Readiness"
TYPE = "article"
URL = urljoin(EXRED_UI_URL, "news/")
PAGE_TITLE = ""


BETA_FEEDBACK = Selector(By.CSS_SELECTOR, "#header-beta-bar span > a")
SUBMIT_BUTTON = Selector(By.CSS_SELECTOR, "form button")
SELECTORS = {
    "header bar": {"itself": Selector(By.ID, "header-bar")},
    "header-menu": {
        "itself": Selector(By.ID, "header-menu"),
        "logo": Selector(By.CSS_SELECTOR, "#header-dit-logo img"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
    },
    "article": {
        "itself": Selector(By.ID, "article"),
        "header": Selector(By.CSS_SELECTOR, "#article h1"),
        "lede": Selector(By.CSS_SELECTOR, "#article p.lede"),
        "back to news": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(1) a"
        ),
        "back to top": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(2) a"
        ),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
