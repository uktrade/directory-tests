# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import random
import string

from requests import Session

from tests.functional.features.context_utils import Actor
from tests.functional.features.settings import EMAIL_VERIFICATION_MSG_SUBJECT
from tests.functional.features.steps.fab_then_impl import (
    prof_should_be_on_profile_page,
    should_be_prompted_to_build_your_profile,
    prof_should_be_told_about_missing_description,
    reg_should_get_verification_email,
    reg_sso_account_should_be_created
)
from tests.functional.features.steps.fab_when_impl import (
    bp_confirm_registration_and_send_letter,
    bp_provide_company_details,
    bp_provide_full_name,
    bp_select_random_sector,
    confirm_company_selection,
    reg_confirm_export_status,
    reg_create_sso_account,
    reg_open_email_confirmation_link,
    select_random_company,
    reg_supplier_confirms_email_address
)


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
        supplier_alias.replace(" ", "_"), random.randint(100000, 999999))
    password_length = 10
    password = ''.join(random.choice(string.ascii_letters)
                       for i in range(password_length))
    actor = Actor(alias=supplier_alias, email=email, password=password,
                  session=session, csrfmiddlewaretoken=None,
                  email_confirmation_link=None, company_alias=None)
    context.add_actor(actor)


def reg_create_sso_account_associated_with_company(context, supplier_alias,
                                                   company_alias):
    export_status = ["Yes, in the last year",
                     "Yes, 1 to 2 years ago",
                     "Yes, but more than 2 years ago",
                     "No, but we are preparing to"]
    select_random_company(context, supplier_alias, company_alias)
    confirm_company_selection(context, supplier_alias, company_alias)
    reg_confirm_export_status(context, supplier_alias, company_alias,
                              random.choice(export_status))
    reg_create_sso_account(context, supplier_alias, company_alias)
    reg_sso_account_should_be_created(context, supplier_alias)


def reg_confirm_email_address(context, supplier_alias):
    subject = EMAIL_VERIFICATION_MSG_SUBJECT
    reg_should_get_verification_email(context, supplier_alias, subject)
    reg_open_email_confirmation_link(context, supplier_alias)
    reg_supplier_confirms_email_address(context, supplier_alias)
    should_be_prompted_to_build_your_profile(context, supplier_alias)


def bp_build_company_profile(context, supplier_alias):
    bp_provide_company_details(context, supplier_alias)
    bp_select_random_sector(context, supplier_alias)
    bp_provide_full_name(context, supplier_alias)
    bp_confirm_registration_and_send_letter(context, supplier_alias)
    prof_should_be_on_profile_page(context, supplier_alias)
    prof_should_be_told_about_missing_description(context, supplier_alias)
