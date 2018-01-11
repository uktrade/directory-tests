# -*- coding: utf-8 -*-
"""great.gov.uk International page"""
import logging
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    find_element,
    take_screenshot
)

NAME = "International"
URL = urljoin(EXRED_UI_URL, "international/")


LANGUAGE_SELECTOR = "#header-bar .LanguageSelectorDialog-Tracker"
FIND_A_SUPPLIER = "section.international-links article:nth-child(1) > a"
SEE_THE_POTENTIAL = "section.international-links article:nth-child(2) > a"
LEARN_MORE = "section.international-links article:nth-child(3) > a"
PLAN_YOUR_TRIP = "section.international-links article:nth-child(4) > a"
BETA_FEEDBACK = "#header-beta-bar-feedback-link"
SECTIONS = {
    "header-bar": {
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
        "link": FIND_A_SUPPLIER
    },
    "invest in the uk": {
        "itself": "section.international-links article:nth-child(2)",
        "image": "section.international-links article:nth-child(2) > img",
        "title": "section.international-links article:nth-child(2) > h2",
        "text": "section.international-links article:nth-child(2) > p",
        "link": SEE_THE_POTENTIAL
    },
    "study in the uk": {
        "itself": "section.international-links article:nth-child(3)",
        "image": "section.international-links article:nth-child(3) > img",
        "title": "section.international-links article:nth-child(3) > h2",
        "text": "section.international-links article:nth-child(3) > p",
        "link": LEARN_MORE
    },
    "visit the uk": {
        "itself": "section.international-links article:nth-child(4)",
        "image": "section.international-links article:nth-child(4) > img",
        "title": "section.international-links article:nth-child(4) > h2",
        "text": "section.international-links article:nth-child(4) > p",
        "link": PLAN_YOUR_TRIP
    }
}


def visit(driver: webdriver):
    driver.get(URL)
    take_screenshot(driver, NAME)


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for section in SECTIONS:
        for element_name, element_selector in SECTIONS[section].items():
            element = find_element(
                driver, by_css=element_selector, wait_for_it=False)
            with assertion_msg(
                    "It looks like '%s' element is not visible on %s",
                    element_name, NAME):
                assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: webdriver, section_names: list):
    """Will check if Actor can see all expected page sections.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param section_names: list of page section to check
    """
    for section_name in section_names:
        section = SECTIONS[section_name.lower()]
        for element_name, element_selector in section.items():
            logging.debug(
                "Looking for '%s' element in '%s' section with '%s' selector",
                element_name, section_name, element_selector)
            element = find_element(driver, by_css=element_selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible",
                    element_name, section_name):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section_name)
    logging.debug(
        "All expected sections: %s on %s page are visible", section_names,
        NAME)


def open(driver: webdriver, group: str, element: str):
    selector = SECTIONS[group.lower()][element.lower()]
    link = driver.find_element_by_css_selector(selector)
    assert link.is_displayed()
    link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
