# -*- coding: utf-8 -*-
"""Invest in Great - Industries pages object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Industries"
SERVICE = "invest"
TYPE = "industries"
URL = urljoin(INVEST_UI_URL, "industries/")
PAGE_TITLE = "Invest In Great Britain - Invest in UK Industries"

SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(
            By.CSS_SELECTOR, "#invest-header > div.header-bar  a"
        ),
        "contact us": Selector(
            By.CSS_SELECTOR, "#invest-header a[href='/contact/']"
        ),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "sectors": {
        "self": Selector(By.CSS_SELECTOR, "section.industries"),
        "industry cards": Selector(
            By.CSS_SELECTOR, "section.industries a.labelled-image-card"
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


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = industry_name.split(" - ")[1]
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
