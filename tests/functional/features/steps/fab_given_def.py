# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import given

from tests.functional.features.steps.fab_given_impl import (
    bp_build_company_profile,
    reg_confirm_email_address,
    reg_create_sso_account_associated_with_company,
    reg_create_verified_profile,
    reg_select_random_company_and_confirm_export_status,
    sso_create_standalone_unverified_sso_account,
    sso_create_standalone_verified_sso_account,
    unauthenticated_supplier
)
from tests.functional.features.steps.fab_then_impl import (
    reg_should_get_verification_email,
    sso_should_be_signed_in_to_sso_account
)
from tests.functional.features.steps.fab_when_impl import (
    prof_set_company_description,
    prof_sign_out_from_fab
)
from tests.settings import EMAIL_VERIFICATION_MSG_SUBJECT


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    unauthenticated_supplier(context, supplier_alias)


@given('"{supplier_alias}" created a SSO/great.gov.uk account associated with '
       'randomly selected company "{company_alias}"')
def given_supplier_created_sso_account_for_company(
        context, supplier_alias, company_alias):
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias)


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


@given('"{supplier_alias}" signed out from Find a Buyer service')
def given_supplier_signed_out_from_fab(context, supplier_alias):
    prof_sign_out_from_fab(context, supplier_alias)


@given('"{supplier_alias}" created a standalone SSO/great.gov.uk account with '
       'unverified email address')
def given_supplier_creates_standalone_unverified_sso_account(
        context, supplier_alias):
    sso_create_standalone_unverified_sso_account(context, supplier_alias)


@given('"{supplier_alias}" has a verified standalone SSO/great.gov.uk account')
def given_verified_standalone_sso_account(context, supplier_alias):
    sso_create_standalone_verified_sso_account(context, supplier_alias)


@given('"{supplier_alias}" is signed in to SSO/great.gov.uk account')
def given_supplier_is_signed_in_to_sso(context, supplier_alias):
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


@given('"{supplier_alias}" selected an active company without a Directory '
       'Profile identified by an alias "{company_alias}"')
def given_supplier_selects_random_company(context, supplier_alias, company_alias):
    reg_select_random_company_and_confirm_export_status(
        context, supplier_alias, company_alias)
