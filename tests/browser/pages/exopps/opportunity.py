# -*- coding: utf-8 -*-
"""Export Opportunities - Opportunity page"""
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages.common_actions import check_for_sections

NAME = "Opportunity"
SERVICE = Service.EXPORT_OPPORTUNITIES
TYPE = PageType.OPPORTUNITY
URL = URLs.EXOPPS_OPPORTUNITY.absolute_template
PAGE_TITLE = " - Export opportunities - great.gov.uk"


SELECTORS = {}


def should_be_here(driver: WebDriver):
    check_url_path_matches_template(URL, driver.current_url)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)
