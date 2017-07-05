# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import random
import string
import uuid

from requests import Session

from tests.functional.features.context_utils import Actor
from tests.functional.features.steps.fab_then_impl import (
    bp_should_be_prompted_to_build_your_profile,
    prof_should_be_on_profile_page,
    prof_should_be_told_about_missing_description,
    prof_should_be_told_that_company_is_published,
    reg_should_get_verification_email,
    reg_sso_account_should_be_created,
    sso_should_be_on_landing_page,
    sso_should_be_signed_in_to_sso_account
)
from tests.functional.features.steps.fab_when_impl import (
    bp_confirm_registration_and_send_letter,
    bp_provide_company_details,
    bp_provide_full_name,
    bp_select_random_sector,
    prof_set_company_description,
    prof_verify_company,
    reg_confirm_company_selection,
    reg_confirm_export_status,
    reg_create_sso_account,
    reg_create_standalone_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    select_random_company,
    sso_go_to_create_trade_profile,
    sso_supplier_confirms_email_address
)
from tests.functional.features.utils import get_positive_exporting_status
from tests.settings import EMAIL_VERIFICATION_MSG_SUBJECT


def unauthenticated_supplier(context, supplier_alias):
    """Create an instance of an unauthenticated Supplier Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
     * initialize `requests` Session object that allows you to keep the cookies
        across multiple requests

    NOTE:
    Will use test email account "test@directory.uktrade.io" which is configured
    on AWS SES to store all incoming emails in plain text in S3.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used within the scenario's scope
    :type supplier_alias: str
    """
    session = Session()
    email = "test+{}+{}@directory.uktrade.io".format(
        supplier_alias.replace(" ", "_"), str(uuid.uuid4()))
    password_length = 10
    password = ''.join(random.choice(string.ascii_letters)
                       for i in range(password_length))
    actor = Actor(alias=supplier_alias, email=email, password=password,
                  session=session, csrfmiddlewaretoken=None,
                  email_confirmation_link=None, company_alias=None,
                  has_sso_account=False)
    context.add_actor(actor)


def reg_create_sso_account_associated_with_company(context, supplier_alias,
                                                   company_alias):
    export_status = get_positive_exporting_status()
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    reg_confirm_export_status(context, supplier_alias, export_status)
    reg_create_sso_account(context, supplier_alias, company_alias)
    reg_sso_account_should_be_created(context, supplier_alias)


def reg_confirm_email_address(context, supplier_alias):
    subject = EMAIL_VERIFICATION_MSG_SUBJECT
    reg_should_get_verification_email(context, supplier_alias, subject)
    reg_open_email_confirmation_link(context, supplier_alias)
    reg_supplier_confirms_email_address(context, supplier_alias)
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)


def bp_build_company_profile(context, supplier_alias):
    bp_provide_company_details(context, supplier_alias)
    bp_select_random_sector(context, supplier_alias)
    bp_provide_full_name(context, supplier_alias)
    bp_confirm_registration_and_send_letter(context, supplier_alias)
    prof_should_be_on_profile_page(context, supplier_alias)
    prof_should_be_told_about_missing_description(context, supplier_alias)


def reg_create_verified_profile(context, supplier_alias, company_alias):
    # STEP 0 - initialize actor
    unauthenticated_supplier(context, supplier_alias)

    # STEP 1 - select company, create SSO profile & verify email address
    reg_create_sso_account_associated_with_company(context, supplier_alias,
                                                   company_alias)
    reg_confirm_email_address(context, supplier_alias)

    # STEP 2 - build company profile after email verification
    bp_build_company_profile(context, supplier_alias)

    # STEP 3 - verify company with the code sent by post
    prof_set_company_description(context, supplier_alias)
    prof_verify_company(context, supplier_alias)
    prof_should_be_on_profile_page(context, supplier_alias)
    prof_should_be_told_that_company_is_published(context, supplier_alias)


def sso_create_standalone_unverified_sso_account(context, supplier_alias):
    subject = EMAIL_VERIFICATION_MSG_SUBJECT
    unauthenticated_supplier(context, supplier_alias)
    reg_create_standalone_sso_account(context, supplier_alias)
    reg_sso_account_should_be_created(context, supplier_alias)
    reg_should_get_verification_email(context, supplier_alias, subject)


def sso_create_standalone_verified_sso_account(context, supplier_alias):
    sso_create_standalone_unverified_sso_account(context, supplier_alias)
    reg_open_email_confirmation_link(context, supplier_alias)
    sso_supplier_confirms_email_address(context, supplier_alias)
    sso_should_be_on_landing_page(context, supplier_alias)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


def reg_select_random_company_and_confirm_export_status(
        context, supplier_alias, company_alias):
    export_status = get_positive_exporting_status()
    sso_create_standalone_verified_sso_account(context, supplier_alias)
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)
    sso_go_to_create_trade_profile(context, supplier_alias)
    select_random_company(context, supplier_alias, company_alias)
    reg_confirm_company_selection(context, supplier_alias, company_alias)
    reg_confirm_export_status(context, supplier_alias, export_status)
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)
