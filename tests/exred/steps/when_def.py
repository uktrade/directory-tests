# -*- coding: utf-8 -*-
"""When step definitions."""
from behave import when

from steps.when_impl import (
    guidance_open_category,
    personalised_journey_create_page,
    start_triage,
    triage_select_sector
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


@when('"{actor_alias}" selects her sector')
@when('"{actor_alias}" selects his sector')
def when_actor_selects_sector(context, actor_alias):
    triage_select_sector(context, actor_alias)
