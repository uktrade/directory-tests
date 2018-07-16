# -*- coding: utf-8 -*-
"""When step implementations."""
import logging
import random

from behave.model import Table
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils import (
    VisitedArticle,
    add_actor,
    assertion_msg,
    get_actor,
    take_screenshot,
    unauthenticated_actor,
    update_actor,
)
from utils.gov_notify import get_verification_link

from pages import (
    exread_article_common,
    article_list,
    fas_ui_contact_us,
    footer,
    guidance_common,
    header,
    home,
    international,
    language_selector,
    personalised_journey,
    personalised_what_do_you_want_to_export,
    sso_common,
    sso_confirm_your_email,
    sso_registration,
    sso_registration_confirmation,
    sso_sign_in,
    sso_sign_out,
    triage_are_you_registered_with_companies_house,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_summary,
    triage_what_do_you_want_to_export,
)
from registry.articles import (
    GUIDANCE,
    get_article,
    get_articles,
    get_random_article,
)
from registry.pages import get_page_object
from settings import EXRED_SECTORS

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
    first_time: bool = False
):
    """Will visit specific page.

    NOTE:
    In order for the retry scheme to work properly you should have
    the webdriver' page load timeout set to value lower than the retry's
    `wait_fixed` timer, e.g `driver.set_page_load_timeout(time_to_wait=30)`
    """
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    page = get_page_object(page_name)
    logging.debug(
        "%s will visit '%s' page using: '%s'", actor_alias, page_name, page.URL
    )
    assert hasattr(page, "visit")
    if "industry" in page_name.lower():
        page.visit(context.driver, first_time=first_time, page_name=page_name)
    else:
        page.visit(context.driver, first_time=first_time)
    update_actor(context, actor_alias, visited_page=page_name)


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
    if location.lower() == "home page":
        home.open(driver, group, element)
    elif location.lower() in ["header menu", "header"]:
        header.open(driver, group, element)
    elif location.lower() in ["footer links", "footer"]:
        footer.open(driver, group, element)
    elif location.lower() == "personalised journey":
        personalised_journey.open(driver, group, element)
    elif location.lower() == "international page":
        international.open(driver, group, element, same_tab=True)
    else:
        raise KeyError("Could not recognize location: {}".format(location))


def guidance_open_category(
    context: Context, actor_alias: str, category: str, location: str
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if location.lower() != "personalised journey":
        visit_page(context, actor_alias, "Home")
    logging.debug(
        "%s is about to open Guidance '%s' category from %s",
        actor_alias,
        category,
        location,
    )
    open_group_element(
        context, group="guidance", element=category, location=location
    )
    update_actor(
        context,
        actor_alias,
        article_group="guidance",
        article_category=category,
        article_location=location,
    )


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_webdriver_error,
)
def guidance_open_random_category(
    context: Context,
    actor_alias: str,
    *,
    location: str = "personalised journey"
):
    category = random.choice(list(GUIDANCE.keys()))
    guidance_open_category(context, actor_alias, category, location)


def start_triage(context: Context, actor_alias: str):
    home.start_exporting_journey(context.driver)
    logging.debug("%s started triage process", actor_alias)


def continue_export_journey(context: Context, actor_alias: str):
    home.continue_export_journey(context.driver)
    logging.debug("%s decided to continue export journey", actor_alias)


def personalised_choose_sector(
    context: Context,
    actor_alias: str,
    *,
    goods_or_services: str = None,
    code: str = None,
    sector: str = None
):
    driver = context.driver
    code, sector = personalised_what_do_you_want_to_export.enter(
        driver, code, sector
    )
    personalised_what_do_you_want_to_export.submit(driver)
    triage_have_you_exported.should_be_here(driver)
    update_actor(
        context,
        actor_alias,
        what_do_you_want_to_export=(goods_or_services, code, sector),
    )


def triage_question_what_do_you_want_to_export(
    context: Context, actor_alias: str, goods_or_services: str
):
    if goods_or_services.lower() == "services":
        triage_what_do_you_want_to_export.select_services(context.driver)
    elif goods_or_services.lower() == "goods":
        triage_what_do_you_want_to_export.select_goods(context.driver)
    elif goods_or_services.lower() == "goods and services":
        triage_what_do_you_want_to_export.select_goods_and_services(
            context.driver
        )
    else:
        raise KeyError(
            "Could not recognize what you want to export! {}".format(
                goods_or_services
            )
        )
    triage_what_do_you_want_to_export.submit(context.driver)
    triage_are_you_registered_with_companies_house.should_be_here(
        context.driver
    )
    logging.debug("%s chose to export %s", actor_alias, goods_or_services)


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
    triage_what_do_you_want_to_export.should_be_here(driver)
    update_actor(context, actor_alias, have_you_exported_before=False)


def triage_have_you_exported_before(
    context: Context, actor_alias: str, has_or_has_never: str
):
    if has_or_has_never == "has":
        triage_say_you_exported_before(context, actor_alias)
    elif has_or_has_never == "has never":
        triage_say_you_never_exported_before(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'has' or 'has never'"
            % has_or_has_never
        )


def triage_say_you_want_to_export_goods(
    context: Context, actor_alias: str, code: str, sector: str
):
    triage_what_do_you_want_to_export.select_goods(context.driver)
    triage_what_do_you_want_to_export.submit(context.driver)
    triage_are_you_registered_with_companies_house.should_be_here(
        context.driver
    )
    update_actor(
        context,
        actor_alias,
        what_do_you_want_to_export=("goods", code, sector),
    )


def triage_say_you_want_to_export_services(
    context: Context, actor_alias: str, code: str, sector: str
):
    triage_what_do_you_want_to_export.select_services(context.driver)
    triage_what_do_you_want_to_export.submit(context.driver)
    triage_are_you_registered_with_companies_house.should_be_here(
        context.driver
    )
    update_actor(
        context,
        actor_alias,
        what_do_you_want_to_export=("services", code, sector),
    )


def triage_say_you_want_to_export_goods_and_services(
    context: Context, actor_alias: str, code: str, sector: str
):
    triage_what_do_you_want_to_export.select_goods(context.driver)
    triage_what_do_you_want_to_export.select_services(context.driver)
    triage_what_do_you_want_to_export.submit(context.driver)
    triage_are_you_registered_with_companies_house.should_be_here(
        context.driver
    )
    update_actor(
        context,
        actor_alias,
        what_do_you_want_to_export=("goods and services", code, sector),
    )


def triage_say_you_are_incorporated(context: Context, actor_alias: str):
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


def triage_are_you_incorporated(
    context: Context, actor_alias: str, is_or_not: str
):
    if is_or_not == "is":
        triage_say_you_are_incorporated(context, actor_alias)
    elif is_or_not == "is not":
        triage_say_you_are_not_incorporated(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize %s, please use 'is' or 'is not'" % is_or_not
        )


def triage_say_you_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_yes(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_what_do_you_want_to_export.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=True)


def triage_say_you_do_not_export_regularly(context: Context, actor_alias: str):
    driver = context.driver
    triage_are_you_regular_exporter.select_no(driver)
    triage_are_you_regular_exporter.submit(driver)
    triage_do_you_use_online_marketplaces.should_be_here(driver)
    update_actor(context, actor_alias, do_you_export_regularly=False)


def triage_do_you_export_regularly(
    context: Context, actor_alias: str, regular_or_not: str
):
    if regular_or_not == "a regular":
        triage_say_you_export_regularly(context, actor_alias)
    elif regular_or_not == "not a regular":
        triage_say_you_do_not_export_regularly(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'a regular' or "
            "'not a regular'" % regular_or_not
        )


def triage_say_you_use_online_marketplaces(context: Context, actor_alias: str):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_yes(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_what_do_you_want_to_export.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=True)


def triage_say_you_do_not_use_online_marketplaces(
    context: Context, actor_alias: str
):
    driver = context.driver
    triage_do_you_use_online_marketplaces.select_no(driver)
    triage_do_you_use_online_marketplaces.submit(driver)
    triage_what_do_you_want_to_export.should_be_here(driver)
    update_actor(context, actor_alias, do_you_use_online_marketplaces=False)


def triage_say_whether_you_use_online_marketplaces(
    context: Context, actor_alias: str, decision: str
):
    if decision == "has":
        triage_say_you_use_online_marketplaces(context, actor_alias)
    elif decision == "has never":
        triage_say_you_do_not_use_online_marketplaces(context, actor_alias)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'has' or 'has never'"
            % decision
        )


def triage_enter_company_name(
    context: Context,
    actor_alias: str,
    use_suggestions: bool,
    *,
    company_name: str = None
):
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


def triage_what_is_your_company_name(
    context: Context, actor_alias: str, decision: str
):
    if decision == "types in":
        triage_enter_company_name(context, actor_alias, use_suggestions=False)
    elif decision == "does not provide":
        triage_do_not_enter_company_name(context, actor_alias)
    elif decision == "types in and selects":
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        raise KeyError(
            "Could not recognize '%s', please use 'types in', "
            "'does not provide' or 'types in and selects'" % decision
        )


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
    context: Context,
    actor_alias: str,
    incorporated: bool,
    goods_or_services: str,
    code: str,
    sector: str,
    *,
    start_from_home_page: bool = True
):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_you_never_exported_before(context, actor_alias)
    if goods_or_services == "goods":
        triage_say_you_want_to_export_goods(context, actor_alias, code, sector)
    elif goods_or_services == "services":
        triage_say_you_want_to_export_services(
            context, actor_alias, code, sector
        )
    else:
        triage_say_you_want_to_export_goods_and_services(
            context, actor_alias, code, sector
        )
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_new(context)
    update_actor(context, alias=actor_alias, triage_classification="new")


def triage_classify_as_occasional(
    context: Context,
    actor_alias: str,
    incorporated: bool,
    use_online_marketplaces: bool,
    goods_or_services: str,
    code: str,
    sector: str,
    *,
    start_from_home_page: bool = True
):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_do_not_export_regularly(context, actor_alias)
    if use_online_marketplaces:
        triage_say_you_use_online_marketplaces(context, actor_alias)
    else:
        triage_say_you_do_not_use_online_marketplaces(context, actor_alias)
    if goods_or_services == "goods":
        triage_say_you_want_to_export_goods(context, actor_alias, code, sector)
    elif goods_or_services == "services":
        triage_say_you_want_to_export_services(
            context, actor_alias, code, sector
        )
    else:
        triage_say_you_want_to_export_goods_and_services(
            context, actor_alias, code, sector
        )
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_occasional(context)
    update_actor(
        context, alias=actor_alias, triage_classification="occasional"
    )


def triage_classify_as_regular(
    context: Context,
    actor_alias: str,
    incorporated: bool,
    goods_or_services: str,
    code: str,
    sector: str,
    *,
    start_from_home_page: bool = True
):
    if start_from_home_page:
        start_triage(context, actor_alias)
    triage_say_you_exported_before(context, actor_alias)
    triage_say_you_export_regularly(context, actor_alias)
    if goods_or_services == "goods":
        triage_say_you_want_to_export_goods(context, actor_alias, code, sector)
    elif goods_or_services == "services":
        triage_say_you_want_to_export_services(
            context, actor_alias, code, sector
        )
    else:
        triage_say_you_want_to_export_goods_and_services(
            context, actor_alias, code, sector
        )
    if incorporated:
        triage_say_you_are_incorporated(context, actor_alias)
        triage_enter_company_name(context, actor_alias, use_suggestions=True)
    else:
        triage_say_you_are_not_incorporated(context, actor_alias)
    triage_should_be_classified_as_regular(context)
    update_actor(context, alias=actor_alias, triage_classification="regular")


def triage_classify_as(
    context: Context,
    actor_alias: str,
    *,
    exporter_status: str = None,
    is_incorporated: str = None,
    start_from_home_page: bool = True
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    actor = get_actor(context, actor_alias)

    if actor.what_do_you_want_to_export is not None:
        goods_or_services, code, sector = actor.what_do_you_want_to_export
    else:
        options = ["goods", "services", "goods and services"]
        goods_or_services = random.choice(options)
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
                "Could not recognise: '%s'. Please use 'has' or 'has not'".format(
                    is_incorporated
                )
            )
    else:
        incorporated = random.choice([True, False])

    if start_from_home_page:
        visit_page(context, actor_alias, "home")

    logging.debug(
        "%s decided to classify himself/herself as %s Exporter",
        actor_alias,
        exporter_status,
    )

    if exporter_status == "new":
        triage_classify_as_new(
            context,
            actor_alias,
            incorporated,
            goods_or_services,
            code,
            sector,
            start_from_home_page=start_from_home_page,
        )
    elif exporter_status == "occasional":
        triage_classify_as_occasional(
            context,
            actor_alias,
            incorporated,
            use_online_marketplaces,
            goods_or_services,
            code,
            sector,
            start_from_home_page=start_from_home_page,
        )
    elif exporter_status == "regular":
        triage_classify_as_regular(
            context,
            actor_alias,
            incorporated,
            goods_or_services,
            code,
            sector,
            start_from_home_page=start_from_home_page,
        )
    update_actor(
        context,
        actor_alias,
        article_group="personalised journey",
        article_category=exporter_status,
    )


def triage_should_see_answers_to_questions(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    q_and_a = triage_summary.get_questions_and_answers(context.driver)
    if actor.what_do_you_want_to_export is not None:
        goods_or_services, code, sector = actor.what_do_you_want_to_export
        question = "What do you want to export?"
        with assertion_msg(
            "Expected answer to question '%s' to be '%s', but got '%s' "
            "instead",
            question,
            goods_or_services,
            q_and_a[question],
        ):
            assert q_and_a[question] == goods_or_services.capitalize()
    if actor.company_name is not None:
        name = actor.company_name
        question = "Company name"
        with assertion_msg(
            "Expected answer to question '%s' to be '%s', but got '%s' "
            "instead",
            question,
            name,
            q_and_a[question],
        ):
            assert q_and_a[question] == name
    if actor.have_you_exported_before is not None:
        exported_before = "Yes" if actor.have_you_exported_before else "No"
        question = "Have you exported before?"
        with assertion_msg(
            "Expected answer to question '%s' to be '%s', but got '%s' "
            "instead",
            question,
            exported_before,
            q_and_a[question],
        ):
            assert q_and_a[question] == exported_before
    if actor.do_you_export_regularly is not None:
        export_regularly = "Yes" if actor.do_you_export_regularly else "No"
        question = "Is exporting a regular part of your business activities?"
        with assertion_msg(
            "Expected answer to question '%s' to be '%s', but got '%s' "
            "instead",
            question,
            export_regularly,
            q_and_a[question],
        ):
            assert q_and_a[question] == export_regularly
    if actor.are_you_incorporated is not None:
        incorporated = "Yes" if actor.are_you_incorporated else "No"
        question = "Is your company incorporated in the UK?"
        assert q_and_a[question] == incorporated
    if actor.do_you_use_online_marketplaces is not None:
        sell_online = "Yes" if actor.do_you_use_online_marketplaces else "No"
        question = "Do you use online marketplaces to sell your products?"
        assert q_and_a[question] == sell_online


def personalised_journey_create_page(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    exporter_status = actor.self_classification
    triage_classify_as(context, actor_alias, exporter_status=exporter_status)
    triage_create_exporting_journey(context, actor_alias)
    personalised_journey.should_be_here(context.driver)


def triage_change_answers(context: Context, actor_alias: str):
    triage_summary.change_answers(context.driver)
    triage_have_you_exported.should_be_here(context.driver)
    logging.debug("%s decided to change the Triage answers", actor_alias)


def triage_answer_questions_again(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)

    def continue_from_are_you_incorporated():
        if actor.are_you_incorporated:
            company_name = actor.company_name
            triage_are_you_registered_with_companies_house.is_yes_selected(
                driver
            )
            triage_are_you_registered_with_companies_house.submit(driver)
            triage_company_name.should_be_here(driver)
            triage_company_name.is_company_name(driver, company_name)
            triage_company_name.submit(driver)
        else:
            triage_are_you_registered_with_companies_house.is_no_selected(
                driver
            )
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
                goods_or_services, _, _ = actor.what_do_you_want_to_export
                if goods_or_services == "goods":
                    triage_what_do_you_want_to_export.is_goods_selected(
                        context.driver
                    )
                else:
                    triage_what_do_you_want_to_export.is_services_selected(
                        context.driver
                    )
                triage_what_do_you_want_to_export.submit(driver)
                triage_are_you_registered_with_companies_house.should_be_here(
                    driver
                )
                continue_from_are_you_incorporated()
                triage_summary.should_be_classified_as_regular(driver)
            else:
                triage_are_you_regular_exporter.is_no_selected(driver)
                triage_are_you_regular_exporter.submit(driver)
                triage_do_you_use_online_marketplaces.should_be_here(driver)
                if actor.do_you_use_online_marketplaces:
                    triage_do_you_use_online_marketplaces.is_yes_selected(
                        driver
                    )
                else:
                    triage_do_you_use_online_marketplaces.is_no_selected(
                        driver
                    )
                triage_do_you_use_online_marketplaces.submit(driver)
                triage_what_do_you_want_to_export.should_be_here(driver)
                goods_or_services, _, _ = actor.what_do_you_want_to_export
                if goods_or_services == "goods":
                    triage_what_do_you_want_to_export.is_goods_selected(
                        context.driver
                    )
                else:
                    triage_what_do_you_want_to_export.is_services_selected(
                        context.driver
                    )
                triage_what_do_you_want_to_export.submit(driver)
                triage_are_you_registered_with_companies_house.should_be_here(
                    driver
                )
                continue_from_are_you_incorporated()
                triage_summary.should_be_classified_as_occasional(driver)
        else:
            triage_have_you_exported.is_no_selected(driver)
            triage_have_you_exported.submit(driver)
            goods_or_services, _, _ = actor.what_do_you_want_to_export
            if goods_or_services == "goods":
                triage_what_do_you_want_to_export.is_goods_selected(
                    context.driver
                )
            else:
                triage_what_do_you_want_to_export.is_services_selected(
                    context.driver
                )
            triage_what_do_you_want_to_export.submit(driver)
            triage_are_you_registered_with_companies_house.should_be_here(
                driver
            )
            continue_from_are_you_incorporated()
            triage_summary.should_be_classified_as_new(driver)
        triage_should_see_answers_to_questions(context, actor_alias)
    logging.debug("%s was able to change the Triage answers", actor_alias)


def triage_go_through_again(context: Context, actor_alias: str):
    personalised_journey_update_preference(context, actor_alias)
    triage_change_answers(context, actor_alias)
    triage_classify_as(context, actor_alias, start_from_home_page=False)


def export_readiness_open_category(
    context: Context, actor_alias: str, category: str, location: str
):
    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    if location.lower() != "personalised journey":
        visit_page(context, actor_alias, "Home")
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
    )


def set_sector_preference(
    context: Context,
    actor_alias: str,
    *,
    goods_or_services: str = None,
    good: str = None,
    service: str = None
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


def articles_open_first(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    first_article = get_articles(group, category)[0]
    guidance_common.open_first_article(driver)
    exread_article_common.should_see_article(driver, first_article.title)
    logging.debug(
        "%s is on the first article %s: %s",
        actor_alias,
        first_article.title,
        driver.current_url,
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
    exread_article_common.go_to_article(driver, any_article_but_the_last.title)
    time_to_read = exread_article_common.time_to_read_in_seconds(context.driver)
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

    exread_article_common.go_to_article(driver, name)

    total_articles = exread_article_common.get_total_articles(context.driver)
    articles_read_counter = exread_article_common.get_read_counter(context.driver)
    time_to_complete = exread_article_common.get_time_to_complete(context.driver)
    time_to_read = exread_article_common.time_to_read_in_seconds(context.driver)

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
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    visited_articles = actor.visited_articles
    any_article = get_random_article(group, category)
    article_list.show_all_articles(driver)

    # capture the counter values from Article List page
    article_list_total = exread_article_common.get_total_articles(context.driver)
    article_list_read_counter = exread_article_common.get_read_counter(context.driver)
    article_list_time_to_complete = exread_article_common.get_time_to_complete(
        context.driver
    )

    exread_article_common.go_to_article(driver, any_article.title)

    # capture the counter values from Article page
    total_articles = exread_article_common.get_total_articles(context.driver)
    articles_read_counter = exread_article_common.get_read_counter(context.driver)
    time_to_complete = exread_article_common.get_time_to_complete(context.driver)
    time_to_read = exread_article_common.time_to_read_in_seconds(context.driver)
    logging.debug(
        "%s is on '%s' article page: %s",
        actor_alias,
        any_article.title,
        driver.current_url,
    )
    just_read = VisitedArticle(
        any_article.index, any_article.title, time_to_read
    )
    visited_articles.append(just_read)
    update_actor(
        context,
        actor_alias,
        articles_read_counter=articles_read_counter,
        articles_time_to_complete=time_to_complete,
        articles_total_number=total_articles,
        article_list_read_counter=article_list_read_counter,
        article_list_time_to_complete=article_list_time_to_complete,
        article_list_total_number=article_list_total,
        visited_articles=visited_articles,
    )


def guidance_read_through_all_articles(context: Context, actor_alias: str):
    driver = context.driver
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    category = actor.article_category
    visited_articles = actor.visited_articles

    current_article_name = exread_article_common.get_article_name(driver)
    logging.debug("%s is on '%s' article", actor_alias, current_article_name)
    current_article = get_article(group, category, current_article_name)
    assert current_article, "Could not find Article: %s" % current_article_name
    next_article = current_article.next

    while next_article is not None:
        exread_article_common.check_if_link_to_next_article_is_displayed(
            driver, next_article.title
        )
        exread_article_common.go_to_next_article(driver)
        current_article_name = exread_article_common.get_article_name(driver)
        time_to_read = exread_article_common.time_to_read_in_seconds(context.driver)
        visited = VisitedArticle(
            next_article.index, next_article.title, time_to_read
        )
        visited_articles.append(visited)
        logging.debug(
            "%s is on '%s' article", actor_alias, current_article_name
        )
        current_article = get_article(group, category, current_article_name)
        assert current_article, (
            "Could not find Article: %s" % current_article_name
        )
        next_article = current_article.next
        if next_article:
            logging.debug(
                "The next article to visit is: %s", next_article.title
            )
        else:
            logging.debug("There's no more articles to see")

    update_actor(context, actor_alias, visited_articles=visited_articles)


def articles_open_group(
    context: Context, actor_alias: str, group: str, *, location: str = None
):
    categories = {
        "guidance": [
            "market research",
            "customer insight",
            "finance",
            "business planning",
            "getting paid",
            "operations and compliance",
        ],
        "export readiness": ["new", "occasional", "regular"],
    }
    category = random.choice(categories[group.lower()])
    locations = ["header menu", "footer links", "home page"]
    location = location or random.choice(locations)

    if not get_actor(context, actor_alias):
        add_actor(context, unauthenticated_actor(actor_alias))
    update_actor(
        context, actor_alias, article_group=group, article_category=category
    )

    logging.debug(
        "%s decided to open '%s' '%s' Articles via '%s'",
        actor_alias,
        category,
        group,
        location,
    )
    if group.lower() == "export readiness":
        export_readiness_open_category(
            context, actor_alias, category=category, location=location
        )
    elif group.lower() == "guidance":
        guidance_open_category(context, actor_alias, category, location)
    else:
        raise KeyError(
            "Did not recognize '{}'. Please use: 'Guidance' or 'Export "
            "Readiness'".format(group)
        )
    total_articles = exread_article_common.get_total_articles(context.driver)
    articles_read_counter = exread_article_common.get_read_counter(context.driver)
    time_to_complete = exread_article_common.get_time_to_complete(context.driver)
    update_actor(
        context,
        actor_alias,
        article_list_read_counter=articles_read_counter,
        article_list_time_to_complete=time_to_complete,
        article_list_total_number=total_articles,
    )


def articles_go_back_to_same_group(
    context: Context, actor_alias: str, group: str, location: str
):
    actor = get_actor(context, actor_alias)
    category = actor.article_category
    logging.debug(
        "%s decided to open '%s' '%s' Articles via '%s'",
        actor_alias,
        category,
        group,
        location,
    )
    if group.lower() == "export readiness":
        export_readiness_open_category(
            context, actor_alias, category=category, location=location
        )
    elif group.lower() == "guidance":
        guidance_open_category(context, actor_alias, category, location)
    else:
        raise KeyError(
            "Did not recognize '{}'. Please use: 'Guidance' or 'Export "
            "Readiness'".format(group)
        )


def articles_go_back_to_article_list(context: Context, actor_alias: str):
    exread_article_common.go_back_to_article_list(context.driver)
    logging.debug("%s went back to the Article List page", actor_alias)


def articles_found_useful_or_not(
    context: Context, actor_alias: str, useful_or_not: str
):
    if useful_or_not.lower() == "found":
        exread_article_common.flag_as_useful(context.driver)
    elif useful_or_not.lower() in ["haven't found", "hasn't found"]:
        exread_article_common.flag_as_not_useful(context.driver)
    else:
        raise KeyError(
            "Could not recognize: '{}'. Please use 'found' or 'did not find'".format(
                useful_or_not
            )
        )
    logging.debug("%s %s current article useful", actor_alias, useful_or_not)


def case_studies_go_to(context: Context, actor_alias: str, case_number: str):
    case_study_title = home.get_case_study_title(context.driver, case_number)
    home.open_case_study(context.driver, case_number)
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
    assert page_name.lower() in ["home"]
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
        article_group="guidance",
        article_category=category,
        article_location=location,
    )


def open_service_link_on_interim_page(
    context: Context, actor_alias: str, service: str
):
    page_name = "interim {}".format(service)
    page = get_page_object(page_name)
    assert hasattr(page, "go_to_service")
    page.go_to_service(context.driver)
    logging.debug("%s went to %s service page", actor_alias, service)


def personalised_journey_update_preference(context: Context, actor_alias: str):
    personalised_journey.update_preferences(context.driver)
    logging.debug("%s went to update preferences page", actor_alias)


def articles_read_a_number_of_them(
    context: Context,
    actor_alias: str,
    number: str,
    *,
    stay_on_last_article_page: bool = False
):
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
        "all": 1,
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
        if stay_on_last_article_page and (idx == number_to_read):
            logging.debug("%s will stay on the last article page", actor_alias)
        else:
            articles_go_back_to_article_list(context, actor_alias)
        logging.debug(
            "%s read %d article(s) out of %d (%s of %d articles from '%s'"
            " articles)",
            actor_alias,
            idx,
            number_to_read,
            number,
            len(articles),
            category,
        )


def registration_go_to(context: Context, actor_alias: str, location: str):
    logging.debug(
        "%s decided to go to registration via %s link", actor_alias, location
    )
    if location.lower() == "article":
        exread_article_common.go_to_registration(context.driver)
    elif location.lower() == "article list":
        article_list.go_to_registration(context.driver)
    elif location.lower() == "top bar":
        header.go_to_registration(context.driver)
    else:
        raise KeyError(
            "Could not recognise registration link location: %s. Please use "
            "'article', 'article list' or 'top bar'".format(location)
        )
    sso_registration.should_be_here(context.driver)


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
    sso_confirm_your_email.should_be_here(context.driver)
    logging.debug("Supplier is on the SSO Confirm your email address page")


def registration_submit_form_and_verify_account(
    context: Context, actor_alias: str, *, fake_verification: bool = True
):
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
    update_actor(context, actor_alias, registered=True)


def registration_create_and_verify_account(
    context: Context, actor_alias: str, *, fake_verification: bool = True
):
    visit_page(context, actor_alias, "Home")
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
        exread_article_common.go_to_sign_in(context.driver)
    elif location.lower() == "article list":
        article_list.go_to_sign_in(context.driver)
    elif location.lower() == "top bar":
        header.go_to_sign_in(context.driver)
    else:
        raise KeyError(
            "Could not recognise 'sign in' link location: {}. Please use "
            "'article', 'article list' or 'top bar'".format(location)
        )
    sso_sign_in.should_be_here(context.driver)


def sign_in(context: Context, actor_alias: str, location: str):
    actor = get_actor(context, actor_alias)
    email = actor.email
    password = actor.password
    sign_in_go_to(context, actor_alias, location)
    sso_sign_in.fill_out(context.driver, email, password)
    sso_sign_in.submit(context.driver)


def sign_out(context: Context, actor_alias: str):
    header.go_to_sign_out(context.driver)
    sso_sign_out.submit(context.driver)
    logging.debug("%s signed out", actor_alias)


def articles_go_back_to_last_read_article(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    group = actor.article_group
    location = actor.article_location
    last_read_article = actor.visited_articles[-1].title
    articles_go_back_to_same_group(context, actor_alias, group, location)
    articles_open_specific(context, actor_alias, last_read_article)


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
        exread_article_common.check_if_link_opens_email_client(context.driver)
    else:
        exread_article_common.check_if_link_opens_new_tab(
            context.driver, social_media
        )
        exread_article_common.share_via(context.driver, social_media)
    logging.debug(
        "%s successfully got to the share article on '%s'",
        actor_alias,
        social_media,
    )


def promo_video_watch(
    context: Context, actor_alias: str, *, play_time: int = None
):
    home.open(context.driver, group="hero", element="watch video")
    home.play_video(context.driver, play_time=play_time)
    logging.debug("%s was able to play the video", actor_alias)


def promo_video_close(context: Context, actor_alias: str):
    home.close_video(context.driver)
    logging.debug("%s closed the video", actor_alias)


def language_selector_close(
    context: Context, actor_alias: str, *, with_keyboard: bool = False
):
    logging.debug("%s decided to close language selector", actor_alias)
    language_selector.close(context.driver, with_keyboard=with_keyboard)


def language_selector_open(
    context: Context, actor_alias: str, *, with_keyboard: bool = False
):
    logging.debug("%s decided to go open language selector", actor_alias)
    language_selector.open(context.driver, with_keyboard=with_keyboard)


def language_selector_navigate_through_links_with_keyboard(
    context: Context, actor_alias: str
):
    logging.debug(
        "%s decided to navigate through all language selector links with"
        " keyboard",
        actor_alias,
    )
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    language_selector.navigate_through_links_with_keyboard(
        context.driver, page_name=visited_page
    )


def language_selector_change_to(
    context: Context, actor_alias: str, preferred_language: str
):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    logging.debug(
        "%s decided to change language on %s to %s",
        actor_alias,
        visited_page,
        preferred_language,
    )
    language_selector_open(context, actor_alias)
    language_selector.change_to(
        context.driver, visited_page, preferred_language
    )


def articles_show_all(context: Context, actor_alias: str):
    article_list.show_all_articles(context.driver)
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
    context: Context, actor_alias: str, element_name: str, page_name: str
):
    page_object = get_page_object(page_name)
    assert hasattr(page_object, "click_on_page_element")
    page_object.click_on_page_element(context.driver, element_name)
    logging.debug(
        "%s decided to click on '%s' on '%s' page",
        actor_alias,
        element_name,
        page_name,
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
    page_alias: str = None,
    keyword: str = None,
    sector: str = None
):
    if not page_alias:
        actor = get_actor(context, actor_alias)
        page_alias = actor.visited_page
    page = get_page_object(page_alias)
    assert hasattr(page, "search")
    optional_param_keywords = ["n/a", "no", "empty", "without", "any"]
    if keyword and keyword.lower() in optional_param_keywords:
        keyword = None
    if sector and sector.lower() in optional_param_keywords:
        sector = None
    page.search(context.driver, keyword=keyword, sector=sector)
    logging.debug(
        "%s will visit '%s' page using: '%s'",
        actor_alias,
        page_alias,
        page.URL,
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
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "open_industry")
    page.open_industry(context.driver, industry_name)
    update_actor(context, actor_alias, visited_page=industry_name)
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
    accept_tc: bool = True
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
    fas_ui_contact_us.fill_out(context.driver, contact_us_details)
    fas_ui_contact_us.submit(context.driver)


def generic_see_more_industries(context: Context, actor_alias: str):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "see_more_industries")
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
    assert hasattr(page, "click_breadcrumb")
    page.click_breadcrumb(context.driver, breadcrumb_name)
    logging.debug(
        "%s clicked on '%s' breadcrumb on %s",
        actor_alias,
        breadcrumb_name,
        context.driver.current_url,
    )


def fas_view_more_companies(context: Context, actor_alias: str):
    visited_page = get_actor(context, actor_alias).visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "click_on_page_element")
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
    visited_page = get_actor(context, actor_alias).visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "open_profile")
    page.open_profile(context.driver, number)
    logging.debug(
        "%s clicked on '%s' button on %s",
        actor_alias,
        profile_number,
        context.driver.current_url,
    )


def fas_view_article(context: Context, actor_alias: str, article_number: str):
    number = NUMBERS[article_number]
    visited_page = get_actor(context, actor_alias).visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "open_article")
    page.open_article(context.driver, number)
    logging.debug(
        "%s clicked on '%s' article on %s",
        actor_alias,
        article_number,
        context.driver.current_url,
    )


def invest_read_more(context: Context, actor_alias: str, topic_names: Table):
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "open_link")
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
    actor = get_actor(context, actor_alias)
    visited_page = actor.visited_page
    page = get_page_object(visited_page)
    assert hasattr(page, "open_guide")
    page.open_guide(context.driver, guide_name)
    update_actor(context, actor_alias, visited_page=guide_name)
    logging.debug(
        "%s opened '%s' page on %s", actor_alias, guide_name, page.URL
    )


def generic_unfold_topics(context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    assert hasattr(page, "unfold_topics")
    page.unfold_topics(context.driver)
    update_actor(context, actor_alias, visited_page=page_name)
    logging.debug("%s unfolded all topics on %s", actor_alias, page_name)


def generic_click_on_uk_gov_logo(
        context: Context, actor_alias: str, page_name: str):
    page = get_page_object(page_name)
    assert hasattr(page, "click_on_page_element")
    page.click_on_page_element(context.driver, "uk gov logo")
    logging.debug("%s click on UK Gov logo %s", actor_alias, page_name)
