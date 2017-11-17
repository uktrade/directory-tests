# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging
from urllib.parse import urljoin

from retrying import retry
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import EXRED_UI_URL
from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Home"
URL = urljoin(EXRED_UI_URL, "")

GET_STARTED_BUTTON = ".triage a.button-cta"
NEW_TO_EXPORTING_LINK = "#personas > .container > .group div:nth-child(1) a"
OCCASIONAL_EXPORTER_LINK = "#personas > .container > .group div:nth-child(2) a"
REGULAR_EXPORTED_LINK = "#personas > .container > .group div:nth-child(3) a"
FIND_A_BUYER_SERVICE_LINK = "#services div:nth-child(1) > article > a"
ONLINE_MARKETPLACES_SERVICE_LINK = "#services div:nth-child(2) > article > a"
EXPORT_OPPORTUNITIES_SERVICE_LINK = "#services div:nth-child(3) > article > a"
CAROUSEL_PREVIOUS_BUTTON = "#carousel label.ed-carousel__control--backward"
CAROUSEL_NEXT_BUTTON = "#carousel label.ed-carousel__control--forward"
CAROUSEL_FIRST_INDICATOR = ".ed-carousel__indicator[for='1']"
CAROUSEL_SECOND_INDICATOR = ".ed-carousel__indicator[for='2']"
CAROUSEL_THIRD_INDICATOR = ".ed-carousel__indicator[for='3']"
MARKET_RESEARCH_LINK = "#resource-guidance a[href='/market-research']"
CUSTOMER_INSIGHT_LINK = "#resource-guidance a[href='/customer-insight']"
FINANCE_LINK = "#resource-guidance a[href='/finance']"
BUSINESS_LINK = "#resource-guidance a[href='/business-planning']"
GETTING_PAID_LINK = "#resource-guidance a[href='/getting-paid']"
OPERATIONS_AND_COMPLIANCE_LINK = "#resource-guidance a[href='/operations-and-compliance']"

SECTIONS = {
    "video": {
        "itself": "#content > section.hero-section",
        "teaser": "#content > section.hero-section div.hero-teaser",
        "teaser_title": "#content > section.hero-section div.hero-teaser h1.title",
        "teaser_logo": "#content > section.hero-section div.hero-teaser img",
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
        "find_a_buyer_service_link": FIND_A_BUYER_SERVICE_LINK,
        "online_marketplaces_service_link": ONLINE_MARKETPLACES_SERVICE_LINK,
        "export_opportunities_service_link": EXPORT_OPPORTUNITIES_SERVICE_LINK,
    },
    "case studies": {
        "itself": "#carousel",
        "heading": "#carousel .heading",
        "intro": "#carousel .intro",
        "carousel_previous_button": CAROUSEL_PREVIOUS_BUTTON,
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
            with selenium_action(
                    driver,
                    "Could not find '%s' in '%s' section using following "
                    "selector '%s'", element_name, section_name,
                    element_selector):
                element = driver.find_element_by_css_selector(element_selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible",
                    element_name, section_name):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section_name)
    logging.debug(
        "All expected sections: %s on %s page are visible", section_names,
        NAME)


def start_exporting_journey(driver: webdriver):
    """Start Exporting Journey (Triaging).

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    """
    button = driver.find_element_by_css_selector(GET_STARTED_BUTTON)
    assert button.is_displayed()
    button.click()


def get_number_of_current_carousel_article(driver: webdriver) -> int:
    indicators = driver.find_elements_by_css_selector(".ed-carousel__indicator")
    opacities = [(k, float(v.value_of_css_property("opacity")))
                 for k, v in enumerate(indicators)]
    active_indicator = [opacity[0] for opacity in opacities if opacity[1] == 1]
    return active_indicator[0] + 1


def open_case_study(driver: webdriver, case_number: str):
    case_study_numbers = {
        "first": 1,
        "second": 2,
        "third": 3
    }
    to_open = case_study_numbers[case_number.lower()]
    next_buttons = driver.find_elements_by_css_selector(CAROUSEL_NEXT_BUTTON)
    next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
    current = get_number_of_current_carousel_article(driver)

    if "firefox" not in driver.capabilities["browserName"].lower():
        logging.debug("Moving focus to 'Next Case Study' button")
        action_chains = ActionChains(driver)
        action_chains.move_to_element(next_button)
        action_chains.perform()

    while current != to_open:
        next_button.click()
        next_buttons = driver.find_elements_by_css_selector(CAROUSEL_NEXT_BUTTON)
        next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(driver, "Moving from Case Study {}".format(current))

    links = driver.find_elements_by_css_selector("#carousel h3 > a")
    link = [lnk for lnk in links if lnk.is_displayed()][0]
    link.click()


def open(driver: webdriver, group: str, element: str):
    selector = SECTIONS[group.lower()][element.lower()]
    link = driver.find_element_by_css_selector(selector)
    assert link.is_displayed()
    link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
