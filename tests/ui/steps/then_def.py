# -*- coding: utf-8 -*-
"""Then steps definitions."""
from behave import then

from tests.ui.steps.then_impl import should_see_directory_header


@then('"{actor_alias}" should see the standard Directory page header')
def given_actor_is_on_page(context, actor_alias):
    should_see_directory_header(context, actor_alias)
