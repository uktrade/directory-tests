# -*- coding: utf-8 -*-
"""Common PageObject actions."""
import time

import hashlib
import json
import logging
import os
import random
import string
import sys
import traceback
import uuid
from collections import defaultdict
from collections.__init__ import namedtuple
from contextlib import contextmanager
from datetime import datetime
from os import path
from selenium.webdriver import ActionChains
from types import ModuleType
from typing import Dict, List, Union

import requests
from behave.runner import Context
from bs4 import BeautifulSoup
from mohawk import Sender
from requests import Response, Session
from retrying import retry
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

from pages import ElementType
from settings import (
    BROWSERSTACK_PASS,
    BROWSERSTACK_SESSIONS_URL,
    BROWSERSTACK_USER,
    IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
    IP_RESTRICTOR_SKIP_CHECK_SECRET,
    TAKE_SCREENSHOTS,
)

ScenarioData = namedtuple("ScenarioData", ["actors"])
Actor = namedtuple(
    "Actor",
    [
        "alias",
        "email",
        "password",
        "self_classification",
        "triage_classification",
        "what_do_you_want_to_export",
        "have_you_exported_before",
        "do_you_export_regularly",
        "are_you_incorporated",
        "company_name",
        "do_you_use_online_marketplaces",
        "created_personalised_journey",
        "article_group",
        "article_category",
        "article_location",
        "visited_articles",
        "articles_read_counter",
        "articles_time_to_complete",
        "articles_total_number",
        "article_list_read_counter",
        "article_list_time_to_complete",
        "article_list_total_number",
        "case_study_title",
        "email_confirmation_link",
        "registered",
        "visited_page",
        "last_tag",
    ],
)
VisitedArticle = namedtuple("VisitedArticle", ["index", "title", "time_to_read"])
Executor = Union[WebDriver, Session]
AssertionExecutor = Union[WebDriver, Response]
Selector = namedtuple(
    "Selector", ["by", "value", "in_desktop", "in_mobile", "in_horizontal", "type", "is_visible"]
)

# define default values for various named tuples
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
VisitedArticle.__new__.__defaults__ = (None,) * len(VisitedArticle._fields)
Selector.__new__.__defaults__ = (None, None, True, True, True, None, True)


def get_hawk_cookie():
    sender = Sender(
        credentials={
            'id': IP_RESTRICTOR_SKIP_CHECK_SENDER_ID,
            'key': IP_RESTRICTOR_SKIP_CHECK_SECRET,
            'algorithm': 'sha256'
        },
        url='/',
        method='',
        always_hash_content=False
    )

    return {
        # "domain": "/",
        "name": "ip-restrict-signature",
        "value": sender.request_header,
        # 'secure': False,
    }


def go_to_url(driver: WebDriver, url: str, page_name: str, *, first_time: bool = False):
    """Go to the specified URL and take a screenshot afterwards."""
    if first_time:
        clear_driver_cookies(driver)
    driver.get(url)
    take_screenshot(driver, page_name)


def check_url(driver: WebDriver, expected_url: str, *, exact_match: bool = True):
    """Check if current page URL matches the expected one."""
    with assertion_msg(
        "Expected page URL to be: '%s' but got '%s'", expected_url,
        driver.current_url
    ):
        if exact_match:
            assert driver.current_url == expected_url
        else:
            assert (driver.current_url in expected_url) or (
                expected_url in driver.current_url
            )
    logging.debug("Current page URL matches expected '%s'", driver.current_url)


def check_title(driver: WebDriver, expected_title: str, *, exact_match: bool = False):
    """Check if current page title matches the expected one."""
    with assertion_msg(
        "Expected page title to be: '%s' but got '%s' on %s", expected_title,
        driver.title, driver.current_url
    ):
        if exact_match:
            assert expected_title.lower() == driver.title.lower()
        else:
            assert expected_title.lower() in driver.title.lower()
    logging.debug(
        "Page title on '%s' matches expected '%s'", driver.current_url, expected_title
    )


def check_for_section(driver: WebDriver, all_sections: dict, sought_section: str):
    """Check if all page elements from sought section are visible."""
    section = all_sections[sought_section.lower()]
    for element_name, selector in section.items():
        element = find_element(driver, selector, element_name=element_name)
        with assertion_msg(
            "'%s' in '%s' is not displayed on: %s",
            element_name,
            sought_section,
            driver.current_url,
        ):
            assert element.is_displayed()
            logging.debug("'%s' in '%s' is displayed", element_name, sought_section)


def check_for_expected_elements(
    driver: WebDriver, elements: Dict, *, wait_for_it: bool = True
):
    """Check if all page elements are visible."""
    for element_name, selector in elements.items():
        if not isinstance(selector, Selector):
            raise TypeError(
                "Expected '{}' to be a Selector, got {}"
                .format(selector, type(selector)))
        element = find_element(
            driver, selector, element_name=element_name, wait_for_it=wait_for_it
        )
        with assertion_msg(
            "It looks like '%s' element is not visible on %s",
            element_name,
            driver.current_url,
        ):
            assert element.is_displayed()
    logging.debug("All expected elements are visible on '%s'", driver.current_url)


def check_for_expected_sections_elements(
        driver: WebDriver, sections: Dict[str, Selector]):
    """Check if all elements in page sections are visible."""
    for section in sections:
        for element_name, selector in sections[section].items():
            if not isinstance(selector, Selector):
                raise TypeError(
                    "Expected '{}' to be a Selector, got {}"
                    .format(selector, type(selector)))
            element = find_element(driver, selector, element_name=element_name)
            if not selector.is_visible:
                logging.debug(f"Skipping '{element_name} as it's marker as not visible'")
                continue
            with assertion_msg(
                "It looks like '%s' element in '%s' section is not visible" " on %s",
                element_name,
                section,
                driver.current_url,
            ):
                assert element.is_displayed()
        logging.debug("All expected elements are visible on '%s'", driver.current_url)


def find_and_click_on_page_element(
    driver: WebDriver, sections: dict, element_name: str, *, wait_for_it: bool=True
):
    """Find page element in any page section selectors and click on it."""
    found_selector = False
    for section_name, selectors in sections.items():
        if element_name.lower() in selectors:
            found_selector = True
            selector = selectors[element_name.lower()]
            logging.debug(
                "Found '%s' in '%s' section with following selector: '%s'",
                element_name,
                section_name,
                selector,
            )
            web_element = find_element(
                driver, selector, element_name=element_name, wait_for_it=wait_for_it
            )
            check_if_element_is_visible(web_element, element_name)
            with wait_for_page_load_after_action(driver):
                web_element.click()
    with assertion_msg("Could not find '%s' in any section", element_name):
        assert found_selector


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data."""
    return ScenarioData(actors={})


def unauthenticated_actor(alias: str, *, self_classification: str = None) -> Actor:
    """Create an instance of an unauthenticated Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
    """
    email = (
        "test+{}{}@directory.uktrade.io".format(alias, str(uuid.uuid4()))
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    letters = "".join(random.choice(string.ascii_letters) for _ in range(10))
    digits = "".join(random.choice(string.digits) for _ in range(10))
    password = f"{letters}{digits}"
    return Actor(
        alias=alias,
        email=email,
        password=password,
        self_classification=self_classification,
        visited_articles=[],
    )


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data."""
    assert isinstance(
        actor, Actor
    ), "Expected Actor named tuple but got '{}'" " instead".format(type(actor))
    context.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(context: Context, alias: str) -> Actor:
    """Get actor details from context Scenario Data."""
    return context.scenario_data.actors.get(alias)


def get_last_visited_page(context: Context, actor_alias: str) -> ModuleType:
    """Get last visited Page Object context Scenario Data."""
    actor = context.scenario_data.actors.get(actor_alias)
    return actor.visited_page


def update_actor(context: Context, alias: str, **kwargs):
    """Update Actor's details stored in context.scenario_data"""
    actors = context.scenario_data.actors
    for arg in kwargs:
        if arg in Actor._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            actors[alias] = actors[alias]._replace(**{arg: kwargs[arg]})
    logging.debug("Successfully updated %s's details: %s", alias, actors[alias])


@retry(stop_max_attempt_number=3)
def take_screenshot(driver: WebDriver, page_name: str):
    """Will take a screenshot of current page."""
    if not isinstance(driver, WebDriver):
        logging.debug("Taking screenshots in non-browser executor is not possible")
        return
    if TAKE_SCREENSHOTS:
        session_id = driver.session_id
        browser = driver.capabilities.get("browserName", "unknown_browser")
        version = driver.capabilities.get("version", "unknown_version")
        platform = driver.capabilities.get("platform", "unknown_platform")
        stamp = datetime.isoformat(datetime.utcnow())
        filename = "{}-{}-{}-{}-{}-{}.png".format(
            stamp, page_name, browser, version, platform, session_id
        )
        file_path = path.abspath(path.join("screenshots", filename))
        driver.save_screenshot(file_path)
        logging.debug("Screenshot of %s page saved in: %s", page_name, filename)
    else:
        logging.debug(
            "Taking screenshots is disabled. In order to turn it on please set"
            " an environment variable TAKE_SCREENSHOTS=true"
        )


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


@contextmanager
def selenium_action(driver: WebDriver, message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :raises WebDriverException or NoSuchElementException
    """
    try:
        yield
    except (WebDriverException, NoSuchElementException, TimeoutException) as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = "[{} v:{} os:{} session_id:{}]".format(
            browser, version, platform, session_id
        )
        if args:
            message = message % args
        print("{} - {}".format(info, message))
        logging.debug("%s - %s", info, message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def get_file_log_handler(
    log_formatter: logging.Formatter,
    *,
    log_level: int = logging.DEBUG,
    task_id: str = None,
) -> logging.FileHandler:
    """Configure the console logger.

    Will use DEBUG logging level by default.
    """
    if task_id:
        log_file = os.path.join("reports", ("behave-%s.log" % task_id))
    else:
        log_file = os.path.join("reports", "behave.log")
    print("Behave log file: {}".format(log_file))
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def init_loggers(context: Context, *, task_id: str = None):
    """Will initialize console and file loggers."""
    # configure the formatter
    fmt = (
        "%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: "
        "%(message)s"
    )
    log_formatter = logging.Formatter(fmt)
    log_file_handler = get_file_log_handler(log_formatter, task_id=task_id)
    # Add log file handler to Behave's logging
    logging.getLogger("selenium").setLevel(logging.WARNING)
    context.config.setup_logging(handlers=[log_file_handler])


def flag_browserstack_session_as_failed(session_id: str, reason: str):
    url = BROWSERSTACK_SESSIONS_URL.format(session_id)
    headers = {"Content-Type": "application/json"}
    data = {"status": "failed", "reason": reason}
    auth = (BROWSERSTACK_USER, BROWSERSTACK_PASS)
    response = requests.put(url=url, headers=headers, data=json.dumps(data), auth=auth)
    if not response.ok:
        logging.error(
            "Failed to flagged BrowserStack session: %s as failed. "
            "BrowserStack responded with %d: %s",
            session_id,
            response.status_code,
            response.content,
        )
    else:
        logging.error("Flagged BrowserStack session: %s as failed", session_id)


def wait_for_visibility(
    driver: WebDriver, selector: Selector, *, time_to_wait: int = 5
):
    """Wait until element is visible."""
    by_locator = (selector.by, selector.value)
    with selenium_action(
        driver,
        "Element identified by '{}' was not visible after waiting "
        "for {} seconds".format(selector.value, time_to_wait),
    ):
        WebDriverWait(driver, time_to_wait).until(
            expected_conditions.visibility_of_element_located(by_locator)
        )


def check_if_element_is_not_present(
    driver: WebDriver, selector: Selector, *, element_name: str = ""
):
    """Find element by CSS selector or it's ID."""
    try:
        driver.find_element(by=selector.by, value=selector.value)
        found = True
    except NoSuchElementException:
        found = False
    with assertion_msg(
        "Expected not to find %s element identified by '%s' on %s",
        element_name,
        selector.value,
        driver.current_url,
    ):
        assert not found


def check_if_element_is_visible(web_element: WebElement, element_name: str):
    """Check if provided web element is visible."""
    with assertion_msg(
        "Expected to see '%s' element but it's not visible", element_name
    ):
        assert web_element.is_displayed()


def check_if_element_is_not_visible(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
):
    """Find element by CSS selector or it's ID."""
    try:
        element = find_element(
            driver, selector, element_name=element_name, wait_for_it=wait_for_it
        )
        with assertion_msg(
            "Expected not to see '%s' element identified by '%s' on %s",
            element_name,
            selector.value,
            driver.current_url
        ):
            assert not element.is_displayed()
    except NoSuchElementException:
        logging.debug("As expected '{}' is not present".format(element_name))
        pass


def find_element(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
) -> WebElement:
    """Find element by CSS selector or it's ID."""
    with selenium_action(
        driver,
        "Couldn't find element called '%s' using selector '%s' on" " %s",
        element_name,
        selector.value,
        driver.current_url,
    ):
        element = driver.find_element(by=selector.by, value=selector.value)
    if wait_for_it and selector.is_visible:
        wait_for_visibility(driver, selector)
    return element


def find_selector_by_name(selectors: dict, name: str) -> Selector:
    found_selectors = [
        selector
        for section_selectors in selectors.values()
        for selector_name, selector in section_selectors.items()
        if selector_name.lower() == name.lower()]
    assert len(found_selectors) == 1
    return found_selectors[0]


def find_selector_by_type(selectors: dict, name: str) -> Selector:
    found_selectors = [
        selector
        for section_selectors in selectors.values()
        for selector_name, selector in section_selectors.items()
        if selector_name.lower() == name.lower()]
    assert len(found_selectors) == 1
    return found_selectors[0]


def find_elements(driver: WebDriver, selector: Selector) -> List[WebElement]:
    """Find element by CSS selector or it's ID."""
    with selenium_action(driver, "Couldn't find elements using '%s'", selector.value):
        elements = driver.find_elements(by=selector.by, value=selector.value)
    return elements


def clear_driver_cookies(driver: WebDriver):
    try:
        cookies = driver.get_cookies()
        logging.debug("COOKIES: %s", cookies)
        driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies")
        cookies = driver.get_cookies()
        logging.debug("Driver cookies after clearing them: %s", cookies)
    except WebDriverException as ex:
        logging.error("Failed to clear cookies: '%s'", ex.msg)


def check_hash_of_remote_file(expected_hash: str, file_url: str):
    """Check if the md5 hash of the file is the same as expected."""
    logging.debug("Fetching file: %s", file_url)
    response = requests.get(file_url)
    file_hash = hashlib.md5(response.content).hexdigest()
    with assertion_msg(
        "Expected hash of file downloaded from %s to be %s but got %s",
        file_url,
        expected_hash,
        file_hash,
    ):
        assert expected_hash == file_hash


@contextmanager
def wait_for_page_load(driver: WebDriver, timeout: int = 30):
    """Alternative Context manager for waiting for page to load.
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    """
    old_page = driver.find_element_by_tag_name("html")
    yield
    logging.debug("WAITING FOR STALENESS OF OLD PAGE %s", driver.current_url)
    WebDriverWait(driver, timeout).until(staleness_of(old_page))


class wait_for_page_load_after_action(object):
    """Context manager for waiting the page to load.
    Proved to be a more reliable than wait_for_page_load() ^^^
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    https://www.develves.net/blogs/asd/2017-03-04-selenium-waiting-for-page-load/
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name("html")

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_tag_name("html")
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    def wait_for(self, condition_function):
        import time

        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception("Timeout waiting for {}".format(condition_function.__name__))


def scroll_to(driver: WebDriver, element: WebElement):
    vertical_position = element.location["y"]
    logging.debug("Moving focus to %s", element.id)
    driver.execute_script("window.scrollTo(0, {});".format(vertical_position))


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
    driver.execute_script(script.format(message=message))


def check_for_sections(
    executor: AssertionExecutor, all_sections: dict, sought_sections: List[str]
):
    if isinstance(executor, WebDriver):
        browser_check_for_sections(executor, all_sections, sought_sections)
    elif isinstance(executor, Response):
        requests_check_for_sections(executor, all_sections, sought_sections)
    else:
        raise NotImplementedError(
            "Unsupported type: {}. Please provide one of supported types: "
            "WebDriver or Response".format(type(executor))
        )


def browser_check_for_sections(
    driver: WebDriver,
    all_sections: dict,
    sought_sections: List[str],
    *,
    desktop: bool = True,
    mobile: bool = False,
    horizontal: bool = False,
):
    for name in sought_sections:
        if desktop:
            selectors = get_desktop_selectors(all_sections[name.lower()])
        elif mobile:
            selectors = get_mobile_selectors(all_sections[name.lower()])
        elif horizontal:
            selectors = get_horizontal_selectors(all_sections[name.lower()])
        else:
            raise KeyError(
                "Please choose from desktop, mobile or horizontal (mobile) "
                "selectors"
            )
        for key, selector in selectors.items():
            with selenium_action(
                driver,
                "Could not find element: %s identified by '%s' selector on %s",
                key,
                selector.value,
                driver.current_url
            ):
                element = driver.find_element(by=selector.by, value=selector.value)
            if "firefox" not in driver.capabilities["browserName"].lower():
                logging.debug("Moving focus to '%s' element", key)
                action_chains = ActionChains(driver)
                action_chains.move_to_element(element)
                action_chains.perform()
            if selector.is_visible:
                with assertion_msg(
                    "It looks like '%s' element identified by '%s' selector is"
                    " not visible on %s",
                    key,
                    selector,
                    driver.current_url,
                ):
                    assert element.is_displayed()
            else:
                logging.debug(
                    f"Skipping visiblity check for '{key} -> {selector}' as "
                    f"its selector is flagged as not visible")


def requests_check_for_sections(
    response: Response, all_sections: dict, sought_sections: List[str]
):
    for name in sought_sections:
        selectors = get_desktop_selectors(all_sections[name.lower()])
        for key, selector in selectors.items():
            soup = BeautifulSoup(response.content, "lxml")
            if selector.by == By.ID:
                element = soup.find_all(id=selector.value)
            else:
                element = soup.find_all(selector.value)
            assert element is not None


def get_desktop_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_desktop}


def get_mobile_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_mobile}


def get_horizontal_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector for key, selector in section.items() if selector.in_horizontal
    }


def get_selectors(section: dict, element_type: ElementType) -> Dict[str, Selector]:
    return {key: selector
            for key, selector in section.items()
            if selector.type == element_type}


def browser_visit(driver: WebDriver, url: str):
    driver.get(url)


def requests_visit(session: Session, url: str) -> Response:
    return session.get(url)


def visit_url(executor: Executor, url: str) -> Union[Response, None]:
    if isinstance(executor, WebDriver):
        executor.get(url)
    elif isinstance(executor, Session):
        return executor.get(url)
    else:
        raise NotImplementedError(
            "Unsupported type: {}. Please provide one of supported types: "
            "WedDriver or Session".format(type(executor))
        )


def tick_captcha_checkbox(driver: WebDriver):
    im_not_a_robot = Selector(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
    iframe = driver.find_element_by_tag_name("iframe")
    scroll_to(driver, iframe)
    driver.switch_to.frame(iframe)
    captcha = find_element(driver, im_not_a_robot)
    captcha.click()
    # wait 2s after user clicks on the CAPTCHA checkbox
    # otherwise the test might fail
    time.sleep(2)
    driver.switch_to.parent_frame()


def fill_out_input_fields(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    input_selectors = get_selectors(form_selectors, ElementType.INPUT)
    for key, selector in input_selectors.items():
        value_to_type = form_details[key]
        if not value_to_type:
            continue
        logging.debug(f"Filling out input field {key} with '{value_to_type}'")
        input_field = find_element(
            driver, selector, element_name=key, wait_for_it=False)
        input_field.send_keys(value_to_type)


def fill_out_textarea_fields(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    textarea_selectors = get_selectors(form_selectors, ElementType.TEXTAREA)
    for key, selector in textarea_selectors.items():
        value_to_type = form_details[key]
        if not value_to_type:
            continue
        logging.debug(f"Filling out textarea: {key} with '{value_to_type}'")
        textarea = find_element(
            driver, selector, element_name=key, wait_for_it=False)
        textarea.send_keys(value_to_type)


def pick_option(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    select_selectors = get_selectors(form_selectors, ElementType.SELECT)
    for key, selector in select_selectors.items():
        logging.debug(f"Picking option from {key} dropdown list")
        select = find_element(
            driver, selector, element_name=key, wait_for_it=False)
        if form_details.get(key, None):
            option = form_details[key]
        else:
            options = select.find_elements_by_css_selector("option")
            values = [option.get_property("value")
                      for option in options
                      if option.get_property("value")]
            logging.debug("Available options: {}".format(values))
            option = random.choice(values)
        logging.debug("Will select option: {}".format(option))
        option_value_selector = "option[value='{}']".format(option)
        option_element = select.find_element_by_css_selector(option_value_selector)
        option_element.click()


def pick_option_from_autosuggestion(
    driver: WebDriver, form_selectors: Dict[str, Selector],
    form_details: dict):
    select_selectors = get_selectors(form_selectors, ElementType.SELECT)
    for key, selector in select_selectors.items():
        logging.debug(f"Picking option from {key} dropdown list")
        select = find_element(
            driver, selector, element_name=key, wait_for_it=False)
        logging.debug(f"dealing with {key} {selector}")
        if form_details.get(key, None):
            option = form_details[key]
        else:
            options = select.find_elements_by_css_selector("option")
            values = [option.get_property("text") for option in options]
            logging.debug("Available options: {}".format(values))
            option = random.choice(values)
        logging.debug("Selected option: {}".format(option))
        if key == "country":
            js_field_selector = Selector(By.ID, "js-country-select")
            js_field = find_element(driver, js_field_selector)
            js_field.click()
            js_field.clear()
            js_field.send_keys(option)
            first_suggestion_selector = Selector(
                By.CSS_SELECTOR, "#js-country-select__listbox li:nth-child(1)")
            first_suggestion = find_element(
                driver, first_suggestion_selector, wait_for_it=True)
            first_suggestion.click()
        else:
            option_value_selector = "option[value='{}']".format(option)
            option_element = select.find_element_by_css_selector(option_value_selector)
            option_element.click()


def check_radio(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    for key, selector in radio_selectors.items():
        assert key in form_details, f"Can't find form detail for '{key}'"
        if form_details[key]:
            radio = find_element(
                driver, selector, element_name=key, wait_for_it=False)
            if not radio.get_property("checked"):
                logging.debug(f"Checking '{key}' radio")
                radio.click()


def choose_one_form_option(
        driver: WebDriver, radio_selectors: Dict[str, Selector], name: str):
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key] = (key == name.lower())
    logging.debug(f"Form details: {form_details}")
    check_radio(driver, radio_selectors, form_details)


def choose_one_form_option_except(
        driver: WebDriver, radio_selectors: Dict[str, Selector],
        ignored: List[str]) -> str:
    all_keys = list(radio_selectors.keys())
    without_ignored = list(set(all_keys) - set(ignored))
    selected = random.choice(without_ignored)
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key.lower()] = (key.lower() == selected)
    logging.debug(f"Form details (with ignored: {ignored}): {form_details}")
    check_radio(driver, radio_selectors, form_details)
    return selected


def tick_checkboxes(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    checkbox_selectors = get_selectors(form_selectors, ElementType.CHECKBOX)
    for key, selector in checkbox_selectors.items():
        logging.debug(f"Ticking {key} checkbox (if necessary)")
        if form_details[key]:
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False)
            if not checkbox.get_property("checked"):
                checkbox.click()


def tick_checkboxes_by_labels(
        driver: WebDriver, form_selectors: Dict[str, Selector],
        form_details: dict):
    checkbox_selectors = get_selectors(form_selectors, ElementType.LABEL)
    for key, selector in checkbox_selectors.items():
        logging.debug(f"Ticking {key} checkbox by its label (if necessary)")
        if form_details[key]:
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False)
            if not checkbox.get_property("checked"):
                checkbox.click()
