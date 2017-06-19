# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import given

from tests.functional.features.steps.fab_given_impl import (
    create_sso_account_associated_with_company,
    unauthenticated_supplier
)
from tests.functional.features.steps.fab_then_impl import (
    should_get_verification_email
)


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    unauthenticated_supplier(context, supplier_alias)


@given('"{supplier_alias}" created a SSO account associated with randomly '
       'selected company "{company_alias}"')
def given_supplier_created_sso_account_for_company(context, supplier_alias,
                                                   company_alias):
    create_sso_account_associated_with_company(context, supplier_alias,
                                               company_alias)


@given('"{alias}" received the email verification message with the email '
       'confirmation link')
def then_supplier_should_receive_verification_email(context, alias):
    subject = "Your great.gov.uk account: Please Confirm Your E-mail Address"
    should_get_verification_email(context, alias, subject)
