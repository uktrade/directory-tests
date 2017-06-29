# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import given

from tests.functional.features.steps.fab_given_impl import (
    bp_build_company_profile,
    reg_confirm_email_address,
    reg_create_sso_account_associated_with_company,
    reg_create_verified_profile,
    unauthenticated_supplier
)
from tests.functional.features.steps.fab_then_impl import (
    reg_should_get_verification_email
)
from tests.functional.features.steps.fab_when_impl import (
    prof_set_company_description
)
from tests.settings import EMAIL_VERIFICATION_MSG_SUBJECT


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    unauthenticated_supplier(context, supplier_alias)


@given('"{supplier_alias}" created a SSO account associated with randomly '
       'selected company "{company_alias}"')
def given_supplier_created_sso_account_for_company(context, supplier_alias,
                                                   company_alias):
    reg_create_sso_account_associated_with_company(context, supplier_alias,
                                                   company_alias)


@given('"{alias}" received the email verification message with the email '
       'confirmation link')
def given_supplier_received_verification_email(context, alias):
    subject = EMAIL_VERIFICATION_MSG_SUBJECT
    reg_should_get_verification_email(context, alias, subject)


@given('"{supplier_alias}" confirmed her email address')
@given('"{supplier_alias}" confirmed his email address')
def given_supplier_confirmed_email_address(context, supplier_alias):
    reg_confirm_email_address(context, supplier_alias)


@given('"{supplier_alias}" built the company profile')
def given_supplier_built_company_profile(context, supplier_alias):
    bp_build_company_profile(context, supplier_alias)


@given('"{supplier_alias}" set the company description')
def given_supplier_set_company_description(context, supplier_alias):
    prof_set_company_description(context, supplier_alias)


@given('"{supplier_alias}" has created and verified profile for randomly '
       'selected company "{company_alias}"')
def given_supplier_creates_verified_profile(context, supplier_alias,
                                            company_alias):
    reg_create_verified_profile(context, supplier_alias, company_alias)
