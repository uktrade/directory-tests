# -*- coding: utf-8 -*-
"""Selenium driver getters"""
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from settings import HUB_URL


def get_chrome_driver():
    return Remote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.CHROME,
    )


def get_firefox_driver():
    return Remote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.FIREFOX)


def get_phantom_js_driver():
    return Remote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.PHANTOMJS)


def get(browser_name, *, width: int = 1600, height: int = 1200):
    browser_map = {
        "chrome": get_chrome_driver,
        "firefox": get_firefox_driver,
        "phantomjs": get_phantom_js_driver
    }
    remote_driver = browser_map[browser_name.lower()]()
    remote_driver.set_window_size(width, height)
    return remote_driver
