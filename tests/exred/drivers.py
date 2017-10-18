# -*- coding: utf-8 -*-
"""Selenium driver getters"""
import os

from selenium.webdriver import Chrome, Firefox, PhantomJS, Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HUB_URL = os.environ.get("HUB_URL", "http://127.0.0.1:4444/wd/hub")
DRIVERS = (Remote, Chrome, Firefox, PhantomJS)


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
    remote_driver = browser_map[browser_name]()
    remote_driver.set_window_size(width, height)
    return remote_driver
