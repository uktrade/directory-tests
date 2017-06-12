# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import \
    confirm_company_selection
from tests.functional.features.steps.fab_when_impl import \
    confirm_export_status
from tests.functional.features.steps.fab_when_impl import \
    create_sso_account_for_selected_company
from tests.functional.features.steps.fab_when_impl import select_random_company


@when('"{supplier_alias}" randomly selects an active company without a profile '
      'identified by an alias "{alias}"')
def when_random_company_is_selected(context, supplier_alias, alias):
    select_random_company(context, alias)


@when('"{supplier_alias}" confirms that "{alias}" is the correct one')
def when_company_selection_is_confirmed(context, supplier_alias, alias):
    confirm_company_selection(context, alias)


@when('"{supplier_alias}" confirms that the export status of "{alias}" is '
      '"{export_status}"')
def when_supplier_confirms_export_status(context, supplier_alias, alias,
                                         export_status):
    confirm_export_status(context, supplier_alias, alias, export_status)


@when('"{supplier_alias}" creates a SSO account for "{alias}" using '
      '"{are_valid}" credentials')
def when_supplier_creates_sso_account_for_selected_company(context,
                                                           supplier_alias,
                                                           alias,
                                                           are_valid):
    create_sso_account_for_selected_company(context, supplier_alias, alias,
                                            are_valid)
