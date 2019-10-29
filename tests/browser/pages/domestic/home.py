# -*- coding: utf-8 -*-
"""Domestic Home Page Object."""
import logging
import random
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    assertion_msg,
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
TYPE = PageType.HOME
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
ARTICLES = Selector(By.CSS_SELECTOR, "#eu-exit-news-section .article a")
ADVICE_ARTICLE_LINKS = Selector(By.CSS_SELECTOR, "#resource-advice a")
SELECTORS = {
    "prepare your business for brexit": {
        "prepare for brexit banner": Selector(
            By.CSS_SELECTOR, "section.prepare-for-brexit-section"
        ),
        "prepare your business for brexit": Selector(
            By.CSS_SELECTOR,
            "section.prepare-for-brexit-section a.chevron-banner__link",
            type=ElementType.LINK,
        ),
        "brexit related links to gov.uk": Selector(
            By.CSS_SELECTOR,
            "section.prepare-for-brexit-section a.card-link",
            type=ElementType.LINK,
        ),
    },
    "how dit helps": {
        "how dit helps section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(3)"
        ),
        "how dit helps links": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(3) a"
        ),
        "how dit helps link images": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(3) a img"
        ),
    },
    "find new markets": {
        "find new markets section": Selector(
            By.CSS_SELECTOR, "section.sector-potential-section"
        ),
        "select your sector": Selector(By.ID, "id_sector", type=ElementType.SELECT),
        "show markets": Selector(By.ID, "sector-submit", type=ElementType.SUBMIT),
        "sector selector quick links": Selector(
            By.CSS_SELECTOR,
            "section.sector-potential-section div.sector-selector-quick-links ul li a",
        ),
        "view all market guides": Selector(
            By.CSS_SELECTOR, "section.sector-potential-section a.view-markets"
        ),
    },
    "export goods from the uk": {
        "export goods from the uk section": Selector(
            By.CSS_SELECTOR, "section.export-goods-from-uk"
        ),
        "find out more": Selector(By.CSS_SELECTOR, "section.export-goods-from-uk a"),
    },
    "what's new": {
        "what's new section": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(6)"
        ),
        "what's new section heading": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(6) h2"
        ),
        "what's new image heading": Selector(
            By.CSS_SELECTOR, "#content section:nth-child(6) h3.campaign-heading"
        ),
        "watch video": Selector(
            By.ID, "hero-campaign-section-watch-video-button", type=ElementType.LINK
        ),
        "card links": Selector(
            By.CSS_SELECTOR,
            "#content section:nth-child(6) a.card-link",
            type=ElementType.LINK,
        ),
    },
}
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.DOMESTIC_HERO_WITH_LINK)
SELECTORS.update(common_selectors.SSO_LOGGED_OUT)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_link_to(driver: WebDriver, section: str, item_name: str):
    item_selector = SELECTORS[section.lower()][item_name.lower()]
    menu_item = find_element(driver, item_selector, element_name=item_name)
    with assertion_msg(
        "It looks like '%s' in '%s' section is not visible", item_name, section
    ):
        assert menu_item.is_displayed()


def open(driver: WebDriver, group: str, element: str):
    selector = SELECTORS[group.lower()][element.lower()]
    link = find_element(driver, selector, element_name=element, wait_for_it=True)
    check_if_element_is_visible(link, element_name=element)
    link.click()
    take_screenshot(driver, NAME + " after clicking on: %s link".format(element))


def play_video(driver: WebDriver, *, play_time: int = 5):
    open(driver, group="what's new", element="watch video")
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
