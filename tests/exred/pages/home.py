# -*- coding: utf-8 -*-
"""ExRed Home Page Object."""
import logging
import random
import time
from urllib.parse import urljoin

from selenium import webdriver

from settings import EXRED_UI_URL
from utils import (
    assertion_msg,
    check_if_element_is_not_present,
    find_element,
    find_elements,
    selenium_action,
    take_screenshot
)

NAME = "ExRed Home"
URL = urljoin(EXRED_UI_URL, "?lang=en-gb")

PROMO_VIDEO = "body > div.video-container.Modal-Container.open > div > video"
CLOSE_VIDEO = "#hero-campaign-section-videoplayer-close"
VIDEO_MODAL_WINDOW = "body > div.video-container.Modal-Container.open"
GET_STARTED_BUTTON = "#triage-section-get-started"
CONTINUE_EXPORT_JOURNEY = "#triage-section-continue-your-journey"
NEW_TO_EXPORTING_LINK = "#personas-section-new"
OCCASIONAL_EXPORTER_LINK = "#personas-section-occasional"
REGULAR_EXPORTED_LINK = "#personas-section-regular"
FIND_A_BUYER_SERVICE_LINK = "#services-section-find-a-buyer-link"
SELLING_ONLINE_OVERSEAS_SERVICE_LINK = "#services-section-selling-online-overseas-link"
EXPORT_OPPORTUNITIES_SERVICE_LINK = "#services-section-export-opportunities-link"
CAROUSEL_INDICATORS_SECTION = "#carousel  div.ed-carousel__indicators"
CAROUSEL_INDICATORS = ".ed-carousel__indicator"
CAROUSEL_PREV_BUTTON = "#carousel label.ed-carousel__control--backward"
CAROUSEL_NEXT_BUTTON = "#carousel label.ed-carousel__control--forward"
CAROUSEL_FIRST_INDICATOR = ".ed-carousel__indicator[for='1']"
CAROUSEL_SECOND_INDICATOR = ".ed-carousel__indicator[for='2']"
CAROUSEL_THIRD_INDICATOR = ".ed-carousel__indicator[for='3']"
CASE_STUDIES_LINK = "#carousel h3 > a"
CASE_STUDY_LINK = "#carousel div.ed-carousel__slide:nth-child({}) h3 > a"
MARKET_RESEARCH_LINK = "#guidance-market-research-link"
CUSTOMER_INSIGHT_LINK = "#guidance-section-customer-insight-link"
FINANCE_LINK = "#guidance-section-finance-link"
BUSINESS_LINK = "#guidance-section-business-planning-link"
GETTING_PAID_LINK = "#guidance-section-getting-paid-link"
OPERATIONS_AND_COMPLIANCE_LINK = "#guidance-section-operations-and-compliance-link"
CAROUSEL = {
    "itself": "#carousel",
    "title": "#case-studies-section-title",
    "description": "#case-studies-section-description",
    "carousel_previous_button": CAROUSEL_PREV_BUTTON,
    "carousel_next_button": CAROUSEL_NEXT_BUTTON,
    "carousel - indicator 1": "#case-studies-section-indicator-1",
    "carousel - indicator 2": "#case-studies-section-indicator-2",
    "carousel - indicator 3": "#case-studies-section-indicator-3",
    "carousel - case study 1 - link": "#case-studies-section-case-study-1-link",
    "carousel - case study 2 - link": "#case-studies-section-case-study-2-link",
    "carousel - case study 3 - link": "#case-studies-section-case-study-3-link",
    "carousel - case study 1 - image": "#case-studies-section-case-study-1-image",
    "carousel - case study 2 - image": "#case-studies-section-case-study-2-image",
    "carousel - case study 3 - image": "#case-studies-section-case-study-3-image",
}

SECTIONS = {
    "beta": {
        "itself": "#header-beta-bar",
        "sticker": "#header-beta-bar .sticker",
        "message": "#header-beta-bar p.beta-message",
        "link": "#header-beta-bar-feedback-link"
    },
    "hero": {
        "itself": "#content > section.hero-campaign-section",
        "title": "#hero-campaign-section-title",
        "description": "#hero-campaign-section-description",
        "logo": "#hero-campaign-section-eig-logo",
        "watch video": "#hero-campaign-section-watch-video-button"
    },
    "exporting journey": {
        "itself": "#content > section.triage.triage-section",
        "heading": "#triage-section-title",
        "introduction": "#triage-section-description",
        "get_started_button": GET_STARTED_BUTTON,
        "image": "#triage-section-image"
    },
    "export readiness": {
        "itself": "#personas",
        "title": "#personas-section-title",
        "description": "#personas-section-description",
        "groups": "#personas > .container > .group",
        "new": NEW_TO_EXPORTING_LINK,
        "occasional": OCCASIONAL_EXPORTER_LINK,
        "regular": REGULAR_EXPORTED_LINK,
        "i'm new to exporting": NEW_TO_EXPORTING_LINK,
        "i export occasionally": OCCASIONAL_EXPORTER_LINK,
        "i'm a regular exporter": REGULAR_EXPORTED_LINK,
        "new exporter - image": "#personas-section-new-image",
        "occasional exporter - image": "#personas-section-occasional-image",
        "regular exporter - image": "#personas-section-regular-image",
    },
    "guidance": {
        "itself": "#resource-guidance",
        "title": "#guidance-section-title",
        "description": "#guidance-section-description",
        "groups": "#resource-guidance .group",
        "market research - group": "#guidance-section-market-research",
        "customer insight - group": "#guidance-section-customer-insight",
        "finance - group": "#guidance-section-finance",
        "business planning - group": "#guidance-section-business-planning",
        "getting paid - group": "#guidance-section-getting-paid",
        "operations and compliance - group": "#guidance-section-operations-and-compliance",

        "market research - icon": "#guidance-section-market-research-icon",
        "customer insight - icon": "#guidance-section-customer-insight-icon",
        "finance - icon": "#guidance-section-finance-icon",
        "business planning - icon": "#guidance-section-business-planning-icon",
        "getting paid - icon": "#guidance-section-getting-paid-icon",
        "operations and compliance - icon": "#guidance-section-operations-and-compliance-icon",

        "market research - read counter": "#guidance-section-market-research-read-counter",
        "customer insight - read counter": "#guidance-section-customer-insight-read-counter",
        "finance - read counter": "#guidance-section-finance-article-read-counter",
        "business planning - read counter": "#guidance-section-business-planning-article-read-counter",
        "getting paid - read counter": "#guidance-section-getting-paid-article-read-counter",
        "operations and compliance - read counter": "#guidance-section-operations-and-compliance-article-read-counter",

        "market research - total number of articles": "#guidance-section-market-research-total-number-of-articles",
        "customer insight - total number of articles": "#guidance-section-customer-insight-total-number-of-articles",
        "finance - total number of articles": "#guidance-section-finance-total-number-of-articles",
        "business planning - total number of articles": "#guidance-section-business-planning-total-number-of-articles",
        "getting paid - total number of articles": "#guidance-section-getting-paid-total-number-of-articles",
        "operations and compliance - total number of articles": "#guidance-section-operations-and-compliance-total-number-of-articles",

        "market research - description": "#guidance-section-market-research-description",
        "customer insight - description": "#guidance-section-customer-insight-description",
        "finance - description": "#guidance-section-finance-description",
        "business planning - description": "#guidance-section-business-planning-description",
        "getting paid - description": "#guidance-section-getting-paid-description",
        "operations and compliance - description": "#guidance-section-operations-and-compliance-description",

        "market research": MARKET_RESEARCH_LINK,
        "customer insight": CUSTOMER_INSIGHT_LINK,
        "finance": FINANCE_LINK,
        "business planning": BUSINESS_LINK,
        "getting paid": GETTING_PAID_LINK,
        "operations and compliance": OPERATIONS_AND_COMPLIANCE_LINK,
    },
    "services": {
        "itself": "#services",
        "title": "#services-section-title",
        "description": "#services-section-description",
        "groups": "#services .group",

        "find a buyer - article": "#services div:nth-child(1) > article",
        "online marketplaces - article": "#services div:nth-child(2) > article",
        "export opportunities - article": "#services div:nth-child(3) > article",

        "find a buyer - image": "#services-section-find-a-buyer-image",
        "online marketplaces - image": "#services-section-selling-online-overseas-image",
        "export opportunities - image": "#services-section-export-opportunities-image",

        "find a buyer - description": "#services-section-find-a-buyer-description",
        "online marketplaces - description": "#services-section-selling-online-overseas-description",
        "export opportunities - description": "#services-section-export-opportunities-description",

        "find a buyer": FIND_A_BUYER_SERVICE_LINK,
        "selling online overseas": SELLING_ONLINE_OVERSEAS_SERVICE_LINK,
        "export opportunities": EXPORT_OPPORTUNITIES_SERVICE_LINK,
    },
    "case studies": {
        "itself": "#carousel",
        "title": "#case-studies-section-title",
        "description": "#case-studies-section-description",
        "carousel_previous_button": CAROUSEL_PREV_BUTTON,
        "carousel_next_button": CAROUSEL_NEXT_BUTTON,
        "carousel - indicator 1": "#case-studies-section-indicator-1",
        "carousel - indicator 2": "#case-studies-section-indicator-2",
        "carousel - indicator 3": "#case-studies-section-indicator-3",
        "carousel - case study 1 - link": "#case-studies-section-case-study-1-link",
        "carousel - case study 1 - image": "#case-studies-section-case-study-1-image",
    },
    "business is great": {
        "itself": "#beis",
        "title": "#business-is-great-title",
        # "image": "#business-is-great-image",
        "description": "#business-is-great-description",
        "link": "#business-is-great-link",
    },
    "error reporting": {
        "itself": "section.error-reporting",
        "link": "#error-reporting-section-contact-us"
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


def should_be_here(driver: webdriver):
    take_screenshot(driver, NAME)
    for section in SECTIONS:
        for element_name, element_selector in SECTIONS[section].items():
            element = driver.find_element_by_css_selector(element_selector)
            with assertion_msg(
                    "It looks like '%s' element is not visible on %s",
                    element_name, NAME):
                assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_section(driver: webdriver, name: str):
    section = SECTIONS[name.lower()]
    for key, selector in section.items():
        with selenium_action(
                driver, "Could not find: '%s' element in '%s' section using "
                        "'%s' selector",
                key, name, selector):
            element = find_element(driver, by_css=selector)
        with assertion_msg(
                "'%s' in '%s' is not displayed", key, name):
            assert element.is_displayed()
            logging.debug("'%s' in '%s' is displayed", key, name)


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    with selenium_action(
            driver, "Could not find '%s' using '%s'", item_name,
            item_selector):
        menu_item = driver.find_element_by_css_selector(item_selector)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


def start_exporting_journey(driver: webdriver):
    """Start Exporting Journey (Triaging).

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    """
    button = find_element(driver, by_css=GET_STARTED_BUTTON)
    assert button.is_displayed()
    button.click()


def continue_export_journey(driver: webdriver):
    """Continue your Export Journey (Triage)."""
    button = find_element(driver, by_css=CONTINUE_EXPORT_JOURNEY)
    assert button.is_displayed()
    button.click()


def get_number_of_current_carousel_article(driver: webdriver) -> int:
    indicators = find_elements(driver, by_css=CAROUSEL_INDICATORS)
    opacities = [(k, float(v.value_of_css_property("opacity")))
                 for k, v in enumerate(indicators)]
    active_indicator = [opacity[0] for opacity in opacities if opacity[1] == 1]
    return active_indicator[0] + 1


def find_case_study_by_going_left(driver: webdriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    prev_buttons = find_elements(driver, by_css=CAROUSEL_PREV_BUTTON)
    prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        prev_button.click()
        prev_buttons = find_elements(driver, by_css=CAROUSEL_PREV_BUTTON)
        prev_button = [nb for nb in prev_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver,
            "After moving left to find Case Study {}".format(to_open))
        max_actions -= 1


def find_case_study_by_going_right(driver: webdriver, to_open: int):
    current = get_number_of_current_carousel_article(driver)
    next_buttons = find_elements(driver, by_css=CAROUSEL_NEXT_BUTTON)
    next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
    max_actions = 5
    while (current != to_open) and (max_actions > 0):
        next_button.click()
        next_buttons = find_elements(driver, by_css=CAROUSEL_NEXT_BUTTON)
        next_button = [nb for nb in next_buttons if nb.is_displayed()][0]
        current = get_number_of_current_carousel_article(driver)
        take_screenshot(
            driver,
            "After moving right to find Case Study {}".format(to_open))
        max_actions -= 1


def move_to_case_study_navigation_buttons(driver: webdriver):
    prev_button = driver.find_element_by_css_selector(CAROUSEL_PREV_BUTTON)
    vertical_position = prev_button.location['y']
    logging.debug("Moving focus to Carousel navigation buttons")
    driver.execute_script("window.scrollTo(0, {});".format(vertical_position))


def open_case_study(driver: webdriver, case_number: str):
    case_study_numbers = {
        "first": 1,
        "second": 2,
        "third": 3
    }
    case_study_number = case_study_numbers[case_number.lower()]

    move_to_case_study_navigation_buttons(driver)

    current_case_study_number = get_number_of_current_carousel_article(driver)
    if current_case_study_number != case_study_number:
        if random.choice([True, False]):
            find_case_study_by_going_left(driver, case_study_number)
        else:
            find_case_study_by_going_right(driver, case_study_number)

    link_selector = CASE_STUDY_LINK.format(case_study_number)
    case_study_link = find_element(driver, by_css=link_selector)
    case_study_link.click()


def get_case_study_title(driver: webdriver, case_number: str) -> str:
    case_study_numbers = {"first": 1, "second": 2, "third": 3}
    case_number = case_study_numbers[case_number.lower()]
    link_selector = CASE_STUDY_LINK.format(case_number)
    case_study_link = find_element(
        driver, by_css=link_selector, wait_for_it=False)
    return case_study_link.text.strip()


def open(driver: webdriver, group: str, element: str):
    selector = SECTIONS[group.lower()][element.lower()]
    link = driver.find_element_by_css_selector(selector)
    assert link.is_displayed()
    link.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))


def play_video(driver: webdriver, *, play_time: int = 5):
    video_load_delay = 2
    play_js = "document.querySelector(\"{}\").play()".format(PROMO_VIDEO)
    pause = "document.querySelector(\"{}\").pause()".format(PROMO_VIDEO)
    driver.execute_script(play_js)
    if play_time:
        time.sleep(play_time + video_load_delay)
        driver.execute_script(pause)


def get_video_watch_time(driver: webdriver) -> int:
    watch_time_js = (
        "return document.querySelector(\"{}\").currentTime"
        .format(PROMO_VIDEO))
    duration_js = (
        "return document.querySelector(\"{}\").duration".format(PROMO_VIDEO))
    watch_time = driver.execute_script(watch_time_js)
    duration = driver.execute_script(duration_js)
    logging.debug("Video watch time: %d", watch_time)
    logging.debug("Video duration : %d", duration)
    return int(watch_time)


def close_video(driver: webdriver):
    take_screenshot(driver, NAME + " before closing video modal window")
    close_button = find_element(driver, by_css=CLOSE_VIDEO)
    close_button.click()


def should_not_see_video_modal_window(driver: webdriver):
    check_if_element_is_not_present(driver, by_css=VIDEO_MODAL_WINDOW)
