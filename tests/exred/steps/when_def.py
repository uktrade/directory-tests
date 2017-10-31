# -*- coding: utf-8 -*-
"""When step definitions."""
from behave import when

from steps.given_imp import guidance_open_category
from steps.when_impl import start_triage


@when('"{actor_alias}" decides to continue in Exporting journey section')
@when('"{actor_alias}" decides to get started in Exporting journey section')
def when_actor_starts_triage(context, actor_alias):
    start_triage(context, actor_alias)


@when('"{actor_alias}" goes to the "{category}" Guidance articles via "{location}"')
def step_impl(context, actor_alias, category, location):
    guidance_open_category(context, actor_alias, category, location)
