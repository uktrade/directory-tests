# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""Given step definitions."""
from behave import given
from behave.runner import Context

from steps.then_impl import should_be_on_page, should_see_sections
from steps.when_impl import (
    articles_open_any,
    case_studies_go_to_random,
    click_on_page_element,
    contact_us_get_to_page_via,
    contact_us_navigate_through_options,
    exred_open_random_advice_article,
    generic_at_least_n_news_articles,
    generic_create_great_account,
    generic_get_in_touch,
    generic_open_any_news_article,
    generic_open_industry_page,
    generic_open_random_news_article,
    generic_set_basic_auth_creds,
    get_barred_actor,
    registration_create_and_verify_account,
    sign_in,
    soo_find_and_open_random_marketplace,
    soo_find_random_marketplace_and_apply_via_dit,
    soo_look_for_marketplaces_from_home_page,
    sso_actor_received_email_confirmation_code,
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


@given('"{actor_alias}" is on the Case Study page accessed via "{page_name}" page')
def given_actor_is_on_random_case_study_page(context, actor_alias, page_name):
    case_studies_go_to_random(context, actor_alias, page_name)


@given('"{actor_alias}" decided to use "{element_name}" link on "{page_name}" page')
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


@given('"{actor_alias}" got in touch with us via "{page_name}" page')
def given_actor_got_in_touch_with_us(
        context: Context, actor_alias: str, page_name: str):
    generic_get_in_touch(context, actor_alias, page_name)


@given('at least "{no_articles:d}" published "{visitor_type}" news articles on "{service}"')
@given('at least "{no_articles:d}" published "{visitor_type}" news article on "{service}"')
def given_min_number_of_articles(
        context: Context, no_articles: int, visitor_type: str, service: str):
    generic_at_least_n_news_articles(context, no_articles, visitor_type, service)


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
    generic_set_basic_auth_creds(context, page_name)


@given('"{actor_alias}" is on randomly selected Advice article page')
def given_actor_in_on_random_advice_article(context: Context, actor_alias: str):
    exred_open_random_advice_article(context, actor_alias)


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


@given('"{actor_alias}" searches for marketplaces in {countries} to sell {products}')
def given_actor_looks_for_marketplace_using_countries_and_products(
        context: Context, actor_alias: str, countries: str, products: str):
    soo_look_for_marketplaces_from_home_page(
        context, actor_alias, countries, products
    )


@given('"{actor_alias}" found a marketplace in {countries} to sell {products}')
def given_actor_found_marketplace(
        context: Context, actor_alias: str, countries: str, products: str):
    soo_find_and_open_random_marketplace(context, actor_alias, countries, products)


@given('"{actor_alias}" applied via DIT to contact randomly selected marketplace in "{countries}" to sell "{products}"')
def actor_applied_via_dit(
        context: Context, actor_alias: str, countries: str, products: str):
    soo_find_random_marketplace_and_apply_via_dit(
        context, actor_alias, countries, products
    )


###############################################################################
# Currently unused but useful steps
###############################################################################


@given('"{actor_alias}" is a registered and verified user')
def given_actor_is_registered_and_verified(context, actor_alias):
    registration_create_and_verify_account(
        context, actor_alias, fake_verification=True)


@given('"{actor_alias}" is signed in')
def given_actor_is_signed_in(context, actor_alias):
    sign_in(context, actor_alias)


@given('"{actor_alias}" decided to find out out more about "{industry_name}" industry')
def fas_given_actor_opened_industry_page(
        context: Context, actor_alias: str, industry_name: str):
    generic_open_industry_page(context, actor_alias, industry_name)


@given('"{actor_alias}" opened any news Article')
def given_actor_opens_any_news_article(context, actor_alias):
    generic_open_any_news_article(context, actor_alias)


@given('"{actor_alias}" opened random "{article_type}" news article')
def given_actor_opened_random_news_article(
        context: Context, actor_alias: str, article_type: str):
    generic_open_random_news_article(context, actor_alias, article_type)


@given('"{actor_alias}" has created a great.gov.uk account for a "{business_type}"')
def given_actor_created_great_account(
        context: Context, actor_alias: str, business_type: str
):
    generic_create_great_account(context, actor_alias, business_type)
