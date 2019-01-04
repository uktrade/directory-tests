# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random
from urllib.parse import urljoin

from behave.model import Table
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils.cms_api import get_news_articles
from utils.gov_notify import get_verification_link

from pages import common_language_selector, exread, fas, get_page_object, sso
from pages.common_actions import (
    add_actor,
    get_actor,
    get_hawk_cookie,
    get_last_visited_page,
    take_screenshot,
    unauthenticated_actor,
    update_actor,
    VisitedArticle,
)
from registry.articles import (
    get_article,
    get_articles,
)
from settings import EXRED_SECTORS
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


def generic_set_hawk_cookie(context: Context, page_name: str):
    page = get_page_object(page_name)
    driver = context.driver
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
    *,
    first_time: bool = False,
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
        page.visit(context.driver, first_time=first_time, page_name=page_name)
    else:
        page.visit(context.driver, first_time=first_time)
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
    logging.debug(f"{actor_alias} is on {page.SERVICE} - {page.NAME} - {page.TYPE} -> {page}")


def actor_classifies_himself_as(
    context: Context, actor_alias: str, exporter_status: str
):
    actor = unauthenticated_actor(
        actor_alias, self_classification=exporter_status
    )
    add_actor(context, actor)


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
        exread.home.open(driver, group, element)
    elif location.lower() in "export readiness - header":
        exread.header.open(driver, group, element)
    elif location.lower() in "export readiness - footer":
        exread.footer.open(driver, group, element)
    elif location.lower() == "export readiness - personalised journey":
        exread.personalised_journey.open(driver, group, element)
    elif location.lower() == "export readiness - international":
        exread.international.open(driver, group, element, same_tab=True)
    else:
        raise KeyError("Could not recognize location: {}".format(location))


def export_readiness_open_category(
    context: Context, actor_alias: str, category: str, location: str
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if location.lower() != "personalised journey":
        visit_page(context, actor_alias, "export readiness - home")
    logging.debug(
        "%s is about to open Export Readiness '%s' category from %s",
        actor_alias,
        category,
        location,
    )
    open_group_element(
        context, group="export readiness", element=category, location=location
    )
    update_actor(
        context,
        actor_alias,
        article_group="export readiness",
        article_category=category,
        article_location=location,
        visited_page=exread.article_list,
    )


def set_sector_preference(
    context: Context,
    actor_alias: str,
    *,
    goods_or_services: str = None,
    good: str = None,
    service: str = None,
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    assert goods_or_services or not (good and service)
    message = (
        "You can provide only one of the following arguments: "
        "`goods_or_services`, `good` or `service`. You've passed: "
        "`goods_or_services={} good={} service={}".format(
            goods_or_services, good, service
        )
    )
    optional_args = [goods_or_services, good, service]
    assert len([arg for arg in optional_args if arg is not None]) == 1, message
    logging.debug(
        "%s exports: `goods_or_services=%s good=%s service=5s",
        goods_or_services,
        good,
        service,
    )
    if goods_or_services is not None:
        if goods_or_services.lower() == "goods":
            sectors = [
                (code, sector)
                for code, sector in EXRED_SECTORS.items()
                if code.startswith("HS")
            ]
        elif goods_or_services.lower() == "services":
            sectors = [
                (code, sector)
                for code, sector in EXRED_SECTORS.items()
                if code.startswith("EB")
            ]
        elif goods_or_services.lower() == "goods and services":
            goods_sectors = [
                (code, sector)
                for code, sector in EXRED_SECTORS.items()
                if code.startswith("HS")
            ]
            services_sectors = [
                (code, sector)
                for code, sector in EXRED_SECTORS.items()
                if code.startswith("EB")
            ]
            sectors = goods_sectors + services_sectors
        else:
            raise KeyError(
                "Could not recognise '%s' as valid sector. Please use 'goods' "
                "or 'services'" % goods_or_services
            )
        code, sector = random.choice(sectors)
    else:
        filtered_sectors = [
            (code, sector)
            for code, sector in EXRED_SECTORS.items()
            if sector == (good or service)
        ]
        assert len(filtered_sectors) == 1, (
            "Could not find code & sector for"
            " '{}'".format((good or service))
        )
        code, sector = filtered_sectors[0]
    logging.debug("Code: %s - Sector: %s", code, sector)
    update_actor(
        context,
        actor_alias,
        what_do_you_want_to_export=(goods_or_services.lower(), code, sector),
    )
    logging.debug(
        "%s decided that her/his preferred sector is: %s %s",
        actor_alias,
        code,
        sector,
    )


def set_online_marketplace_preference(
    context: Context, actor_alias: str, used_or_not: str
):
    """Will set preference for past usage of Online Marketplaces

     NOTE:
     It will add new Actor is specified one doesn't exist,
    """
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if used_or_not.lower() == "used":
        used = True
    elif used_or_not.lower() == "never used":
        used = False
    else:
        raise KeyError(
            "Could not recognise '%s' as valid preference for pass usage of"
            " Online Marketplaces. Please use 'used' or 'never used'"
            % used_or_not
        )
    update_actor(context, actor_alias, do_you_use_online_marketplaces=used)
    logging.debug(
        "%s decided that he/she %s online marketplaces before",
        actor_alias,
        used_or_not,
    )


def articles_open_any_but_the_last(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    visited_articles = actor.visited_articles
    group = actor.article_group
    category = actor.article_category
    articles = get_articles(group, category)
    # select random article
    random_article = random.choice(articles[:-1])
    # then get it's index in the reading list
    any_article_but_the_last = get_article(
        group, category, random_article.title
    )
    exread.article_common.go_to_article(driver, any_article_but_the_last.title)
    time_to_read = exread.article_common.time_to_read_in_seconds(
        context.driver
    )
    logging.debug(
        "%s is on '%s' article page: %s",
        actor_alias,
        any_article_but_the_last.title,
        driver.current_url,
    )
    just_read = VisitedArticle(
        any_article_but_the_last.index,
        any_article_but_the_last.title,
        time_to_read,
    )
    if visited_articles:
        visited_articles.append(just_read)
    else:
        visited_articles = [just_read]
    update_actor(context, actor_alias, visited_articles=visited_articles)


def articles_open_specific(context: Context, actor_alias: str, name: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    article = get_article(group, category, name)
    visited_articles = actor.visited_articles

    exread.article_common.go_to_article(driver, name)

    total_articles = exread.article_common.get_total_articles(context.driver)
    articles_read_counter = exread.article_common.get_read_counter(
        context.driver
    )
    time_to_complete = exread.article_common.get_time_to_complete(
        context.driver
    )
    time_to_read = exread.article_common.time_to_read_in_seconds(
        context.driver
    )

    logging.debug(
        "%s is on '%s' article: %s", actor_alias, name, driver.current_url
    )
    just_read = VisitedArticle(article.index, article.title, time_to_read)
    visited_articles.append(just_read)
    update_actor(
        context,
        actor_alias,
        articles_read_counter=articles_read_counter,
        articles_time_to_complete=time_to_complete,
        articles_total_number=total_articles,
        visited_articles=visited_articles,
    )


def articles_open_any(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "open_any_article")
    element_details = page.open_any_article(context.driver)
    update_actor(context, actor_alias, element_details=element_details)
    logging.info(f"{actor_alias} opened article: {element_details}")


def articles_found_useful_or_not(
    context: Context, actor_alias: str, useful_or_not: str
):
    if useful_or_not.lower() == "found":
        exread.article_common.flag_as_useful(context.driver)
    elif useful_or_not.lower() in ["haven't found", "hasn't found"]:
        exread.article_common.flag_as_not_useful(context.driver)
    else:
        raise KeyError(
            "Could not recognize: '{}'. Please use 'found' or 'did not find'".format(
                useful_or_not
            )
        )
    logging.debug("%s %s current article useful", actor_alias, useful_or_not)


def case_studies_go_to(context: Context, actor_alias: str, case_number: str):
    case_study_title = exread.home.get_case_study_title(
        context.driver, case_number
    )
    exread.home.open_case_study(context.driver, case_number)
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


def registration_go_to(context: Context, actor_alias: str, location: str):
    logging.debug(
        "%s decided to go to registration via %s link", actor_alias, location
    )
    if location.lower() == "article":
        exread.article_common.go_to_registration(context.driver)
    elif location.lower() == "article list":
        exread.article_list.go_to_registration(context.driver)
    elif location.lower() == "top bar":
        exread.header.go_to_registration(context.driver)
    else:
        raise KeyError(
            "Could not recognise registration link location: %s. Please use "
            "'article', 'article list' or 'top bar'".format(location)
        )
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
    registration_go_to(context, actor_alias, "top bar")
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
    if location.lower() == "article":
        exread.article_common.go_to_sign_in(context.driver)
    elif location.lower() == "article list":
        exread.article_list.go_to_sign_in(context.driver)
    elif location.lower() == "top bar":
        exread.header.go_to_sign_in(context.driver)
    else:
        raise KeyError(
            "Could not recognise 'sign in' link location: {}. Please use "
            "'article', 'article list' or 'top bar'".format(location)
        )
    sso.sign_in.should_be_here(context.driver)


def sign_in(context: Context, actor_alias: str, location: str):
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sign_in_go_to(context, actor_alias, location)
    sso.sign_in.fill_out(context.driver, email, password)
    sso.sign_in.submit(context.driver)


def sign_out(context: Context, actor_alias: str):
    exread.header.go_to_sign_out(context.driver)
    sso.sign_out.submit(context.driver)
    logging.debug("%s signed out", actor_alias)


def get_geo_ip(context: Context, actor_alias: str):
    driver = context.driver
    driver.get("https://www.geoiptool.com/")
    take_screenshot(driver, "geoip")
    logging.debug("%s checked the geoip", actor_alias)


@retry(wait_fixed=30000, stop_max_attempt_number=3)
def articles_share_on_social_media(
    context: Context, actor_alias: str, social_media: str
):
    context.article_url = context.driver.current_url
    if social_media.lower() == "email":
        exread.article_common.check_if_link_opens_email_client(context.driver)
    else:
        exread.article_common.check_if_link_opens_new_tab(
            context.driver, social_media
        )
        exread.article_common.share_via(context.driver, social_media)
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
    exread.home.close_video(context.driver)
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


def articles_show_all(context: Context, actor_alias: str):
    exread.article_list.show_all_articles(context.driver)
    logging.debug(
        "%s showed up all articled on the page: %s",
        actor_alias,
        context.driver.current_url,
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
    optional_param_keywords = ["n/a", "no", "empty", "without", "any"]
    if keyword and keyword.lower() in optional_param_keywords:
        keyword = None
    if sector and sector.lower() in optional_param_keywords:
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


def generic_fill_out_and_submit_form(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "generate_form_details")
    has_action(page, "fill_out")
    has_action(page, "submit")
    details = page.generate_form_details(actor)
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


def generic_visit_current_page_with_lang_param(
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


def generic_open_random_news_article(context: Context, actor_alias: str, article_type: str):
    flow = {
        "domestic": {
            "start": "Export Readiness - Updates for UK companies on EU Exit - Domestic",
            "finish": "Export Readiness - Domestic EU Exit news - article",
        },
        "international": {
            "start": "Export Readiness - Updates for non-UK companies on EU Exit - International",
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


def generic_pick_radio_option_and_submit(context: Context, actor_alias: str, option: str):
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
    element_details = page.open_any_element_in_section(context.driver, element_type, section_name)
    update_actor(context, actor_alias, element_details=element_details)
    logging.info(f"{actor_alias} opened random {element_type} from {section_name}")


def exred_open_random_advice_article(context: Context, actor_alias: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    driver = context.driver
    exread.advice_landing.visit(driver)
    exread.advice_landing.open_any_article(driver)
    exread.advice_article_list.open_any_article(driver)
    exread.advice_article.should_be_here(driver)
    update_actor(context, actor_alias, visited_page=exread.advice_article)


def generic_report_problem_with_page(context: Context, actor_alias: str):
    page = get_last_visited_page(context, actor_alias)
    has_action(page, "report_problem")
    page.report_problem(context.driver)
