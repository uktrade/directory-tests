# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random
from inspect import signature
from types import MethodType
from typing import Dict
from urllib.parse import urljoin, urlparse

from behave.model import Table
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.gov_notify import (
    get_email_verification_code,
    get_verification_link,
)
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER
from directory_tests_shared.utils import check_for_errors
from pages import (
    common_language_selector,
    domestic,
    erp,
    fas,
    get_page_object,
    profile,
    soo,
    sso,
)
from pages.common_actions import (
    add_actor,
    avoid_browser_stack_idle_timeout_exception,
    barred_actor,
    find_and_click_on_page_element,
    find_elements,
    find_selector_by_name,
    get_actor,
    get_full_page_name,
    get_last_visited_page,
    go_to_url,
    scroll_to,
    selenium_action,
    take_screenshot,
    try_alternative_click_on_exception,
    unauthenticated_actor,
    untick_selected_checkboxes,
    update_actor,
    update_actor_forms_data,
    wait_for_page_load_after_action,
)
from steps import has_action
from utils.cms_api import get_news_articles
from utils.gtm import get_gtm_event_definitions, trigger_js_event

NUMBERS = {
    "random": 0,
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
}


def retry_if_webdriver_error(exception):
    """Return True if we should retry on WebDriverException, False otherwise"""
    return isinstance(exception, (TimeoutException, WebDriverException))


def retry_if_assertion_error(exception):
    """Return True if we should retry on AssertionError, False otherwise"""
    return isinstance(exception, AssertionError)


def generic_set_basic_auth_creds(context: Context, page_name: str):
    driver = context.driver
    page = get_page_object(page_name)
    parsed = urlparse(page.URL)
    with_creds = f"{parsed.scheme}://{BASICAUTH_USER}:{BASICAUTH_PASS}@{parsed.netloc}{parsed.path}"
    if with_creds.endswith("/"):
        with_creds += "automated-test-auth"
    else:
        with_creds += "/automated-test-auth"
    logging.debug(f"Visiting {page.URL} in order to pass basic auth")
    with wait_for_page_load_after_action(driver):
        driver.get(with_creds)
    with selenium_action(driver, f"Request to {driver.current_url} was blocked"):
        assert "Access Denied" not in driver.page_source


# BrowserStack times out after 60 seconds of inactivity
# https://www.browserstack.com/automate/timeouts
@retry(
    wait_fixed=5000,
    stop_max_attempt_number=5,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def visit_page(context: Context, actor_alias: str, page_name: str):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """

    def is_special_case(page_name: str) -> bool:
        parts = page_name.split(" - ")
        return len(parts) == 3

    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))

    page = get_page_object(page_name)

    has_action(page, "visit")

    if is_special_case(page_name) and hasattr(page, "SubURLs"):
        subpage_name = page_name.split(" - ")[1].lower()
        special_url = page.SubURLs[subpage_name]
        logging.debug(
            f"{actor_alias} will visit '{page_name}' subpage using: '{special_url}"
        )
        page.visit(context.driver, page_name=subpage_name)
    else:
        logging.debug(
            f"{actor_alias} will visit '{page_name}' page using: '{page.URL}'"
        )
        page.visit(context.driver)

    check_for_errors(context.driver.page_source, context.driver.current_url)
    update_actor(context, actor_alias, visited_page=page)
    take_screenshot(context.driver, page_name)


def set_small_screen(context: Context):
    context.driver.set_window_position(0, 0)
    context.driver.set_window_size(768, 1024)


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    if "access denied" in context.driver.page_source.lower():
        logging.debug(f"Trying to re-authenticate on '{page_name}' {page.URL}")
        generic_set_basic_auth_creds(context, page_name)
        context.driver.get(page.URL)
        error = f"Got blocked again on {context.driver.current_url}"
        assert "access denied" not in context.driver.page_source.lower(), error
    check_for_errors(context.driver.page_source, context.driver.current_url)
    has_action(page, "should_be_here")
    take_screenshot(context.driver, page_name)
    if hasattr(page, "SubURLs"):
        special_page_name = page_name.split(" - ")[1].lower()
        if signature(page.should_be_here).parameters.get("page_name"):
            page.should_be_here(context.driver, page_name=special_page_name)
        else:
            raise TypeError(
                f"{page.__name__}.should_be_here() doesn't accept 'page_name' keyword "
                f"argument but it should as this Page Object has 'SubURLs' attribute."
            )
    else:
        page.should_be_here(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(
        f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> " f"{page}"
    )


def articles_open_any(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_article")
    article_name = page.open_any_article(context.driver)
    update_actor(context, actor_alias, visited_articles=article_name)
    logging.info(f"{actor_alias} opened article: {article_name}")


def registration_should_get_verification_email(context: Context, actor_alias: str):
    """Will check if the Exporter received an email verification message."""
    logging.debug("Searching for an email verification message...")
    actor = get_actor(context, actor_alias)
    link = get_verification_link(actor.email)
    update_actor(context, actor_alias, email_confirmation_link=link)


def generic_get_verification_code(
    context: Context, actor_alias: str, *, resent_code: bool = False
):
    """Will check if the Exporter received an email verification message."""
    logging.debug("Searching for an email verification message...")
    actor = get_actor(context, actor_alias)
    code = get_email_verification_code(actor.email, resent_code=resent_code)
    update_actor(context, actor_alias, email_confirmation_code=code)


def registration_open_email_confirmation_link(context: Context, actor_alias: str):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.
    """
    actor = get_actor(context, actor_alias)
    link = actor.email_confirmation_link

    # Step 1 - open confirmation link
    context.driver.get(link)

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    sso.confirm_your_email.should_be_here(context.driver)
    logging.debug("Supplier is on the SSO Confirm your email address page")


def registration_submit_form_and_verify_account(
    context: Context, actor_alias: str, *, fake_verification: bool = True
):
    actor = get_actor(context, actor_alias)

    generic_fill_out_and_submit_form(
        context, actor_alias, custom_details_table=context.table
    )

    if fake_verification:
        sso.common.verify_account(actor.email)
    else:
        registration_should_get_verification_email(context, actor_alias)
        registration_open_email_confirmation_link(context, actor_alias)
        sso.confirm_your_email.submit(context.driver)
    update_actor(context, actor_alias, registered=True)


def registration_create_and_verify_account(
    context: Context, actor_alias: str, *, fake_verification: bool = True
):
    visit_page(context, actor_alias, "SSO - Registration")
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=fake_verification
    )


def clear_the_cookies(context: Context, actor_alias: str):
    try:
        cookies = context.driver.get_cookies()
        logging.debug("COOKIES: %s", cookies)
        context.driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies for %s", actor_alias)
        cookies = context.driver.get_cookies()
        logging.debug("Driver cookies after clearing them: %s", cookies)
    except WebDriverException:
        logging.error("Failed to clear cookies for %s", actor_alias)


def sign_in(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sso.sign_in.visit(context.driver)
    sso.sign_in.should_be_here(context.driver)
    sso.sign_in.fill_out(context.driver, email, password)
    sso.sign_in.submit(context.driver)
    check_for_errors(context.driver.page_source, context.driver.current_url)


def sign_out(context: Context, actor_alias: str):
    domestic.actions.go_to_sign_out(context.driver)
    sso.sign_out.submit(context.driver)
    logging.debug("%s signed out", actor_alias)


# BrowserStack times out after 60 seconds of inactivity
# https://www.browserstack.com/automate/timeouts
@retry(wait_fixed=10000, stop_max_attempt_number=3)
def articles_share_on_social_media(
    context: Context, actor_alias: str, social_media: str
):
    avoid_browser_stack_idle_timeout_exception(context.driver)
    context.article_url = context.driver.current_url
    if social_media.lower() == "email":
        domestic.advice_article.check_if_link_opens_email_client(context.driver)
    else:
        domestic.advice_article.check_if_link_opens_new_tab(
            context.driver, social_media
        )
        if not social_media.lower() == "linkedin":
            domestic.advice_article.share_via(context.driver, social_media)
    logging.debug(
        "%s successfully got to the share article on '%s'", actor_alias, social_media
    )


def promo_video_watch(context: Context, actor_alias: str, *, play_time: int = None):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "play_video")
    page.play_video(context.driver, play_time=play_time)
    logging.debug("%s was able to play the video", actor_alias)


def promo_video_close(context: Context, actor_alias: str):
    domestic.home.close_video(context.driver)
    logging.debug("%s closed the video", actor_alias)


def language_selector_close(context: Context, actor_alias: str):
    logging.debug("%s decided to close language selector", actor_alias)
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.close(context.driver, page=page)


def language_selector_open(
    context: Context, actor_alias: str, *, with_keyboard: bool = False
):
    logging.debug("%s decided to go open language selector", actor_alias)
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.open(
        context.driver, page=page, with_keyboard=with_keyboard
    )


def language_selector_navigate_through_links_with_keyboard(
    context: Context, actor_alias: str
):
    logging.debug(
        "%s decided to navigate through all language selector links with" " keyboard",
        actor_alias,
    )
    page = get_last_visited_page(context, actor_alias)
    common_language_selector.navigate_through_links_with_keyboard(
        context.driver, page=page
    )


def language_selector_change_to(
    context: Context, actor_alias: str, preferred_language: str
):
    page = get_last_visited_page(context, actor_alias)
    logging.debug(
        f"{actor_alias} decided to change language on {visit_page} to"
        f" {preferred_language}"
    )
    common_language_selector.open(context.driver, page=page)
    common_language_selector.change_to(context.driver, page, preferred_language)


def click_on_page_element(
    context: Context, actor_alias: str, element_name: str, *, page_name: str = None
):
    if page_name:
        page = get_page_object(page_name)
    else:
        page = get_last_visited_page(context, actor_alias)
    find_and_click_on_page_element(context.driver, page.SELECTORS, element_name)
    logging.debug(
        "%s decided to click on '%s' on '%s' page", actor_alias, element_name, page.NAME
    )


def fas_search_for_companies(
    context: Context, actor_alias: str, *, keyword: str = None, sector: str = None
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "search")
    optional_parameter_keywords = ["n/a", "no", "empty", "without", "any"]
    if keyword and keyword.lower() in optional_parameter_keywords:
        keyword = None
    if sector and sector.lower() in optional_parameter_keywords:
        sector = None
    page.search(context.driver, keyword=keyword, sector=sector)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page.NAME, page.URL
    )


def fas_searched_for_companies(
    context: Context, actor_alias: str, *, keyword: str = None, sector: str = None
):
    visit_page(context, actor_alias, f"{fas.landing.SERVICE} - {fas.landing.NAME}")
    fas_search_for_companies(context, actor_alias, keyword=keyword, sector=sector)
    should_be_on_page(
        context,
        actor_alias,
        f"{fas.search_results.SERVICE} - {fas.search_results.NAME}",
    )


@retry(
    wait_fixed=5000,
    stop_max_attempt_number=4,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def generic_open_industry_page(context: Context, actor_alias: str, industry_name: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_industry")
    page.open_industry(context.driver, industry_name)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug("%s opened '%s' page on %s", actor_alias, industry_name, page.URL)


def fas_view_selected_company_profile(
    context: Context, actor_alias: str, profile_number: str
):
    number = NUMBERS[profile_number]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_profile")
    page.open_profile(context.driver, number)
    logging.debug(
        "%s clicked on '%s' button on %s",
        actor_alias,
        profile_number,
        context.driver.current_url,
    )


def fas_view_article(context: Context, actor_alias: str, article_number: str):
    number = NUMBERS[article_number]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_article")
    page.open_article(context.driver, number)
    logging.debug(
        "%s clicked on '%s' article on %s",
        actor_alias,
        article_number,
        context.driver.current_url,
    )


# BrowserStack times out after 60 seconds of inactivity
# https://www.browserstack.com/automate/timeouts
@retry(
    wait_fixed=5000,
    stop_max_attempt_number=4,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def generic_open_guide_link(context: Context, actor_alias: str, guide_name: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_guide")
    page.open_guide(context.driver, guide_name)
    update_actor(context, actor_alias, visited_page=guide_name)
    logging.debug("%s opened '%s' page on %s", actor_alias, guide_name, page.URL)


def check_for_errors_or_non_trading_companies(
    driver: WebDriver, *, go_back: bool = False
):
    """Throws an AssertionError if error message is visible."""
    try:
        content = driver.page_source
        is_500 = f"Got 500 ISE on {driver.current_url}"
        assert "there is a problem with the service" not in content, is_500
        already_exists = "A Business Profile already exists for this company"
        assert "already exists for this company" not in content, already_exists
        no_industry = f"Missing Industry field. Maybe company already has a profile"
        assert "industry" in content, no_industry
        no_website = f"Missing Website field. Maybe company already has a profile"
        assert "website" in content, no_website
        # fail when a non-trading company is selected (SIC=74990)
        assert "74990" not in content, f"Found a non-trading company: SIC=74990"
        error = driver.find_element(by=By.CSS_SELECTOR, value=".error-message")
        assert not error.is_displayed(), f"Found error on form page"
    except NoSuchElementException:
        # skip if no error was found
        pass
    except AssertionError as e:
        logging.debug(f"Picked wrong company: {e}")
        if go_back:
            logging.debug(f"Going back 1 page because assertion failed: {e}")
            with wait_for_page_load_after_action(driver):
                driver.back()
        raise e


def generic_remove_previous_field_selections(
    context: Context, actor_alias: str, selector_name: str
):
    page = get_last_visited_page(context, actor_alias)
    selector = find_selector_by_name(page.SELECTORS, selector_name)
    untick_selected_checkboxes(context.driver, selector)


@retry(
    wait_fixed=1000,
    stop_max_attempt_number=8,
    retry_on_exception=retry_if_assertion_error,
    wrap_exception=False,
)
def generic_fill_out_and_submit_form(
    context: Context,
    actor_alias: str,
    *,
    custom_details_table: Table = None,
    retry_on_errors: bool = False,
    go_back: bool = False,
    form_name: str = None,
):
    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "generate_form_details")
    has_action(page, "fill_out")
    has_action(page, "submit")
    if form_name:
        error = f"generate_form_details() in {page} should accept 'form_name' but it doesn't"
        assert signature(page.generate_form_details).parameters.get("form_name"), error
        error = f"fill_out() in {page} should accept 'form_name' but it doesn't"
        assert signature(page.fill_out).parameters.get("form_name"), error
        error = f"submit() in {page} should accept 'form_name' but it doesn't"
        assert signature(page.submit).parameters.get("form_name"), error
    if custom_details_table:
        custom_details_table.require_column("field")
        custom_details_table.require_column("value")
        value_mapping = {"unchecked": False, "checked": True, "empty": None}
        custom_details = {}
        for row in custom_details_table.rows:
            key = row["field"].lower()
            value = row["value"]
            custom_details[key] = value_mapping.get(value, value)
        if form_name:
            details = page.generate_form_details(
                actor, custom_details=custom_details, form_name=form_name
            )
        else:
            details = page.generate_form_details(actor, custom_details=custom_details)
    else:
        if form_name:
            details = page.generate_form_details(actor, form_name=form_name)
        else:
            details = page.generate_form_details(actor)
    logging.debug(f"{actor_alias} will fill out the form with: {details}")

    update_actor_forms_data(context, actor, details)

    if form_name:
        page.fill_out(context.driver, details, form_name=form_name)
    else:
        page.fill_out(context.driver, details)

    if hasattr(page, "get_form_details"):
        logging.debug(f"Getting form details from filled out form: {page}")
        form_data = page.get_form_details(context.driver)
        if form_data:
            update_actor_forms_data(context, actor, form_data)
    else:
        if details:
            update_actor_forms_data(context, actor, details)

    if form_name:
        page.submit(context.driver, form_name=form_name)
    else:
        page.submit(context.driver)
    if retry_on_errors:
        check_for_errors_or_non_trading_companies(context.driver, go_back=go_back)


def generic_submit_form(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "submit")
    page.submit(context.driver)


def generic_get_in_touch(
    context: Context, actor_alias: str, page_name: str, custom_details_table: Table
):
    visit_page(context, actor_alias, page_name)
    generic_fill_out_and_submit_form(
        context, actor_alias, custom_details_table=custom_details_table
    )


def generic_download_all_pdfs(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "download_all_pdfs")
    context.pdfs = page.download_all_pdfs(context.driver)


def generic_visit_current_page_with_lang_parameter(
    context: Context, actor_alias: str, preferred_language: str
):
    page = get_last_visited_page(context, actor_alias)
    url = urljoin(page.URL, f"?lang={preferred_language}")
    context.driver.get(url)


def generic_at_least_n_news_articles(
    context: Context, n: int, visitor_type: str, service: str
):
    context.articles = get_news_articles(service, visitor_type)
    error = (
        f"Expected to find at least {n} news articles on {service} but "
        f"got {len(context.articles)}"
    )
    assert len(context.articles) >= n, error


def generic_open_news_article(context: Context, actor_alias: str, ordinal_number: str):
    ordinals = {"first": 1, "second": 2, "third": 3}
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_news_article")
    page.open_news_article(context.driver, ordinals[ordinal_number.lower()])


def generic_open_any_tag(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_tag")
    tag = page.open_any_tag(context.driver)
    update_actor(context, actor_alias, last_tag=tag)


def generic_click_on_random_industry(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_article")
    page.open_any_article(context.driver)


def generic_click_on_random_element(
    context: Context, actor_alias: str, elements_name: str
):
    page = get_last_visited_page(context, actor_alias)
    selector = find_selector_by_name(page.SELECTORS, elements_name)
    elements = find_elements(context.driver, selector)
    element = random.choice(elements)
    href = f" → {element.get_attribute('href')}" if element.tag_name == "a" else ""
    logging.debug(f"Will click on: '{element.text.strip()}'{href}")
    scroll_to(context.driver, element)
    with wait_for_page_load_after_action(context.driver, timeout=10):
        with try_alternative_click_on_exception(context.driver, element):
            element.click()


def generic_click_on_random_marketplace(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_random_marketplace")
    page.open_random_marketplace(context.driver)


def generic_select_dropdown_option(
    context: Context, actor_alias: str, dropdown: str, option: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "select_dropdown_option")
    page.select_dropdown_option(context.driver, dropdown, option)


def generic_pick_radio_option(context: Context, actor_alias: str, option: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "pick_radio_option")
    page.pick_radio_option(context.driver, option)


def generic_pick_radio_option_and_submit(
    context: Context, actor_alias: str, option: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "pick_radio_option_and_submit")
    new_page = page.pick_radio_option_and_submit(context.driver, option)
    update_actor(context, actor_alias, visited_page=new_page)


def generic_pick_random_radio_option_and_submit(
    context: Context, actor_alias: str, ignored: str
):
    ignored = [item.strip().lower() for item in ignored.split(",")]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "pick_random_radio_option_and_submit")
    new_page = page.pick_random_radio_option_and_submit(context.driver, ignored)
    update_actor(context, actor_alias, visited_page=new_page)


def contact_us_get_to_page_via(
    context: Context,
    actor_alias: str,
    final_page: str,
    via: str,
    *,
    start_page: str = None,
):
    start_page = start_page or "Domestic - Contact us"
    intermediate = [name.strip() for name in via.split("->")]
    # 1) start at the Contact us "choose location" page
    visit_page(context, actor_alias, start_page)
    # 2) click through every listed option
    for option in intermediate:
        generic_pick_radio_option_and_submit(context, actor_alias, option)
    # 3) check if we're on the appropriate page
    should_be_on_page(context, actor_alias, final_page)


def contact_us_navigate_through_options(context: Context, actor_alias: str, via: str):
    intermediate = [name.strip() for name in via.split("->")]
    # 1) start at the Contact us "choose location" page
    visit_page(context, actor_alias, "Domestic - Contact us")
    # 2) click through every listed option
    for option in intermediate:
        generic_pick_radio_option_and_submit(context, actor_alias, option)


def domestic_open_random_advice_article(context: Context, actor_alias: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    driver = context.driver
    domestic.advice_landing.visit(driver)
    check_for_errors(driver.page_source, driver.current_url)
    advice_name = domestic.advice_landing.open_any_article(driver)
    article_name = domestic.advice_article_list.open_any_article(driver)
    domestic.advice_article.should_be_here(driver)
    update_actor(
        context,
        actor_alias,
        visited_page=domestic.advice_article,
        article_url=driver.current_url,
        article_category=advice_name,
        visited_articles=article_name,
    )


def generic_report_problem_with_page(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "report_problem")
    page.report_problem(context.driver)


def office_finder_find_trade_office(context: Context, actor_alias: str, post_code: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "find_trade_office")
    page.find_trade_office(context.driver, post_code)


def get_barred_actor(context: Context, actor_alias: str):
    if not get_actor(context, actor_alias):
        add_actor(context, barred_actor(actor_alias))


def sso_actor_received_email_confirmation_code(
    context: Context, actor_alias: str, business_type: str
):
    page_name = (
        f"Profile - Enter your email address and set a password ({business_type})"
    )
    visit_page(context, actor_alias, page_name)
    generic_fill_out_and_submit_form(context, actor_alias)
    end_page_name = f"Profile - Enter your confirmation code ({business_type})"
    should_be_on_page(context, actor_alias, end_page_name)
    generic_get_verification_code(context, actor_alias)


def generic_create_great_account(
    context: Context, actor_alias: str, business_type: str
):
    page_name = (
        f"Profile - Enter your email address and set a password ({business_type})"
    )  # noqa

    visit_page(context, actor_alias, page_name)
    generic_fill_out_and_submit_form(context, actor_alias)
    should_be_on_page(
        context,
        actor_alias,
        f"Profile - Enter your confirmation code ({business_type})",
    )

    generic_get_verification_code(context, actor_alias)
    generic_fill_out_and_submit_form(context, actor_alias)

    if business_type == "LTD, PLC or Royal Charter":
        should_be_on_page(
            context,
            actor_alias,
            f"Profile - Enter your business details ({business_type})",
        )
        generic_fill_out_and_submit_form(
            context, actor_alias, retry_on_errors=True, go_back=True
        )
        should_be_on_page(
            context,
            actor_alias,
            f"Profile - Enter your business details [step 2] ({business_type})",
        )
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context, actor_alias, f"Profile - Enter your details ({business_type})"
        )
        generic_fill_out_and_submit_form(context, actor_alias)
    elif business_type == "Sole trader or other type of business":
        should_be_on_page(
            context,
            actor_alias,
            f"Profile - Enter your business details ({business_type})",
        )
        generic_fill_out_and_submit_form(
            context, actor_alias, retry_on_errors=False, go_back=False
        )
        should_be_on_page(
            context, actor_alias, f"Profile - Enter your details ({business_type})"
        )
        generic_fill_out_and_submit_form(context, actor_alias)
    elif business_type == "UK taxpayer":
        should_be_on_page(
            context, actor_alias, f"Profile - Enter your details ({business_type})"
        )
        generic_fill_out_and_submit_form(context, actor_alias)

    should_be_on_page(
        context, actor_alias, f"Profile - Account created ({business_type})"
    )


def profile_start_registration_as(
    context: Context, actor_alias: str, business_type: str
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    profile.enrol_select_business_type.visit(context.driver)
    second_page = profile.enrol_select_business_type.pick_radio_option_and_submit(
        context.driver, name=business_type
    )
    should_be_on_page(
        context, actor_alias, f"{second_page.SERVICE} - {second_page.NAME}"
    )


def soo_look_for_marketplace(
    context: Context, actor_alias: str, country: str, category: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "search")
    page.search(context.driver, country, category)


def soo_look_for_marketplaces_from_home_page(
    context: Context, actor_alias: str, country: str, category: str
):
    visit_page(context, actor_alias, f"{soo.home.SERVICE} - {soo.home.NAME}")
    soo_look_for_marketplace(context, actor_alias, country, category)
    should_be_on_page(
        context,
        actor_alias,
        f"{soo.search_results.SERVICE} - {soo.search_results.NAME}",
    )


def soo_find_and_open_random_marketplace(
    context: Context, actor_alias: str, country: str, category: str
):
    soo_look_for_marketplaces_from_home_page(context, actor_alias, country, category)
    generic_click_on_random_marketplace(context, actor_alias)
    should_be_on_page(
        context, actor_alias, f"{soo.marketplace.SERVICE} - {soo.marketplace.NAME}"
    )


def domestic_submit_soo_contact_us_form(
    context: Context, actor_alias: str, custom_details_table: Table
):
    generic_fill_out_and_submit_form(
        context, actor_alias, custom_details_table=custom_details_table
    )
    domestic.contact_us_soo_3_about_your_products.should_be_here(context.driver)

    generic_fill_out_and_submit_form(context, actor_alias)
    domestic.contact_us_soo_4_your_experience.should_be_here(context.driver)

    generic_fill_out_and_submit_form(context, actor_alias)
    domestic.contact_us_soo_1_contact_details.should_be_here(context.driver)

    generic_fill_out_and_submit_form(context, actor_alias)
    domestic.contact_us_soo_5_thank_you.should_be_here(context.driver)


def generic_search_for_phrase(context: Context, actor_alias: str, phrase: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "search")
    page.search(context.driver, phrase)


def domestic_search_for_phrase_on_page(
    context: Context, actor_alias: str, phrase: str, page_name: str
):
    visit_page(context, actor_alias, page_name)
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "search")
    page.search(context.driver, phrase)


def domestic_find_more_about_search_result_type(
    context: Context, actor_alias: str, type_of: str
):
    should_be_on_page(context, actor_alias, get_full_page_name(domestic.search_results))
    domestic.search_results.click_on_result_of_type(context.driver, type_of)


def domestic_search_result_has_more_than_one_page(
    context: Context, actor_alias: str, min_page_num: int
):
    should_be_on_page(
        context,
        actor_alias,
        f"{domestic.search_results.SERVICE} - {domestic.search_results.NAME}",
    )
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "has_pagination")
    page.has_pagination(context.driver, min_page_num)


def generic_trigger_all_gtm_events(
    context: Context, actor_alias: str, tagging_package: str, *, event_group: str = None
):
    events = get_gtm_event_definitions(
        context.driver, tagging_package, event_group=event_group
    )
    assert events, f"No GTM events were found on {context.driver.current_url}"
    for event_group, events in events.items():
        for event in events:
            trigger_js_event(context.driver, event)
    logging.debug(f"{actor_alias} triggered all events for GTM event handlers")


def click_on_header_menu_button(context: Context):
    try:
        button = context.driver.find_element(by=By.ID, value="js-mobile-button")
    except NoSuchElementException:
        button = context.driver.find_element(by=By.ID, value="mobile-menu-button")
    button.click()


def erp_drill_down_hierarchy_tree(
    context: Context, actor_alias: str, *, use_expanded_category: bool = False
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "drill_down_hierarchy_tree")
    next_page, selected_code_value = page.drill_down_hierarchy_tree(
        context.driver, use_expanded_category=use_expanded_category
    )
    actor = get_actor(context, actor_alias)
    update_actor_forms_data(context, actor, selected_code_value)
    update_actor(context, actor_alias, visited_page=next_page)


def erp_save_for_later(context: Context, actor_alias: str):
    click_on_page_element(context, actor_alias, "save for later")
    should_be_on_page(context, actor_alias, get_full_page_name(erp.save_for_later))
    generic_fill_out_and_submit_form(context, actor_alias)
    should_be_on_page(
        context, actor_alias, get_full_page_name(erp.save_for_later_progress_saved)
    )


def erp_user_flow_individual_customer(
    context: Context, actor_alias
) -> Dict[str, MethodType]:
    user_type = "UK consumer"
    uk_consumer_type = "individual consumer"

    def select_user_type():
        visit_page(context, actor_alias, get_full_page_name(erp.triage_user_type))
        update_actor_forms_data(
            context,
            get_actor(context, actor_alias),
            {"business type": "UK consumer or consumer representative"},
        )
        generic_pick_radio_option_and_submit(context, actor_alias, option=user_type)

    def product_search():
        erp_drill_down_hierarchy_tree(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_product_detail),
        )

    def product_detail():
        click_on_page_element(context, actor_alias, element_name="continue")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_aware_of_changes),
        )

    def aware_of_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_other_changes_after_brexit),
        )

    def other_information():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context, actor_alias, page_name=get_full_page_name(erp.consumer_type)
        )

    def consumer_type():
        generic_pick_radio_option_and_submit(
            context, actor_alias, option=uk_consumer_type
        )
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_personal_details),
        )

    def personal_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.summary, page_sub_type=user_type),
        )

    def summary():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.finished, page_sub_type=user_type),
        )

    return {
        "User type": select_user_type,
        f"Product search ({user_type})": product_search,
        f"Product detail ({user_type})": product_detail,
        f"Are you aware of changes ({user_type})": aware_of_changes,
        f"Other information ({user_type})": other_information,
        f"Consumer type ({user_type})": consumer_type,
        f"Personal details ({user_type})": personal_details,
        f"Summary ({user_type})": summary,
    }


def erp_user_flow_consumer_group(
    context: Context, actor_alias
) -> Dict[str, MethodType]:
    user_type = "UK consumer"
    uk_consumer_type = "consumer group"

    def select_user_type():
        visit_page(context, actor_alias, get_full_page_name(erp.triage_user_type))
        update_actor_forms_data(
            context,
            get_actor(context, actor_alias),
            {"business type": "UK consumer or consumer representative"},
        )
        generic_pick_radio_option_and_submit(context, actor_alias, option=user_type)

    def product_search():
        erp_drill_down_hierarchy_tree(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_product_detail),
        )

    def product_detail():
        click_on_page_element(context, actor_alias, element_name="continue")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_aware_of_changes),
        )

    def aware_of_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_other_changes_after_brexit),
        )

    def other_information():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context, actor_alias, page_name=get_full_page_name(erp.consumer_type)
        )

    def consumer_type():
        generic_pick_radio_option_and_submit(
            context, actor_alias, option=uk_consumer_type
        )
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.consumer_group_details),
        )

    def group_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.summary, page_sub_type=user_type),
        )

    def summary():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.finished, page_sub_type=user_type),
        )

    return {
        "User type": select_user_type,
        f"Product search ({user_type})": product_search,
        f"Product detail ({user_type})": product_detail,
        f"Are you aware of changes ({user_type})": aware_of_changes,
        f"Other information ({user_type})": other_information,
        f"Consumer type ({user_type})": consumer_type,
        f"Consumer group details ({user_type})": group_details,
        f"Summary ({user_type})": summary,
    }


def erp_user_flow_uk_business(
    context: Context, actor_alias: str
) -> Dict[str, MethodType]:
    user_type = "UK business"

    def select_user_type():
        visit_page(context, actor_alias, get_full_page_name(erp.triage_user_type))
        update_actor_forms_data(
            context, get_actor(context, actor_alias), {"business type": user_type}
        )
        generic_pick_radio_option_and_submit(context, actor_alias, option=user_type)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.triage_import_from_overseas),
        )

    def import_from_overseas():
        update_actor_forms_data(
            context,
            get_actor(context, actor_alias),
            {"import from overseas": "I produce the affected goods in the UK"},
        )
        generic_pick_radio_option_and_submit(
            context, actor_alias, option="not imported"
        )
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_search, page_sub_type=user_type),
        )

    def product_search():
        erp_drill_down_hierarchy_tree(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_detail, page_sub_type=user_type),
        )

    def product_detail():
        click_on_page_element(context, actor_alias, element_name="continue")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_volumes, page_sub_type=user_type),
        )

    def sales_volume():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_revenue, page_sub_type=user_type),
        )

    def sales_revenue():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_sales_changes, page_sub_type=user_type
            ),
        )

    def sales_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_market_size_changes, page_sub_type=user_type
            ),
        )

    def market_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_other_changes_after_brexit, page_sub_type=user_type
            ),
        )

    def other_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.market_size, page_sub_type=user_type),
        )

    def market_size():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.outocome, page_sub_type=user_type),
        )

    def outcome():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.business_details, page_sub_type=user_type),
        )

    def business_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.personal_details, page_sub_type=user_type),
        )

    def personal_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.summary, page_sub_type=user_type),
        )

    def summary():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.finished, page_sub_type=user_type),
        )

    return {
        "User type": select_user_type,
        f"Import from overseas ({user_type})": import_from_overseas,
        f"Product search ({user_type})": product_search,
        f"Product detail ({user_type})": product_detail,
        f"Sales volumes ({user_type})": sales_volume,
        f"Sales revenue ({user_type})": sales_revenue,
        f"Are you aware of sales changes ({user_type})": sales_changes,
        f"Are you aware of market size changes ({user_type})": market_changes,
        f"Are you aware of other changes ({user_type})": other_changes,
        f"Market size ({user_type})": market_size,
        f"What outcome are you seeking for ({user_type})": outcome,
        f"Business details ({user_type})": business_details,
        f"Personal details ({user_type})": personal_details,
        f"Summary ({user_type})": summary,
    }


def erp_user_flow_uk_importer(
    context: Context, actor_alias: str
) -> Dict[str, MethodType]:
    user_type = "UK importer"

    def select_user_type():
        visit_page(context, actor_alias, get_full_page_name(erp.triage_user_type))
        update_actor_forms_data(
            context, get_actor(context, actor_alias), {"business type": user_type}
        )
        generic_pick_radio_option_and_submit(context, actor_alias, option="UK business")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.triage_import_from_overseas),
        )

    def import_from_overseas():
        update_actor_forms_data(
            context,
            get_actor(context, actor_alias),
            {"import from overseas": "I import the affected goods from overseas"},
        )
        generic_pick_radio_option_and_submit(context, actor_alias, option="imported")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_search, page_sub_type=user_type),
        )

    def product_search():
        erp_drill_down_hierarchy_tree(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_detail, page_sub_type=user_type),
        )

    def product_detail():
        click_on_page_element(context, actor_alias, element_name="continue")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.uk_importer_where_do_you_import_from),
        )

    def where_do_you_import_from():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.uk_importer_are_goods_used_to_make_something_else
            ),
        )

    def something_else():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_volumes, page_sub_type=user_type),
        )

    def sales_volume():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_revenue, page_sub_type=user_type),
        )

    def sales_revenue():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_sales_changes, page_sub_type=user_type
            ),
        )

    def sales_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_market_size_changes, page_sub_type=user_type
            ),
        )

    def market_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_other_changes_after_brexit, page_sub_type=user_type
            ),
        )

    def other_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.uk_importer_production_percentage),
        )

    def percentage():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.uk_importer_equivalent_uk_goods),
        )

    def equivalents():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.market_size, page_sub_type=user_type),
        )

    def market_size():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.outocome, page_sub_type=user_type),
        )

    def outcome():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.business_details, page_sub_type=user_type),
        )

    def business_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.personal_details, page_sub_type=user_type),
        )

    def personal_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.summary, page_sub_type=user_type),
        )

    def summary():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.finished, page_sub_type=user_type),
        )

    return {
        "User type": select_user_type,
        f"Import from overseas ({user_type})": import_from_overseas,
        f"Product search ({user_type})": product_search,
        f"Product detail ({user_type})": product_detail,
        f"Where do you import from ({user_type})": where_do_you_import_from,
        f"Are there goods used to make something else ({user_type})": something_else,
        f"Sales volumes ({user_type})": sales_volume,
        f"Sales revenue ({user_type})": sales_revenue,
        f"Are you aware of sales changes ({user_type})": sales_changes,
        f"Are you aware of market size changes ({user_type})": market_changes,
        f"Are you aware of other changes ({user_type})": other_changes,
        f"What percentage of your production do these goods make up ({user_type})": percentage,
        f"Are there equivalent goods made in the UK ({user_type})": equivalents,
        f"Market size ({user_type})": market_size,
        f"What outcome are you seeking for ({user_type})": outcome,
        f"Business details ({user_type})": business_details,
        f"Personal details ({user_type})": personal_details,
        f"Summary ({user_type})": summary,
    }


def erp_user_flow_developing_country(
    context: Context, actor_alias: str
) -> Dict[str, MethodType]:
    user_type = "Developing country"
    user_friendly_name = "exporter from developing country"

    def select_user_type():
        visit_page(context, actor_alias, get_full_page_name(erp.triage_user_type))
        update_actor_forms_data(
            context, get_actor(context, actor_alias), {"business type": user_type}
        )
        generic_pick_radio_option_and_submit(
            context, actor_alias, option=user_friendly_name
        )
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.developing_country_select),
        )

    def select_country():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_search, page_sub_type=user_type),
        )

    def product_search():
        erp_drill_down_hierarchy_tree(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.product_detail, page_sub_type=user_type),
        )

    def product_detail():
        click_on_page_element(context, actor_alias, element_name="continue")
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_volumes, page_sub_type=user_type),
        )

    def sales_volume():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.sales_revenue, page_sub_type=user_type),
        )

    def sales_revenue():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_sales_changes, page_sub_type=user_type
            ),
        )

    def sales_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_market_size_changes, page_sub_type=user_type
            ),
        )

    def market_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(
                erp.aware_of_other_changes_after_brexit, page_sub_type=user_type
            ),
        )

    def other_changes():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.outocome, page_sub_type=user_type),
        )

    def outcome():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.developing_country_business_details),
        )

    def business_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.personal_details, page_sub_type=user_type),
        )

    def personal_details():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.summary, page_sub_type=user_type),
        )

    def summary():
        generic_fill_out_and_submit_form(context, actor_alias)
        should_be_on_page(
            context,
            actor_alias,
            page_name=get_full_page_name(erp.finished, page_sub_type=user_type),
        )

    return {
        "User type": select_user_type,
        "Select country (Developing country)": select_country,
        "Product search (Developing country)": product_search,
        "Product detail (Developing country)": product_detail,
        "Sales volumes (Developing country)": sales_volume,
        "Sales revenue (Developing country)": sales_revenue,
        "Are you aware of sales changes (Developing country)": sales_changes,
        "Are you aware of market size changes (Developing country)": market_changes,
        "Are you aware of other changes (Developing country)": other_changes,
        "What outcome are you seeking for (Developing country)": outcome,
        "Business details (Developing country)": business_details,
        "Personal details (Developing country)": personal_details,
        "Summary (Developing country)": summary,
    }


def erp_run_flow_steps(
    flow_name: str, flow_steps: Dict[str, MethodType], stop_at: str, resume_from: str
):
    flow_step_names = list(flow_steps.keys())

    stop_or_resume_page_name = stop_at or resume_from
    if stop_or_resume_page_name:
        error = (
            f"Provide page name: '{stop_or_resume_page_name}' is not recognised. Please"
            f" use one the names from the following list: {flow_step_names}"
        )
        assert stop_or_resume_page_name in flow_step_names, error
        if stop_at:
            logging.debug(f"Will stop ERP flow at: '{stop_at}'")
        if resume_from:
            logging.debug(f"Will resume ERP flow from: '{resume_from}'")

    if stop_at:
        index_of_last_page = flow_step_names.index(stop_at)
        remaining_steps = {
            key: value
            for key, value in flow_steps.items()
            if key in flow_step_names[:index_of_last_page]
        }
    elif resume_from:
        index_of_first_page = flow_step_names.index(resume_from)
        remaining_steps = {
            key: value
            for key, value in flow_steps.items()
            if key in flow_step_names[index_of_first_page:]
        }
    else:
        remaining_steps = flow_steps
        logging.debug(f"Will go through the whole ERP flow for: {flow_name}")

    for step_name, step_code_block in remaining_steps.items():
        logging.debug(f"ERP step: {step_name}")
        step_code_block()


def erp_follow_user_flow(
    context: Context,
    actor_alias: str,
    user_type,
    *,
    stop_at: str = None,
    resume_from: str = None,
):
    erp_flows = {
        "individual consumer": erp_user_flow_individual_customer(context, actor_alias),
        "consumer group": erp_user_flow_consumer_group(context, actor_alias),
        "UK business": erp_user_flow_uk_business(context, actor_alias),
        "UK importer": erp_user_flow_uk_importer(context, actor_alias),
        "exporter from developing country": erp_user_flow_developing_country(
            context, actor_alias
        ),
    }
    flow_steps = erp_flows[user_type]
    erp_run_flow_steps(user_type, flow_steps, stop_at, resume_from)


def erp_open_restore_session_link(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    assert actor.saved_progress_link
    go_to_url(context.driver, actor.saved_progress_link, "Restore saved ERP progress")


def erp_select_random_search_result(
    context: Context, actor_alias: str, result_type: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "click_on_random_search_result")
    page.click_on_random_search_result(context.driver, result_type)
