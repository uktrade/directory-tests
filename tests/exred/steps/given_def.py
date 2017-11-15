# -*- coding: utf-8 -*-
"""Given step definitions."""
from behave import given

from steps.then_impl import should_be_on_page
from steps.when_impl import (
    actor_classifies_himself_as,
    articles_open_any_but_the_last,
    articles_open_first,
    articles_open_group,
    export_readiness_open_category,
    guidance_open_category,
    guidance_open_random_category,
    set_online_marketplace_preference,
    set_sector_preference,
    start_triage,
    triage_classify_as,
    triage_create_exporting_journey,
    visit_page
)


@given('"{actor_alias}" goes to the "{page_name}" page')
@given('"{actor_alias}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@given('"{actor_alias}" visits the "{page_name}" page for the first time')
def given_actor_visits_page_for_the_first_time(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name, first_time=True)


@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_is_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@given('"{actor_alias}" classifies herself as "{exporter_status}" exporter')
@given('"{actor_alias}" classifies himself as "{exporter_status}" exporter')
def given_actor_classifies_as(context, actor_alias, exporter_status):
    actor_classifies_himself_as(context, actor_alias, exporter_status)


@given('"{actor_alias}" was classified as "{exporter_status}" exporter in the triage process')
def given_actor_was_classified_as(context, actor_alias, exporter_status):
    triage_classify_as(context, actor_alias, exporter_status=exporter_status)


@given('"{actor_alias}" answered triage questions')
def given_actor_answered_triage_questions(context, actor_alias):
    triage_classify_as(context, actor_alias)


@given('"{actor_alias}" accessed "{category}" guidance articles using "{location}"')
def given_actor_opened_guidance(context, actor_alias, category, location):
    guidance_open_category(context, actor_alias, category, location)


@given('"{actor_alias}" decided to build her exporting journey')
@given('"{actor_alias}" decided to build his exporting journey')
def given_actor_starts_exporting_journey(context, actor_alias):
    start_triage(context, actor_alias)


@given('"{actor_alias}" decided to create her personalised journey page')
@given('"{actor_alias}" decided to create his personalised journey page')
def given_actor_decided_to_create_personalised_page(context, actor_alias):
    triage_create_exporting_journey(context, actor_alias)


@given('"{actor_alias}" was classified as "{exporter_status}" Exporter which "{is_incorporated}" incorporated the company')
def given_actor_was_classified_as(
        context, actor_alias, exporter_status, is_incorporated):
    triage_classify_as(
        context, actor_alias, exporter_status=exporter_status,
        is_incorporated=is_incorporated)


@given('"{actor_alias}" exports "{goods_or_services}"')
def given_actor_sets_sector_preference(context, actor_alias, goods_or_services):
    set_sector_preference(context, actor_alias, goods_or_services)


@given('"{actor_alias}" "{used_or_not}" online marketplaces before')
def given_actor_set_preferences_for_online_marketplaces(
        context, actor_alias, used_or_not):
    set_online_marketplace_preference(context, actor_alias, used_or_not)


@given('"{actor_alias}" opened first Article from the list')
def given_actor_opened_first_article(context, actor_alias):
    articles_open_first(context, actor_alias)


@given('"{actor_alias}" accessed Export Readiness articles for "{category}" Exporters via "{location}"')
def given_actor_goes_to_export_readiness_articles(
        context, actor_alias, category, location):
    export_readiness_open_category(context, actor_alias, category, location)


@given('"{actor_alias}" opened any Article but the last one')
def given_actor_opens_any_article_but_the_last_one(context, actor_alias):
    articles_open_any_but_the_last(context, actor_alias)


@given('"{actor_alias}" is on the "{group}" Article List for randomly selected category')
def given_actor_is_on_article_list(context, actor_alias, group):
    articles_open_group(context, actor_alias, group)


@given('"{actor_alias}" went to randomly selected Guidance Articles category')
def given_actor_selects_random_guidance_category(context, actor_alias):
    guidance_open_random_category(context, actor_alias)
