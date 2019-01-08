# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging
import random
import time
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    assertion_msg,
    check_for_section,
    check_for_sections,
    check_if_element_is_not_present,
    check_if_element_is_visible,
    check_url,
    find_and_click_on_page_element,
    find_element,
    find_elements,
    get_selectors,
    go_to_url,
    Selector,
    take_screenshot,
    wait_for_page_load_after_action,
)
from settings import EXRED_UI_URL

NAME = "Home"
SERVICE = "Export Readiness"
TYPE = "home"
URL = urljoin(EXRED_UI_URL, "?lang=en-gb")
PAGE_TITLE = "Welcome to great.gov.uk"

PROMO_VIDEO = Selector(
    By.CSS_SELECTOR, "body > div.video-container.Modal-Container.open > div > video"
)
CLOSE_VIDEO = Selector(By.ID, "hero-campaign-section-videoplayer-close")
VIDEO_MODAL_WINDOW = Selector(
    By.CSS_SELECTOR, "body > div.video-container.Modal-Container.open"
)
GET_STARTED_BUTTON = Selector(By.ID, "triage-section-get-started")
CONTINUE_EXPORT_JOURNEY = Selector(By.ID, "triage-section-continue-your-journey")
NEW_TO_EXPORTING_LINK = Selector(By.ID, "personas-section-new")
OCCASIONAL_EXPORTER_LINK = Selector(By.ID, "personas-section-occasional")
REGULAR_EXPORTED_LINK = Selector(By.ID, "personas-section-regular")
FIND_A_BUYER_SERVICE_LINK = Selector(By.CSS_SELECTOR, "#services-section-find-a-buyer a")
SELLING_ONLINE_OVERSEAS_SERVICE_LINK = Selector(
    By.CSS_SELECTOR, "#services-section-selling-online-overseas a"
)
EXPORT_OPPORTUNITIES_SERVICE_LINK = Selector(
    By.CSS_SELECTOR, "#services-section-export-opportunities a"
)
CAROUSEL_INDICATORS_SECTION = Selector(
    By.CSS_SELECTOR, "#carousel  div.ed-carousel__indicators"
)
CAROUSEL_INDICATORS = Selector(By.CSS_SELECTOR, ".ed-carousel__indicator")
CAROUSEL_PREV_BUTTON = Selector(
    By.CSS_SELECTOR, "#carousel label.ed-carousel__control--backward"
)
CAROUSEL_NEXT_BUTTON = Selector(
    By.CSS_SELECTOR, "#carousel label.ed-carousel__control--forward"
)
CAROUSEL_FIRST_INDICATOR = Selector(By.CSS_SELECTOR, ".ed-carousel__indicator[for='1']")
CAROUSEL_SECOND_INDICATOR = Selector(
    By.CSS_SELECTOR, ".ed-carousel__indicator[for='2']"
)
CAROUSEL_THIRD_INDICATOR = Selector(By.CSS_SELECTOR, ".ed-carousel__indicator[for='3']")
CASE_STUDIES_LINK = Selector(By.CSS_SELECTOR, "#carousel h3 > a")
CASE_STUDY_LINK = Selector(
    By.CSS_SELECTOR, "#carousel div.ed-carousel__slide:nth-child({}) h3 > a"
)
CAROUSEL = {
    "itself": Selector(By.ID, "carousel"),
    "title": Selector(By.ID, "case-studies-section-title"),
    "description": Selector(By.ID, "case-studies-section-description"),
    "carousel_previous_button": CAROUSEL_PREV_BUTTON,
    "carousel_next_button": CAROUSEL_NEXT_BUTTON,
    "carousel - indicator 1": Selector(By.ID, "case-studies-section-indicator-1"),
    "carousel - indicator 2": Selector(By.ID, "case-studies-section-indicator-2"),
    "carousel - indicator 3": Selector(By.ID, "case-studies-section-indicator-3"),
    "carousel - case study 1 - link": Selector(
        By.ID, "case-studies-section-case-study-1-link"
    ),
    "carousel - case study 2 - link": Selector(
        By.ID, "case-studies-section-case-study-2-link"
    ),
    "carousel - case study 3 - link": Selector(
        By.ID, "case-studies-section-case-study-3-link"
    ),
    "carousel - case study 1 - image": Selector(
        By.ID, "case-studies-section-case-study-1-image"
    ),
    "carousel - case study 2 - image": Selector(
        By.ID, "case-studies-section-case-study-2-image"
    ),
    "carousel - case study 3 - image": Selector(
        By.ID, "case-studies-section-case-study-3-image"
    ),
}
HEADER_ADVICE_LINKS = Selector(By.ID, "header-advice-links")
ARTICLES = Selector(By.CSS_SELECTOR, "#eu-exit-news-section .article a")
SELECTORS = {
    "header - advice": {
        "links": Selector(By.CSS_SELECTOR, "#advice-links-list a", type=ElementType.LINK),
    },
    "footer - advice": {
        "links": Selector(By.CSS_SELECTOR, "#footer-advice-links ~ ul a", type=ElementType.LINK),
    },
    "beta bar": {
        "itself": Selector(By.ID, "header-beta-bar"),
        "badge": Selector(By.CSS_SELECTOR, "#header-beta-bar .phase-tag"),
        "message": Selector(By.CSS_SELECTOR, "#header-beta-bar span"),
        "link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "hero": {
        "itself": Selector(By.ID, "hero-campaign-section"),
        "title": Selector(By.ID, "hero-campaign-section-title"),
        "description": Selector(By.ID, "hero-campaign-section-description"),
        "logo": Selector(By.ID, "hero-campaign-section-eig-logo"),
        "watch video": Selector(By.ID, "hero-campaign-section-watch-video-button"),
    },
    "exporting journey": {
        "itself": Selector(By.CSS_SELECTOR, "section.triage"),
        "heading": Selector(By.ID, "triage-section-title"),
        "introduction": Selector(By.ID, "triage-section-description"),
        "get_started_button": GET_STARTED_BUTTON,
        "image": Selector(By.ID, "triage-section-image"),
    },
    "news": {
        "itself": Selector(By.ID, "eu-exit-news-section"),
        "description": Selector(By.CSS_SELECTOR, "#eu-exit-news-section h2 ~ p"),
        "articles": ARTICLES,
        "see all news": Selector(By.ID, "see-all-eu-exit-news"),
    },
    "export readiness": {
        "itself": Selector(By.ID, "personas"),
        "title": Selector(By.ID, "personas-section-title"),
        "description": Selector(By.ID, "personas-section-description"),
        "groups": Selector(By.CSS_SELECTOR, "#personas a"),
        "new": NEW_TO_EXPORTING_LINK,
        "occasional": OCCASIONAL_EXPORTER_LINK,
        "regular": REGULAR_EXPORTED_LINK,
        "i'm new to exporting": NEW_TO_EXPORTING_LINK,
        "i export occasionally": OCCASIONAL_EXPORTER_LINK,
        "i'm a regular exporter": REGULAR_EXPORTED_LINK,
        "new exporter - image": Selector(By.ID, "personas-section-new-image"),
        "occasional exporter - image": Selector(
            By.ID, "personas-section-occasional-image"
        ),
        "regular exporter - image": Selector(By.ID, "personas-section-regular-image"),
    },
    "advice": {
        "itself": Selector(By.ID, "resource-advice"),
        "title": Selector(By.ID, "advice-section-title"),
        "description": Selector(By.ID, "advice-section-description"),
        "groups": Selector(By.CSS_SELECTOR, "#resource-advice .card"),
        "cards": Selector(By.CSS_SELECTOR, "#resource-advice .card-link", type=ElementType.LINK),
    },
    "services": {
        "itself": Selector(By.ID, "services"),
        "title": Selector(By.ID, "services-section-title"),
        "description": Selector(By.ID, "services-section-description"),
        "fab": Selector(By.ID, "services-section-find-a-buyer"),
        "soo": Selector(By.ID, "services-section-selling-online-overseas"),
        "exops": Selector(By.ID, "services-section-export-opportunities"),
        "find a buyer": FIND_A_BUYER_SERVICE_LINK,
        "selling online overseas": SELLING_ONLINE_OVERSEAS_SERVICE_LINK,
        "export opportunities": EXPORT_OPPORTUNITIES_SERVICE_LINK,
    },
    "case studies": {
        "itself": Selector(By.ID, "carousel"),
        "title": Selector(By.ID, "case-studies-section-title"),
        "description": Selector(By.ID, "case-studies-section-description"),
        "carousel_previous_button": CAROUSEL_PREV_BUTTON,
        "carousel_next_button": CAROUSEL_NEXT_BUTTON,
        "carousel - indicator 1": Selector(By.ID, "case-studies-section-indicator-1"),
        "carousel - indicator 2": Selector(By.ID, "case-studies-section-indicator-2"),
        "carousel - indicator 3": Selector(By.ID, "case-studies-section-indicator-3"),
        "carousel - case study 1 - link": Selector(
            By.ID, "case-studies-section-case-study-1-link"
        ),
        "carousel - case study 1 - image": Selector(
            By.ID, "case-studies-section-case-study-1-image"
        ),
    },
    "business is great": {
        "itself": Selector(By.ID, "beis"),
        "title": Selector(By.ID, "business-is-great-title"),
        # "image": Selector(By.ID, "business-is-great-image"),
        "description": Selector(By.ID, "business-is-great-description"),
        "link": Selector(By.ID, "business-is-great-link"),
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


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


def get_number_of_current_carousel_article(driver: WebDriver) -> int:
    indicators = find_elements(driver, CAROUSEL_INDICATORS)
    opacities = [
        (k, float(v.value_of_css_property("opacity"))) for k, v in enumerate(indicators)
    ]
    active_indicator = [opacity[0] for opacity in opacities if opacity[1] == 1]
    return active_indicator[0] + 1


def find_case_study_by_going_left(driver: WebDriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    prev_buttons = find_elements(driver, CAROUSEL_PREV_BUTTON)
    prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        prev_button.click()
        prev_buttons = find_elements(driver, CAROUSEL_PREV_BUTTON)
        prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver, "After moving left to find Case Study {}".format(to_open)
        )
        max_actions -= 1


def find_case_study_by_going_right(driver: WebDriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    next_buttons = find_elements(driver, CAROUSEL_NEXT_BUTTON)
    next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        next_button.click()
        next_buttons = find_elements(driver, CAROUSEL_NEXT_BUTTON)
        next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver, "After moving right to find Case Study {}".format(to_open)
        )
        max_actions -= 1


def move_to_case_study_navigation_buttons(driver: WebDriver):
    prev_button = find_element(
        driver,
        CAROUSEL_PREV_BUTTON,
        element_name="Carousel Previous button",
        wait_for_it=False,
    )
    vertical_position = prev_button.location["y"]
    logging.debug("Moving focus to Carousel navigation buttons")
    driver.execute_script("window.scrollTo(0, {});".format(vertical_position))


def open_case_study(driver: WebDriver, case_number: str):
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    case_study_number = case_study_numbers[case_number.lower()]

    move_to_case_study_navigation_buttons(driver)

    current_case_study_number = get_number_of_current_carousel_article(driver)
    if current_case_study_number != case_study_number:
        if random.choice([True, False]):
            find_case_study_by_going_left(driver, case_study_number)
        else:
            find_case_study_by_going_right(driver, case_study_number)

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


def extract_text(text: str, section_name: str) -> tuple:
    if section_name.lower() == "advice":
        advice_name_index = 1
        article_counter_index = -2
        name = text.splitlines()[advice_name_index]
        counter = int(text.split()[article_counter_index])
        return name, counter


def open_any_element_in_section(
        driver: WebDriver, element_type: str, section_name: str) -> tuple:
    section = SELECTORS[section_name.lower()]
    sought_type = ElementType[element_type.upper()]
    selectors = get_selectors(section, sought_type)
    assert selectors, f"Could't find any {element_type} in {section_name} section"
    selector_key = random.choice(list(selectors))
    selector = SELECTORS[section_name.lower()][selector_key]
    if section_name.lower().startswith("header"):
        find_element(driver, HEADER_ADVICE_LINKS).click()
    elements = find_elements(driver, selector)
    element = random.choice(elements)
    check_if_element_is_visible(element, element_name=selector_key)
    element_text = extract_text(element.text, section_name)
    with wait_for_page_load_after_action(driver):
        element.click()
    return element_text