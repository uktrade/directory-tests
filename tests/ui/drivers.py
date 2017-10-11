import os
from needle.driver import NeedleRemote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

HUB_URL = os.environ.get("HUB_URL", "http://127.0.0.1:4444/wd/hub")


def get_chrome_driver():
    return NeedleRemote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.CHROME)


def get_firefox_driver():
    return NeedleRemote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.FIREFOX)


def get_phantomjs_driver():
    return NeedleRemote(
        command_executor=HUB_URL,
        desired_capabilities=DesiredCapabilities.PHANTOMJS)


def get_needle_web_driver(browser_name):
    browser_map = {
        "chrome": get_chrome_driver,
        "firefox": get_firefox_driver,
        "phantomjs": get_phantomjs_driver
    }
    return browser_map[browser_name]()
