# -*- coding: utf-8 -*-
"""Domestic Home Page Object."""
import logging
import random
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_section,
    check_for_sections,
    check_if_element_is_not_present,
    check_if_element_is_visible,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)
from pages.domestic import actions as domestic_actions

NAME = "Home"
SERVICE = Service.DOMESTIC
TYPE = "home"
URL = URLs.DOMESTIC_LANDING_UK.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

PROMO_VIDEO = Selector(
    By.CSS_SELECTOR, "body > div.video-container.Modal-Container.open > div > video"
)
CLOSE_VIDEO = Selector(
    By.CSS_SELECTOR, "body > div.video-container.Modal-Container.open > button"
)
VIDEO_MODAL_WINDOW = Selector(
    By.CSS_SELECTOR, "body > div.video-container.Modal-Container.open"
)
CASE_STUDY_LINK = Selector(
    By.CSS_SELECTOR, "section.casestudy-section > div > div > div:nth-child({}) a"
)
ARTICLES = Selector(By.CSS_SELECTOR, "#eu-exit-news-section .article a")
ADVICE_ARTICLE_LINKS = Selector(By.CSS_SELECTOR, "#resource-advice a")
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero-campaign-section"),
        "title": Selector(By.ID, "hero-campaign-section-title"),
        "description": Selector(By.CSS_SELECTOR, "#hero-campaign-section p"),
        "become an export advocate": Selector(
            By.CSS_SELECTOR, "#hero-campaign-section a", type=ElementType.LINK
        ),
        "watch video": Selector(By.ID, "hero-campaign-section-watch-video-button"),
    },
    "eu exit enquiries banner": {
        "itself": Selector(By.CSS_SELECTOR, ".eu-exit-banner"),
        "guidance on how to prepare for eu exit": Selector(
            By.CSS_SELECTOR, ".eu-exit-banner a:nth-child(1)", type=ElementType.LINK
        ),
        "eu exit enquiry form": Selector(
            By.CSS_SELECTOR, ".eu-exit-banner a:nth-child(2)", type=ElementType.LINK
        ),
    },
    "export community": {
        "itself": Selector(By.ID, "community"),
        "heading": Selector(By.ID, "export-community-title"),
        "description": Selector(By.ID, "export-community-description"),
        "become an export advocate": Selector(By.ID, "export-community-link"),
    },
    "advice": {
        "itself": Selector(By.ID, "resource-advice"),
        "title": Selector(By.ID, "advice-section-title"),
        "description": Selector(By.ID, "advice-section-description"),
        "groups": Selector(By.CSS_SELECTOR, "#resource-advice .card"),
        "cards": Selector(
            By.CSS_SELECTOR, "#resource-advice .card-link", type=ElementType.LINK
        ),
        "create an export plan": Selector(By.LINK_TEXT, "Create an export plan"),
        "find an export market": Selector(By.LINK_TEXT, "Find an export market"),
        "define route to market": Selector(By.LINK_TEXT, "Define route to market"),
        "get export finance and funding": Selector(
            By.LINK_TEXT, "Get export finance and funding"
        ),
        "manage payment for export orders": Selector(
            By.LINK_TEXT, "Manage payment for export orders"
        ),
        "prepare to do business in a foreign country": Selector(
            By.LINK_TEXT, "Prepare to do business in a foreign country"
        ),
        "manage legal and ethical compliance": Selector(
            By.LINK_TEXT, "Manage legal and ethical compliance"
        ),
        "prepare for export procedures and logistics": Selector(
            By.LINK_TEXT, "Prepare for export procedures and logistics"
        ),
    },
    "services": {
        "itself": Selector(By.ID, "services"),
        "title": Selector(By.ID, "services-section-title"),
        "description": Selector(By.ID, "services-section-description"),
        "fab": Selector(By.ID, "services-section-find-a-buyer"),
        "soo": Selector(By.ID, "services-section-selling-online-overseas"),
        "exops": Selector(By.ID, "services-section-export-opportunities"),
        "find a buyer": (Selector(By.CSS_SELECTOR, "#services-section-find-a-buyer a")),
        "selling online overseas": (
            Selector(By.CSS_SELECTOR, "#services-section-selling-online-overseas a")
        ),
        "export opportunities": (
            Selector(By.CSS_SELECTOR, "#services-section-export-opportunities a")
        ),
    },
    "case studies": {
        "itself": Selector(By.CSS_SELECTOR, "section.casestudy-section"),
        "title": Selector(By.ID, "case-studies-section-title"),
        "description": Selector(By.ID, "case-studies-section-description"),
    },
    "business is great": {
        "itself": Selector(By.ID, "beis"),
        "title": Selector(By.ID, "business-is-great-title"),
        # "image": Selector(By.ID, "business-is-great-image"),
        "description": Selector(By.ID, "business-is-great-description"),
        "link": Selector(By.ID, "business-is-great-link"),
    },
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_section(driver: WebDriver, name: str):
    check_for_section(driver, all_sections=SELECTORS, sought_section=name)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_link_to(driver: WebDriver, section: str, item_name: str):
    item_selector = SELECTORS[section.lower()][item_name.lower()]
    menu_item = find_element(driver, item_selector, element_name=item_name)
    with assertion_msg(
        "It looks like '%s' in '%s' section is not visible", item_name, section
    ):
        assert menu_item.is_displayed()


def open_case_study(driver: WebDriver, case_number: str):
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    case_study_number = case_study_numbers[case_number.lower()]

    selector = Selector(
        CASE_STUDY_LINK.by, CASE_STUDY_LINK.value.format(case_study_number)
    )
    case_study_link = find_element(driver, selector)
    with wait_for_page_load_after_action(driver):
        case_study_link.click()


def get_case_study_title(driver: WebDriver, case_number: str) -> str:
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    case_number = case_study_numbers[case_number.lower()]
    selector = Selector(CASE_STUDY_LINK.by, CASE_STUDY_LINK.value.format(case_number))
    case_study_link = find_element(driver, selector, wait_for_it=False)
    return case_study_link.text.strip()


def open(driver: WebDriver, group: str, element: str):
    selector = SELECTORS[group.lower()][element.lower()]
    link = find_element(driver, selector, element_name=element, wait_for_it=True)
    check_if_element_is_visible(link, element_name=element)
    link.click()
    take_screenshot(driver, NAME + " after clicking on: %s link".format(element))


def play_video(driver: WebDriver, *, play_time: int = 5):
    open(driver, group="hero", element="watch video")
    video_load_delay = 2
    play_js = 'document.querySelector("{}").play()'.format(PROMO_VIDEO.value)
    pause = 'document.querySelector("{}").pause()'.format(PROMO_VIDEO.value)
    driver.execute_script(play_js)
    if play_time:
        time.sleep(play_time + video_load_delay)
        driver.execute_script(pause)


def get_video_watch_time(driver: WebDriver) -> int:
    watch_time_js = 'return document.querySelector("{}").currentTime'.format(
        PROMO_VIDEO.value
    )
    duration_js = 'return document.querySelector("{}").duration'.format(
        PROMO_VIDEO.value
    )
    watch_time = driver.execute_script(watch_time_js)
    duration = driver.execute_script(duration_js)
    logging.debug("Video watch time: %d", watch_time)
    logging.debug("Video duration : %d", duration)
    return int(watch_time)


def close_video(driver: WebDriver):
    take_screenshot(driver, NAME + " before closing video modal window")
    close_button = find_element(driver, CLOSE_VIDEO)
    close_button.click()


def should_not_see_video_modal_window(driver: WebDriver):
    time.sleep(1)
    check_if_element_is_not_present(driver, VIDEO_MODAL_WINDOW)


def open_news_article(driver: WebDriver, article_number: int):
    article_links = find_elements(driver, ARTICLES)
    assert len(article_links) >= article_number
    article_links[article_number - 1].click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def open_any_article(driver: WebDriver) -> str:
    article_links = find_elements(driver, ADVICE_ARTICLE_LINKS)
    link = random.choice(article_links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text


def search(driver: WebDriver, phrase: str):
    domestic_actions.search(driver, phrase)
