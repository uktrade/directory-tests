# -*- coding: utf-8 -*-
"""Behave configuration file."""
import json
import logging
import socket
from http.client import CannotSendRequest

import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver

CAPABILITIES_TEMPLATES = {
    "local": {
        "common_capabilities": {"desktop": {}, "mobile": {}},
        "browser_capabilities": {
            "chrome": {"browser": "Chrome"},
            "firefox": {"browser": "Firefox"},
        },
    },
    "remote": {
        "common_capabilities": {
            "desktop": {
                "browserstack.debug": False,
                "browserstack.selenium_version": "3.141.59",
                "browserstack.timezone": "UTC",
                "browserstack.use_w3c": True,
                "browserstack.networkLogs": False,
                "project": "DIT",
                "resolution": "1600x1200",
                "build": None,
            },
            "mobile": {
                "browserstack.debug": False,
                "browserstack.selenium_version": "3.141.59",
                "browserstack.timezone": "UTC",
                "browserstack.use_w3c": True,
                "browserstack.networkLogs": False,
                "project": "DIT",
                "build": None,
            },
        },
        "browser_capabilities": {
            "chrome": {
                "browser": "Chrome",
                "browser_version": "76.0",
                "pageLoadStrategy": "none",
                "os": "Windows",
                "os_version": "10",
                "browserstack.chrome.driver": "75.0.3770.8",
            },
            "edge": {
                "browser": "Edge",
                "browser_version": "16.0",
                "os": "Windows",
                "os_version": "10",
            },
            "firefox": {
                "browser": "Firefox",
                "browser_version": "68.0",
                "pageLoadStrategy": "eager",
                "os": "Windows",
                "os_version": "10",
                "browserstack.geckodriver": "0.24.0",
            },
            "ie": {
                "browser": "IE",
                "browser_version": "11.0",
                "os": "Windows",
                "os_version": "10",
            },
        },
    },
}


def get_driver_capabilities() -> dict:
    from directory_tests_shared.settings import (
        BROWSER,
        BROWSER_CUSTOM_CAPABILITIES,
        BROWSER_ENVIRONMENT,
        BROWSER_TYPE,
        BROWSER_VERSION,
        BUILD_ID,
    )

    common = CAPABILITIES_TEMPLATES[BROWSER_ENVIRONMENT]["common_capabilities"][
        BROWSER_TYPE
    ]
    browser = CAPABILITIES_TEMPLATES[BROWSER_ENVIRONMENT]["browser_capabilities"][
        BROWSER
    ]
    capabilities = {}
    capabilities.update(common)
    capabilities.update(browser)
    if BUILD_ID:
        capabilities["build"] = BUILD_ID
    if BROWSER_VERSION:
        capabilities["browser_version"] = BROWSER_VERSION
    if BROWSER_CUSTOM_CAPABILITIES:
        capabilities.update(BROWSER_CUSTOM_CAPABILITIES)
    return capabilities


def flag_browserstack_session_as_failed(session_id: str, reason: str):
    from directory_tests_shared.settings import (
        BROWSERSTACK_PASS,
        BROWSERSTACK_SESSIONS_URL,
        BROWSERSTACK_USER,
    )

    url = BROWSERSTACK_SESSIONS_URL.format(session_id)
    headers = {"Content-Type": "application/json"}
    data = {"status": "failed", "reason": reason}
    auth = (BROWSERSTACK_USER, BROWSERSTACK_PASS)
    response = requests.put(url=url, headers=headers, data=json.dumps(data), auth=auth)
    if response.ok:
        logging.error(
            f"Flagged BrowserStack session: {session_id} as failed, reason: {reason}"
        )
    else:
        logging.error(
            f"Failed to flagged BrowserStack session: {session_id} as failed. "
            f"BrowserStack responded with {response.status_code}: {response.content}"
        )


def start_driver_session(session_name: str, capabilities: dict) -> WebDriver:
    from directory_tests_shared.settings import BROWSER_HEADLESS, HUB_URL

    capabilities["name"] = session_name

    if HUB_URL:
        driver = webdriver.Remote(
            desired_capabilities=capabilities, command_executor=HUB_URL
        )
        logging.warning(f"Started new remote session: {driver.session_id}")
    else:
        browser_name = capabilities["browser"].lower()
        drivers = {
            "chrome": webdriver.Chrome,
            "edge": webdriver.Edge,
            "firefox": webdriver.Firefox,
            "ie": webdriver.Ie,
        }

        options = None
        if browser_name == "chrome":
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if BROWSER_HEADLESS:
                options.add_argument("--headless")
                options.add_argument("--window-size=1600x2200")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
        elif browser_name == "firefox":
            from selenium.webdriver.firefox.options import Options

            options = Options()
            if BROWSER_HEADLESS:
                options.add_argument("--headless")
                options.add_argument("--window-size=1600x2200")

        print(
            f"Starting local instance of {browser_name} with options: {options.arguments}"
        )
        driver = drivers[browser_name](options=options)

    driver.set_page_load_timeout(time_to_wait=30)
    try:
        driver.maximize_window()
        logging.debug("Maximized the window.")
    except WebDriverException:
        logging.debug("Failed to maximize the window.")
        try:
            driver.set_window_size(1600, 1200)
            logging.warning("Set window size to 1600x1200")
        except WebDriverException:
            logging.warning("Failed to set window size, will continue as is")
    logging.debug(f"Browser Capabilities: {driver.capabilities}")

    return driver


def terminate_driver(driver: WebDriver):
    if not driver:
        logging.warning(f"Can't terminate an empty driver!")
        return
    try:
        logging.debug("Quit driver")
        driver.quit()
    except WebDriverException as ex:
        logging.error(f"Failed to quit the driver {ex.msg}")


def is_driver_responsive(driver: WebDriver) -> bool:
    responsive = False
    try:
        response = driver.execute(Command.STATUS)
        logging.debug(f"WebDriver Status: {response}")
        responsive = True
    except (socket.error, CannotSendRequest):
        logging.error(f"Remote browser driver became unresponsive!")
    return responsive


def clear_driver_cookies(driver: WebDriver, *, log_cleanup: bool = False):
    if not driver:
        logging.warning(f"Can't clear cookies from an empty driver!")
        return
    try:
        if log_cleanup:
            logging.debug(f"COOKIES: {driver.get_cookies()}")
        driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies")
        if log_cleanup:
            logging.debug(f"Driver cookies after clearing them: {driver.get_cookies()}")
    except WebDriverException as ex:
        logging.error(f"Failed to clear cookies: '{ex.msg}'")
