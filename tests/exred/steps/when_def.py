# -*- coding: utf-8 -*-
"""When step definitions."""
from behave import when

from tests.exred.steps.when_impl import start_triage


@when('"{actor_alias}" decides to get started in Exporting journey section')
def when_actor_starts_triage(context, actor_alias):
    start_triage(context, actor_alias)
