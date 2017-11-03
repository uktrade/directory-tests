# -*- coding: utf-8 -*-
"""When step definitions."""
from behave import when

from steps.when_impl import (
    guidance_open_category,
    personalised_journey_create_page,
    start_triage,
    triage_are_you_incorporated,
    triage_do_you_export_regularly,
    triage_have_you_exported_before,
    triage_say_what_do_you_want_to_export,
)


@when('"{actor_alias}" decides to continue in Exporting journey section')
@when('"{actor_alias}" decides to get started in Exporting journey section')
def when_actor_starts_triage(context, actor_alias):
    start_triage(context, actor_alias)


@when('"{actor_alias}" goes to the "{category}" Guidance articles via "{location}"')
def when_actor_goes_to_guidance_articles(
        context, actor_alias, category, location):
    guidance_open_category(context, actor_alias, category, location)


@when('"{actor_alias}" creates a personalised journey page for herself')
def when_actor_creates_personalised_journey_page(context, actor_alias):
    personalised_journey_create_page(context, actor_alias)


@when('"{actor_alias}" says what does he wants to export')
@when('"{actor_alias}" says what does she wants to export')
def when_actor_says_what_he_wants_to_export(context, actor_alias):
    triage_say_what_do_you_want_to_export(context, actor_alias)


@when('"{actor_alias}" says that he "{has_or_has_never}" exported before')
@when('"{actor_alias}" says that she "{has_or_has_never}" exported before')
def when_actor_answers_whether_he_exported_before(
        context, actor_alias, has_or_has_never):
    triage_have_you_exported_before(context, actor_alias, has_or_has_never)


@when('"{actor_alias}" says that exporting is "{regular_or_not}" part of her business')
@when('"{actor_alias}" says that exporting is "{regular_or_not}" part of his business')
def when_actor_tells_whether_he_exports_regularly_or_not(
        context, actor_alias, regular_or_not):
    triage_do_you_export_regularly(context, actor_alias, regular_or_not)


@when('"{actor_alias}" says that her company "{is_or_not}" incorporated')
@when('"{actor_alias}" says that his company "{is_or_not}" incorporated')
def when_actor_says_whether_company_is_incorporated(
        context, actor_alias, is_or_not):
    triage_are_you_incorporated(context, actor_alias, is_or_not)
