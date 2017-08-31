# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import given

from tests.functional.features.steps.fab_given_impl import (
    bp_build_company_profile,
    fas_find_company_by_name,
    reg_confirm_email_address,
    reg_create_sso_account_associated_with_company,
    reg_create_unverified_profile,
    reg_create_verified_profile,
    reg_select_random_company_and_confirm_export_status,
    sso_create_standalone_unverified_sso_account,
    sso_create_standalone_verified_sso_account,
    unauthenticated_buyer,
    unauthenticated_supplier
)
from tests.functional.features.steps.fab_then_impl import (
    fab_should_see_all_case_studies,
    fas_should_see_png_logo_thumbnail,
    prof_should_see_logo_picture,
    reg_should_get_verification_email,
    sso_should_be_signed_in_to_sso_account
)
from tests.functional.features.steps.fab_when_impl import (
    prof_add_case_study,
    prof_add_online_profiles,
    prof_set_company_description,
    prof_sign_out_from_fab,
    prof_supplier_uploads_logo
)


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    supplier = unauthenticated_supplier(supplier_alias)
    context.add_actor(supplier)


@given('"{supplier_alias}" created a SSO/great.gov.uk account associated with '
       'randomly selected company "{company_alias}"')
def given_supplier_created_sso_account_for_company(
        context, supplier_alias, company_alias):
    reg_create_sso_account_associated_with_company(
        context, supplier_alias, company_alias)


@given('"{alias}" received the email verification message with the email '
       'confirmation link')
def given_supplier_received_verification_email(context, alias):
    reg_should_get_verification_email(context, alias)


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


@given('"{supplier_alias}" has added links to online profiles')
def given_supplier_adds_valid_links_to_online_profiles(context, supplier_alias):
    prof_add_online_profiles(context, supplier_alias, context.table)


@given('"{supplier_alias}" created an unverified profile for randomly selected '
       'company "{company_alias}"')
def given_unverified_profile(context, supplier_alias, company_alias):
    reg_create_unverified_profile(context, supplier_alias, company_alias)


@given('"{supplier_alias}" has set "{picture}" picture as company\'s logo')
def given_supplier_sets_logo_picture(context, supplier_alias, picture):
    prof_supplier_uploads_logo(context, supplier_alias, picture)


@given('"{supplier_alias}" can see that logo on FAB Company\'s Directory '
       'Profile page')
def given_supplier_can_see_correct_logo_on_fab_profile(context, supplier_alias):
    prof_should_see_logo_picture(context, supplier_alias)


@given('"{supplier_alias}" added a complete case study called "{case_alias}"')
def given_supplier_added_complete_case_study(context, supplier_alias, case_alias):
    prof_add_case_study(context, supplier_alias, case_alias)
    fab_should_see_all_case_studies(context, supplier_alias)


@given('"{buyer_alias}" is a buyer')
def given_unauthenticated_buyer(context, buyer_alias):
    buyer = unauthenticated_buyer(buyer_alias)
    context.add_actor(buyer)


@given('"{buyer_alias}" has found a company "{company_alias}" on Find a '
       'Supplier site')
def given_buyer_finds_company_by_name(context, buyer_alias, company_alias):
    fas_find_company_by_name(context, buyer_alias, company_alias)


@given('"{actor_alias}" can see a PNG logo thumbnail on FAS Company\'s '
       'Directory Profile page')
def given_actor_can_see_logo_on_fas_profile_page(context, actor_alias):
    fas_should_see_png_logo_thumbnail(context, actor_alias)
