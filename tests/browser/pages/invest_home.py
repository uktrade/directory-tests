# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils import assertion_msg, find_element, take_screenshot

from pages import (
    AssertionExecutor,
    Executor,
    Selector,
    check_for_sections,
    visit_url,
)
from pages.common_actions import check_title, find_and_click_on_page_element
from settings import INVEST_UI_URL

URL = urljoin(INVEST_UI_URL, "")
PAGE_TITLE = "Invest in Great Britain - Home"

SECTIONS = {
    "header": {
        "self": Selector(By.ID, "invest-header"),
        "logo": Selector(
            By.CSS_SELECTOR, "#invest-header > div.header-bar  a"
        ),
    },
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {"self": Selector(By.CSS_SELECTOR, "#content > section.hero")},
    "reasons to move business to the uk": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-accordions"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions.section-underlined li:nth-child(1) > a",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions.section-underlined li:nth-child(2) > a",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-accordions.section-underlined li:nth-child(3) > a",
        ),
    },
    "sectors": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-industries"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(1) > a",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(2) > a",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(3) > a",
        ),
        "fourth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(4) > a",
        ),
        "fifth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(5) > a",
        ),
        "sixth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-industries > div > div > div:nth-child(6) > a",
        ),
        "see more industries": Selector(
            By.CSS_SELECTOR, "section.landing-page-industries > div > a"
        ),
    },
    "setup guides": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-setup-guide"),
        "first": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.grid-row > div:nth-child(1) a h3",
        ),
        "second": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.grid-row > div:nth-child(2) a h3",
        ),
        "third": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.grid-row > div:nth-child(3) a h3",
        ),
        "fourth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.grid-row > div:nth-child(4) a h3",
        ),
        "fifth": Selector(
            By.CSS_SELECTOR,
            "section.landing-page-setup-guide div.grid-row > div:nth-child(5) a h3",
        ),
    },
    "how we help": {
        "self": Selector(By.CSS_SELECTOR, "section.landing-page-how-we-help")
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

TOPIC_CONTENTS = {
    "Bring your business to the UK": Selector(
        By.CSS_SELECTOR,
        "#content > section.landing-page-accordions ul > li:nth-child(1) div.accordion-content",
    ),
    "Access a highly skilled workforce": Selector(
        By.CSS_SELECTOR,
        "#content > section.landing-page-accordions ul > li:nth-child(2) div.accordion-content",
    ),
    "Benefit from low business costs": Selector(
        By.CSS_SELECTOR,
        "#content > section.landing-page-accordions ul > li:nth-child(3) div.accordion-content",
    ),
}


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=True)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SECTIONS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def should_see_topic(driver: WebDriver, name: str):
    selector = TOPIC_CONTENTS[name]
    content = driver.find_element(by=selector.by, value=selector.value)
    with assertion_msg("Can't see contents for topic: {}".format(name)):
        assert content.is_displayed()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = industry_name.replace("Invest - ", "")
    industry_link = find_element(
        driver,
        by_partial_link_text=industry_name,
        element_name="Industry card",
        wait_for_it=False,
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SECTIONS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)


def see_more_industries(driver: WebDriver):
    click_on_page_element(driver, "see more industries")
