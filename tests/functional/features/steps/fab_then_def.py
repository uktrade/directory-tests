# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import then

from tests.functional.features.steps.fab_then_impl import \
    verify_response_sso_account_was_created


@then("the supplier should be told about the verification email")
def then_sso_account_was_created(context):
    verify_response_sso_account_was_created(context)
