# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import then

from tests.functional.features.steps.fab_then_impl import (
    should_be_on_profile_page,
    should_be_prompted_to_build_your_profile,
    should_be_told_about_missing_description,
    should_get_verification_email,
    sso_account_should_be_created
)


@then('"{alias}" should be told about the verification email')
def then_sso_account_was_created(context, alias):
    sso_account_should_be_created(context, alias)


@then('"{alias}" should receive an email verification msg entitled "{subject}"')
def then_supplier_should_receive_verification_email(context, alias, subject):
    should_get_verification_email(context, alias, subject)


@then('"{supplier_alias}" should be prompted to Build and improve your profile')
def then_supplier_should_be_prompted_to_build_your_profile(context, supplier_alias):
    should_be_prompted_to_build_your_profile(context, supplier_alias)


@then('"{supplier_alias}" should be on company profile page')
def then_supplier_should_be_on_profile_page(context, supplier_alias):
    should_be_on_profile_page(context, supplier_alias)


@then('"{supplier_alias}" should be told that her company has no description')
def then_supplier_should_be_told_about_missing_description(context, supplier_alias):
    should_be_told_about_missing_description(context, supplier_alias)
