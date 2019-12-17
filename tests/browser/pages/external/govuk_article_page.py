# -*- coding: utf-8 -*-
"""GOV.UK - Generic article page."""
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import check_url_path_matches_template
from pages.common_actions import go_to_url

NAME = "Brexit related article"
SERVICE = Service.GOVUK
TYPE = PageType.ARTICLE
URL = URLs.GOVUK_WILDCARD.absolute_template
SELECTORS = {}

SubURLs = {
    "How to export goods to the EU after Brexit": URL.format(
        slug="starting-to-export/within-eu"
    ),
    "How to export goods outside of the EU after Brexit": URL.format(
        slug="starting-to-export/outside-eu"
    ),
    "Providing services and travelling to EEA and EFTA countries": URL.format(
        slug="government/collections/providing-services-to-eea-and-efta-countries-after-eu-exit"
    ),
}
SubURLs = {key.lower(): val for key, val in SubURLs.items()}
NAMES = list(SubURLs.keys())


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name]
    go_to_url(driver, url, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    check_url_path_matches_template(URL, driver.current_url)
