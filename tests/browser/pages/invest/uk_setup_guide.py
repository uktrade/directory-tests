# -*- coding: utf-8 -*-
"""UK Setup Guide - landing page."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Executor,
    Selector,
    check_for_sections,
    check_title,
    check_url,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "UK Setup guide"
SERVICE = "invest"
TYPE = "landing"
URL = urljoin(INVEST_UI_URL, "uk-setup-guide/")
PAGE_TITLE = "Invest In Great Britain - UK Setup Guide"


SELECTORS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(By.CSS_SELECTOR, "#invest-header > div.header-bar  a"),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "introduction": {
        "self": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro"),
        "header": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro h2"),
        "paragraph": Selector(By.CSS_SELECTOR, "#content section.setup-guide .intro p"),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
    "guides": {
        "self": Selector(
            By.CSS_SELECTOR, "#content > section.setup-guide > div:nth-child(2)"
        ),
        "cards": Selector(By.CSS_SELECTOR, "#content > section.setup-guide div.card"),
        "Apply for a UK visa": Selector(
            By.CSS_SELECTOR, "div.card a[href='apply-for-a-uk-visa']"
        ),
        "Establish a base for business in the UK": Selector(
            By.CSS_SELECTOR,
            "div.card a[href='establish-a-base-for-business-in-the-uk']",
        ),
        "Hire skilled workers for your UK operations": Selector(
            By.CSS_SELECTOR,
            "div.card a[href='hire-skilled-workers-for-your-uk-operations']",
        ),
        "Open a UK business bank account": Selector(
            By.CSS_SELECTOR, "div.card a[href='open-a-uk-business-bank-account']"
        ),
        "Set up a company in the UK": Selector(
            By.CSS_SELECTOR, "div.card a[href='set-up-a-company-in-the-uk']"
        ),
        "Understand the UK's tax, incentives and legal framework": Selector(
            By.CSS_SELECTOR, "div.card a[href='understand-uk-tax-and-incentives']"
        ),
    },
    "footer": {
        "self": Selector(By.ID, "invest-footer"),
        "uk gov logo": Selector(
            By.CSS_SELECTOR, "#invest-footer div.footer-branding > img:nth-child(1)"
        ),
        "invest logo": Selector(
            By.CSS_SELECTOR, "#invest-footer div.footer-branding > img:nth-child(2)"
        ),
    },
}


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=True)
    check_url(executor, URL, exact_match=True)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = guide_name.split(" - ")[1].strip()
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
