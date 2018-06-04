# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver import ActionChains

from pages.common_actions import check_for_section, check_title, check_url
from registry.articles import get_articles
from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    check_if_element_is_not_visible,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "ExRed Personalised Journey"
URL = urljoin(EXRED_UI_URL, "custom/")
PAGE_TITLE = "Your export journey - great.gov.uk"

READ_COUNTER = "#articles .scope-indicator .position > span.from"
TOTAL_ARTICLES = "#articles .scope-indicator .position > span.to"

UPDATE_PREFERENCE_LINK = "#content a.preferences"
SECTOR_NAME = "#largest-importers > p.commodity-name"
MARKET_RESEARCH_LINK = "#resource-guidance a[href='/market-research/']"
CUSTOMER_INSIGHT_LINK = "#resource-guidance a[href='/customer-insight/']"
FINANCE_LINK = "#resource-guidance a[href='/finance/']"
BUSINESS_LINK = "#resource-guidance a[href='/business-planning/']"
GETTING_PAID_LINK = "#resource-guidance a[href='/getting-paid/']"
OPERATIONS_AND_COMPLIANCE_LINK = (
    "#resource-guidance a[href='/operations-and-compliance/']"
)
TOP_IMPORTER = "#top_importer_name"
TOP_IMPORTERS = "#content > section.top-markets > div > ol > li > dl"
TRADE_VALUE = "#top_importer_global_trade_value"
TOP_10_TRADE_VALUE = ".cell-global_trade_value"
REGISTER = "section.intro-section a.link:nth-child(1)"
SIGN_IN = "section.intro-section a.link:nth-child(2)"
SECTIONS = {
    "hero": {
        "title": "section.hero-section h1",
        "update preferences link": "section.intro-section a.preferences",
    },
    "facts": {
        "intro": "#content > section.sector-fact p.intro",
        "figures": "#content > section.sector-fact p.figure",
    },
    "articles": {
        "heading": "#persona-overview h2",
        "introduction": "#persona-overview p.intro",
        "article list": "#persona-overview div.section-content-list",
    },
    "top 10": {
        "heading": "section.top-markets h2",
        "intro": "section.top-markets .intro",
        "table": "ol.top-markets-list",
        "source data": "section.top-markets #market-source-data",
    },
    "services": {
        "heading": "section.service-section h2",
        "intro": "section.service-section .intro",
        "other": "#other-services > div > div",
    },
    "fab section": {
        "heading": "section.service-section.fas h2",
        "fas image": "section.service-section.fas img",
        "intro": "section.service-section.fas .intro",
        "create a trade profile": "section.service-section.fas .intro .button",
    },
    "exopps tile": {
        "heading": "#other-services div.lg-2:nth-child(2) h3",
        "exopps image": "#other-services div.lg-2:nth-child(2) img",
        "intro": "#other-services div.lg-2:nth-child(2) p",
        "find marketplaces link": "#other-services div.lg-2:nth-child(2) a",
    },
    "exopps section": {
        "heading": "section.service-section.soo h2",
        "exopps image": "section.service-section.soo img",
        "intro": "section.service-section.soo .intro",
        "find marketplaces button": "section.service-section.soo .intro .button",
    },
    "soo section": {
        "heading": "section.service-section.soo h2",
        "soo image": "section.service-section.soo img",
        "intro": "section.service-section.soo .intro",
        "find marketplaces button": "section.service-section.soo .intro .button",
    },
    "soo tile": {
        "heading": "#other-services div.lg-2:nth-child(1) h3",
        "soo image": "#other-services div.lg-2:nth-child(1) img",
        "intro": "#other-services div.lg-2:nth-child(1) p",
        "find marketplaces link": "#other-services div.lg-2:nth-child(1) a",
    },
    "article list": {
        "itself": "#articles",
        "heading": "#articles h2",
        "introduction": "#articles div.section-intro p",
        "article list": "#articles .section-content-list",
    },
    "guidance": {
        "itself": "#resource-guidance",
        "guidance - title": "#guidance-section-title",
        "guidance - description": "#guidance-section-description",
        "guidance - categories": "#resource-guidance .group",
        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    },
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
    "case studies": {
        "heading": "#carousel h2",
        "intro": "#carousel .intro",
        "article": "#carousel .ed-carousel-container",
        "previous article": "#carousel label.ed-carousel__control--backward",
        "next article": "#carousel label.ed-carousel__control--forward",
        "case study head link": ".ed-carousel__track > div:nth-child(1) h3 a",
        "case study intro": ".ed-carousel__track > div:nth-child(1) p",
        "case study intro link": ".ed-carousel__track > div:nth-child(1) div > a",
        "carousel indicator #1": "#carousel .ed-carousel__indicator[for='1']",
        "carousel indicator #2": "#carousel .ed-carousel__indicator[for='2']",
        "carousel indicator #3": "#carousel .ed-carousel__indicator[for='3']",
    },
}


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=False)
    check_for_section(driver, SECTIONS, sought_section="hero")
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_read_counter(
    driver: webdriver,
    *,
    exporter_status: str = None,
    expected_number_articles: int = 0
):
    counter = find_element(
        driver, by_css=READ_COUNTER, element_name="Article Read Counter"
    )
    if "firefox" not in driver.capabilities["browserName"].lower():
        logging.debug("Moving focus to 'Read Counter' on %s", NAME)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(counter)
        action_chains.perform()
    with assertion_msg(
        "Guidance Article Read Counter is not visible on '%s' page", NAME
    ):
        assert counter.is_displayed()
    given_number_articles = int(counter.text)
    with assertion_msg(
        "Expected the Article Read Counter to be: %d but got %d",
        expected_number_articles,
        given_number_articles,
    ):
        assert given_number_articles == expected_number_articles


def should_see_total_articles_to_read(
    driver: webdriver, *, exporter_status: str = None
):
    counter = find_element(
        driver, by_css=TOTAL_ARTICLES, element_name="Total Articles to Read"
    )
    with assertion_msg(
        "Guidance Article Read Counter is not visible on '%s' page", NAME
    ):
        assert counter.is_displayed()
    if exporter_status:
        expected_number_articles = len(
            get_articles(
                group="personalised journey", category=exporter_status.lower()
            )
        )
        given_number_articles = int(counter.text)
        with assertion_msg(
            "Expected the Article Read Counter to be: %d but got %d",
            expected_number_articles,
            given_number_articles,
        ):
            assert given_number_articles == expected_number_articles


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = find_element(
        driver, by_css=link, element_name=element, wait_for_it=False
    )
    assert button.is_displayed()
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element)
    )


def should_see_section(driver: webdriver, name: str):
    check_for_section(driver, SECTIONS, sought_section=name)


def should_not_see_section(driver: webdriver, name: str):
    section = SECTIONS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(
            driver, by_css=selector, element_name=key
        )


def check_top_facts_values(driver: webdriver):
    top_importer = find_element(driver, by_css=TOP_IMPORTER).text
    top_trade_value = find_element(driver, by_css=TRADE_VALUE).text
    top_importers_list = find_elements(driver, by_css=TOP_IMPORTERS)

    exporting_values = {}
    for importer in top_importers_list:
        country = importer.find_element_by_css_selector("dd.country").text
        trade_value = importer.find_element_by_css_selector("dd.world").text
        exporting_values.update({country: trade_value})

    if top_importer in exporting_values:
        with assertion_msg(
            "Expected to see 'Export value from the world' for %s to "
            "be %s but got %s",
            top_importer,
            top_trade_value,
            exporting_values[top_importer],
        ):
            assert exporting_values[top_importer] == top_trade_value
    else:
        logging.debug(
            "Country mentioned in Top Facts: %s is not present in the Top 10 "
            "Importers table. Won't check the the trade value",
            top_importer,
        )


def check_facts_and_top_10(driver: webdriver, sector_code: str):
    """There are no Facts & Top 10 data for Service Sectors (start with EB)."""
    if sector_code.startswith("EB"):
        logging.debug(
            "Exported chose service sector: %s for which there are no facts "
            "and information on top 10 importers",
            sector_code,
        )
    else:
        should_see_section(driver, "facts")
        should_see_section(driver, "top 10")
        check_top_facts_values(driver)


def layout_for_new_exporter(
    driver: webdriver, incorporated: bool, *, sector_code: str = None
):
    """
    * a new exporter says his company:
    ** incorporated, then only `FAB` is displayed
    ** is not incorporated, then `no services are displayed`
    """
    should_see_section(driver, "hero")
    should_see_section(driver, "article list")
    if incorporated:
        should_see_section(driver, "fab section")
    should_see_section(driver, "case studies")


def layout_for_occasional_exporter(
    driver: webdriver,
    incorporated: bool,
    use_online_marketplaces: bool,
    *,
    sector_code: str = None
):
    """
    * an occasional exporter says his company:
    ** used online marketplaces and is incorporated,
        then `FAB & SOO` are displayed
    ** used online marketplaces but it is not incorporated,
        then only `SOO` is displayed
    ** haven't used online marketplaces but it is incorporated,
        then only `FAB` is displayed
    ** haven't used online marketplaces and it is not incorporated,
        then `no services are displayed`
    """
    should_see_section(driver, "hero")
    should_see_section(driver, "article list")
    if incorporated and use_online_marketplaces:
        should_see_section(driver, "fab section")
        should_see_section(driver, "soo section")
    if not incorporated and use_online_marketplaces:
        should_see_section(driver, "soo section")
    if not incorporated and not use_online_marketplaces:
        logging.debug("Nothing to show here")
    should_see_section(driver, "case studies")


def layout_for_regular_exporter(
    driver: webdriver, incorporated: bool, *, sector_code: str = None
):
    """
    * a regular exporter says his company is:
    ** incorporated, then `FAB, SOO & ExOpps` are displayed
    ** not incorporated, then `SOO & ExOpps` are displayed
    """
    should_see_section(driver, "hero")
    if incorporated:
        should_see_section(driver, "fab section")
    should_see_section(driver, "soo tile")
    should_see_section(driver, "exopps tile")
    should_see_section(driver, "guidance")


def should_not_see_banner_and_top_10_table(driver: webdriver):
    should_not_see_section(driver, "facts")
    should_not_see_section(driver, "top 10")


def should_see_top_10_importers_in_sector(driver: webdriver, sector: str):
    visible_sector_name = find_element(driver, by_css=SECTOR_NAME).text
    with assertion_msg(
        "Expected to see Top 10 Importers table for '%s' sector but got it"
        " for '%s' sector",
        sector,
        visible_sector_name,
    ):
        assert visible_sector_name == sector


def should_see_banner_and_top_10_table(driver: webdriver, sector: str):
    should_see_section(driver, "facts")
    should_see_section(driver, "top 10")
    should_see_top_10_importers_in_sector(driver, sector)


def update_preferences(driver: webdriver):
    update_preferences_link = find_element(
        driver, by_css=UPDATE_PREFERENCE_LINK
    )
    with assertion_msg("Update preferences link is not displayed"):
        assert update_preferences_link.is_displayed()
    with wait_for_page_load_after_action(driver):
        update_preferences_link.click()
    take_screenshot(driver, NAME + " after deciding to update preferences")
