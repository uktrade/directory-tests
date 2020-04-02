# -*- coding: utf-8 -*-
"""UKEF - Trade Finance Page Object."""
import logging
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    go_to_url,
    scroll_to,
)

NAME = "Trade Finance"
SERVICE = Service.DOMESTIC
TYPE = PageType.CONTENT
URL = URLs.DOMESTIC_TRADE_FINANCE.absolute
PAGE_TITLE = "Get finance - great.gov.uk"

PROMO_VIDEO = Selector(By.CSS_SELECTOR, "section.get-finance-video video")
BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "nav.breadcrumbs a")
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "get-finance-hero"),
        "header": Selector(By.CSS_SELECTOR, "#get-finance-hero h1"),
        "description": Selector(By.CSS_SELECTOR, "#get-finance-hero p"),
        "logo": Selector(By.CSS_SELECTOR, "#get-finance-hero img"),
    },
    "ukef breadcrumbs": {
        "great.gov.uk": Selector(
            By.CSS_SELECTOR, "nav.breadcrumbs li:nth-child(1) > a"
        ),
        "ukef": Selector(By.CSS_SELECTOR, "nav.breadcrumbs li:nth-child(2) > a"),
    },
    "tell us about your business": {
        "itself": Selector(By.ID, "contact-section"),
        "description": Selector(By.CSS_SELECTOR, "#contact-section p"),
        "tell us about your business": Selector(
            By.CSS_SELECTOR, "#contact-section a", type=ElementType.LINK
        ),
    },
    "video": {
        "itself": Selector(By.CSS_SELECTOR, "section.get-finance-video"),
        "heading": Selector(By.CSS_SELECTOR, "section.get-finance-video h2"),
        "description": Selector(By.CSS_SELECTOR, "section.get-finance-video p"),
        "read more about getting money to grow your business": Selector(
            By.CSS_SELECTOR, "section.get-finance-video a"
        ),
        "video": PROMO_VIDEO,
    },
    "advantages": {
        "itself": Selector(By.ID, "advantages-section"),
        "heading": Selector(By.CSS_SELECTOR, "#advantages-section h2"),
        "advantage heading": Selector(By.CSS_SELECTOR, "#advantages-section h3"),
        "advantage description": Selector(By.CSS_SELECTOR, "#advantages-section p"),
        "advantage image": Selector(By.CSS_SELECTOR, "#advantages-section img"),
    },
    "contact us": {
        "itself": Selector(By.ID, "contact-section-bottom"),
        "description": Selector(By.CSS_SELECTOR, "#contact-section-bottom p"),
        "check your eligibility bottom": Selector(
            By.CSS_SELECTOR, "#contact-section-bottom a", type=ElementType.LINK
        ),
    },
}
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.DOMESTIC_HEADER)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.DOMESTIC_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    check_url(driver, URL, exact_match=False)
    logging.debug(f"All expected elements are visible on '{NAME}' page")


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def play_video(driver: WebDriver, *, play_time: int = 5):
    video_load_delay = 2
    video = driver.find_element(by=PROMO_VIDEO.by, value=PROMO_VIDEO.value)
    scroll_to(driver, video)
    video.click()
    play_js = f'document.querySelector("{PROMO_VIDEO.value}").play()'
    pause = f'document.querySelector("{PROMO_VIDEO.value}").pause()'
    driver.execute_script(play_js)
    if play_time:
        time.sleep(play_time + video_load_delay)
        driver.execute_script(pause)


def get_video_watch_time(driver: WebDriver) -> int:
    watch_time_js = f'return document.querySelector("{PROMO_VIDEO.value}").currentTime'
    duration_js = f'return document.querySelector("{PROMO_VIDEO.value}").duration'
    watch_time = driver.execute_script(watch_time_js)
    duration = driver.execute_script(duration_js)
    logging.debug(f"Video watch time: {watch_time}")
    logging.debug(f"Video duration : {duration}")
    return int(watch_time)
