# -*- coding: utf-8 -*-
"""Invest in Great - HPO Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    assertion_msg,
    AssertionExecutor,
    check_for_sections,
    check_if_element_is_not_visible,
    check_title,
    check_url,
    Executor,
    find_and_click_on_page_element,
    Selector,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "HPO"
NAMES = [
    "High productivity food production",
    "Lightweight structures",
    "Rail infrastructure",
]
SERVICE = "invest"
TYPE = "HPO"
URL = urljoin(INVEST_UI_URL, "high-potential-opportunities/")
BASE_URL = urljoin(INVEST_UI_URL, "high-potential-opportunities/")
PAGE_TITLE = "high potential"


URLs = {
    "high productivity food production": urljoin(BASE_URL, "food-production/"),
    "lightweight structures": urljoin(BASE_URL, "lightweight-structures/"),
    "rail infrastructure": urljoin(BASE_URL, "rail-infrastructure/"),
}


SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(By.CSS_SELECTOR, "#invest-header > div.header-bar a"),
        "home": Selector(By.CSS_SELECTOR, "#invest-header a[href='/'] img"),
        "contact us": Selector(
            By.CSS_SELECTOR, "#invest-header a[href='/contact/']"
        ),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {
        "self": Selector(By.ID, "hero"),
        "heading": Selector(By.CSS_SELECTOR, "#hero h1"),
    },
    "contact us": {
        "self": Selector(By.ID, "contact-section"),
        "heading": Selector(By.CSS_SELECTOR, "#contact-section h3"),
        "get in touch": Selector(By.CSS_SELECTOR, "#contact-section a"),
    },
    "proposition one": {
        "self": Selector(By.ID, "proposition-one"),
        "heading": Selector(By.CSS_SELECTOR, "#proposition-one h2"),
        # "image": Selector(By.CSS_SELECTOR, "#proposition-one img"),
    },
    "opportunity list": {"self": Selector(By.ID, "opportunity-list")},
    "proposition two": {
        "self": Selector(By.ID, "proposition-two"),
        "heading": Selector(
            By.CSS_SELECTOR, "#proposition-two div:nth-child(1) h2"
        ),
        # "image": Selector(By.CSS_SELECTOR, "#proposition-two div:nth-child(1) img"),
        "list of propositions": Selector(
            By.CSS_SELECTOR, "#proposition-two ul"
        ),
    },
    "competitive advantages": {
        "self": Selector(By.ID, "competitive-advantages"),
        "first - icon": Selector(
            By.CSS_SELECTOR, "#competitive-advantages div:nth-child(1) > img"
        ),
        "first - heading": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(1) > div > h3",
        ),
        "first - list": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(1) > div > ul",
        ),
        "second - icon": Selector(
            By.CSS_SELECTOR, "#competitive-advantages div:nth-child(1) > img"
        ),
        "second - heading": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(2) > div > h3",
        ),
        "second - list": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(2) > div > ul",
        ),
        "third - icon": Selector(
            By.CSS_SELECTOR, "#competitive-advantages div:nth-child(1) > img"
        ),
        "third - heading": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(3) > div > h3",
        ),
        "third - list": Selector(
            By.CSS_SELECTOR,
            "#competitive-advantages div:nth-child(3) > div > ul",
        ),
    },
    "testimonial": {
        "self": Selector(By.ID, "testimonial"),
        # "heading": Selector(By.CSS_SELECTOR, "#testimonial h2"),
        "quote": Selector(By.CSS_SELECTOR, "#testimonial p"),
    },
    "company list": {
        "self": Selector(By.ID, "company-list"),
        "heading": Selector(By.CSS_SELECTOR, "#company-list p"),
        "list": Selector(By.CSS_SELECTOR, "#company-list ul"),
        "images": Selector(By.CSS_SELECTOR, "#company-list ul img"),
    },
    "case studies": {
        "self": Selector(By.ID, "case-studies"),
        "heading": Selector(By.CSS_SELECTOR, "#case-studies h2"),
        "first": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(1)"
        ),
        "first - heading": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(1) h3"
        ),
        "first - text": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(1) p"
        ),
        "second": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(2)"
        ),
        "second - heading": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(2) h3"
        ),
        "second - text": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(2) p"
        ),
        "third": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(3)"
        ),
        "third - heading": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(3) h3"
        ),
        "third - text": Selector(
            By.CSS_SELECTOR, "#case-studies ul > li:nth-child(3) p"
        ),
    },
    "other opportunities": {
        "self": Selector(By.ID, "other-opportunities"),
        "first opportunity": Selector(
            By.CSS_SELECTOR, "#other-opportunities div:nth-child(1) > div > a"
        ),
        "second opportunity": Selector(
            By.CSS_SELECTOR, "#other-opportunities div:nth-child(2) > div > a"
        ),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
    "footer": {
        "self": Selector(By.ID, "invest-footer"),
        "uk gov logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(1)",
        ),
        "invest logo": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-branding > img:nth-child(2)",
        ),
    },
}


UNEXPECTED_ELEMENTS = {
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs")}
}


def visit(
    executor: Executor, *, first_time: bool = False, page_name: str = None
):
    key = page_name.split(" - ")[1].lower()
    url = URLs[key]
    visit_url(executor, url)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=False)
    check_url(executor, URL, exact_match=False)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def should_see_content_for(driver: WebDriver, hpo_name: str):
    source = driver.page_source
    hpo_name = clean_name(hpo_name)
    logging.debug("Looking for: {}".format(hpo_name))
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        hpo_name,
        driver.current_url,
    ):
        assert hpo_name.lower() in source.lower()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_ELEMENTS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(
            driver, selector, element_name=key, wait_for_it=False
        )
