# -*- coding: utf-8 -*-
"""Given step definitions."""
from behave import given

from tests.exred.steps.given_impl import visit_page


@given('"{actor_name}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_name, page_name):
    visit_page(context, actor_name, page_name)
