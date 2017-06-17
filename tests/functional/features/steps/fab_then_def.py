# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import then

from tests.functional.features.steps.fab_then_impl import \
    verify_response_sso_account_was_created
from tests.functional.features.steps.fab_then_impl import \
    should_receive_verification_email


@then('"{alias}" should be told about the verification email')
def then_sso_account_was_created(context, alias):
    verify_response_sso_account_was_created(context, alias)


@then('"{alias}" should receive a verification email')
@then('"{alias}" should receive a verification email entitled "{title}"')
def then_supplier_should_receive_a_verification_email(context, alias,
                                                      title=None):
    should_receive_verification_email(context, alias, title)
