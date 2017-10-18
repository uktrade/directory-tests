# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging

from selenium.webdriver import ActionChains

from tests import get_absolute_url
from tests.exred.utils import take_screenshot
from settings import DRIVERS

URL = get_absolute_url("exred:home")
NAME = "ExRed Home"

GET_STARTED_BUTTON = ("#content > section.triage.triage-section .intro "
                      ".content .button-cta")
SECTION_VIDEO = {
    "itself": "#content > section.hero-section",
    "teaser": "#content > section.hero-section div.hero-teaser",
    "teaser_title": "#content > section.hero-section div.hero-teaser > .title",
    "teaser_logo": "#content > section.hero-section div.hero-teaser > img",
    "watch_video_button": "#content > section.hero-section .video-button"
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
    "new_to_exporting_link": "#personas > .container > .group a[href='/new']",
    "occasional_exporter_link":
        "#personas > .container > .group a[href='/occasional']",
    "regular_exported_link":
        "#personas > .container > .group a[href='/regular']",
}
SECTION_GUIDANCE = {
    "itself": "#resource-guidance",
    "header": "#resource-guidance > .container > .section-header",
    "intro": "#resource-guidance > .container > .section-intro",
    "groups": "#resource-guidance > .container > .group",
    "market_research_group":
        "#resource-guidance > .container > .group > div > .market-research",
    "customer_insight_group":
        "#resource-guidance > .container > .group > div > .customer-insight",
    "finance_group":
        "#resource-guidance > .container > .group > div > .finance",
    "business_planning_group":
        "#resource-guidance > .container > .group > div > .business-planning",
    "getting_paid_group":
        "#resource-guidance > .container > .group > div > .getting-paid",
    "operations_and_compliance_group":
        "#resource-guidance > .container > .group > div > "
        ".operations-and-compliance",

}
SECTION_SERVICES = {
    "itself": "#services",
    "intro": "#services > div > .intro",
    "groups": "#services > div > .group",
    "find_a_buyer_service":
        "#services .group > div:nth-child(1) > article",
    "online_marketplaces_service":
        "#services .group > div:nth-child(2) > article",
    "export_opportunities_service":
        "#services .group > div:nth-child(3) > article",
}
SECTION_CASE_STUDIES = {
    "itself": "#stories",
    "header": "#stories .header",
    "intro": "#stories .intro"
}


def visit(driver: DRIVERS, *, first_time: bool = False):
    if first_time:
        logging.debug(
            "Deleting all cookies in order to enforce the first time visit "
            "simulation")
        driver.delete_all_cookies()
    driver.get(URL)
    take_screenshot(driver, NAME)


def should_see_sections(driver: DRIVERS, section_names: list):
    sections = {
        "video": SECTION_VIDEO,
        "exporting_journey": SECTION_EXPORTING_JOURNEY,
        "personas": SECTION_PERSONAS,
        "guidance": SECTION_GUIDANCE,
        "services": SECTION_SERVICES,
        "case_studies": SECTION_CASE_STUDIES
    }
    for section_name in section_names:
        section = sections[section_name.lower().replace(" ", "_")]
        for element_name, element_selector in section.items():
            element = driver.find_element_by_css_selector(element_selector)
            assert element.is_displayed(), ("It looks like '{}' in '{}' "
                                            "section is not visible"
                                            .format(element_name,
                                                    section_name))
        logging.debug("All elements in '%s' section are visible", section_name)
    logging.debug(
        "All expected sections: %s on %s page are visible", section_names,
        NAME)


def start_exporting_journey(driver: DRIVERS):
    button = driver.find_element_by_css_selector(GET_STARTED_BUTTON)
    assert button.is_displayed()
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click(button)
    actions.perform()
