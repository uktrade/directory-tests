# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging

from selenium import webdriver
from selenium.webdriver import ActionChains

from utils import get_absolute_url, take_screenshot, assertion_msg

NAME = "ExRed Home"
URL = get_absolute_url(NAME)

GET_STARTED_BUTTON = ".triage a.button-cta"
NEW_TO_EXPORTING_LINK = "#personas > .container > .group div:nth-child(1) a"
OCCASIONAL_EXPORTER_LINK = "#personas > .container > .group div:nth-child(2) a"
REGULAR_EXPORTED_LINK = "#personas > .container > .group div:nth-child(3) a"
FIND_A_BUYER_SERVICE_LINK = "#services div:nth-child(1) > article > a"
ONLINE_MARKETPLACES_SERVICE_LINK = "#services div:nth-child(2) > article > a"
EXPORT_OPPORTUNITIES_SERVICE_LINK = "#services div:nth-child(3) > article > a"
CAROUSEL_PREVIOUS_BUTTON = "#carousel label.ed-carousel__control--backward"
CAROUSEL_NEXT_BUTTON = "#carousel label.ed-carousel__control--forward"
SECTION_VIDEO = {
    "itself": "#content > section.hero-section",
    "teaser": "#content > section.hero-section div.hero-teaser",
    "teaser_title": "#content > section.hero-section div.hero-teaser h1.title",
    "teaser_logo": "#content > section.hero-section div.hero-teaser img",
}
SECTION_EXPORTING_JOURNEY = {
    "itself": "#content > section.triage.triage-section",
    "heading": "#content > section.triage.triage-section .heading",
    "introduction": "#content > section.triage.triage-section .intro",
    "get_started_button": GET_STARTED_BUTTON,
    "image": "#content > section.triage.triage-section .container > img"
}
SECTION_PERSONAS = {
    "itself": "#personas",
    "header": "#personas > .container > .header",
    "intro": "#personas > .container > .intro",
    "groups": "#personas > .container > .group",
    "new_to_exporting_link": NEW_TO_EXPORTING_LINK,
    "occasional_exporter_link": OCCASIONAL_EXPORTER_LINK,
    "regular_exported_link": REGULAR_EXPORTED_LINK,
}
SECTION_GUIDANCE = {
    "itself": "#resource-guidance",
    "header": "#resource-guidance > .container .section-header",
    "intro": "#resource-guidance > .container .section-intro",
    "groups": "#resource-guidance > .container .group",
    "market_research_group": "#resource-guidance .group .market-research",
    "customer_insight_group": "#resource-guidance .group .customer-insight",
    "finance_group": "#resource-guidance .group .finance",
    "business_planning_group": "#resource-guidance .group .business-planning",
    "getting_paid_group": "#resource-guidance .group .getting-paid",
    "operations_and_compliance_group":
        "#resource-guidance .group .operations-and-compliance",
}
SECTION_SERVICES = {
    "itself": "#services",
    "intro": "#services .intro",
    "groups": "#services .group",
    "find_a_buyer_service": "#services div:nth-child(1) > article",
    "online_marketplaces_service": "#services div:nth-child(2) > article",
    "export_opportunities_service": "#services div:nth-child(3) > article",
    "find_a_buyer_service_link": FIND_A_BUYER_SERVICE_LINK,
    "online_marketplaces_service_link": ONLINE_MARKETPLACES_SERVICE_LINK,
    "export_opportunities_service_link": EXPORT_OPPORTUNITIES_SERVICE_LINK,
}
SECTION_CASE_STUDIES = {
    "itself": "#carousel",
    "heading": "#carousel .heading",
    "intro": "#carousel .intro",
    "carousel_previous_button": CAROUSEL_PREVIOUS_BUTTON,
    "carousel_next_button": CAROUSEL_NEXT_BUTTON
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
    sections = {
        "video": SECTION_VIDEO,
        "exporting_journey": SECTION_EXPORTING_JOURNEY,
        "personas": SECTION_PERSONAS,
        "guidance": SECTION_GUIDANCE,
        "services": SECTION_SERVICES,
        "case_studies": SECTION_CASE_STUDIES
    }
    browser = "%s v:%s %s" % (driver.capabilities.get("browserName",
                                                      "unknown browse"),
                              driver.capabilities.get("version",
                                                      "unknown version"),
                              driver.capabilities.get("platform",
                                                      "unknown platform"))
    for section_name in section_names:
        section = sections[section_name.lower().replace(" ", "_")]
        for element_name, element_selector in section.items():
            logging.debug(
                "Looking for '%s' element in '%s' section with '%s' selector",
                element_name, section_name, element_selector)
            element = driver.find_element_by_css_selector(element_selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible (%s)",
                    element_name, section_name, browser):
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
