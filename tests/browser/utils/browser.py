# -*- coding: utf-8 -*-
"""Behave configuration file."""
import json
import logging
import socket
import time
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


def get_driver_capabilities(
    environment: str,
    browser_type: str,
    browser: str,
    version: str = None,
    custom_capabilities: dict = None,
    build: str = None,
) -> dict:
    common = CAPABILITIES_TEMPLATES[environment]["common_capabilities"][browser_type]
    browser = CAPABILITIES_TEMPLATES[environment]["browser_capabilities"][browser]
    capabilities = {}
    capabilities.update(common)
    capabilities.update(browser)
    if build:
        capabilities["build"] = build
    if version:
        capabilities["browser_version"] = version
    if custom_capabilities:
        capabilities.update(custom_capabilities)
    return capabilities


def flag_browserstack_session_as_failed(session_id: str, reason: str):
    from settings import BROWSERSTACK_SESSIONS_URL, BROWSERSTACK_USER, BROWSERSTACK_PASS

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


def start_driver_session(session_name: str) -> WebDriver:
    from settings import BROWSER_HEADLESS, DRIVER_CAPABILITIES, HUB_URL

    capabilities = DRIVER_CAPABILITIES
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

        print(f"Starting local instance of {browser_name} with options: {options}")
        driver = drivers[browser_name](options=options)

    driver.set_page_load_timeout(time_to_wait=27.0)
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


def show_snackbar_message(driver: WebDriver, message: str):
    script = """
    function removeElement(id) {{
        var existing = document.getElementById(id);
        if(existing) {{
            existing.parentNode.removeChild(existing);
        }};
    }};

    function addElement(tag, innerHTML, id) {{
        removeElement(id);
        var node = document.createElement(tag);
        node.innerHTML = innerHTML;
        node.id = id;
        document.body.appendChild(node);
    }};

    function showSnackBar() {{
        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function(){{ x.className = x.className.replace("show", ""); }}, 3000);
    }};

    function createSnackBarElements(message) {{
        var snackbar_css = `
        #snackbar {{
            visibility: hidden;
            min-width: 250px;
            margin-left: -125px;
            background-color: #333;
            color: #00FF00;
            text-align: center;
            border-radius: 2px;
            padding: 16px;
            position: fixed;
            z-index: 1;
            left: 10%;
            top: 30px;
        }}

        #snackbar.show {{
            visibility: visible;
            -webkit-animation: fadein 0.1s, fadeout 0.1s 1s;
            animation: fadein 0.1s, fadeout 0.1s 1s;
        }}

        @-webkit-keyframes fadein {{
            from {{top: 0; opacity: 0;}}
            to {{top: 30px; opacity: 1;}}
        }}

        @keyframes fadein {{
            from {{top: 0; opacity: 0;}}
            to {{top: 30px; opacity: 1;}}
        }}

        @-webkit-keyframes fadeout {{
            from {{top: 30px; opacity: 1;}}
            to {{top: 0; opacity: 0;}}
        }}

        @keyframes fadeout {{
            from {{top: 30px; opacity: 1;}}
            to {{top: 0; opacity: 0;}}
        }}`;

        addElement('style', snackbar_css, 'snackbar_css');
        addElement('div', message, 'snackbar');
    }};

    function deleteSnackBarElements() {{
        removeElement('snackbar');
        removeElement('snackbar_css');
    }};

    function showMessage(message) {{
        deleteSnackBarElements();
        createSnackBarElements(message);
        showSnackBar();
        setTimeout(deleteSnackBarElements, 1000);
    }};

    showMessage(`{message}`);
    """
    message = message.replace("`", "")
    try:
        driver.execute_script(script.format(message=message))
    except WebDriverException:
        logging.error(f"Failed to show snackbar with message: {message}")

    # in order to keep the snackbar visible after the scenario is finished,
    # wait for 200ms
    time.sleep(0.2)
