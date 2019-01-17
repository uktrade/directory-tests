# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random
from datetime import datetime
from urllib.parse import urljoin

from behave.model import Table
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from settings import SET_HAWK_COOKIE, REUSE_COOKIE
from utils.cms_api import get_news_articles
from utils.gov_notify import get_verification_link

from pages import common_language_selector, exred, fas, get_page_object, sso
from pages.common_actions import (
    add_actor,
    barred_actor,
    get_actor,
    get_hawk_cookie,
    get_last_visited_page,
    unauthenticated_actor,
    update_actor,
)
from steps import has_action

NUMBERS = {
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


def try_to_reuse_hawk_cookie(driver: WebDriver):
    """
    An example 'ip-restrict-signature' cookie returned by WebDriver looks like this:
    {
     'domain': 'invest.great.gov.uk',
     'expiry': 2177925215,
     'httpOnly': False,
     'name': 'ip-restrict-signature',
     'path': '/',
     'secure': True,
     'value': 'Hawk mac="IzYtf...=", id="test", ts="1547205215", nonce="avYGOt"'
    }
    In order to reuse the cookie, we need to check if the difference between current
    datetime and `ts` value (from 'value' property) is less than 60s.
    It's because Hawk cookie is valid for 60s.
    see https://github.com/hueniverse/hawk#replay-protection
    To avoid situations when cookie is rejected as it expired due to slow page load,
    we'll renew it when it's older than 50s.

    """
    logging.debug(f"Checking if IP Restrictor cookie can be reused")
    cookies = driver.get_cookies()
    restrictor_cookie = [c for c in cookies if c['name'] == 'ip-restrict-signature']
    if restrictor_cookie:
        logging.debug(f"Found IP Restrictor cookie")
        cookie_ts = int(restrictor_cookie[0]['value'].split(', ')[2][4:-1])
        now = int(datetime.now().timestamp())
        time_difference = now - cookie_ts
        if time_difference < 50:
            logging.debug(
                f"IP Restrictor cookie is still valid for {60 - time_difference}s, "
                f"will re-use it"
            )
            return
        else:
            logging.debug(f"IP Restrictor cookie is not valid anymore")
    else:
        logging.debug(f"IP Restrictor cookie is not present")
    

def generic_set_hawk_cookie(context: Context, page_name: str):
    if not SET_HAWK_COOKIE:
        logging.debug("Setting HAWK cookie is disabled")
        return
    driver = context.driver
    if REUSE_COOKIE:
        try_to_reuse_hawk_cookie(driver)
    page = get_page_object(page_name)
    logging.debug(f"Visiting {page.URL} in order to set IP Restrictor cookie")
    driver.get(page.URL)
    hawk_cookie = get_hawk_cookie()
    logging.debug(f"Generated hawk cookie: {hawk_cookie}")
    driver.add_cookie(hawk_cookie)
    logging.debug(f"Added hawk cookie to driver! {driver.get_cookies()}")


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def visit_page(
    context: Context,
    actor_alias: str,
    page_name: str,
):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """

    def is_special_case(page_name: str) -> bool:
        parts = page_name.split(" - ")
        return len(parts) > 2

    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))

    page = get_page_object(page_name)

    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page_name, page.URL
    )
    has_action(page, "visit")

    if is_special_case(page_name):
        page.visit(context.driver, page_name=page_name)
    else:
        page.visit(context.driver)
    update_actor(context, actor_alias, visited_page=page)


def should_be_on_page(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    has_action(page, "should_be_here")
    if hasattr(page, "URLs"):
        special_page_name = page_name.split(" - ")[1]
        page.should_be_here(context.driver, page_name=special_page_name)
    else:
        page.should_be_here(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(
        f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> {page}"
    )


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
)
def open_group_element(
    context: Context, group: str, element: str, location: str
):
    driver = context.driver
    if location.lower() == "export readiness - home":
        exred.home.open(driver, group, element)
    elif location.lower() in "export readiness - header":
        exred.header.open(driver, group, element)
    elif location.lower() in "export readiness - footer":
        exred.footer.open(driver, group, element)
    elif location.lower() == "export readiness - personalised journey":
        exred.personalised_journey.open(driver, group, element)
    elif location.lower() == "export readiness - international":
        exred.international.open(driver, group, element, same_tab=True)
    else:
        raise KeyError("Could not recognize location: {}".format(location))


def articles_open_any(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_article")
    element_details = page.open_any_article(context.driver)
    update_actor(context, actor_alias, element_details=element_details)
    logging.info(f"{actor_alias} opened article: {element_details}")


def case_studies_go_to(context: Context, actor_alias: str, case_number: str):
    case_study_title = exred.home.get_case_study_title(
        context.driver, case_number
    )
    exred.home.open_case_study(context.driver, case_number)
    update_actor(context, actor_alias, case_study_title=case_study_title)
    logging.debug(
        "%s opened %s case study, entitled: %s",
        actor_alias,
        case_number,
        case_study_title,
    )


def case_studies_go_to_random(
    context: Context, actor_alias: str, page_name: str
):
    assert page_name.lower() in ["export readiness - home"]
    visit_page(context, actor_alias, page_name)
    case_number = random.choice(["first", "second", "third"])
    case_studies_go_to(context, actor_alias, case_number)


def open_link(
    context: Context,
    actor_alias: str,
    group: str,
    category: str,
    location: str,
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    update_actor(
        context, actor_alias, article_group=group, article_category=category
    )
    logging.debug(
        "%s is about to open link to '%s' '%s' via %s",
        actor_alias,
        group,
        category,
        location,
    )
    open_group_element(
        context, group=group, element=category, location=location
    )
    update_actor(
        context,
        actor_alias,
        article_group="advice",
        article_category=category,
        article_location=location,
    )


def open_service_link_on_interim_page(
    context: Context, actor_alias: str, service: str
):
    page_name = "export readiness - interim {}".format(service)
    page = get_page_object(page_name)
    has_action(page, "go_to_service")
    page.go_to_service(context.driver)
    logging.debug("%s went to %s service page", actor_alias, service)


def registration_go_to(context: Context, actor_alias: str):
    logging.debug("%s decided to go to registration", actor_alias)
    exred.header.go_to_registration(context.driver)
    sso.registration.should_be_here(context.driver)


def registration_should_get_verification_email(
    context: Context, actor_alias: str
):
    """Will check if the Exporter received an email verification message."""
    logging.debug("Searching for an email verification message...")
    actor = get_actor(context, actor_alias)
    link = get_verification_link(actor.email)
    update_actor(context, actor_alias, email_confirmation_link=link)


def registration_open_email_confirmation_link(
    context: Context, actor_alias: str
):
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
    driver = context.driver
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sso.registration.fill_out(driver, email, password)
    sso.registration.submit(driver)
    sso.registration_confirmation.should_be_here(driver)
    if fake_verification:
        sso.common.verify_account(email)
    else:
        registration_should_get_verification_email(context, actor_alias)
        registration_open_email_confirmation_link(context, actor_alias)
        sso.confirm_your_email.submit(context.driver)
    update_actor(context, actor_alias, registered=True)


def registration_create_and_verify_account(
    context: Context, actor_alias: str, *, fake_verification: bool = True
):
    visit_page(context, actor_alias, "export readiness - home")
    registration_go_to(context, actor_alias)
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


def sign_in_go_to(context: Context, actor_alias: str, location: str):
    logging.debug(
        "%s decided to go to sign in page via %s link", actor_alias, location
    )
    exred.header.go_to_sign_in(context.driver)
    sso.sign_in.should_be_here(context.driver)


def sign_in(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sign_in_go_to(context, actor_alias)
    sso.sign_in.fill_out(context.driver, email, password)
    sso.sign_in.submit(context.driver)


def sign_out(context: Context, actor_alias: str):
    exred.header.go_to_sign_out(context.driver)
    sso.sign_out.submit(context.driver)
    logging.debug("%s signed out", actor_alias)


@retry(wait_fixed=30000, stop_max_attempt_number=3)
def articles_share_on_social_media(
    context: Context, actor_alias: str, social_media: str
):
    context.article_url = context.driver.current_url
    if social_media.lower() == "email":
        exred.advice_article.check_if_link_opens_email_client(context.driver)
    else:
        exred.advice_article.check_if_link_opens_new_tab(
            context.driver, social_media
        )
        if not social_media.lower() == "linkedin":
            exred.advice_article.share_via(context.driver, social_media)
    logging.debug(
        "%s successfully got to the share article on '%s'",
        actor_alias,
        social_media,
    )


def promo_video_watch(
    context: Context, actor_alias: str, *, play_time: int = None
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "play_video")
    page.play_video(context.driver, play_time=play_time)
    logging.debug("%s was able to play the video", actor_alias)


def promo_video_close(context: Context, actor_alias: str):
    exred.home.close_video(context.driver)
    logging.debug("%s closed the video", actor_alias)


def language_selector_close(
    context: Context, actor_alias: str, *, with_keyboard: bool = False
):
    logging.debug("%s decided to close language selector", actor_alias)
    common_language_selector.close(context.driver, with_keyboard=with_keyboard)


def language_selector_open(
    context: Context, actor_alias: str, *, with_keyboard: bool = False
):
    logging.debug("%s decided to go open language selector", actor_alias)
    common_language_selector.open(context.driver, with_keyboard=with_keyboard)


def language_selector_navigate_through_links_with_keyboard(
    context: Context, actor_alias: str
):
    logging.debug(
        "%s decided to navigate through all language selector links with"
        " keyboard",
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
    language_selector_open(context, actor_alias)
    common_language_selector.change_to(
        context.driver, page, preferred_language
    )


def header_footer_open_link(
    context: Context,
    actor_alias: str,
    group: str,
    link_name: str,
    location: str,
):
    open_group_element(
        context, group=group, element=link_name, location=location
    )
    logging.debug(
        "%s decided to go to '%s' page via '%s' links in header menu",
        actor_alias,
        link_name,
        group,
    )


def click_on_page_element(
    context: Context,
    actor_alias: str,
    element_name: str,
    *,
    page_name: str = None,
):
    if page_name:
        page = get_page_object(page_name)
    else:
        page = get_last_visited_page(context, actor_alias)
    has_action(page, "click_on_page_element")
    page.click_on_page_element(context.driver, element_name)
    logging.debug(
        "%s decided to click on '%s' on '%s' page",
        actor_alias,
        element_name,
        page.NAME,
    )


def header_footer_click_on_dit_logo(
    context: Context, actor_alias: str, location: str
):
    open_group_element(
        context, group="general", element="logo", location=location
    )
    logging.debug("%s clicked on DIT logo", actor_alias)


def fas_search_for_companies(
    context: Context,
    actor_alias: str,
    *,
    keyword: str = None,
    sector: str = None,
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


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def generic_open_industry_page(
    context: Context, actor_alias: str, industry_name: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_industry")
    page.open_industry(context.driver, industry_name)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug(
        "%s opened '%s' page on %s", actor_alias, industry_name, page.URL
    )


def fas_fill_out_and_submit_contact_us_form(
    context: Context,
    actor_alias: str,
    *,
    sector: str = None,
    sources: str = None,
    company_size: str = None,
    accept_tc: bool = True,
    captcha: bool = True,
):
    actor = get_actor(context, actor_alias)
    company_name = actor.company_name or "Automated test"
    contact_us_details = {
        "full name": actor.alias,
        "email": actor.email,
        "industry": sector,
        "organisation": company_name,
        "organisation size": company_size,
        "country": "DIT QA TEAM",
        "body": "This is a test message sent via automated tests",
        "source": sources,
        "accept t&c": accept_tc,
    }
    fas.contact_us.fill_out(context.driver, contact_us_details, captcha=captcha)
    fas.contact_us.submit(context.driver)


def generic_see_more_industries(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "see_more_industries")
    page.see_more_industries(context.driver)
    logging.debug(
        "%s clicked on 'See more industries' button on %s",
        actor_alias,
        context.driver.current_url,
    )


def fas_use_breadcrumb(
    context: Context, actor_alias: str, breadcrumb_name: str, page_name: str
):
    page = get_page_object(page_name)
    has_action(page, "click_breadcrumb")
    page.click_breadcrumb(context.driver, breadcrumb_name)
    logging.debug(
        "%s clicked on '%s' breadcrumb on %s",
        actor_alias,
        breadcrumb_name,
        context.driver.current_url,
    )


def fas_view_more_companies(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "click_on_page_element")
    page.click_on_page_element(context.driver, "view more")
    logging.debug(
        "%s clicked on 'view more companies' button on %s",
        actor_alias,
        context.driver.current_url,
    )


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


def invest_read_more(context: Context, actor_alias: str, topic_names: Table):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_link")
    topics = [row[0] for row in topic_names]
    update_actor(context, actor_alias, visited_articles=topics)
    for topic in topics:
        page.open_link(context.driver, topic)
        logging.debug(
            "%s clicked on '%s' topic on %s",
            actor_alias,
            topic,
            context.driver.current_url,
        )


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
    wrap_exception=False,
)
def generic_open_guide_link(
    context: Context, actor_alias: str, guide_name: str
):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_guide")
    page.open_guide(context.driver, guide_name)
    update_actor(context, actor_alias, visited_page=guide_name)
    logging.debug(
        "%s opened '%s' page on %s", actor_alias, guide_name, page.URL
    )


def generic_unfold_topics(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "unfold_topics")
    page.unfold_topics(context.driver)
    update_actor(context, actor_alias, visited_page=page)
    logging.debug("%s unfolded all topics on %s", actor_alias, page.NAME)


def generic_click_on_uk_gov_logo(
    context: Context, actor_alias: str, page_name: str
):
    page = get_page_object(page_name)
    has_action(page, "click_on_page_element")
    page.click_on_page_element(context.driver, "uk gov logo")
    logging.debug("%s click on UK Gov logo %s", actor_alias, page_name)


def generic_fill_out_and_submit_form(
        context: Context, actor_alias: str, *, custom_details_table: Table = None):
    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "generate_form_details")
    has_action(page, "fill_out")
    has_action(page, "submit")
    if custom_details_table:
        custom_details_table.require_column("field")
        custom_details_table.require_column("value")
        value_mapping = {
            "unchecked": False,
            "checked": True,
            "empty": None,
        }
        custom_details = {}
        for row in custom_details_table.rows:
            key = row["field"].lower()
            value = row["value"]
            custom_details[key] = value_mapping.get(value, value)
        details = page.generate_form_details(actor, custom_details=custom_details)
    else:
        details = page.generate_form_details(actor)
    logging.debug(f"{actor_alias} will fill out the form with: {details}")
    page.fill_out(context.driver, details)
    page.submit(context.driver)


def generic_submit_form(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "submit")
    page.submit(context.driver)


def generic_get_in_touch(context: Context, actor_alias: str, page_name: str):
    visit_page(context, actor_alias, page_name)
    generic_fill_out_and_submit_form(context, actor_alias)


def generic_download_all_pdfs(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "download_all_pdfs")
    context.pdfs = page.download_all_pdfs(context.driver)


def generic_visit_current_page_with_lang_parameter(
        context: Context, actor_alias: str,  preferred_language: str):
    page = get_last_visited_page(context, actor_alias)
    url = urljoin(page.URL, f"?lang={preferred_language}")
    context.driver.get(url)


def generic_at_least_n_news_articles(
        context: Context, n: int, visitor_type: str, service: str):
    articles = get_news_articles(service, visitor_type)
    error = (f"Expected to find at least {n} news articles on {service} but "
             f"got {len(articles)}")
    assert len(articles) >= n, error
    context.articles = articles


def generic_open_news_article(
        context: Context, actor_alias: str, ordinal_number: str):
    ordinals = {
        "first": 1,
        "second": 2,
        "third": 3,
    }
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_news_article")
    page.open_news_article(context.driver, ordinals[ordinal_number.lower()])


def generic_open_any_news_article(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_news_article")
    page.open_any_news_article(context.driver)


def generic_open_any_tag(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_tag")
    tag = page.open_any_tag(context.driver)
    update_actor(context, actor_alias, last_tag=tag)


def generic_open_random_news_article(
        context: Context, actor_alias: str, article_type: str
):
    flow = {
        "domestic": {
            "start":
                "Export Readiness - Updates for UK companies on EU Exit - Domestic",
            "finish": "Export Readiness - Domestic EU Exit news - article",
        },
        "international": {
            "start":
                "Export Readiness - Updates for non-UK companies on EU Exit - International",
            "finish": "Export Readiness - International EU Exit news - article",
        }
    }
    start = flow[article_type.lower()]["start"]
    finish = flow[article_type.lower()]["finish"]
    visit_page(context, actor_alias, start)
    generic_open_any_news_article(context, actor_alias)
    should_be_on_page(context, actor_alias, finish)


def generic_click_on_random_industry(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_article")
    page.open_any_article(context.driver)


def generic_pick_radio_option_and_submit(
        context: Context, actor_alias: str, option: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "pick_radio_option_and_submit")
    new_page = page.pick_radio_option_and_submit(context.driver, option)
    update_actor(context, actor_alias, visited_page=new_page)


def generic_pick_random_radio_option_and_submit(
        context: Context, actor_alias: str, ignored: str):
    ignored = [item.strip().lower() for item in ignored.split(",")]
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "pick_random_radio_option_and_submit")
    new_page = page.pick_random_radio_option_and_submit(context.driver, ignored)
    update_actor(context, actor_alias, visited_page=new_page)


def contact_us_get_to_page_via(
        context: Context, actor_alias: str, final_page: str, via: str):
    intermediate = [name.strip() for name in via.split("->")]
    # 1) start at the Contact us "choose location" page
    visit_page(context, actor_alias, "Export Readiness - Contact us")
    # 2) click through every listed option
    for option in intermediate:
        generic_pick_radio_option_and_submit(context, actor_alias, option)
    # 3) check if we're on the appropriate page
    should_be_on_page(context, actor_alias, final_page)


def contact_us_navigate_through_options(context: Context, actor_alias: str, via: str):
    intermediate = [name.strip() for name in via.split("->")]
    # 1) start at the Contact us "choose location" page
    visit_page(context, actor_alias, "Export Readiness - Contact us")
    # 2) click through every listed option
    for option in intermediate:
        generic_pick_radio_option_and_submit(context, actor_alias, option)


def open_any_element(
        context: Context, actor_alias: str, element_type: str, section_name: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_element_in_section")
    element_details = page.open_any_element_in_section(
        context.driver, element_type, section_name
    )
    update_actor(context, actor_alias, element_details=element_details)
    logging.info(f"{actor_alias} opened random {element_type} from {section_name}")


def exred_open_random_advice_article(context: Context, actor_alias: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    driver = context.driver
    exred.advice_landing.visit(driver)
    exred.advice_landing.open_any_article(driver)
    exred.advice_article_list.open_any_article(driver)
    exred.advice_article.should_be_here(driver)
    update_actor(context, actor_alias, visited_page=exred.advice_article)
    update_actor(context, actor_alias, article_url=driver.current_url)


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
