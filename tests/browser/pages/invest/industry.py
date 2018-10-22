# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Executor,
    Selector,
    assertion_msg,
    check_for_sections,
    check_title,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    take_screenshot,
    visit_url,
)
from settings import INVEST_UI_URL

NAME = "Industry"
NAMES = [
    "Advanced manufacturing",
    "Aerospace",
    "Agri-tech",
    "Asset management",
    "Automotive research and development",
    "Automotive supply chain",
    "Automotive",
    "Capital Investment",
    "Chemicals",
    "Creative content and production",
    "Creative industries",
    "Data Analytics",
    "Digital media",
    "Electrical networks",
    "Energy from waste market",
    "Energy",
    "Financial services",
    "Financial technology",
    "Food and drink",
    "Free-from foods",
    "Health and life sciences",
    "Meat, poultry and dairy",
    "Medical technology",
    "Motorsport",
    "Nuclear energy",
    "Offshore wind energy",
    "Oil and gas",
    "Pharmaceutical manufacturing",
    "Retail",
    "Technology",
]
SERVICE = "invest"
TYPE = "industry"
URL = urljoin(INVEST_UI_URL, "industries/")
BASE_URL = urljoin(INVEST_UI_URL, "industries/")
PAGE_TITLE = "Invest in Great Britain - "


URLs = {
    "advanced manufacturing": urljoin(BASE_URL, "advanced-manufacturing/"),
    "aerospace": urljoin(BASE_URL, "aerospace/"),
    "agri-tech": urljoin(BASE_URL, "agri-tech/"),
    "asset management": urljoin(BASE_URL, "asset-management/"),
    "automotive": urljoin(BASE_URL, "automotive/"),
    "automotive research and development": urljoin(
        BASE_URL, "automotive-research-and-development/"
    ),
    "automotive supply chain": urljoin(BASE_URL, "automotive-supply-chain/"),
    "capital investment": urljoin(BASE_URL, "capital-investment/"),
    "chemicals": urljoin(BASE_URL, "chemicals/"),
    "creative content and production": urljoin(
        BASE_URL, "creative-content-and-production/"
    ),
    "creative industries": urljoin(BASE_URL, "creative-industries/"),
    "data analytics": urljoin(BASE_URL, "data-analytics/"),
    "digital media": urljoin(BASE_URL, "digital-media/"),
    "electrical": urljoin(BASE_URL, "electrical/"),
    "electrical networks": urljoin(BASE_URL, "electrical-networks/"),
    "energy": urljoin(BASE_URL, "energy/"),
    "energy from waste market": urljoin(BASE_URL, "energy-waste/"),
    "financial services": urljoin(BASE_URL, "financial-services/"),
    "financial technology": urljoin(BASE_URL, "financial-technology/"),
    "food and drink": urljoin(BASE_URL, "food-and-drink/"),
    "food service and catering": urljoin(
        BASE_URL, "food-service-and-catering/"
    ),
    "free-from foods": urljoin(BASE_URL, "free-foods/"),
    "health and life sciences": urljoin(BASE_URL, "health-and-life-sciences/"),
    "meat, poultry and dairy": urljoin(BASE_URL, "meat-poultry-and-dairy/"),
    "medical technology": urljoin(BASE_URL, "medical-technology/"),
    "motorsport": urljoin(BASE_URL, "motorsport/"),
    "networks": urljoin(BASE_URL, "networks/"),
    "nuclear energy": urljoin(BASE_URL, "nuclear-energy/"),
    "offshore wind energy": urljoin(BASE_URL, "offshore-wind-energy/"),
    "oil and gas": urljoin(BASE_URL, "oil-and-gas/"),
    "pharmaceutical manufacturing": urljoin(
        BASE_URL, "pharmaceutical-manufacturing/"
    ),
    "retail": urljoin(BASE_URL, "retail/"),
    "technology": urljoin(BASE_URL, "technology/"),
}


TOPIC_EXPANDERS = Selector(
    By.CSS_SELECTOR, "section.industry-page-accordions a.accordion-expander"
)

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
    "industry pullout": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-pullout")
    },
    "big number": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-pullout div.data")
    },
    "topics": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-page-accordions"),
        "accordion expanders": Selector(
            By.CSS_SELECTOR,
            "section.industry-page-accordions a.accordion-expander",
        ),
    },
    "topics contents": {
        "paragraphs": Selector(By.CSS_SELECTOR, "div.accordion-content p")
    },
    "related industries": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-page-related"),
        "industry cards": Selector(
            By.CSS_SELECTOR, "section.industry-page-related a"
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


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def should_see_content_for(driver: WebDriver, industry_name: str):
    source = driver.page_source
    industry_name = clean_name(industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    with assertion_msg(
        "Expected to find term '%s' in the source of the page %s",
        industry_name,
        driver.current_url,
    ):
        assert industry_name.lower() in source.lower()


def unfold_topics(driver: WebDriver):
    expanders = find_elements(driver, TOPIC_EXPANDERS)
    assert (
        expanders
    ), "Expected to see at least 1 topic but found 0 on {}".format(
        driver.current_url
    )
    for expander in expanders:
        expander.click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
