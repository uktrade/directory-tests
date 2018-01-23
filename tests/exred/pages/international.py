# -*- coding: utf-8 -*-
"""great.gov.uk International page"""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from pages.common_actions import (
    check_for_expected_sections_elements,
    check_for_section,
    check_url,
    go_to_url
)
from settings import EXRED_UI_URL
from utils import take_screenshot

NAME = "International"
URL = urljoin(EXRED_UI_URL, "international/")


LANGUAGE_SELECTOR = "#header-bar .LanguageSelectorDialog-Tracker"
LANGUAGE_SELECTOR_CLOSE = "#header-language-selector-close"
FIND_A_SUPPLIER = "section.international-links article:nth-child(1) > a"
SEE_THE_POTENTIAL = "section.international-links article:nth-child(2) > a"
LEARN_MORE = "section.international-links article:nth-child(3) > a"
PLAN_YOUR_TRIP = "section.international-links article:nth-child(4) > a"
BETA_FEEDBACK = "#header-beta-bar-feedback-link"
SECTIONS = {
    "header bar": {
        "itself": "#header-bar",
        "language selector": LANGUAGE_SELECTOR
    },
    "beta": {
        "itself": "#header-beta-bar",
        "sticker": "#header-beta-bar .sticker",
        "message": "#header-beta-bar p.beta-message",
        "link": BETA_FEEDBACK
    },
    "header-menu": {
        "itself": "#header-menu",
        "logo": "#header-logo"
    },
    "intro": {
        "itself": "#content > section.international-intro",
        "title": "#content > section.international-intro > div > h1",
        "description": "#content > section.international-intro > div > p"
    },
    "buy from the uk": {
        "itself": "section.international-links article:nth-child(1)",
        "image": "section.international-links article:nth-child(1) > img",
        "title": "section.international-links article:nth-child(1) > h2",
        "text": "section.international-links article:nth-child(1) > p",
        "find a supplier": FIND_A_SUPPLIER
    },
    "invest in the uk": {
        "itself": "section.international-links article:nth-child(2)",
        "image": "section.international-links article:nth-child(2) > img",
        "title": "section.international-links article:nth-child(2) > h2",
        "text": "section.international-links article:nth-child(2) > p",
        "invest in great": SEE_THE_POTENTIAL
    },
    "study in the uk": {
        "itself": "section.international-links article:nth-child(3)",
        "image": "section.international-links article:nth-child(3) > img",
        "title": "section.international-links article:nth-child(3) > h2",
        "text": "section.international-links article:nth-child(3) > p",
        "british council": LEARN_MORE
    },
    "visit the uk": {
        "itself": "section.international-links article:nth-child(4)",
        "image": "section.international-links article:nth-child(4) > img",
        "title": "section.international-links article:nth-child(4) > h2",
        "text": "section.international-links article:nth-child(4) > p",
        "visit britain": PLAN_YOUR_TRIP
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    check_for_expected_sections_elements(driver, SECTIONS)


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def open(
        driver: webdriver, group: str, element: str, *, same_tab: bool = True):
    selector = SECTIONS[group.lower()][element.lower()]
    link = driver.find_element_by_css_selector(selector)
    assert link.is_displayed()
    if same_tab:
        href = link.get_attribute("href")
        logging.debug("Opening '%s' link '%s' in the same tab", element, href)
        driver.get(href)
    else:
        link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
