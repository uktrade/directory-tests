# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import do_something
from tests.functional.features.steps.fab_when_impl import select_random_company


@when('"{supplier_alias}" does something')
def step_impl(context, supplier_alias):
    do_something(context, supplier_alias)


@when("the supplier selects randomly chosen company for profile registration")
def step_impl(context):
    select_random_company(context)
