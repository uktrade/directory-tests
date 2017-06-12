# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import \
    confirm_company_selection
from tests.functional.features.steps.fab_when_impl import select_random_company


@when("the supplier randomly selects an active company without a profile "
      "identified by an alias '{alias}'")
def when_random_company_is_selected(context, alias):
    select_random_company(context, alias)


@when("the supplier confirms that '{alias}' is the correct one")
def when_company_selection_is_confirmed(context, alias):
    confirm_company_selection(context, alias)
