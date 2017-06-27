# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import (
    bp_provide_company_details,
    bp_select_random_sector,
    confirm_company_selection,
    confirm_export_status,
    create_sso_account,
    open_email_confirmation_link,
    select_random_company,
    supplier_confirms_email_address)


@when('"{supplier_alias}" randomly selects an active company without a profile'
      ' identified by an alias "{alias}"')
def when_supplier_selects_random_company(context, supplier_alias, alias):
    select_random_company(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that "{alias}" is the correct one')
def when_company_selection_is_confirmed(context, supplier_alias, alias):
    confirm_company_selection(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that the export status of "{alias}" is '
      '"{export_status}"')
def when_supplier_confirms_export_status(context, supplier_alias, alias,
                                         export_status):
    confirm_export_status(context, supplier_alias, alias, export_status)


@when('"{supplier_alias}" creates a SSO account for "{alias}" using '
      'valid credentials')
def when_supplier_creates_sso_account_for_selected_company(context,
                                                           supplier_alias,
                                                           alias):
    create_sso_account(context, supplier_alias, alias)


@when('"{supplier_alias}" decides to confirm her email address by using the '
      'email confirmation link')
def when_supplier_confirms_the_email_address(context, supplier_alias):
    open_email_confirmation_link(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address')
def when_supplier_confirms_email_address(context, supplier_alias):
    supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" provides valid details of selected company')
def when_supplier_provides_company_details(context, supplier_alias):
    bp_provide_company_details(context, supplier_alias)


@when('"{supplier_alias}" selects random sector the company is interested in '
      'working in')
def when_supplier_selects_random_sector(context, supplier_alias):
    bp_select_random_sector(context, supplier_alias)
