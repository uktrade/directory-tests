# -*- coding: utf-8 -*-
"""Common PageObject actions

REMEMBER:
 to overwrite variables from this module in your PageObject.
"""
from selenium import webdriver

from utils import clear_driver_cookies, take_screenshot


def go_to_url(
        driver: webdriver, url: str, page_name: str, *,
        first_time: bool = False):
    """Go to the specified URL and take a screenshot afterwards.

    :param driver: Any Selenium Driver (Remote, Chrome, Firefox, PhantomJS etc.
    :param url: URL to open
    :param page_name: human friend page name used in screenshot name
    :param first_time: (optional) will delete all cookies if True
    """
    if first_time:
        clear_driver_cookies(driver)
    driver.get(url)
    take_screenshot(driver, page_name)
