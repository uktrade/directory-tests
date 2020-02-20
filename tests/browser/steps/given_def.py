# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""Given step definitions."""
from behave import given
from behave.runner import Context

from pages.common_actions import generic_set_basic_auth_creds
from steps.then_impl import (
    domestic_search_finder_should_see_page_number,
    should_be_on_page,
    should_see_sections,
)
from steps.when_impl import (
    articles_open_any,
    clear_the_cookies,
    click_on_page_element,
    contact_us_get_to_page_via,
    contact_us_navigate_through_options,
    domestic_open_random_advice_article,
    domestic_open_random_market,
    domestic_search_for_phrase_on_page,
    domestic_search_result_has_more_than_one_page,
    erp_follow_user_flow,
    fas_searched_for_companies,
    generic_at_least_n_news_articles,
    generic_create_great_account,
    generic_fill_out_and_submit_form,
    generic_get_in_touch,
    generic_open_industry_page,
    get_barred_actor,
    profile_start_registration_as,
    registration_create_and_verify_account,
    set_small_screen,
    sign_in,
    soo_find_and_open_random_marketplace,
    soo_look_for_marketplaces_from_home_page,
    sso_actor_received_email_confirmation_code,
    visit_page,
)


@given('"{actor_alias}" has a small screen')
def given_actor_has_small_screen(context, actor_alias):
    set_small_screen(context)


@given('"{actor_alias}" went to the "{page_name}" page')
@given('"{actor_alias}" goes to the "{page_name}" page')
@given('"{actor_alias}" visited the "{page_name}" page')
@given('"{actor_alias}" visited "{page_name}" page')
@given('"{actor_alias}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@given('"{actor_alias}" got to the "{page_name}" page')
@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_is_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@given('"{actor_alias}" can see "{sections}" section on "{page_name}" page')
@given('"{actor_alias}" can see "{sections}" sections on "{page_name}" page')
def given_can_see_sections(context, actor_alias, sections, page_name):
    should_see_sections(
        context, actor_alias, page_name, sections_list=sections.split(", "))


@given('"{actor_alias}" decided to use "{element_name}" button')
@given('"{actor_alias}" decided to use "{element_name}" link')
@given('"{actor_alias}" decided to "{element_name}"')
def given_actor_decided_to_click_on_page_element(
        context, actor_alias, element_name):
    click_on_page_element(context, actor_alias, element_name)


@given('"{actor_alias}" got in touch with us via "{page_name}" page')
def given_actor_got_in_touch_with_us(
        context: Context, actor_alias: str, page_name: str):
    generic_get_in_touch(context, actor_alias, page_name, custom_details_table=context.table)


@given('at least "{no_articles:d}" published "{visitor_type}" news articles on "{service}"')
@given('at least "{no_articles:d}" published "{visitor_type}" news article on "{service}"')
def given_min_number_of_articles(
        context: Context, no_articles: int, visitor_type: str, service: str):
    generic_at_least_n_news_articles(context, no_articles, visitor_type, service)


@given('"{actor_alias}" got to "{final_page}" from "{start_page}" via "{via}"')
def given_actor_gets_to_a_page_via(
        context: Context, actor_alias: str, final_page: str, start_page: str, via: str):
    contact_us_get_to_page_via(context, actor_alias, final_page, via, start_page=start_page)


@given('"{actor_alias}" got to the "{final_page}" page via "{via}"')
def given_actor_gets_to_a_page_via(
        context: Context, actor_alias: str, final_page: str, via: str):
    contact_us_get_to_page_via(context, actor_alias, final_page, via)


@given('"{actor_alias}" navigates via "{via}"')
def given_actor_navigates_via_contact_us_options(
        context: Context, actor_alias: str, via: str):
    contact_us_navigate_through_options(context, actor_alias, via)


@given('basic authentication is done for "{page_name}" page')
def given_user_did_basic_auth(context: Context, page_name: str):
    generic_set_basic_auth_creds(context.driver, page_name)


@given('"{actor_alias}" is on randomly selected Market page')
def given_actor_in_on_random_market(context: Context, actor_alias: str):
    domestic_open_random_market(context, actor_alias)


@given('"{actor_alias}" is on randomly selected Advice article page')
def given_actor_in_on_random_advice_article(context: Context, actor_alias: str):
    domestic_open_random_advice_article(context, actor_alias)


@given('"{actor_alias}" was barred from contacting us')
def given_a_barred_actor(context: Context, actor_alias: str):
    get_barred_actor(context, actor_alias)


@given('"{actor_alias}" has received the email confirmation code by opting to register as "{business_type}"')
def given_actor_received_email_confirmation_code(
        context: Context, actor_alias: str, business_type: str
):
    sso_actor_received_email_confirmation_code(
        context, actor_alias, business_type
    )


@given('"{actor_name}" decided to create a great.gov.uk account as "{business_type}"')
def given_actor_wants_to_register_as(context: Context, actor_name: str, business_type: str):
    profile_start_registration_as(context, actor_name, business_type)


@given('"{actor_alias}" searches for marketplaces in "{country}" to sell "{category}"')
def given_actor_looks_for_marketplace_using_countries_and_products(
        context: Context, actor_alias: str, country: str, category: str):
    soo_look_for_marketplaces_from_home_page(
        context, actor_alias, country, category
    )


@given('"{actor_alias}" found a marketplace in "{country}" to sell "{category}"')
def given_actor_found_marketplace(
        context: Context, actor_alias: str, country: str, category: str):
    soo_find_and_open_random_marketplace(context, actor_alias, country, category)


@given('"{actor_alias}" has a verified standalone SSO/great.gov.uk account')
@given('"{actor_alias}" is a registered and verified user')
def given_actor_is_registered_and_verified(context, actor_alias):
    registration_create_and_verify_account(
        context, actor_alias, fake_verification=True)


@given('"{actor_alias}" has created a great.gov.uk account for a "{business_type}"')
def given_actor_created_great_account(
        context: Context, actor_alias: str, business_type: str
):
    generic_create_great_account(context, actor_alias, business_type)


@given('"{actor_alias}" is signed in')
def given_actor_is_signed_in(context, actor_alias):
    sign_in(context, actor_alias)


@given('"{actor_alias}" searched for companies using "{keyword}" keyword in "{sector}" sector')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str, sector: str):
    fas_searched_for_companies(
        context, actor_alias, keyword=keyword, sector=sector)


@given('"{actor_alias}" searched using "{phrase}" on the "{page_name}" page')
def given_actor_searched_phrase(
        context: Context, actor_alias: str, phrase: str, page_name: str):
    domestic_search_for_phrase_on_page(context, actor_alias, phrase, page_name)


@given('"{actor_alias}" sees more than "{min_page_num:d}" search result page')
def given_actor_sees_more_than_one_page(
        context: Context, actor_alias: str, min_page_num: int):
    domestic_search_result_has_more_than_one_page(context, actor_alias, min_page_num)


@given('"{actor_alias}" sees search results page number "{page_num:d}" for "{first_phrase}"')
def then_actor_should_see_page_number(
        context: Context, actor_alias: str, page_num: int, first_phrase: str):
    domestic_search_finder_should_see_page_number(context, actor_alias, page_num)


@given('"{actor_alias}" filled out and submitted the form')
def given_actor_fills_out_and_submits_the_form(context: Context, actor_alias: str):
    generic_fill_out_and_submit_form(context, actor_alias, custom_details_table=context.table)


@given('"{actor_alias}" cleared the cookies')
@given('"{actor_alias}" quickly signed out')
def when_actor_clears_the_cookies(context, actor_alias):
    clear_the_cookies(context, actor_alias)


@given('"{actor_alias}" submitted her ERP form as an "{user_type}"')
@given('"{actor_alias}" submitted his ERP form as an "{user_type}"')
@given('"{actor_alias}" submitted her ERP form as "{user_type}"')
@given('"{actor_alias}" submitted his ERP form as "{user_type}"')
@given('"{actor_alias}" got to "{stop_at}" ERP page as "{user_type}"')
def given_actor_got_to_expected_erp_page(
        context: Context, actor_alias: str, user_type: str, *, stop_at: str = None
):
    erp_follow_user_flow(context, actor_alias, user_type, stop_at=stop_at)


###############################################################################
# Currently unused but useful steps
###############################################################################


@given('"{actor_alias}" decided to find out out more about "{industry_name}" industry')
def fas_given_actor_opened_industry_page(
        context: Context, actor_alias: str, industry_name: str):
    generic_open_industry_page(context, actor_alias, industry_name)


@given('"{actor_alias}" opened any Article')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)
