# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from enum import Enum
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
from pages.common_actions import check_title, check_url
from settings import INVEST_UI_URL

URL = urljoin(INVEST_UI_URL, "industries/")
BASE_URL = urljoin(INVEST_UI_URL, "industries/")
PAGE_TITLE = "Invest in Great Britain - "


class URLS(Enum):
    """Lists all URLs for industry pages."""

    ADVANCED_MANUFACTURING = urljoin(BASE_URL, "advanced-manufacturing/")
    AEROSPACE = urljoin(BASE_URL, "aerospace/")
    AGRI_TECH = urljoin(BASE_URL, "agri-tech/")
    ASSET_MANAGEMENT = urljoin(BASE_URL, "asset-management/")
    AUTOMOTIVE = urljoin(BASE_URL, "automotive/")
    AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT = urljoin(
        BASE_URL, "automotive-research-and-development/"
    )
    AUTOMOTIVE_SUPPLY_CHAIN = urljoin(BASE_URL, "automotive-supply-chain/")
    CAPITAL_INVESTMENT = urljoin(BASE_URL, "capital-investment/")
    CHEMICALS = urljoin(BASE_URL, "chemicals/")
    CREATIVE_CONTENT_AND_PRODUCTION = urljoin(
        BASE_URL, "creative-content-and-production/"
    )
    CREATIVE_INDUSTRIES = urljoin(BASE_URL, "creative-industries/")
    DATA_ANALYTICS = urljoin(BASE_URL, "data-analytics/")
    DIGITAL_MEDIA = urljoin(BASE_URL, "digital-media/")
    ELECTRICAL = urljoin(BASE_URL, "electrical/")
    ELECTRICAL_NETWORKS = urljoin(BASE_URL, "electrical-networks/")
    ENERGY = urljoin(BASE_URL, "energy/")
    ENERGY_FROM_WASTE = urljoin(BASE_URL, "energy-from-waste/")
    FINANCIAL_SERVICES = urljoin(BASE_URL, "financial-services/")
    FINANCIAL_TECHNOLOGY = urljoin(BASE_URL, "financial-technology/")
    FOOD_AND_DRINK = urljoin(BASE_URL, "food-and-drink/")
    FOOD_SERVICE_AND_CATERING = urljoin(BASE_URL, "food-service-and-catering/")
    FREE_FROM_FOODS = urljoin(BASE_URL, "free-from-foods/")
    HEALTH_AND_LIFE_SCIENCES = urljoin(BASE_URL, "health-and-life-sciences/")
    MEAT_POULTRY_AND_DAIRY = urljoin(BASE_URL, "meat-poultry-and-dairy/")
    MEDICAL_TECHNOLOGY = urljoin(BASE_URL, "medical-technology/")
    MOTORSPORT = urljoin(BASE_URL, "motorsport/")
    NETWORKS = urljoin(BASE_URL, "networks/")
    NUCLEAR_ENERGY = urljoin(BASE_URL, "nuclear-energy/")
    OFFSHORE_WIND_ENERGY = urljoin(BASE_URL, "offshore-wind-energy/")
    OIL_AND_GAS = urljoin(BASE_URL, "oil-and-gas/")
    PHARMACEUTICAL_MANUFACTURING = urljoin(
        BASE_URL, "pharmaceutical-manufacturing/"
    )
    RETAIL = urljoin(BASE_URL, "retail/")
    TECHNOLOGY = urljoin(BASE_URL, "technology/")


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
    "industry pullout": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-pullout"),
        "data": Selector(By.CSS_SELECTOR, "section.industry-pullout div.data"),
    },
    "industry accordions": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-page-accordions"),
        "accordion expanders": Selector(
            By.CSS_SELECTOR,
            "section.industry-page-accordions a.accordion-expander",
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

OPTIONAL_SECTIONS = {
    "related industries": {
        "self": Selector(By.CSS_SELECTOR, "section.industry-page-related"),
        "links": Selector(By.CSS_SELECTOR, "a.labelled-card"),
    }
}


def visit(
    executor: Executor, *, first_time: bool = False, page_name: str = None
):
    if page_name:
        enum_key = (
            page_name.lower()
            .replace("invest - ", "")
            .replace(" industry", "")
            .replace(" ", "_")
            .replace(",", "")
            .replace("-", "_")
            .upper()
        )
        url = URLS[enum_key].value
    else:
        url = URL
    visit_url(executor, url)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=False)
    check_url(executor, URL, exact_match=False)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SECTIONS, sought_sections=names)


def open_link(driver: WebDriver, name: str):
    driver.find_element_by_link_text(name).click()


def clean_name(name: str) -> str:
    return name.replace("Invest - ", "").replace("industry", "").strip()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    industry_link = find_element(
        driver,
        by_partial_link_text=industry_name,
        element_name="Industry card",
        wait_for_it=False,
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
