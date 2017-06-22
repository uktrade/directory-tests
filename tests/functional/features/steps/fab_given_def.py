# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import given

from tests.functional.features.steps.fab_given_impl import (
    unauthenticated_supplier
)


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    unauthenticated_supplier(context, supplier_alias)
