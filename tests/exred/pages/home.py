# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging
import random
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    find_element,
    find_elements,
    selenium_action,
    take_screenshot,
    wait_for_visibility
)

NAME = "ExRed Home"
URL = urljoin(EXRED_UI_URL, "?lang=en-gb")

GET_STARTED_BUTTON = ".triage a.button-cta"
CONTINUE_EXPORT_JOURNEY = "#continue-export-journey"
NEW_TO_EXPORTING_LINK = "#personas > .container > .group div:nth-child(1) a"
OCCASIONAL_EXPORTER_LINK = "#personas > .container > .group div:nth-child(2) a"
REGULAR_EXPORTED_LINK = "#personas > .container > .group div:nth-child(3) a"
FIND_A_BUYER_SERVICE_LINK = "#services div:nth-child(1) > article > a"
ONLINE_MARKETPLACES_SERVICE_LINK = "#services div:nth-child(2) > article > a"
EXPORT_OPPORTUNITIES_SERVICE_LINK = "#services div:nth-child(3) > article > a"
CAROUSEL_INDICATORS_SECTION = "#carousel  div.ed-carousel__indicators"
CAROUSEL_INDICATORS = ".ed-carousel__indicator"
CAROUSEL_PREV_BUTTON = "#carousel label.ed-carousel__control--backward"
CAROUSEL_NEXT_BUTTON = "#carousel label.ed-carousel__control--forward"
CAROUSEL_FIRST_INDICATOR = ".ed-carousel__indicator[for='1']"
CAROUSEL_SECOND_INDICATOR = ".ed-carousel__indicator[for='2']"
CAROUSEL_THIRD_INDICATOR = ".ed-carousel__indicator[for='3']"
CASE_STUDIES_LINK = "#carousel h3 > a"
CASE_STUDY_LINK = "#carousel div.ed-carousel__slide:nth-child({}) h3 > a"
MARKET_RESEARCH_LINK = "#resource-guidance a[href='/market-research/']"
CUSTOMER_INSIGHT_LINK = "#resource-guidance a[href='/customer-insight/']"
FINANCE_LINK = "#resource-guidance a[href='/finance/']"
BUSINESS_LINK = "#resource-guidance a[href='/business-planning/']"
GETTING_PAID_LINK = "#resource-guidance a[href='/getting-paid/']"
OPERATIONS_AND_COMPLIANCE_LINK = "#resource-guidance a[href='/operations-and-compliance/']"

SECTIONS = {
    "video": {
        "itself": "section.hero-campaign-section > div > div",
        "teaser_title": "section.hero-campaign-section > div > div > h1",
        "teaser description": "section.hero-campaign-section > div > div > p:nth-child(2)",
        "teaser_logo": "section.hero-campaign-section > div > div > img",
    },
    "exporting journey": {
        "itself": "#content > section.triage.triage-section",
        "heading": "#content > section.triage.triage-section .heading",
        "introduction": "#content > section.triage.triage-section .intro",
        "get_started_button": GET_STARTED_BUTTON,
        "image": "#content > section.triage.triage-section .container > img"
    },
    "export readiness": {
        "itself": "#personas",
        "header": "#personas > .container > .header",
        "intro": "#personas > .container > .intro",
        "groups": "#personas > .container > .group",
        "new": NEW_TO_EXPORTING_LINK,
        "occasional": OCCASIONAL_EXPORTER_LINK,
        "regular": REGULAR_EXPORTED_LINK,
        "i'm new to exporting": NEW_TO_EXPORTING_LINK,
        "i export occasionally": OCCASIONAL_EXPORTER_LINK,
        "i'm a regular exporter": REGULAR_EXPORTED_LINK,
    },
    "guidance": {
        "itself": "#resource-guidance",
        "header": "#resource-guidance .section-header",
        "intro": "#resource-guidance .intro",
        "groups": "#resource-guidance .group",
        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    },
    "services": {
        "itself": "#services",
        "intro": "#services .intro",
        "groups": "#services .group",
        "find_a_buyer_service": "#services div:nth-child(1) > article",
        "online_marketplaces_service": "#services div:nth-child(2) > article",
        "export_opportunities_service": "#services div:nth-child(3) > article",
        "find a buyer": FIND_A_BUYER_SERVICE_LINK,
        "selling online overseas": ONLINE_MARKETPLACES_SERVICE_LINK,
        "export opportunities": EXPORT_OPPORTUNITIES_SERVICE_LINK,
    },
    "case studies": {
        "itself": "#carousel",
        "heading": "#carousel .heading",
        "intro": "#carousel .intro",
        "carousel_previous_button": CAROUSEL_PREV_BUTTON,
        "carousel_next_button": CAROUSEL_NEXT_BUTTON
    }
}


def visit(driver: webdriver, *, first_time: bool = False):
    """Visit the Home Page.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param first_time: (optional) will delete all cookies if True
    """
    if first_time:
        logging.debug(
            "Deleting all cookies in order to enforce the first time visit"
            " simulation")
        # if driver.get_cookies():
        #     driver.delete_all_cookies()
    driver.get(URL)
    take_screenshot(driver, NAME)


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


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    with selenium_action(
            driver, "Could not find '%s' using '%s'", item_name,
            item_selector):
        menu_item = driver.find_element_by_css_selector(item_selector)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


def start_exporting_journey(driver: webdriver):
    """Start Exporting Journey (Triaging).

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    """
    button = find_element(driver, by_css=GET_STARTED_BUTTON)
    assert button.is_displayed()
    button.click()


def continue_export_journey(driver: webdriver):
    """Continue your Export Journey (Triage)."""
    button = find_element(driver, by_css=CONTINUE_EXPORT_JOURNEY)
    assert button.is_displayed()
    button.click()


def get_number_of_current_carousel_article(driver: webdriver) -> int:
    indicators = find_elements(driver, by_css=CAROUSEL_INDICATORS)
    opacities = [(k, float(v.value_of_css_property("opacity")))
                 for k, v in enumerate(indicators)]
    active_indicator = [opacity[0] for opacity in opacities if opacity[1] == 1]
    return active_indicator[0] + 1


def find_case_study_by_going_left(driver: webdriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    prev_buttons = find_elements(driver, by_css=CAROUSEL_PREV_BUTTON)
    prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        prev_button.click()
        prev_buttons = find_elements(driver, by_css=CAROUSEL_PREV_BUTTON)
        prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver,
            "After moving left to find Case Study {}".format(to_open))
        max_actions -= 1


def find_case_study_by_going_right(driver: webdriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    next_buttons = find_elements(driver, by_css=CAROUSEL_NEXT_BUTTON)
    next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        next_button.click()
        next_buttons = find_elements(driver, by_css=CAROUSEL_NEXT_BUTTON)
        next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver,
            "After moving right to find Case Study {}".format(to_open))
        max_actions -= 1


def move_to_case_study_navigation_buttons(driver: webdriver):
    prev_button = driver.find_element_by_css_selector(CAROUSEL_PREV_BUTTON)
    vertical_position = prev_button.location['y']
    logging.debug("Moving focus to Carousel navigation buttons")
    driver.execute_script("window.scrollTo(0, {});".format(vertical_position))


def open_case_study(driver: webdriver, case_number: str):
    case_study_numbers = {
        "first": 1,
        "second": 2,
        "third": 3
    }
    case_study_number = case_study_numbers[case_number.lower()]

    move_to_case_study_navigation_buttons(driver)

    current_case_study_number = get_number_of_current_carousel_article(driver)
    if current_case_study_number != case_study_number:
        if random.choice([True, False]):
            find_case_study_by_going_left(driver, case_study_number)
        else:
            find_case_study_by_going_right(driver, case_study_number)

    link_selector = CASE_STUDY_LINK.format(case_study_number)
    wait_for_visibility(driver, by_css=link_selector)
    case_study_link = find_element(driver, by_css=link_selector)
    case_study_link.click()


def get_case_study_title(driver: webdriver, case_number: str) -> str:
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    case_number = case_study_numbers[case_number.lower()]
    link_selector = CASE_STUDY_LINK.format(case_number)
    case_study_link = find_element(driver, by_css=link_selector)
    return case_study_link.text.strip()


def open(driver: webdriver, group: str, element: str):
    selector = SECTIONS[group.lower()][element.lower()]
    link = driver.find_element_by_css_selector(selector)
    assert link.is_displayed()
    link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
