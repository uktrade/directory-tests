# -*- coding: utf-8 -*-
"""Given step definitions."""
from behave import given

from steps.given_impl import visit_page


@given('"{actor_name}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_name, page_name):
    visit_page(context, actor_name, page_name)


@given('"{actor_name}" visits the "{page_name}" page for the first time')
def given_actor_visits_page_for_the_first_time(context, actor_name, page_name):
    visit_page(context, actor_name, page_name, first_time=True)
