# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import then

from tests.functional.features.steps.fab_then_impl import \
    sso_account_should_be_created
from tests.functional.features.steps.fab_then_impl import \
    should_get_verification_email


@then('"{alias}" should be told about the verification email')
def then_sso_account_was_created(context, alias):
    sso_account_should_be_created(context, alias)


@then('"{alias}" should receive an email verification msg entitled "{title}"')
def then_supplier_should_receive_verification_email(context, alias, title):
    should_get_verification_email(context, alias, title)

