import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.common_actions import Selector, find_element

ALLOWED = {
    "google tag manager": Selector(
        By.CSS_SELECTOR, "script[src='https://www.googletagmanager.com/gtm.js?id=']"
    ),
    "google tag manager - no script": Selector(
        By.XPATH, "//noscript[contains(text(),'googletagmanager.com')]"
    ),
    "utm cookie domain": Selector(By.ID, "utmCookieDomain"),
}


NOT_ALLOWED = {
    "facebook tracking pixel": Selector(
        By.XPATH, "//script[contains(text(),'connect.facebook.net')]"
    ),
    "linkedin tracking pixel": Selector(
        By.XPATH, "//script[contains(text(),'linkedin.com')]"
    ),
}


def find_element_with_selector(driver: WebDriver, selector: Selector) -> WebElement:
    if selector.by == By.CSS_SELECTOR:
        result = find_element(driver, by_css=selector.value, wait_for_it=False)
    elif selector.by == By.ID:
        result = find_element(driver, by_id=selector.value, wait_for_it=False)
    elif selector.by == By.LINK_TEXT:
        result = find_element(driver, by_link_text=selector.value, wait_for_it=False)
    elif selector.by == By.PARTIAL_LINK_TEXT:
        result = find_element(
            driver, by_partial_link_text=selector.value, wait_for_it=False
        )
    elif selector.by == By.XPATH:
        result = find_element(driver, by_xpath=selector.value, wait_for_it=False)
    else:
        raise AttributeError("Please provide valid element locator")

    return result


def should_be_present(driver: WebDriver, name: str):
    find_element_with_selector(driver, ALLOWED[name.lower()])
    logging.debug("As expected '{}' is present".format(name))


def should_not_be_present(driver: WebDriver, name: str):
    try:
        find_element_with_selector(driver, NOT_ALLOWED[name.lower()])
    except NoSuchElementException:
        logging.debug("As expected '{}' is not present".format(name))
        pass
