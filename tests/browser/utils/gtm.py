# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import selenium_action


def replace_string_representations(dictionary: dict) -> dict:
    result = {}
    for key, value in dictionary.items():
        if value == "None":
            result[key] = None
        elif value == "True":
            result[key] = True
        elif value == "False":
            result[key] = False
        elif value == "Empty string":
            result[key] = ""
        else:
            result[key] = value
    return result


def get_gtm_data_layer_properties(driver: WebDriver) -> dict:
    """
    WebDriver returns GTM data layer properties formatted like so:
    [
     {
      'event': 'gtm.js',
      'gtm.start': 1559324711826
     },
     {
      'businessUnit': 'International',
      'loginStatus': 'False',
      'siteLanguage': 'en-gb',
      'siteSection': 'Topic',
      'siteSubsection': 'ListingPage',
      'userId': 'None'
     }
    ]
    We're only interested in the seconds item.

    In order to make the result easier to work with, some extra parsing is done.
    Only if a value contains string representation of boolean & None type.
    """
    script_result = driver.execute_script("return window.dataLayer;")
    assert script_result, f"window.dataLayer on {driver.current_url} is empty!"

    data_layer_raw = {
        key: value
        for item in script_result
        for key, value in item.items()
        if "businessUnit" in item
    }

    return replace_string_representations(data_layer_raw)


def get_gtm_data_layer_events(driver: WebDriver, *, dedupe: bool = True) -> List[dict]:
    """Get all GTM events registered in window.dataLayer object.

    An example array of GTM events looks like this:
    [
    {gtm.start: 1561102115795, event: "gtm.js"},
    {pageCategory: "HomePage", site_section: "Great homepage", site_subsection: "", …},
    {event: "gaEvent", action: "Navigation", element: "HeaderMenuLink", value: "Advice"},
    ]

    This returns only items containing following fields: event, action & element.
    """
    script_result = driver.execute_script("return window.dataLayer;")
    assert script_result, f"window.dataLayer on {driver.current_url} is empty!"
    logging.debug(f"Contents of window.dataLayer: {script_result}")
    raw_events = [
        item
        for item in script_result
        if "event" in item and "action" in item and "element" in item
    ]
    result = [replace_string_representations(raw_event) for raw_event in raw_events]
    assert result, f"No GTM events were found on {driver.current_url}"
    logging.debug(f"All GTM events found on {driver.current_url}: {result}")
    if dedupe:
        result = [dict(tup) for tup in {tuple(item.items()) for item in result}]
        logging.debug(f"Unique GTM events found on {driver.current_url}: {result}")
    return result


def find_all_substring_indexes(string: str, substring: str) -> list:
    """Find indexes of all substring occurrences."""
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return
        yield start
        start += len(substring)


def get_dit_tagging_js_event_source_code(driver: WebDriver, package: str) -> str:
    """Return JS source code for specific DIT Tagging package"""
    packages = {"Domestic header": "domesticHeader", "Domestic pages": "domestic"}
    error = (
        f"'{package}' is not supported, please use one of the following: "
        f"{list(packages.keys())}"
    )
    assert package in packages, error
    return driver.execute_script(
        f"return dit.tagging.{packages[package]}.constructor.toString();"
    )


def get_event_details(raw_code: str) -> dict:
    """Find relevant event registration details in raw JS code,

    * element name ie. 'HeaderSignInLink'
    * event name i.e. 'gaEvent'
    * event action i.e. 'SignIn'
    * event type i.e. 'Account'

    PS. event value is omitted as it contains a CSS selector which refers to the element
    itself, i.e.: $(this).text()
    """
    key_index = 0
    value_index = 1
    return {
        line.strip().split(": ")[key_index]: line.strip().split(": ")[value_index]
        for line in raw_code.replace("'", "").replace(",", "").splitlines()
        if ":" in line and "value" not in line
    }


def get_all_raw_per_page_events(raw_code: str) -> dict:
    """Domestic Tagging defines events for multiple pages. This extracts them all."""
    result = {}
    function_signature_prefix = "function addTaggingFor"
    for signature in find_all_substring_indexes(raw_code, function_signature_prefix):
        signature_start = signature + len(function_signature_prefix)
        signature_end = raw_code.index("()", signature)
        page_name = raw_code[signature_start:signature_end]
        try:
            end_of_function = raw_code.index(function_signature_prefix, signature_end)
        except ValueError:
            end_of_function = len(raw_code)
        raw_function = raw_code[signature_start:end_of_function]
        result[page_name] = raw_function
    return result


def get_selector_and_on_what_action(raw_code: str) -> tuple:
    """Find event selector & triggering action in raw JS event registration code

    :return: ('#header-sign-in-link', 'click')
    """
    selector_line_start = "$("
    register_event_call = ").on("
    event_function_start = ", function"
    if ").on(" in raw_code.strip():
        selector_start = (
            raw_code.index(selector_line_start) + len(selector_line_start) + 1
        )
        selector_end = raw_code.index(register_event_call) - 1
        selector = raw_code[selector_start:selector_end]
        event_start = raw_code.index(register_event_call) + len(register_event_call) + 1
        event_end = raw_code.index(event_function_start) - 1
        event_action = raw_code[event_start:event_end]
        return selector, event_action
    else:
        return ()


def get_keypress_event_trigger_key(event: str) -> int:
    """Find the key number which triggers particular keypress event."""
    comparison_str = "e.which == "
    if comparison_str not in event:
        return -1
    comparison_start = event.index(comparison_str) + len(comparison_str)
    comparison_end = event.find(")", comparison_start)
    key = int(event[comparison_start:comparison_end])
    return key


def get_details_from_raw_events(event_group: str, events: str) -> dict:
    """Converts raw JS event definitions into a useful dict"""
    result = defaultdict(list)
    for on_offset in find_all_substring_indexes(events, ").on("):
        start = events.rfind("$(", 0, on_offset)
        end = events.find("});", on_offset)
        event = events[start:end]

        selector, on_what = get_selector_and_on_what_action(event)
        details = get_event_details(event)
        details["selector"] = selector
        details["on_what"] = on_what
        if on_what == "keypress":
            details["key"] = get_keypress_event_trigger_key(event)
        result[event_group].append(details)
    return dict(result)


def get_gtm_events_from_raw_js(raw_code: str) -> dict:
    """Parse raw JS event registration code & extract event details.

    An example jQuery event registration looks like this:

    $('#header-sign-in-link').on('click', function() {
        window.dataLayer.push({
          'event': 'gaEvent',
          'action': 'SignIn',
          'type': 'Account',
          'element': 'HeaderSignInLink'
        });
    });

    An example result will look like this:
    """
    result = defaultdict(list)
    # per page events defined in dit.tagging.{hash}.js
    if "function " in raw_code:
        raw_per_page_events = get_all_raw_per_page_events(raw_code)
        for page_name, events in raw_per_page_events.items():
            per_page_events = get_details_from_raw_events(page_name, events)
            result.update(per_page_events)
    else:
        # Domestic Header events defined in dit.tagging.domesticHeader.{hash}.js
        per_page_events = get_details_from_raw_events("Domestic Header", raw_code)
        result.update(per_page_events)
    return dict(result)


def get_gtm_event_definitions(
    driver: WebDriver, tagging_package: str, *, event_group: str = None
) -> dict:
    """Extracts details of all GTM events from a specific JS DIT tagging package.
    ATM. it supports both: dit.tagging.domestic & dit.tagging.domesticHeader packages

    If event_group is specified, then only matching event group is returned.

    Example output:
    {
        'MarketsLandingPage': [
            {
                'event': 'gaEvent',
                'action': 'Cta',
                'element': 'MarketCta',
                'selector': '#markets-list-section .card-link',
                'on_what': 'click'
            }
        ],
        'ArticleList': [
            {
                'event': 'gaEvent',
                'action': 'ContentLink',
                'type': '$(".article-list-page h1").text().trim()',
                'element': 'Article',
                'selector': '#article-list-page .article a',
                'on_what': 'click'
            }
        ],
        ...
    }
    """
    raw_code = get_dit_tagging_js_event_source_code(driver, tagging_package)
    result = get_gtm_events_from_raw_js(raw_code)
    assert result, f"No JS events found in '{tagging_package}' package"
    if event_group:
        result = {event_group: result[event_group]}
    logging.debug(f"JS events found in: '{tagging_package}' package: {result}")
    return result


def trigger_js_event(driver: WebDriver, event: dict):
    """Trigger an event without performing actual action."""
    selector = event["selector"]
    on_what = event["on_what"]
    if on_what == "keypress":
        key = event["key"]
        js = (
            f"""$('{selector}').trigger({{type:"keypress", which: {key}}});"""
        )  # fmt: off
    elif on_what == "submit":
        js = (
            f"""$('{selector}').get(0).dispatchEvent(new Event("submit"));"""
        )  # fmt: off
    elif on_what == "click":
        js = f"""$('{selector}').click();"""  # fmt: off
    else:
        raise KeyError(f"'{on_what}' events are not supported, yet!")
    action = event["action"]
    element = event["element"]
    logging.debug(
        f"Triggering '{on_what}' event for '{action}' in '{element}' found using "
        f"'{selector}'"
    )
    with selenium_action(
        driver, f"Failed to trigger '{on_what}' event for '{selector}'"
    ):
        driver.execute_script(js)
