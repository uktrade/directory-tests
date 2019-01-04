# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""Given step definitions."""
from behave import given
from behave.runner import Context

from steps.then_impl import (
    should_be_on_page,
    should_see_sections
)
from steps.when_impl import (
    articles_open_any,
    articles_show_all,
    case_studies_go_to_random,
    click_on_page_element,
    contact_us_get_to_page_via,
    contact_us_navigate_through_options,
    exred_open_random_advice_article,
    generic_at_least_n_news_articles,
    generic_get_in_touch,
    generic_open_any_news_article,
    generic_open_industry_page,
    generic_open_random_news_article,
    generic_set_hawk_cookie,
    get_geo_ip,
    registration_create_and_verify_account,
    sign_in,
    visit_page,
)


@given('"{actor_alias}" went to the "{page_name}" page')
@given('"{actor_alias}" goes to the "{page_name}" page')
@given('"{actor_alias}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_is_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@given('"{actor_alias}" opened any Article')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)


@given('"{actor_alias}" can see "{sections}" section on "{page_name}" page')
@given('"{actor_alias}" can see "{sections}" sections on "{page_name}" page')
def given_can_see_sections(context, actor_alias, sections, page_name):
    should_see_sections(
        context, actor_alias, page_name, sections_list=sections.split(", "))


@given('"{actor_alias}" is a registered and verified user')
def given_actor_is_registered_and_verified(context, actor_alias):
    registration_create_and_verify_account(
        context, actor_alias, fake_verification=True)


@given("{actor_alias} checks her geoip")
@given("{actor_alias} checks his geoip")
def given_actor_checks_the_goeip(context, actor_alias):
    get_geo_ip(context, actor_alias)


@given('"{actor_alias}" signed in using link in the "{location}"')
@given('"{actor_alias}" is signed in')
def given_actor_is_signed_in(context, actor_alias, *, location="top bar"):
    sign_in(context, actor_alias, location)


@given('"{actor_alias}" is on the Case Study page accessed via "{page_name}" page')
def given_actor_is_on_random_case_study_page(context, actor_alias, page_name):
    case_studies_go_to_random(context, actor_alias, page_name)


@given('"{actor_alias}" shows all of the articles on the page whenever possible')
def given_actor_shows_all_articles(context, actor_alias):
    articles_show_all(context, actor_alias)


@given('"{actor_alias}" decided to use "{element_name}" button on "{page_name}" page')
@given('"{actor_alias}" decided to use "{element_name}" link on "{page_name}" page')
@given('"{actor_alias}" decided to use "{element_name}" on "{page_name}" page')
@given('"{actor_alias}" decided to use "{element_name}" button on "{page_name}" page')
@given('"{actor_alias}" decided to use "{element_name}" link in "{page_name}"')
@given('"{actor_alias}" decided to use "{element_name}" in "{page_name}"')
@given('"{actor_alias}" decided to "{element_name}" via "{page_name}" page')
def given_actor_decides_to_click_on_page_element(
        context, actor_alias, element_name, page_name):
    click_on_page_element(context, actor_alias, element_name, page_name=page_name)


@given('"{actor_alias}" decided to use "{element_name}" button')
@given('"{actor_alias}" decided to use "{element_name}" link')
def given_actor_decided_to_click_on_page_element(
        context, actor_alias, element_name):
    click_on_page_element(context, actor_alias, element_name)


@given('"{actor_alias}" decided to find out out more about "{industry_name}" industry')
def fas_given_actor_opened_industry_page(
        context: Context, actor_alias: str, industry_name: str):
    generic_open_industry_page(context, actor_alias, industry_name)


@given('"{actor_alias}" got in touch with us via "{page_name}" page')
def given_actor_got_in_touch_with_us(
        context: Context, actor_alias: str, page_name: str):
    generic_get_in_touch(context, actor_alias, page_name)


@given('at least "{no_articles:d}" published "{visitor_type}" news articles on "{service}"')
@given('at least "{no_articles:d}" published "{visitor_type}" news article on "{service}"')
def given_min_number_of_articles(
        context: Context, no_articles: int, visitor_type: str, service: str):
    generic_at_least_n_news_articles(context, no_articles, visitor_type, service)


@given('"{actor_alias}" opened any news Article')
def given_actor_opens_any_news_article(context, actor_alias):
    generic_open_any_news_article(context, actor_alias)


@given('"{actor_alias}" opened random "{article_type}" news article')
def given_actor_opened_random_news_article(
        context: Context, actor_alias: str, article_type: str):
    generic_open_random_news_article(context, actor_alias, article_type)


@given('"{actor_alias}" got to the "{final_page}" page via "{via}"')
def given_actor_gets_to_a_page_via(
        context: Context, actor_alias: str, final_page: str, via: str):
    contact_us_get_to_page_via(context, actor_alias, final_page, via)


@given('"{actor_alias}" navigates via "{via}"')
def given_actor_navigates_via_contact_us_options(
        context: Context, actor_alias: str, via: str):
    contact_us_navigate_through_options(context, actor_alias, via)


@given('hawk cookie is set on "{page_name}" page')
def given_hawk_cookie_is_set(context: Context, page_name: str):
    generic_set_hawk_cookie(context, page_name)


@given('"{actor_alias}" is on randomly selected Advice article page')
def given_actor_in_on_random_advice_article(context: Context, actor_alias: str):
    exred_open_random_advice_article(context, actor_alias)
