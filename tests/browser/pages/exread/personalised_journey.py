# -*- coding: utf-8 -*-
"""ExRed Personalised Journey - Page Object."""
import logging
from typing import List
from urllib.parse import urljoin

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    AssertionExecutor,
    Selector,
    assertion_msg,
    check_for_sections,
    check_if_element_is_not_visible,
    check_url,
    find_element,
    find_elements,
    take_screenshot,
    wait_for_page_load_after_action,
)
from registry.articles import get_articles
from settings import EXRED_UI_URL

NAME = "Personalised Journey"
SERVICE = "Export Readiness"
TYPE = "custom"
URL = urljoin(EXRED_UI_URL, "custom/")
PAGE_TITLE = "Your export journey - great.gov.uk"

READ_COUNTER = Selector(
    By.CSS_SELECTOR, "#articles .scope-indicator .position > span.from"
)
TOTAL_ARTICLES = Selector(
    By.CSS_SELECTOR, "#articles .scope-indicator .position > span.to"
)

UPDATE_PREFERENCE_LINK = Selector(By.CSS_SELECTOR, "#content a.preferences")
SECTOR_NAME = Selector(By.CSS_SELECTOR, "#largest-importers > p.commodity-name")
MARKET_RESEARCH_LINK = Selector(
    By.CSS_SELECTOR, "#resource-advice a[href='/market-research/']"
)
CUSTOMER_INSIGHT_LINK = Selector(
    By.CSS_SELECTOR, "#resource-advice a[href='/customer-insight/']"
)
FINANCE_LINK = Selector(By.CSS_SELECTOR, "#resource-advice a[href='/finance/']")
BUSINESS_LINK = Selector(
    By.CSS_SELECTOR, "#resource-advice a[href='/business-planning/']"
)
GETTING_PAID_LINK = Selector(
    By.CSS_SELECTOR, "#resource-advice a[href='/getting-paid/']"
)
OPERATIONS_AND_COMPLIANCE_LINK = Selector(
    By.CSS_SELECTOR, "#resource-advice a[href='/operations-and-compliance/']"
)
TOP_IMPORTER = Selector(By.ID, "top_importer_name")
TOP_IMPORTERS = Selector(
    By.CSS_SELECTOR, "#content > section.top-markets > div > ol > li > dl"
)
TRADE_VALUE = Selector(By.ID, "top_importer_global_trade_value")
TOP_10_TRADE_VALUE = Selector(By.CSS_SELECTOR, ".cell-global_trade_value")
REGISTER = Selector(By.CSS_SELECTOR, "section.intro-section a.link:nth-child(1)")
SIGN_IN = Selector(By.CSS_SELECTOR, "section.intro-section a.link:nth-child(2)")
SELECTORS = {
    "hero": {
        "title": Selector(By.CSS_SELECTOR, "section.hero-section h1"),
        "update preferences link": Selector(
            By.CSS_SELECTOR, "section.intro-section a.preferences"
        ),
    },
    "facts": {
        "intro": Selector(By.CSS_SELECTOR, "#content > section.sector-fact p.intro"),
        "figures": Selector(By.CSS_SELECTOR, "#content > section.sector-fact p.figure"),
    },
    "articles": {
        "heading": Selector(By.CSS_SELECTOR, "#persona-overview h2"),
        "introduction": Selector(By.CSS_SELECTOR, "#persona-overview p.intro"),
        "article list": Selector(
            By.CSS_SELECTOR, "#persona-overview div.section-content-list"
        ),
    },
    "top 10": {
        "heading": Selector(By.CSS_SELECTOR, "section.top-markets h2"),
        "intro": Selector(By.CSS_SELECTOR, "section.top-markets .intro"),
        "table": Selector(By.CSS_SELECTOR, "ol.top-markets-list"),
        "source data": Selector(
            By.CSS_SELECTOR, "section.top-markets #market-source-data"
        ),
    },
    "services": {
        "heading": Selector(By.CSS_SELECTOR, "section.service-section h2"),
        "intro": Selector(By.CSS_SELECTOR, "section.service-section .intro"),
        "other": Selector(By.CSS_SELECTOR, "#other-services > div > div"),
    },
    "fab section": {
        "heading": Selector(By.CSS_SELECTOR, "section.service-section.fas h2"),
        "fas image": Selector(By.CSS_SELECTOR, "section.service-section.fas img"),
        "intro": Selector(By.CSS_SELECTOR, "section.service-section.fas .intro"),
        "create a business profile": Selector(
            By.CSS_SELECTOR, "section.service-section.fas .intro .button"
        ),
    },
    "exopps tile": {
        "heading": Selector(
            By.CSS_SELECTOR,
            "#other-services  > div > div >  div:nth-child(2) div.card-inner > h3"
        ),
        "soo image": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(2) > div > a > div.card-image"
        ),
        "intro": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(2) > div > a > div.card-inner > p"),
        "find marketplaces link": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(2) > div > a"
        ),
    },
    "exopps section": {
        "heading": Selector(By.CSS_SELECTOR, "section.service-section.soo h2"),
        "exopps image": Selector(By.CSS_SELECTOR, "section.service-section.soo img"),
        "intro": Selector(By.CSS_SELECTOR, "section.service-section.soo .intro"),
        "find marketplaces button": Selector(
            By.CSS_SELECTOR, "section.service-section.soo .intro .button"
        ),
    },
    "soo section": {
        "heading": Selector(By.CSS_SELECTOR, "section.service-section.soo h2"),
        "soo image": Selector(By.CSS_SELECTOR, "section.service-section.soo img"),
        "intro": Selector(By.CSS_SELECTOR, "section.service-section.soo .intro"),
        "find marketplaces button": Selector(
            By.CSS_SELECTOR, "section.service-section.soo .intro .button"
        ),
    },
    "soo tile": {
        "heading": Selector(
            By.CSS_SELECTOR,
            "#other-services  > div > div >  div:nth-child(1) div.card-inner > h3"
        ),
        "soo image": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(1) > div > a > div.card-image"
        ),
        "intro": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(1) > div > a > div.card-inner > p"),
        "find marketplaces link": Selector(
            By.CSS_SELECTOR,
            "#other-services > div > div > div:nth-child(1) > div > a"
        ),
    },
    "article list": {
        "itself": Selector(By.ID, "articles"),
        "heading": Selector(By.CSS_SELECTOR, "#articles h2"),
        "introduction": Selector(By.CSS_SELECTOR, "#articles div.section-intro p"),
        "article list": Selector(By.CSS_SELECTOR, "#articles .section-content-list"),
    },
    "advice": {
        "itself": Selector(By.ID, "resource-advice"),
        "advice - title": Selector(By.ID, "advice-section-title"),
        "advice - description": Selector(By.ID, "advice-section-description"),
        "advice - categories": Selector(By.CSS_SELECTOR, "#resource-advice .group"),
        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    },
    "save progress": {"register link": REGISTER, "sign-in link": SIGN_IN},
    "case studies": {
        "heading": Selector(By.ID, "case-studies-section-title"),
        "intro": Selector(By.ID, "case-studies-section-description"),
        "article": Selector(By.CSS_SELECTOR, "#carousel .ed-carousel-container"),
        "previous article": Selector(
            By.CSS_SELECTOR, "#carousel label.ed-carousel__control--backward"
        ),
        "next article": Selector(
            By.CSS_SELECTOR, "#carousel label.ed-carousel__control--forward"
        ),
        "case study head link": Selector(
            By.CSS_SELECTOR, ".ed-carousel__track > div:nth-child(1) h3 a"
        ),
        "case study intro": Selector(
            By.CSS_SELECTOR, ".ed-carousel__track > div:nth-child(1) p"
        ),
        "case study intro link": Selector(
            By.CSS_SELECTOR, ".ed-carousel__track > div:nth-child(1) div > a"
        ),
        "carousel indicator #1": Selector(
            By.CSS_SELECTOR, "#carousel .ed-carousel__indicator[for='1']"
        ),
        "carousel indicator #2": Selector(
            By.CSS_SELECTOR, "#carousel .ed-carousel__indicator[for='2']"
        ),
        "carousel indicator #3": Selector(
            By.CSS_SELECTOR, "#carousel .ed-carousel__indicator[for='3']"
        ),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_read_counter(
    driver: WebDriver, *, exporter_status: str = None, expected_number_articles: int = 0
):
    counter = find_element(driver, READ_COUNTER, element_name="Article Read Counter")
    if "firefox" not in driver.capabilities["browserName"].lower():
        logging.debug("Moving focus to 'Read Counter' on %s", NAME)
        action_chains = ActionChains(driver)
        action_chains.move_to_element(counter)
        action_chains.perform()
    with assertion_msg(
        "Advice Article Read Counter is not visible on '%s' page", NAME
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
    driver: WebDriver, *, exporter_status: str = None
):
    counter = find_element(
        driver, TOTAL_ARTICLES, element_name="Total Articles to Read"
    )
    with assertion_msg(
        "Advice Article Read Counter is not visible on '%s' page", NAME
    ):
        assert counter.is_displayed()
    if exporter_status:
        expected_number_articles = len(
            get_articles(group="personalised journey", category=exporter_status.lower())
        )
        given_number_articles = int(counter.text)
        with assertion_msg(
            "Expected the Article Read Counter to be: %d but got %d",
            expected_number_articles,
            given_number_articles,
        ):
            assert given_number_articles == expected_number_articles


def open(driver: WebDriver, group: str, element: str):
    link = SELECTORS[group.lower()][element.lower()]
    button = find_element(driver, link, element_name=element, wait_for_it=False)
    assert button.is_displayed()
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after clicking on: %s link".format(element))


def should_see_section(driver: WebDriver, name: str):
    check_for_sections(driver, SELECTORS, sought_sections=[name])


def should_see_sections(executor: AssertionExecutor, names: List[str]):
    check_for_sections(executor, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = SELECTORS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def check_top_facts_values(driver: WebDriver):
    top_importer = find_element(driver, TOP_IMPORTER).text
    top_trade_value = find_element(driver, TRADE_VALUE).text
    top_importers_list = find_elements(driver, TOP_IMPORTERS)

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


def check_facts_and_top_10(driver: WebDriver, sector_code: str):
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
    driver: WebDriver, incorporated: bool, *, sector_code: str = None
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
    driver: WebDriver,
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
    driver: WebDriver, incorporated: bool, *, sector_code: str = None
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
    should_see_section(driver, "advice")


def should_not_see_banner_and_top_10_table(driver: WebDriver):
    should_not_see_section(driver, "facts")
    should_not_see_section(driver, "top 10")


def should_see_top_10_importers_in_sector(driver: WebDriver, sector: str):
    visible_sector_name = find_element(driver, SECTOR_NAME).text
    with assertion_msg(
        "Expected to see Top 10 Importers table for '%s' sector but got it"
        " for '%s' sector",
        sector,
        visible_sector_name,
    ):
        assert visible_sector_name == sector


def should_see_banner_and_top_10_table(driver: WebDriver, sector: str):
    should_see_section(driver, "facts")
    should_see_section(driver, "top 10")
    should_see_top_10_importers_in_sector(driver, sector)


def update_preferences(driver: WebDriver):
    update_preferences_link = find_element(driver, UPDATE_PREFERENCE_LINK)
    with assertion_msg("Update preferences link is not displayed"):
        assert update_preferences_link.is_displayed()
    with wait_for_page_load_after_action(driver):
        update_preferences_link.click()
    take_screenshot(driver, NAME + " after deciding to update preferences")
