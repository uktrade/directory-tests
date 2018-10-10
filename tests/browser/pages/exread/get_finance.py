# -*- coding: utf-8 -*-
"""Get Finance Page Object."""
import logging
import time
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_for_expected_sections_elements,
    check_for_sections,
    check_if_element_is_not_visible,
    check_title,
    check_url,
    go_to_url,
    take_screenshot,
    scroll_to,
    find_and_click_on_page_element,
    find_elements
)
from settings import EXRED_UI_URL

from pages import ElementType

NAME = "Get Finance"
SERVICE = "Export Readiness"
TYPE = "interim"
URL = urljoin(EXRED_UI_URL, "get-finance/")
PAGE_TITLE = "Get finance - great.gov.uk"

PROMO_VIDEO = Selector(By.CSS_SELECTOR, "section.get-finance-video video")
BREADCRUMB_LINKS = Selector(By.CSS_SELECTOR, "div.breadcrumbs a")
SELECTORS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, "div.breadcrumbs li[aria-current='page']"
        ),
        "links": BREADCRUMB_LINKS,
    },
    "hero": {
        "itself": Selector(By.CSS_SELECTOR, "section.get-finance-banner"),
        "header": Selector(By.CSS_SELECTOR, "section.get-finance-banner h1"),
    },
    "check you eligibility": {
        "itself": Selector(By.ID, "contact-section"),
        "description": Selector(By.CSS_SELECTOR, "#contact-section p"),
        "check your eligibility": Selector(By.CSS_SELECTOR, "#contact-section a", type=ElementType.LINK),
    },
    "video": {
        "itself": Selector(By.CSS_SELECTOR, "section.get-finance-video"),
        "heading": Selector(By.CSS_SELECTOR, "section.get-finance-video h2"),
        "description": Selector(By.CSS_SELECTOR, "section.get-finance-video p"),
        "read more about getting money to grow your business": Selector(By.CSS_SELECTOR, "section.get-finance-video a"),
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
        "check your eligibility": Selector(By.CSS_SELECTOR, "#contact-section-bottom a", type=ElementType.LINK),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}

UNEXPECTED_ELEMENTS = {
    "share widget": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
    },
    "article counters and indicators": {
        "itself": Selector(By.CSS_SELECTOR, "#top > div.scope-indicator"),
    },
    "tasks completed counter": {
        "itself": Selector(By.CSS_SELECTOR, ".TASKS_ARE_NOT_IMPLEMENTED_YES"),
    },
    "tasks total number": {
        "itself": Selector(By.CSS_SELECTOR, ".TASKS_ARE_NOT_IMPLEMENTED_YES"),
    },
    "total number of articles": {
        "itself": Selector(By.CSS_SELECTOR, "dd.position > span.to"),
    },
    "articles read counter": {
        "itself": Selector(By.CSS_SELECTOR, "dd.position > span.from"),
    },
    "time to complete remaining chapters": {
        "itself": Selector(By.CSS_SELECTOR, "dd.time span.value"),
    },
    "share menu": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
    }
}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=True)
    check_title(driver, PAGE_TITLE, exact_match=True)
    check_for_expected_sections_elements(driver, SELECTORS)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def check_elements_are_not_visible(driver: WebDriver, elements: list):
    take_screenshot(driver, NAME + " should not see some elements")
    for element_name in elements:
        selector = UNEXPECTED_ELEMENTS[element_name.lower()]
        check_if_element_is_not_visible(
            driver, selector, element_name=element_name, wait_for_it=False
        )


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_ELEMENTS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)


def play_video(driver: WebDriver, *, play_time: int = 5):
    video_load_delay = 2
    video = driver.find_element(by=PROMO_VIDEO.by, value=PROMO_VIDEO.value)
    scroll_to(driver, video)
    video.click()
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


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def click_breadcrumb(driver: WebDriver, name: str):
    breadcrumbs = find_elements(driver, BREADCRUMB_LINKS)
    url = driver.current_url
    link = None
    for breadcrumb in breadcrumbs:
        if breadcrumb.text.lower() == name.lower():
            link = breadcrumb
    assert link, "Couldn't find '{}' breadcrumb on {}".format(name, url)
    link.click()
    take_screenshot(driver, " after clicking on " + name + " breadcrumb")
