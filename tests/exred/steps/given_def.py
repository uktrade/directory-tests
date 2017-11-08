# -*- coding: utf-8 -*-
"""Given step definitions."""
from behave import given

from steps.then_impl import should_be_on_page
from steps.when_impl import (
    actor_classifies_himself_as,
    guidance_open_category,
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
def step_impl(context, actor_alias, used_or_not):
    set_online_marketplace_preference(context, actor_alias, used_or_not)
