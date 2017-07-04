# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import (
    bp_confirm_registration_and_send_letter,
    bp_provide_company_details,
    bp_provide_full_name,
    bp_select_random_sector,
    prof_attempt_to_sign_in_to_fab,
    prof_sign_in_to_fab,
    prof_verify_company,
    prof_view_published_profile,
    reg_confirm_company_selection,
    reg_confirm_export_status,
    reg_create_sso_account,
    reg_create_standalone_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    reg_supplier_is_not_ready_to_export,
    select_random_company,
    sso_supplier_confirms_email_address,
    sso_go_to_create_trade_profile
)


@when('"{supplier_alias}" randomly selects an active company without a '
      'Directory Profile identified by an alias "{alias}"')
def when_supplier_selects_random_company(context, supplier_alias, alias):
    select_random_company(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that "{alias}" is the correct one')
def when_company_selection_is_confirmed(context, supplier_alias, alias):
    reg_confirm_company_selection(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that the export status of "{alias}" is '
      '"{export_status}"')
def when_supplier_confirms_export_status(context, supplier_alias, alias,
                                         export_status):
    reg_confirm_export_status(context, supplier_alias, alias, export_status)


@when('"{supplier_alias}" creates a SSO/great.gov.uk account for "{alias}" '
      'using valid credentials')
def when_supplier_creates_sso_account_for_selected_company(context,
                                                           supplier_alias,
                                                           alias):
    reg_create_sso_account(context, supplier_alias, alias)


@when('"{supplier_alias}" decides to confirm her email address by using the '
      'email confirmation link')
def when_supplier_confirms_the_email_address(context, supplier_alias):
    reg_open_email_confirmation_link(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address')
def when_supplier_confirms_email_address(context, supplier_alias):
    reg_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address for SSO/great.gov.uk '
      'account')
def when_supplier_confirms_email_address_for_sso(context, supplier_alias):
    sso_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" provides valid details of selected company')
def when_supplier_provides_company_details(context, supplier_alias):
    bp_provide_company_details(context, supplier_alias)


@when('"{supplier_alias}" selects random sector the company is interested in '
      'working in')
def when_supplier_selects_random_sector(context, supplier_alias):
    bp_select_random_sector(context, supplier_alias)


@when('"{supplier_alias}" provides her full name which will be used to sent '
      'the verification letter')
@when('"{supplier_alias}" provides his full name which will be used to sent '
      'the verification letter')
def when_supplier_provides_full_name(context, supplier_alias):
    bp_provide_full_name(context, supplier_alias)


@when('"{supplier_alias}" confirms the details which will be used to sent '
      'the verification letter')
def step_impl(context, supplier_alias):
    bp_confirm_registration_and_send_letter(context, supplier_alias)


@when('"{supplier_alias}" verifies the company with the verification code '
      'from the letter sent after Directory Profile was created')
def when_supplier_verifies_company(context, supplier_alias):
    prof_verify_company(context, supplier_alias)


@when('"{supplier_alias}" decides to view published Directory Profile')
def when_supplier_views_published_profile(context, supplier_alias):
    prof_view_published_profile(context, supplier_alias)


@when('"{supplier_alias}" decides that the export status of his company is '
      '"No, we are not planning to sell overseas"')
def when_supplier_says_his_not_ready_to_export(context, supplier_alias):
    reg_supplier_is_not_ready_to_export(context, supplier_alias)


@when('"{supplier_alias}" attempts to sign in to Find a Buyer profile')
def when_supplier_attempts_to_sign_in_to_fab(context, supplier_alias):
    prof_attempt_to_sign_in_to_fab(context, supplier_alias)


@when('"{supplier_alias}" signs in to Find a Buyer profile')
def when_supplier_signs_in_to_fab(context, supplier_alias):
    prof_sign_in_to_fab(context, supplier_alias)


@when('"{supplier_alias}" creates a SSO/great.gov.uk account')
def when_supplier_creates_standalone_sso_account(context, supplier_alias):
    reg_create_standalone_sso_account(context, supplier_alias)


@when('"{supplier_alias}" decides to create a trade profile')
def when_supplier_decide_to_create_trade_profile(context, supplier_alias):
    sso_go_to_create_trade_profile(context, supplier_alias)
