# -*- coding: utf-8 -*-
"""Given steps definitions."""
from behave import given

from tests.ui.steps.given_impl import go_to_page


@given('"{actor_alias}" goes to the "{page_name}" page')
def given_actor_is_on_page(context, actor_alias, page_name):
    go_to_page(context, actor_alias, page_name)
