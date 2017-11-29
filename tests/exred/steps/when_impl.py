# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random

from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import WebDriverException

from pages import (
    article_common,
    footer,
    guidance_common,
    header,
    home,
    personalised_journey,
    sso_common,
    sso_confirm_your_email,
    sso_profile_about,
    sso_registration,
    sso_registration_confirmation,
    sso_sign_in,
    triage_are_you_registered_with_companies_house,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_summary,
    triage_what_do_you_want_to_export
)
from registry.articles import GUIDANCE, get_article, get_articles
from registry.pages import get_page_object
from settings import EXRED_SECTORS
from utils import (
    add_actor,
    assertion_msg,
    get_actor,
    unauthenticated_actor,
    update_actor
)
from utils.mail_gun import get_verification_link


@retry(wait_fixed=30000, stop_max_attempt_number=3)
def visit_page(
        context: Context, actor_alias: str, page_name: str, *,
        first_time: bool = False):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    context.current_page = get_page_object(page_name)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page_name,
        context.current_page.URL)
    context.current_page.visit(context.driver, first_time=first_time)


def actor_classifies_himself_as(
        context: Context, actor_alias: str, exporter_status: str):
    actor = unauthenticated_actor(
        actor_alias, self_classification=exporter_status)
    add_actor(context, actor)


@retry(wait_fixed=30000, stop_max_attempt_number=3)
def open_group_element(
        context: Context, group: str, element: str, location: str):
    driver = context.driver
    if location == "home page":
        home.open(driver, group, element)
    elif location == "header menu":
        header.open(driver, group, element)
    elif location == "footer links":
        footer.open(driver, group, element)
    elif location == "personalised journey":
        personalised_journey.open(driver, group, element)
    else:
        raise KeyError("Could not recognize location: {}".format(location))


def guidance_open_category(
        context: Context, actor_alias: str, category: str, location: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if location.lower() != "personalised journey":
        visit_page(context, actor_alias, "Home")
    logging.debug(
        "%s is about to open Guidance '%s' category from %s",
        actor_alias, category, location)
    open_group_element(
        context, group="guidance", element=category, location=location)
    update_actor(
        context, actor_alias, article_group="guidance",
        article_category=category, article_location=location)


@retry(wait_fixed=30000, stop_max_attempt_number=3)
def guidance_open_random_category(
        context, actor_alias, *, location: str = "personalised journey"):
    category = random.choice(list(GUIDANCE.keys()))
    guidance_open_category(context, actor_alias, category, location)


def start_triage(context: Context, actor_alias: str):
    home.start_exporting_journey(context.driver)
    logging.debug("%s started triage process", actor_alias)


def continue_export_journey(context: Context, actor_alias: str):
    home.continue_export_journey(context.driver)
    logging.debug("%s decided to continue export journey", actor_alias)


def triage_say_what_do_you_want_to_export(
        context: Context, actor_alias: str, *, code: str = None,
        sector: str = None):
    driver = context.driver
    code, sector = triage_what_do_you_want_to_export.enter(
        driver, code, sector)
    triage_what_do_you_want_to_export.submit(driver)
    triage_have_you_exported.should_be_here(driver)
    update_actor(
        context, actor_alias, what_do_you_want_to_export=(code, sector))


def triage_say_you_exported_before(context: Context, actor_alias: str):
    driver = context.driver
    triage_have_you_exported.select_yes(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_regular_exporter.should_be_here(driver)
    update_actor(context, actor_alias, have_you_exported_before=True)


def triage_say_you_never_exported_before(context: Context, actor_alias: str):
    driver = context.driver
    triage_have_you_exported.select_no(driver)
    triage_have_you_exported.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, have_you_exported_before=False)


def triage_have_you_exported_before(context, actor_alias, has_or_has_never):
    if has_or_has_never == "has":
        triage_say_you_exported_before(context, actor_alias)
    elif has_or_has_never == "has never":
        triage_say_you_never_exported_before(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'has' or 'has never'" %
            has_or_has_never)


def triage_say_you_are_incorporated(
        context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_yes(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_company_name.should_be_here(driver)
    update_actor(context, actor_alias, are_you_incorporated=True)


def triage_say_you_are_not_incorporated(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_registered_with_companies_house.select_no(driver)
    triage_are_you_registered_with_companies_house.submit(driver)
    triage_summary.should_be_here(driver)
    update_actor(context, actor_alias, are_you_incorporated=False)


def triage_are_you_incorporated(context, actor_alias, is_or_not):
    if is_or_not == "is":
        triage_say_you_are_incorporated(context, actor_alias)
    elif is_or_not == "is not":
        triage_say_you_are_not_incorporated(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'is' or 'is not'" % is_or_not)


def triage_say_you_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_yes(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=True)


def triage_say_you_do_not_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_no(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_do_you_use_online_marketplaces.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=False)


def triage_do_you_export_regularly(context, actor_alias, regular_or_not):
    if regular_or_not == "a regular":
        triage_say_you_export_regularly(context, actor_alias)
    elif regular_or_not == "not a regular":
        triage_say_you_do_not_export_regularly(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'a regular' or "
            "'not a regular'" % regular_or_not)


def triage_say_you_use_online_marketplaces(context: Context, actor_alias: str):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_yes(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=True)


def triage_say_you_do_not_use_online_marketplaces(
        context: Context, actor_alias: str):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_no(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_are_you_registered_with_companies_house.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=False)


def triage_say_whether_you_use_online_marketplaces(
        context: Context, actor_alias: str, decision: str):
    if decision == "has":
        triage_say_you_use_online_marketplaces(context, actor_alias)
    elif decision == "has never":
        triage_say_you_do_not_use_online_marketplaces(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'has' or 'has never'" %
            decision)


def triage_enter_company_name(
        context: Context, actor_alias: str, use_suggestions: bool, *,
        company_name: str = None):
    driver = context.driver
    triage_company_name.enter_company_name(driver, company_name)
    if use_suggestions:
        triage_company_name.click_on_first_suggestion(driver)
    else:
        triage_company_name.hide_suggestions(driver)
    final_company_name = triage_company_name.get_company_name(driver)
    triage_company_name.submit(driver)
    triage_summary.should_be_here(driver)
    update_actor(context, actor_alias, company_name=final_company_name)


def triage_do_not_enter_company_name(context: Context, actor_alias: str):
    driver = context.driver
    triage_company_name.submit(driver)
    triage_summary.should_be_here(driver)
    update_actor(context, actor_alias, company_name=None)


def triage_what_is_your_company_name(context, actor_alias, decision):
    if decision == "types in":
        triage_enter_company_name(context, actor_alias, use_suggestions=False)
    elif decision == "does not provide":
        triage_do_not_enter_company_name(context, actor_alias)
    elif decision == "types in and selects":
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'types in', "
            "'does not provide' or 'types in and selects'" % decision)


def triage_should_be_classified_as_new(context: Context):
    triage_summary.should_be_classified_as_new(context.driver)


def triage_should_be_classified_as_occasional(context: Context):
    triage_summary.should_be_classified_as_occasional(context.driver)


def triage_should_be_classified_as_regular(context: Context):
    triage_summary.should_be_classified_as_regular(context.driver)


def triage_create_exporting_journey(context: Context, actor_alias: str):
    triage_summary.create_exporting_journey(context.driver)
    update_actor(context, alias=actor_alias, created_personalised_journey=True)


def triage_classify_as_new(
        context: Context, actor_alias: str, incorporated: bool, code: str,
        sector: str, *, start_from_home_page: bool = True):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_what_do_you_want_to_export(
        context, actor_alias, code=code, sector=sector)
    triage_say_you_never_exported_before(context, actor_alias)
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_new(context)
    update_actor(context, alias=actor_alias, triage_classification="new")


def triage_classify_as_occasional(
        context: Context, actor_alias: str, incorporated: bool,
        use_online_marketplaces: bool, code: str, sector: str, *,
        start_from_home_page: bool = True):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_what_do_you_want_to_export(
        context, actor_alias, code=code, sector=sector)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_do_not_export_regularly(context, actor_alias)
    if use_online_marketplaces:
        triage_say_you_use_online_marketplaces(context, actor_alias)
    else:
        triage_say_you_do_not_use_online_marketplaces(context, actor_alias)
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_occasional(context)
    update_actor(context, alias=actor_alias, triage_classification="occasional")


def triage_classify_as_regular(
        context: Context, actor_alias: str, incorporated: bool, code: str,
        sector: str, *, start_from_home_page: bool = True):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_what_do_you_want_to_export(
        context, actor_alias, code=code, sector=sector)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_export_regularly(context, actor_alias)
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_regular(context)
    update_actor(context, alias=actor_alias, triage_classification="regular")


def triage_classify_as(
        context: Context, actor_alias: str, *, exporter_status: str = None,
        is_incorporated: str = None, start_from_home_page: bool = True):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    actor = get_actor(context, actor_alias)

    if actor.what_do_you_want_to_export is not None:
        code, sector = actor.what_do_you_want_to_export
    else:
        code, sector = random.choice(list(EXRED_SECTORS.items()))

    if actor.do_you_use_online_marketplaces is not None:
        use_online_marketplaces = actor.do_you_use_online_marketplaces
    else:
        use_online_marketplaces = random.choice([True, False])

    if exporter_status:
        exporter_status = exporter_status.lower()
    else:
        exporter_status = random.choice(["new", "occasional", "regular"])

    if is_incorporated is not None:
        if is_incorporated.lower() == "has":
            incorporated = True
        elif is_incorporated.lower() == "has not":
            incorporated = False
        else:
            raise KeyError(
                "Could not recognise: '%s'. Please use 'has' or 'has not'"
                .format(is_incorporated))
    else:
        incorporated = random.choice([True, False])

    if start_from_home_page:
        visit_page(context, actor_alias, "home")

    logging.debug(
        "%s decided to classify himself/herself as %s Exporter", actor_alias,
        exporter_status)

    if exporter_status == "new":
        triage_classify_as_new(
            context, actor_alias, incorporated, code, sector,
            start_from_home_page=start_from_home_page)
    elif exporter_status == "occasional":
        triage_classify_as_occasional(
            context, actor_alias, incorporated, use_online_marketplaces, code,
            sector, start_from_home_page=start_from_home_page)
    elif exporter_status == "regular":
        triage_classify_as_regular(
            context, actor_alias, incorporated, code, sector,
            start_from_home_page=start_from_home_page)
    update_actor(
        context, actor_alias, article_group="personalised journey",
        article_category=exporter_status)


def triage_should_see_answers_to_questions(context, actor_alias):
    actor = get_actor(context, actor_alias)
    q_and_a = triage_summary.get_questions_and_answers(context.driver)
    if actor.what_do_you_want_to_export is not None:
        code, sector = actor.what_do_you_want_to_export
        question = "What do you want to export?"
        with assertion_msg(
                "Expected answer to question '%s' to be '%s', but got '%s' "
                "instead", question, sector, q_and_a[question]):
            assert q_and_a[question] == sector
    if actor.company_name is not None:
        name = actor.company_name
        question = "Company name"
        with assertion_msg(
                "Expected answer to question '%s' to be '%s', but got '%s' "
                "instead", question, name, q_and_a[question]):
            assert q_and_a[question] == name
    if actor.have_you_exported_before is not None:
        exported_before = "Yes" if actor.have_you_exported_before else "No"
        question = "Have you exported before?"
        with assertion_msg(
                "Expected answer to question '%s' to be '%s', but got '%s' "
                "instead", question, exported_before, q_and_a[question]):
            assert q_and_a[question] == exported_before
    if actor.do_you_export_regularly is not None:
        export_regularly = "Yes" if actor.do_you_export_regularly else "No"
        question = "Is exporting a regular part of your business activities?"
        with assertion_msg(
                "Expected answer to question '%s' to be '%s', but got '%s' "
                "instead", question, export_regularly, q_and_a[question]):
            assert q_and_a[question] == export_regularly
    if actor.are_you_incorporated is not None:
        incorporated = "Yes" if actor.are_you_incorporated else "No"
        assert q_and_a["Is your company incorporated in the UK?"] == incorporated
    if actor.do_you_use_online_marketplaces is not None:
        sell_online = "Yes" if actor.do_you_use_online_marketplaces else "No"
        assert q_and_a["Do you use online marketplaces to sell your products?"] == sell_online


def personalised_journey_create_page(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    exporter_status = actor.self_classification
    triage_classify_as(context, actor_alias, exporter_status=exporter_status)
    triage_create_exporting_journey(context, actor_alias)
    personalised_journey.should_be_here(context.driver)


def triage_change_answers(context: Context, actor_alias: str):
    triage_summary.change_answers(context.driver)
    triage_what_do_you_want_to_export.should_be_here(context.driver)
    logging.debug("%s decided to change the Triage answers", actor_alias)


def triage_answer_questions_again(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    code, sector = actor.what_do_you_want_to_export
    triage_what_do_you_want_to_export.is_sector(driver, code, sector)
    triage_what_do_you_want_to_export.submit(driver)

    def continue_from_are_you_incorporated():
        if actor.are_you_incorporated:
            company_name = actor.company_name
            triage_are_you_registered_with_companies_house.is_yes_selected(driver)
            triage_are_you_registered_with_companies_house.submit(driver)
            triage_company_name.should_be_here(driver)
            triage_company_name.is_company_name(driver, company_name)
            triage_company_name.submit(driver)
        else:
            triage_are_you_registered_with_companies_house.is_no_selected(driver)
            triage_are_you_registered_with_companies_house.submit(driver)
        triage_summary.should_be_here(driver)

    if actor.have_you_exported_before is not None:
        if actor.have_you_exported_before:
            triage_have_you_exported.is_yes_selected(driver)
            triage_have_you_exported.submit(driver)
            triage_are_you_regular_exporter.should_be_here(driver)
            if actor.do_you_export_regularly:
                triage_are_you_regular_exporter.is_yes_selected(driver)
                triage_are_you_regular_exporter.submit(driver)
                triage_are_you_registered_with_companies_house.should_be_here(driver)
                continue_from_are_you_incorporated()
                triage_summary.should_be_classified_as_regular(driver)
            else:
                triage_are_you_regular_exporter.is_no_selected(driver)
                triage_are_you_regular_exporter.submit(driver)
                triage_do_you_use_online_marketplaces.should_be_here(driver)
                if actor.do_you_use_online_marketplaces:
                    triage_do_you_use_online_marketplaces.is_yes_selected(driver)
                else:
                    triage_do_you_use_online_marketplaces.is_no_selected(driver)
                triage_do_you_use_online_marketplaces.submit(driver)
                continue_from_are_you_incorporated()
                triage_summary.should_be_classified_as_occasional(driver)
        else:
            triage_have_you_exported.is_no_selected(driver)
            triage_have_you_exported.submit(driver)
            triage_are_you_registered_with_companies_house.should_be_here(driver)
            continue_from_are_you_incorporated()
            triage_summary.should_be_classified_as_new(driver)
        triage_should_see_answers_to_questions(context, actor_alias)
    logging.debug("%s was able to change the Triage answers", actor_alias)


def triage_go_through_again(context: Context, actor_alias: str):
    personalised_journey_update_preference(context, actor_alias)
    triage_change_answers(context, actor_alias)
    triage_classify_as(context, actor_alias, start_from_home_page=False)


def export_readiness_open_category(
        context: Context, actor_alias: str, category: str, location: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if location.lower() != "personalised journey":
        visit_page(context, actor_alias, "Home")
    logging.debug(
        "%s is about to open Export Readiness '%s' category from %s",
        actor_alias, category, location)
    open_group_element(
        context, group="export readiness", element=category, location=location)
    update_actor(
        context, actor_alias, article_group="export readiness",
        article_category=category, article_location=location)


def set_sector_preference(
        context: Context, actor_alias: str, *, goods_or_services: str = None,
        good: str = None, service: str = None):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    assert goods_or_services or not (good and service)
    message = ("You can provide only one of the following arguments: "
               "`goods_or_services`, `good` or `service`. You've passed: "
               "`goods_or_services={} good={} service={}"
               .format(goods_or_services, good, service))
    optional_args = [goods_or_services, good, service]
    assert len([arg for arg in optional_args if arg is not None]) == 1, message
    logging.debug(
        "%s exports: `goods_or_services=%s good=%s service=5s",
        goods_or_services, good, service)
    if goods_or_services is not None:
        if goods_or_services.lower() == "goods":
            sectors = [(code, sector)
                       for code, sector in EXRED_SECTORS.items()
                       if code.startswith("HS")]
        elif goods_or_services.lower() == "services":
            sectors = [(code, sector)
                       for code, sector in EXRED_SECTORS.items()
                       if code.startswith("EB")]
        else:
            raise KeyError(
                "Could not recognise '%s' as valid sector. Please use 'goods' "
                "or 'services'" % goods_or_services)
        code, sector = random.choice(sectors)
    else:
        filtered_sectors = [(code, sector)
                            for code, sector in EXRED_SECTORS.items()
                            if sector == (good or service)
                            ]
        assert len(filtered_sectors) == 1, ("Could not find code & sector for"
                                            " '{}'".format((good or service)))
        code, sector = filtered_sectors[0]
    logging.debug("Code: %s - Sector: %s", code, sector)
    update_actor(
        context, actor_alias, what_do_you_want_to_export=(code, sector))
    logging.debug(
        "%s decided that her/his preferred sector is: %s %s", actor_alias,
        code, sector)


def set_online_marketplace_preference(
        context: Context, actor_alias: str, used_or_not: str):
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
            % used_or_not)
    update_actor(
        context, actor_alias, do_you_use_online_marketplaces=used)
    logging.debug(
        "%s decided that he/she %s online marketplaces before", actor_alias,
        used_or_not)


def articles_open_first(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    first_article = get_articles(group, category)[0]
    guidance_common.open_first_article(driver)
    article_common.should_see_article(driver, first_article.title)
    logging.debug(
        "%s is on the first article %s: %s", actor_alias,
        first_article.title, driver.current_url)


def articles_open_any_but_the_last(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    articles = get_articles(group, category)
    any_article_but_the_last = random.choice(articles[:-1])
    guidance_common.show_all_articles(driver)
    article_common.go_to_article(driver, any_article_but_the_last.title)
    logging.debug(
        "%s is on '%s' article page: %s", actor_alias,
        any_article_but_the_last.title, driver.current_url)


def articles_open_any(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    visited_articles = actor.visited_articles
    articles = get_articles(group, category)
    any_article = random.choice(articles)
    article_common.show_all_articles(driver)

    article_common.go_to_article(driver, any_article.title)
    total_articles = article_common.get_total_articles(context.driver)
    articles_read_counter = article_common.get_read_counter(context.driver)
    time_to_complete = article_common.get_time_to_complete(context.driver)
    time_to_read = article_common.time_to_read_in_seconds(context.driver)
    logging.debug(
        "%s is on '%s' article page: %s", actor_alias,
        any_article .title, driver.current_url)
    just_read = (any_article.index, any_article.title, time_to_read)
    if visited_articles:
        visited_articles.append(just_read)
    else:
        visited_articles = [just_read]
    update_actor(
        context, actor_alias, articles_read_counter=articles_read_counter,
        articles_time_to_complete=time_to_complete,
        articles_total_number=total_articles,
        visited_articles=visited_articles)


def guidance_read_through_all_articles(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category

    visited_articles = []

    current_article_name = article_common.get_article_name(driver)
    time_to_read = article_common.time_to_read_in_seconds(context.driver)
    logging.debug("%s is on '%s' article", actor_alias, current_article_name)
    current_article = get_article(group, category, current_article_name)
    assert current_article, "Could not find Article: %s" % current_article_name
    visited_articles.append(
        (current_article.index, current_article_name, time_to_read)
    )
    next_article = current_article.next

    while next_article is not None:
        article_common.check_if_link_to_next_article_is_displayed(
            driver, next_article.title)
        article_common.go_to_next_article(driver)
        current_article_name = article_common.get_article_name(driver)
        time_to_read = article_common.time_to_read_in_seconds(context.driver)
        visited_articles.append(
            (next_article.index, next_article.title, time_to_read)
        )
        logging.debug(
            "%s is on '%s' article", actor_alias, current_article_name)
        current_article = get_article(group, category, current_article_name)
        assert current_article, ("Could not find Article: %s" %
                                 current_article_name)
        next_article = current_article.next
        if next_article:
            logging.debug(
                "The next article to visit is: %s", next_article.title)
        else:
            logging.debug("There's no more articles to see")

    update_actor(context, actor_alias, visited_articles=visited_articles)


def articles_open_group(
        context: Context, actor_alias: str, group: str, *,
        location: str = None):
    categories = {
        "guidance": [
            "market research",
            "customer insight",
            "finance",
            "business planning",
            "getting paid",
            "operations and compliance"
        ],
        "export readiness": [
            "new",
            "occasional",
            "regular"
        ]
    }
    category = random.choice(categories[group.lower()])
    locations = ["header menu", "footer links", "home page"]
    location = location or random.choice(locations)

    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    update_actor(
        context, actor_alias, article_group=group, article_category=category)

    logging.debug(
        "%s decided to open '%s' '%s' Articles via '%s'", actor_alias,
        category, group, location)
    if group.lower() == "export readiness":
        export_readiness_open_category(
            context, actor_alias, category=category, location=location)
    elif group.lower() == "guidance":
        guidance_open_category(context, actor_alias, category, location)
    else:
        raise KeyError(
            "Did not recognize '{}'. Please use: 'Guidance' or 'Export "
            "Readiness'".format(group))
    total_articles = article_common.get_total_articles(context.driver)
    articles_read_counter = article_common.get_read_counter(context.driver)
    time_to_complete = article_common.get_time_to_complete(context.driver)
    update_actor(
        context, actor_alias, articles_read_counter=articles_read_counter,
        articles_time_to_complete=time_to_complete,
        articles_total_number=total_articles)


def articles_go_back_to_same_group(
        context: Context, actor_alias: str, group: str, location: str):
    actor = get_actor(context, actor_alias)
    category = actor.article_category
    logging.debug(
        "%s decided to open '%s' '%s' Articles via '%s'", actor_alias,
        category, group, location)
    if group.lower() == "export readiness":
        export_readiness_open_category(
            context, actor_alias, category=category, location=location)
    elif group.lower() == "guidance":
        guidance_open_category(context, actor_alias, category, location)
    else:
        raise KeyError(
            "Did not recognize '{}'. Please use: 'Guidance' or 'Export "
            "Readiness'".format(group))


def articles_go_back_to_article_list(context: Context, actor_alias: str):
    article_common.go_back_to_article_list(context.driver)
    logging.debug("%s went back to the Article List page", actor_alias)


def articles_found_useful_or_not(
        context: Context, actor_alias: str, useful_or_not: str):
    if useful_or_not.lower() == "found":
        article_common.flag_as_useful(context.driver)
    elif useful_or_not.lower() in ["haven't found", "hasn't found"]:
        article_common.flag_as_not_useful(context.driver)
    else:
        raise KeyError(
            "Could not recognize: '{}'. Please use 'found' or 'did not find'"
            .format(useful_or_not))
    logging.debug("%s %s current article useful", actor_alias, useful_or_not)


def case_studies_go_to(context: Context, actor_alias: str, case_number: str):
    case_study_title = home.get_case_study_title(context.driver, case_number)
    home.open_case_study(context.driver, case_number)
    update_actor(context, actor_alias, case_study_title=case_study_title)
    logging.debug(
        "%s opened %s case study, entitled: %s", actor_alias, case_number,
        case_study_title)


def open_link(
        context: Context, actor_alias: str, group: str, category: str,
        location: str):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    update_actor(
        context, actor_alias, article_group=group, article_category=category)
    logging.debug(
        "%s is about to open link to '%s' '%s' via %s", actor_alias, group,
        category, location)
    open_group_element(
        context, group=group, element=category, location=location)
    update_actor(
        context, actor_alias, article_group="guidance",
        article_category=category, article_location=location)


def open_service_link_on_interim_page(
        context: Context, actor_alias: str, service: str):
    page_name = "interim {}".format(service)
    page = get_page_object(page_name)
    page.go_to_service(context.driver)
    logging.debug("%s went to %s service page", actor_alias, service)


def personalised_journey_update_preference(context, actor_alias):
    personalised_journey.update_preferences(context.driver)


def articles_read_a_number_of_them(
        context: Context, actor_alias: str, number: str):
    numbers = {
        "a tenth": 10,
        "a ninth": 9,
        "an eight": 8,
        "a seventh": 7,
        "a sixth": 6,
        "a fifth": 5,
        "a fourth": 4,
        "a quarter": 4,
        "a third": 3,
        "a half": 2,
        "all": 1
    }
    divider = numbers[number.lower()]
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    articles = get_articles(group, category)
    number_to_read = int(len(articles) / divider)
    number_to_read = number_to_read if number_to_read > 0 else 1
    for idx in range(1, number_to_read + 1):
        articles_open_any(context, actor_alias)
        articles_go_back_to_article_list(context, actor_alias)
        logging.debug(
            "%s read %d article(s) out of %d (%s of %d articles from '%s'"
            " articles)", actor_alias, idx, number_to_read, number,
            len(articles), category)


def registration_go_to(context: Context, actor_alias: str, location: str):
    logging.debug(
        "%s decided to go to registration via %s link", actor_alias, location)
    if location.lower() == "article":
        article_common.go_to_registration(context.driver)
    elif location.lower() == "top bar":
        header.go_to_registration(context.driver)
    else:
        raise KeyError(
            "Could not recognise registration link location: %s. Please use "
            "'article' or 'top bar'".format(location))
    sso_registration.should_be_here(context.driver)


def registration_should_get_verification_email(context: Context, actor_alias: str):
    """Will check if the Exporter received an email verification message.

    :param context: behave `context` object
    :param actor_alias: alias of the Actor used in the scope of the scenario
    """
    logging.debug("Searching for an email verification message...")
    actor = get_actor(context, actor_alias)
    link = get_verification_link(context, actor.email)
    update_actor(context, actor_alias, email_confirmation_link=link)


def registration_open_email_confirmation_link(context, actor_alias):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param actor_alias: alias of the Actor used in the scope of the scenario
    :type actor_alias: str
    """
    actor = get_actor(context, actor_alias)
    link = actor.email_confirmation_link

    # Step 1 - open confirmation link
    context.driver.get(link)

    # Step 3 - confirm that Supplier is on SSO Confirm Your Email page
    sso_confirm_your_email.should_be_here(context.driver)
    logging.debug("Supplier is on the SSO Confirm your email address page")


def registration_create_and_verify_account(
        context: Context, actor_alias: str, *, fake_verification: bool = True):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sso_registration.fill_out(driver, email, password)
    sso_registration.submit(driver)
    sso_registration_confirmation.should_be_here(driver)
    if fake_verification:
        sso_common.verify_account(email)
    else:
        registration_should_get_verification_email(context, actor_alias)
        registration_open_email_confirmation_link(context, actor_alias)
        sso_confirm_your_email.submit(context.driver)
        sso_profile_about.should_be_here(context.driver)
    update_actor(context, actor_alias, registered=True)


def clear_the_cookies(context: Context, actor_alias: str):
    try:
        cookies = context.driver.get_cookies()
        logging.debug("COOKIES: %s", cookies)
        context.driver.delete_all_cookies()
        logging.debug("Successfully cleared cookies for %s", actor_alias)
    except WebDriverException:
        logging.error("Failed to clear cookies for %s", actor_alias)


def sign_in_go_to(context, actor_alias, location):
    if location.lower() == "article":
        article_common.go_to_sign_in(context.driver)
    elif location.lower() == "top bar":
        header.go_to_sign_in(context.driver)
    else:
        raise KeyError(
            "Could not recognise registration link location: %s. Please use "
            "'article' or 'top bar'".format(location))
    sso_sign_in.should_be_here(context.driver)


def sign_in(context, actor_alias, location):
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sign_in_go_to(context, actor_alias, location)
    sso_sign_in.fill_out(context.driver, email, password)
    sso_sign_in.submit(context.driver)
