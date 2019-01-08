# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    assertion_msg,
    check_for_expected_sections_elements,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "Footer"
SERVICE = "Export Readiness"
TYPE = "header"
URL = None

SELECTORS = {
    "logos": {
        "dit logo": Selector(By.ID, "footer-dit-logo"),
        "eig logo": Selector(By.ID, "footer-eig-logo"),
    },
    "export readiness": {
        "label": Selector(By.ID, "footer-export-readiness-links"),
        "new": Selector(By.ID, "footer-export-readiness-new"),
        "occasional": Selector(By.ID, "footer-export-readiness-occasional"),
        "regular": Selector(By.ID, "footer-export-readiness-regular"),
        "i'm new to exporting": Selector(By.ID, "footer-export-readiness-new"),
        "i export occasionally": Selector(By.ID, "footer-export-readiness-occasional"),
        "i'm a regular exporter": Selector(By.ID, "footer-export-readiness-regular"),
    },
    "advice": {
        "label": Selector(By.ID, "footer-advice-links"),
        "create an export plan":
            Selector(By.ID, "footer-advice-make-an-export-plan"),
        "find an export market":
            Selector(By.ID, "footer-advice-how-to-find-an-export-market"),
        "define route to market":
            Selector(By.ID, "footer-advice-how-to-enter-an-export-market"),
        "get export finance and funding":
            Selector(By.ID, "footer-advice-managing-finance"),
        "manage payment for export orders":
            Selector(By.ID, "footer-advice-managing-finance"),
        "prepare to do business in a foreign country":
            Selector(By.ID, "footer-advice-doing-business-overseas"),
        "manage legal and ethical compliance":
            Selector(By.ID, "footer-advice-legal-and-compliance"),
        "prepare for export procedures and logistics":
            Selector(By.ID, "footer-advice-legal-and-compliance"),
    },
    "services": {
        "label": Selector(By.ID, "footer-services-links"),
        "find a buyer": Selector(By.ID, "footer-services-find-a-buyer"),
        "selling online overseas": Selector(
            By.ID, "footer-services-selling-online-overseas"
        ),
        "export opportunities": Selector(By.ID, "footer-services-export-opportunities"),
        "get finance": Selector(By.ID, "footer-services-get-finance"),
        "events": Selector(By.ID, "footer-services-events"),
    },
    "general": {
        "your export journey": Selector(By.ID, "footer-custom-page-link"),
        "about": Selector(By.ID, "footer-site-links-about"),
        "contact us": Selector(By.ID, "footer-site-links-contact-us"),
        "privacy and cookies": Selector(By.ID, "footer-site-links-privacy-and-cookies"),
        "terms and conditions": Selector(By.ID, "footer-site-links-t-and-c"),
        "department for international trade": Selector(By.ID, "footer-site-links-dit"),
        "copyright": Selector(By.ID, "footer-copyright"),
    },
}


def should_see_all_menus(driver: WebDriver):
    check_for_expected_sections_elements(driver, SELECTORS)


def should_see_link_to(driver: WebDriver, section: str, item_name: str):
    item_selector = SELECTORS[section.lower()][item_name.lower()]
    menu_item = find_element(driver, item_selector, element_name=item_name)
    with assertion_msg(
        "It looks like '%s' in '%s' section is not visible", item_name, section
    ):
        assert menu_item.is_displayed()


def open(driver: WebDriver, group: str, element: str):
    link = SELECTORS[group.lower()][element.lower()]
    button = find_element(driver, link, element_name=element, wait_for_it=False)
    with wait_for_page_load_after_action(driver):
        button.click()
    take_screenshot(driver, NAME + " after clicking on: %s link".format(element))


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
