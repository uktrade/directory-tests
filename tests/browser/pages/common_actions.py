# -*- coding: utf-8 -*-
"""Common PageObject actions."""
import hashlib
import io
import logging
import random
import string
import sys
import time
import traceback
import uuid
from collections import defaultdict, namedtuple
from contextlib import contextmanager
from io import BytesIO
from types import ModuleType
from typing import Dict, List, Union
from urllib.parse import urlparse

import requests
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import allure
from directory_tests_shared import URLs
from directory_tests_shared.exceptions import PageLoadTimeout, UnexpectedElementPresent
from directory_tests_shared.settings import (
    BARRED_USERS,
    BASICAUTH_PASS,
    BASICAUTH_USER,
    BROWSER,
    TAKE_SCREENSHOTS,
)
from directory_tests_shared.utils import access_was_denied, extract_attributes_by_css
from pages import ElementType
from PIL import Image

ScenarioData = namedtuple("ScenarioData", ["actors"])
Actor = namedtuple(
    "Actor",
    [
        "alias",
        "email",
        "password",
        "company_name",
        "article_category",
        "visited_articles",
        "case_study_title",
        "email_confirmation_link",
        "email_confirmation_code",
        "registered",
        "visited_page",
        "last_tag",
        "forms_data",
        "saved_progress_link",
    ],
)
Selector = namedtuple(
    "Selector",
    [
        "by",
        "value",
        "in_desktop",
        "in_mobile",
        "in_horizontal",
        "type",
        "is_visible",
        "group_id",
        "autocomplete_callback",
        "wait_after_click",
        "next_page",
        "alternative_visibility_check",
        "disabled",
    ],
)

# define default values for various named tuples
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
Selector.__new__.__defaults__ = (
    None,
    None,
    True,
    True,
    True,
    None,
    True,
    None,
    None,
    True,
    None,
    None,
    None,
)


def go_to_url(driver: WebDriver, url: str, page_name: str):
    """Go to the specified URL and take a screenshot afterwards."""
    driver.get(url)
    accept_all_cookies(driver)


def check_url(driver: WebDriver, expected_url: str, *, exact_match: bool = True):
    """Check if current page URL matches the expected one."""
    with assertion_msg(
        f"Expected page URL to be: '{expected_url}' but got '{driver.current_url}'"
    ):
        if exact_match:
            assert driver.current_url == expected_url
        else:
            assert (driver.current_url in expected_url) or (
                expected_url in driver.current_url
            )
    logging.debug(f"Current page URL matches expected '{driver.current_url}'")


def check_title(driver: WebDriver, expected_title: str, *, exact_match: bool = False):
    """Check if current page title matches the expected one."""
    with assertion_msg(
        f"Expected page title to be: '{expected_title}' but got '{driver.title}' on {driver.current_url}"
    ):
        if exact_match:
            assert expected_title.lower() == driver.title.lower()
        else:
            assert expected_title.lower() in driver.title.lower()
    logging.debug(
        f"Page title on '{driver.current_url}' matches expected '{expected_title}'"
    )


def check_for_expected_sections_elements(
    driver: WebDriver, sections: Dict[str, Selector]
):
    """Check if all elements in page sections are visible."""
    for section in sections:
        for element_name, selector in sections[section].items():
            if not isinstance(selector, Selector):
                raise TypeError(
                    f"Expected '{selector}' to be a Selector, got {type(selector)}"
                )
            element = find_element(driver, selector, element_name=element_name)
            if not selector.is_visible:
                logging.debug(f"Skipping '{element_name} as it's marked as invisible'")
                continue
            with assertion_msg(
                f"It looks like '{element_name}' element in '{section}' section is not visible on {driver.current_url}"
            ):
                assert element.is_displayed()
        logging.debug(f"All expected elements are visible on '{driver.current_url}'")


def find_and_click_on_page_element(
    driver: WebDriver, sections: dict, element_name: str, *, wait_for_it: bool = True
):
    """Find page element in any page section selectors and click on it."""
    found_selector = False
    for section_name, selectors in sections.items():
        if element_name.lower() in selectors:
            found_selector = True
            selector = selectors[element_name.lower()]
            logging.debug(
                f"Found selector for '{element_name}' in '{section_name}' section: "
                f"'{selector}'"
            )
            web_element = find_element(
                driver, selector, element_name=element_name, wait_for_it=wait_for_it
            )
            check_if_element_is_visible(web_element, element_name)
            if web_element.get_attribute("target") == "_blank":
                logging.debug(
                    f"'{web_element.text}' opens in new tab, but will "
                    f"forcefully open it in the same one"
                )
                with wait_for_page_load_after_action(driver):
                    href = web_element.get_attribute("href")
                    driver.get(href)
            else:
                scroll_to(driver, web_element)
                if selector.wait_after_click:
                    with wait_for_page_load_after_action(driver, timeout=10):
                        with try_alternative_click_on_exception(driver, web_element):
                            web_element.click()
                else:
                    with try_alternative_click_on_exception(driver, web_element):
                        web_element.click()
    with assertion_msg(f"Could not find '{element_name}' in any section"):
        assert found_selector


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data."""
    return ScenarioData(actors={})


def unauthenticated_actor(alias: str) -> Actor:
    """Create an instance of an unauthenticated Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
    """
    email = (
        "test+{}{}@ci.uktrade.io".format(alias, str(uuid.uuid4()))
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    letters = "".join(random.choice(string.ascii_letters) for _ in range(10))
    digits = "".join(random.choice(string.digits) for _ in range(10))
    password = f"{letters}{digits}"
    return Actor(alias=alias, email=email, password=password, visited_articles=[])


def barred_actor(alias: str) -> Actor:
    actor = unauthenticated_actor(alias)
    actor = actor._replace(**{"email": random.choice(BARRED_USERS)})
    return actor


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data."""
    assert isinstance(actor, Actor), (
        f"Expected Actor named tuple but got '{type(actor)}'" " instead"
    )
    context.scenario_data.actors[actor.alias] = actor
    logging.debug(f"Successfully added actor: {actor.alias} to Scenario Data")


def get_actor(context: Context, alias: str) -> Actor:
    """Get actor details from context Scenario Data."""
    return context.scenario_data.actors.get(alias)


def get_last_visited_page(context: Context, actor_alias: str) -> ModuleType:
    """Get last visited Page Object context Scenario Data."""
    actor = context.scenario_data.actors.get(actor_alias)
    assert actor, f"Check your scenario. There's no such actor as: {actor_alias}"
    return actor.visited_page


def get_full_page_name(page: ModuleType, *, page_sub_type: str = None) -> str:
    if page_sub_type:
        result = (
            f"{page.SERVICE.value} - {page.NAME} ({page_sub_type}) - {page.TYPE.value}"
        )
    else:
        result = f"{page.SERVICE.value} - {page.NAME} - {page.TYPE.value}"

    return result


def update_actor(context: Context, alias: str, **kwargs):
    """Update Actor's details stored in context.scenario_data"""
    actors = context.scenario_data.actors
    for arg in kwargs:
        if arg in Actor._fields:
            if isinstance(getattr(actors[alias], arg), list):
                logging.debug(f"Appended '{kwargs[arg]}' to '{arg}' for {alias}")
                new_value = getattr(actors[alias], arg)
                new_value.append(kwargs[arg])
            else:
                logging.debug(f"Set '{arg}'='{kwargs[arg]}' for {alias}")
                new_value = kwargs[arg]
            actors[alias] = actors[alias]._replace(**{arg: new_value})
    logging.debug(f"Successfully updated {alias}'s details: {actors[alias]}")


def update_actor_forms_data(context: Context, actor: Actor, form_data: dict):
    actor_forms_data = actor.forms_data
    page = actor.visited_page
    if not actor_forms_data:
        actor_forms_data = defaultdict()
    form_data_key = f"{page.SERVICE} - {page.NAME} - {page.TYPE}"
    actor_forms_data[form_data_key] = form_data
    update_actor(context, actor.alias, forms_data=actor_forms_data)


def avoid_browser_stack_idle_timeout_exception(driver: WebDriver):
    """BrowserStack will stop browser session after 90s of inactivity.

    In order to avoid it, this helper will generate random events, like scrolling
    """
    actions = {
        "scroll up": "window.scrollBy(0,-1000);",
        "scroll down": "window.scrollBy(0,1000);",
        "click on body": "document.querySelector('body').click();",
        "scroll to random link": "window.scrollTo(0, document.querySelectorAll('a')[Math.floor(Math.random()*document.querySelectorAll('a').length)].offsetTop);",  # noqa
    }
    action = random.choice(list(actions.keys()))
    message = f"Trigger '{action}' event to avoid 'Idle Timeout exception'"
    logging.debug(message)
    driver.execute_script(actions[action])


def convert_png_to_jpg(screenshot_png: bytes):
    raw_image = Image.open(io.BytesIO(screenshot_png))
    image = raw_image.convert("RGB")
    with BytesIO() as f:
        image.save(f, format="JPEG", quality=90)
        return f.getvalue()


def fullpage_screenshot(driver):
    """A fullscreen screenshot workaround for Chrome driver:

    This script uses a simplified version of the one here:
    https://snipt.net/restrada/python-selenium-workaround-for-full-page-screenshot-using-chromedriver-2x/
    It contains the *crucial* correction added in the comments by Jason Coutu.

    SRC: https://stackoverflow.com/q/41721734
    """
    logging.debug("Starting chrome full page screenshot workaround ...")

    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    logging.debug(
        f"Total: ({total_width}, {total_height}), "
        f"Viewport: ({viewport_width},{viewport_height})"
    )
    rectangles = []

    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height

        if top_height > total_height:
            top_height = total_height

        while ii < total_width:
            top_width = ii + viewport_width

            if top_width > total_width:
                top_width = total_width

            logging.debug(f"Appending rectangle ({ii},{i},{top_width},{top_height})")
            rectangles.append((ii, i, top_width, top_height))

            ii = ii + viewport_width

        i = i + viewport_height

    stitched_image = Image.new("RGB", (total_width, total_height))
    previous = None
    part = 0

    for rectangle in rectangles:
        if previous is not None:
            driver.execute_script(f"window.scrollTo({rectangle[0]}, {rectangle[1]})")
            logging.debug(f"Scrolled To ({rectangle[0]},{rectangle[1]})")
            time.sleep(0.2)

        screenshot_png = driver.get_screenshot_as_png()
        screenshot = Image.open(io.BytesIO(screenshot_png))

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        logging.debug(
            f"Adding to stitched image with offset ({offset[0]}, {offset[1]})"
        )
        stitched_image.paste(screenshot, offset)

        del screenshot
        part = part + 1
        previous = rectangle

    logging.debug("Finishing chrome full page screenshot workaround...")
    with BytesIO() as f:
        stitched_image.save(f, format="JPEG", quality=90)
        return f.getvalue()


@retry(stop_max_attempt_number=3)
def take_screenshot(driver: WebDriver, page_name: str = None):
    """Will take a screenshot of current page."""
    if TAKE_SCREENSHOTS:
        if BROWSER == "firefox":
            # Ref: https://stackoverflow.com/a/52572919/
            original_size = driver.get_window_size()
            required_width = driver.execute_script(
                "return document.body.parentNode.scrollWidth"
            )
            required_height = driver.execute_script(
                "return document.body.parentNode.scrollHeight"
            )
            driver.set_window_size(required_width, required_height)

            element = driver.find_element_by_tag_name("body")
            screenshot_png = element.screenshot_as_png
            screenshot_jpg = convert_png_to_jpg(screenshot_png)
        elif BROWSER == "chrome":
            screenshot_jpg = fullpage_screenshot(driver)

        if page_name:
            page_name = page_name.lower().replace(" ", "_")[0:200]
        allure.attach(
            screenshot_jpg,
            name=page_name or "screenshot.jpg",
            attachment_type=allure.attachment_type.JPG,
        )
        if BROWSER == "firefox":
            driver.set_window_size(original_size["width"], original_size["height"])
    else:
        logging.debug(
            f"Taking screenshots is disabled. In order to turn it on "
            f"please set an environment variable TAKE_SCREENSHOTS=true"
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
        if len(sys._current_frames()) == 1:
            print(f"Found 'shallow' Traceback, will inspect outer traceback frames")
            import inspect

            for f in inspect.getouterframes(sys._getframe(0)):
                print(f"{f.filename} +{f.lineno} - in {f.function}")
                if "_def.py" in f.filename:
                    break
        traceback.print_tb(tb)
        raise


@contextmanager
def selenium_action(driver: WebDriver, message: str, screenshot: bool = True, *args):

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
        print(f"{info} - {message}")
        logging.debug(f"{info} - {message}")
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        if screenshot:
            take_screenshot(driver, message)
        raise


def wait_for_element_visibility(
    driver: WebDriver, element: WebElement, *, time_to_wait: int = 3
):
    """Wait until element is visible."""
    with selenium_action(
        driver,
        (
            f"({element.tag_name}) Element identified by '{element}' was not visible after waiting "
            f"for {time_to_wait} seconds"
        ),
    ):
        WebDriverWait(driver, time_to_wait).until(
            expected_conditions.visibility_of(element)
        )


def wait_for_visibility(
    driver: WebDriver, selector: Selector, *, time_to_wait: int = 5
):
    """Wait until element is visible."""
    by_locator = (selector.by, selector.value)
    with selenium_action(
        driver,
        (
            f"Element identified by '{selector.value}' was not visible after waiting "
            f"for {time_to_wait} seconds"
        ),
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
        f"Expected not to find '{element_name}' element identified by '{selector.value}' on {driver.current_url}"
    ):
        assert not found


def is_element_present(driver: WebDriver, selector: Selector) -> bool:
    """Check if sought element is present"""
    try:
        elements = driver.find_elements(by=selector.by, value=selector.value)
        if elements:
            logging.debug(f"Found following elements: {elements}")
            found = True
        else:
            found = False
    except NoSuchElementException:
        found = False
    return found


def check_if_element_is_visible(web_element: WebElement, element_name: str):
    """Check if provided web element is visible."""
    with assertion_msg(
        f"Expected to see '{element_name}' element but it's not visible"
    ):
        assert web_element.is_displayed()


def check_if_element_is_not_visible(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
    take_screenshot: bool = True,
):
    """Find element by CSS selector or it's ID."""
    try:
        element = find_element(
            driver,
            selector,
            element_name=element_name,
            wait_for_it=wait_for_it,
            take_screenshot=take_screenshot,
        )
        with assertion_msg(
            f"Expected not to see '{element_name}' element identified by '{selector.value}' on {driver.current_url}"
        ):
            assert not element.is_displayed()
    except NoSuchElementException:
        logging.debug(f"As expected '{element_name}' is not present")
        pass


def check_if_element_is_disabled(web_element: WebElement, element_name: str):
    """Check if provided web element is disabled."""
    with assertion_msg(
        f"Expected '{element_name}' element to be disabled but it's not"
    ):
        assert not web_element.is_enabled()
    logging.debug(f"As expected '{element_name}' field is disabled.")


def run_alternative_visibility_check(
    driver: WebDriver,
    element_name: str,
    selector: Selector,
    *,
    element: WebElement = None,
    take_screenshot: bool = True,
):
    element = element or find_element(driver, selector)
    location = element.location
    size = element.size
    if not all(location.values()) or not all(size.values()):
        take_screenshot(driver, f"{element_name}_is_not_visible")
    with assertion_msg(
        f"It looks like '{element_name}' element identified by '{selector.by} →"
        f" {selector.value}' selector is not visible on "
        f"{driver.current_url} as it's location is outside viewport: "
        f"{location}"
    ):
        assert all(location.values())
    with assertion_msg(
        f"It looks like '{element_name}' element identified by '{selector.by} →"
        f" {selector.value}' selector is not visible on "
        f"{driver.current_url} is it's size dimensions are zeroed: "
        f"{size}"
    ):
        assert all(size.values())
    logging.debug(
        f"Visibility of '{element_name} → {selector.by} → {selector.value}' "
        f"was confirmed with an alternative check"
    )


def find_element(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
    take_screenshot: bool = True,
) -> WebElement:
    """Find element by CSS selector or it's ID."""
    with selenium_action(
        driver,
        f"Could not find element called '{element_name}' using selector "
        f"'{selector.value}' on {driver.current_url}",
        screenshot=take_screenshot,
    ):
        element = driver.find_element(by=selector.by, value=selector.value)
    if wait_for_it and selector.is_visible:
        wait_for_visibility(driver, selector)
    if selector.disabled:
        check_if_element_is_disabled(element, element_name)
    elif selector.alternative_visibility_check:
        run_alternative_visibility_check(
            driver,
            element_name,
            selector,
            element=element,
            take_screenshot=take_screenshot,
        )

    return element


def find_selector_by_name(selectors: dict, name: str) -> Selector:
    found_selectors = [
        selector
        for section_selectors in selectors.values()
        for selector_name, selector in section_selectors.items()
        if selector_name.lower() == name.lower()
    ]
    assert len(found_selectors) == 1
    return found_selectors[0]


def find_elements(driver: WebDriver, selector: Selector) -> List[WebElement]:
    """Find element by CSS selector or it's ID."""
    with selenium_action(driver, f"Couldn't find elements using '{selector.value}'"):
        elements = driver.find_elements(by=selector.by, value=selector.value)
    return elements


def check_hash_of_remote_file(expected_hash: str, file_url: str):
    """Check if the md5 hash of the file is the same as expected."""
    from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER

    logging.debug("Fetching file: %s", file_url)
    parsed = urlparse(file_url)
    with_creds = f"{parsed.scheme}://{BASICAUTH_USER}:{BASICAUTH_PASS}@{parsed.netloc}{parsed.path}"
    response = requests.get(with_creds)
    logging.debug(f"Got {response.status_code} from {file_url}")
    assert response.status_code == 200
    file_hash = hashlib.md5(response.content).hexdigest()
    with assertion_msg(
        f"Expected hash of file downloaded from {file_url} to be {expected_hash} but got {file_hash}"
    ):
        assert expected_hash == file_hash


@contextmanager
def scroll_to_element_if_not_visible(
    driver: WebDriver, element: WebElement, *, section: str = None, name: str = None
):
    """Scroll to element only if it's not visible.

    Delaying scrolling to every element can save around 100ms per element.
    """
    try:
        yield
    except TimeoutException as e:
        if section and name:
            logging.debug(f"Scrolling/Moving focus to '{section} → {name}' element")
        else:
            logging.warning(
                f"Element is not visible, will scroll to it & check it's visibility: "
                f"{e.msg}"
            )
        scroll_to(driver, element)
        error = (
            f"Element '{name or element.tag_name}' is not visible even after scrolling "
            f"to it"
        )
        assert element.is_displayed(), error


@contextmanager
def try_alternative_click_on_exception(driver: WebDriver, element: WebElement):
    """Try alternative click methods (JS or ActionChains) if regular way didn't work.

    JS workaround:
        Handle situations when clicking on element triggers:
        selenium.common.exceptions.ElementClickInterceptedException:
            Message: element click intercepted:
            Element <input id="id_terms"> is not clickable at point (714, 1235).
            Other element would receive the click: <label for="id_terms">...</label>
        See: https://stackoverflow.com/a/44916498

    ActionChains workaround:
        Handles situations when clicking on element triggers:
        selenium.common.exceptions.ElementNotInteractableException:
        Message: Element <a href="..."> could not be scrolled into view
        See: https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains
    """
    try:
        yield
    except ElementClickInterceptedException as e:
        logging.warning(
            f"Failed click intercepted. Will try JS workaround for: {e.msg}"
        )
        driver.execute_script("arguments[0].click();", element)
    except ElementNotInteractableException as e:
        logging.warning(
            f"Failed click intercepted. Will try ActionChains workaround for: {e.msg}"
        )
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element)
        action_chains.click()
        action_chains.perform()
        logging.warning(f"ActionChains click workaround is done")


class wait_for_page_load_after_action(object):
    """Context manager for waiting the page to load.
    Proved to be a more reliable than wait_for_page_load() ^^^
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    https://www.develves.net/blogs/asd/2017-03-04-selenium-waiting-for-page-load/
    """

    def __init__(self, driver: WebDriver, *, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name("html")

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_tag_name("html")
        has_loaded = new_page.id != self.old_page.id
        if has_loaded:
            logging.debug(f"Page has loaded. {self.driver.current_url}")
        else:
            logging.debug(f"Waiting for {self.driver.current_url} page to load...")
        return has_loaded

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    def wait_for(self, condition_function):
        import time

        start_time = time.time()
        while time.time() < start_time + self.timeout:
            if condition_function():
                return True
            else:
                time.sleep(0.5)
        raise PageLoadTimeout(
            f"Timed out after {self.timeout}s of waiting for the new page to load"
        )


def scroll_to(driver: WebDriver, element: WebElement):
    if "firefox" in driver.capabilities["browserName"].lower():
        view_port_height = int(driver.execute_script("return window.innerHeight;"))
        vertical_position = int(element.location["y"])
        if vertical_position > view_port_height:
            logging.debug(f"Scrolling to y={vertical_position}")
            driver.execute_script(f"window.scrollTo(0, {vertical_position});")
        else:
            logging.debug(
                f"Element is already positioned ({vertical_position}) within view_port "
                f"({view_port_height})"
            )
        if not element.is_displayed():
            logging.debug(f"Scrolling to element using scrollIntoView: {element}")
            driver.execute_script(f"arguments[0].scrollIntoView(true);", element)
    else:
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element)
        action_chains.perform()


def check_for_sections(
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
                "Please choose from desktop, mobile or horizontal (mobile) selectors"
            )
        for key, selector in selectors.items():
            with selenium_action(
                driver,
                f"Could not find element: '{key} → {selector.by} → {selector.value}'"
                f" on {driver.current_url}",
            ):
                element = driver.find_element(by=selector.by, value=selector.value)
            if selector.is_visible:
                with scroll_to_element_if_not_visible(
                    driver, element, section=name, name=key
                ):
                    wait_for_element_visibility(driver, element)
                logging.debug(f"'{key} → {selector.by} → {selector.value}' is visible")
            else:
                if selector.alternative_visibility_check:
                    run_alternative_visibility_check(
                        driver, key, selector, element=element
                    )
                else:
                    logging.debug(
                        f"Skipping visibility check for '{key} → {selector.by} → "
                        f"{selector.value}' as its selector is flagged as not visible"
                    )


def get_desktop_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_desktop}


def get_mobile_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_mobile}


def get_horizontal_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector for key, selector in section.items() if selector.in_horizontal
    }


def get_selectors(section: dict, element_type: ElementType) -> Dict[str, Selector]:
    return {
        key: selector
        for key, selector in section.items()
        if selector.type == element_type
    }


def find_elements_of_type(
    driver: WebDriver, section: dict, element_type: ElementType
) -> defaultdict:
    selectors = get_selectors(section, element_type)
    result = defaultdict()
    for key, selector in selectors.items():
        element = find_element(driver, selector, element_name=key, wait_for_it=False)
        result[key] = element
    return result


def selectors_by_group(form_selectors: Dict[str, Selector]) -> Dict[str, Selector]:
    groups = defaultdict(lambda: defaultdict(dict))
    for key, selector in form_selectors.items():
        if selector.group_id:
            groups[selector.group_id][key] = selector
        else:
            groups["default"][key] = selector

    return groups


def assert_catcha_in_dev_mode(driver: WebDriver):
    dev_site_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    try:
        g_recaptcha = find_element(
            driver,
            Selector(By.CSS_SELECTOR, ".g-recaptcha"),
            element_name="captcha",
            wait_for_it=False,
        )
    except NoSuchElementException:
        logging.debug(f"Captcha is not present on {driver.current_url}")
    else:
        scroll_to(driver, g_recaptcha)
        current_site_key = g_recaptcha.get_attribute("data-sitekey")
        logging.debug(f"Current site captcha key: {current_site_key}")
        is_in_dev_mode = current_site_key == dev_site_key
        if not is_in_dev_mode:
            raise UnexpectedElementPresent(
                f"Captcha is not in Dev Mode on {driver.current_url}"
            )
        logging.debug(f"Captcha is in Dev mode on {driver.current_url}")


def tick_captcha_checkbox(driver: WebDriver):
    im_not_a_robot = Selector(By.CSS_SELECTOR, "#recaptcha-anchor")
    iframe = driver.find_element_by_tag_name("iframe")
    scroll_to(driver, iframe)
    driver.switch_to.frame(iframe)
    captcha = find_element(driver, im_not_a_robot)
    captcha.click()
    # wait 4s after user clicks on the CAPTCHA checkbox
    # otherwise the test might fail
    time.sleep(4)
    driver.switch_to.parent_frame()


def fill_out_input_fields(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    input_selectors = get_selectors(form_selectors, ElementType.INPUT)
    for key, selector in input_selectors.items():
        value_to_type = form_details.get(key, None)
        if isinstance(value_to_type, bool):
            if value_to_type and selector.autocomplete_callback:
                logging.debug(
                    f"value_to_type=True. Will call autocomplete_callback() for"
                    f" '{key}'"
                )
                selector.autocomplete_callback(driver, value=value_to_type)
        else:
            if not value_to_type:
                logging.debug(f"Skipping '{key}' as there no value for it")
                continue
            logging.debug(
                f"Filling out input field '{key}' with '{value_to_type}' on '{driver.current_url}"
            )
            input_field = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if input_field.is_displayed():
                input_field.clear()
            input_field.send_keys(value_to_type)
            if selector.autocomplete_callback:
                logging.debug(f"Calling autocomplete_callback() for '{key}'")
                selector.autocomplete_callback(driver, value=value_to_type)


def fill_out_textarea_fields(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    textarea_selectors = get_selectors(form_selectors, ElementType.TEXTAREA)
    for key, selector in textarea_selectors.items():
        value_to_type = form_details.get(key)
        if not value_to_type:
            logging.debug(f"Skipping '{key}' as there no value for it")
            continue
        logging.debug(f"Filling out textarea: {key} with '{value_to_type}'")
        textarea = find_element(driver, selector, element_name=key, wait_for_it=False)
        if textarea.is_displayed():
            textarea.clear()
        textarea.send_keys(value_to_type)


def check_form_choices(
    driver: WebDriver, form_selectors: Dict[str, Selector], names: List[str]
):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    for name in names:
        radio_selector = radio_selectors[name.lower()]
        find_element(driver, radio_selector, element_name=name, wait_for_it=False)
    logging.debug(
        f"All expected form choices: '{names}' are visible on " f"{driver.current_url}"
    )


def get_option_values(
    driver: WebDriver, selector: Selector, *, remove_empty_values: bool = True
) -> List[str]:
    error = f"'{selector.by}' not recognised. Only By.ID, By.CSS_SELECTOR are allowed"
    assert selector.by in (By.ID, By.CSS_SELECTOR), error
    if selector.by == By.ID:
        option_selector = f"#{selector.value} option"
    else:
        option_selector = f"{selector.value} option"
    logging.debug(f"Looking for option values using: '{option_selector}'")
    option_values = extract_attributes_by_css(
        driver.page_source, option_selector, attrs=["value"], text=False
    )
    if remove_empty_values:
        option_values = [item for item in option_values if item["value"]]
    logging.debug(f"Available options: {option_values}")
    return [item["value"] for item in option_values]


def pick_option(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    select_selectors = get_selectors(form_selectors, ElementType.SELECT)
    for key, selector in select_selectors.items():
        if form_details.get(key, None):
            option = form_details[key]
        else:
            logging.debug(
                f"Picking an option from '{key}' dropdown list using: {selector}"
            )
            values = get_option_values(driver, selector)
            option = random.choice(values)
        logging.debug(f"Will select option: {option}")
        if selector.autocomplete_callback:
            logging.debug(f"Calling autocomplete_callback() for '{key}'")
            selector.autocomplete_callback(driver, value=option)
        else:
            select = find_element(driver, selector, element_name=key, wait_for_it=False)
            option_value_selector = f"option[value='{option}']"
            option_element = select.find_element_by_css_selector(option_value_selector)
            with try_alternative_click_on_exception(driver, option_element):
                option_element.click()


def check_radio(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    for key, selector in radio_selectors.items():
        assert key in form_details, f"Can't find form detail for '{key}'"
        if form_details[key]:
            radio = find_element(driver, selector, element_name=key, wait_for_it=False)
            if not radio.get_property("checked"):
                logging.debug(f"Checking '{key}' radio")
                radio.click()


def check_random_radio(driver: WebDriver, form_selectors: Dict[str, Selector]):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    grouped_selectors = selectors_by_group(radio_selectors)
    for group, selectors in grouped_selectors.items():
        logging.debug(f"Selecting random radio option from group: {group}")
        key = random.choice(list(selectors.keys()))
        selector = radio_selectors[key]
        radio = find_element(driver, selector, element_name=key, wait_for_it=False)
        if not radio.get_property("checked"):
            logging.debug(f"Checking '{key}' radio")
            radio.click()


def choose_one_form_option(
    driver: WebDriver, radio_selectors: Dict[str, Selector], name: str
):
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key] = key == name.lower()
    logging.debug(f"Form details: {form_details}")
    check_radio(driver, radio_selectors, form_details)


def choose_one_form_option_except(
    driver: WebDriver, radio_selectors: Dict[str, Selector], ignored: List[str]
) -> str:
    all_keys = list(radio_selectors.keys())
    without_ignored = list(set(all_keys) - set(ignored))
    selected = random.choice(without_ignored)
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key.lower()] = key.lower() == selected
    logging.debug(f"Form details (with ignored: {ignored}): {form_details}")
    check_radio(driver, radio_selectors, form_details)
    return selected


def submit_form(
    driver: WebDriver,
    form_selectors: Dict[str, Selector],
    *,
    wait_for_new_page_to_load: bool = True,
) -> Union[ModuleType, None]:
    submit_selectors = get_selectors(form_selectors, ElementType.SUBMIT)

    error = (
        f"Expected to find exactly 1 submit element in form on {driver.current_url} "
        f"instead we got {len(submit_selectors)}"
    )
    with assertion_msg(error):
        assert len(submit_selectors) == 1

    submit_button_selector = list(submit_selectors.values())[0]

    submit_button = find_element(
        driver, submit_button_selector, element_name="submit button", wait_for_it=False
    )
    take_screenshot(driver, "Before submitting the form")
    if wait_for_new_page_to_load:
        with wait_for_page_load_after_action(driver, timeout=25):
            with try_alternative_click_on_exception(driver, submit_button):
                submit_button.click()
    else:
        with try_alternative_click_on_exception(driver, submit_button):
            submit_button.click()
    take_screenshot(driver, "After submitting the form")

    return submit_button_selector.next_page


def pick_one_option_and_submit(
    driver: WebDriver,
    form_selectors: Dict[str, Selector],
    name: str,
    *,
    submit_button_name: str = "submit",
) -> Union[ModuleType, None]:
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    selector = radio_selectors[name.lower()]
    choose_one_form_option(driver, radio_selectors, name)
    take_screenshot(driver, f"Before submitting the form - {name}")
    submit_button_selector = form_selectors[submit_button_name]
    button = find_element(
        driver, submit_button_selector, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, f"After submitting the form - {name}")
    return selector.next_page


def tick_checkboxes(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    checkbox_selectors = get_selectors(form_selectors, ElementType.CHECKBOX)
    for key, selector in checkbox_selectors.items():
        checkbox_value = form_details.get(key)
        if checkbox_value is None:
            logging.debug(f"Skipping '{key}' as there no value for it")
            continue
        logging.debug(f"Will tick off '{key}' checkbox (if necessary)")
        if checkbox_value:
            if not isinstance(checkbox_value, bool):
                logging.debug(f"Will select checkbox with '{checkbox_value}' value")
                selector = Selector(
                    By.CSS_SELECTOR, f"{selector.value}[value={checkbox_value}]"
                )
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if not checkbox.get_property("checked"):
                with try_alternative_click_on_exception(driver, checkbox):
                    checkbox.click()


def tick_checkboxes_by_labels(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    checkbox_selectors = get_selectors(form_selectors, ElementType.LABEL)
    for key, selector in checkbox_selectors.items():
        if form_details[key]:
            logging.debug(f"'{key}' checkbox should be ticked")
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if not checkbox.get_property("checked"):
                logging.debug(f"'{key}' checkbox is not ticked, checking it")
                with try_alternative_click_on_exception(driver, checkbox):
                    checkbox.click()
        else:
            logging.debug(f"'{key}' checkbox should be left unchanged")
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if checkbox.get_property("checked"):
                logging.debug(f"'{key}' checkbox is ticked, unchecking it")
                with try_alternative_click_on_exception(driver, checkbox):
                    checkbox.click()


def untick_selected_checkboxes(driver: WebDriver, selector: Selector):
    checkboxes = find_elements(driver, selector)
    logging.debug(f"There are {len(checkboxes)} checkboxes on {driver.current_url}")
    for checkbox in checkboxes:
        if checkbox.get_property("checked"):
            logging.debug(
                f"Unticking checkbox {checkbox.get_attribute('value') or checkbox.get_attribute('id')}"
            )
            with try_alternative_click_on_exception(driver, checkbox):
                checkbox.click()


def accept_all_cookies(driver: WebDriver):
    from pages import common_selectors

    accept = common_selectors.COOKIE_BANNER["cookie banner"]["accept all cookies"]
    banner_selector = common_selectors.COOKIE_BANNER["cookie banner"]["banner"]
    if is_element_present(driver, banner_selector):
        banner = driver.find_element_by_css_selector(banner_selector.value)
        if banner.is_displayed():
            logging.debug("Accepting all cookies")
            button = driver.find_element_by_css_selector(accept.value)
            button.click()
        else:
            logging.debug("Cookie banner is not visible")
    else:
        logging.debug("Cookie banner is not present")


def generic_set_basic_auth_creds(driver: WebDriver, *, service_name: str = None):
    if service_name == "ERP":
        base_url = URLs.ERP_LANDING.absolute
    else:
        base_url = URLs.DOMESTIC_LANDING.absolute
    parsed = urlparse(base_url)
    with_creds = f"{parsed.scheme}://{BASICAUTH_USER}:{BASICAUTH_PASS}@{parsed.netloc}/automated-test-auth"
    logging.debug(f"Doing basic auth")
    with wait_for_page_load_after_action(driver):
        driver.get(with_creds)
    assertion_msg = f"Access is still denied after authentication attempt → {base_url}"
    with selenium_action(driver, assertion_msg):
        assert "ok" in driver.page_source


def revisit_page_on_access_denied(driver: WebDriver, page: ModuleType, page_name: str):
    if access_was_denied(driver.page_source):
        logging.debug(
            f"Access Denied. Trying to re-authenticate on '{page_name}' {page.URL}"
        )
        generic_set_basic_auth_creds(driver)
        driver.get(page.URL)
