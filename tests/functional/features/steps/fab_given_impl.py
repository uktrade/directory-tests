# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import string
import random

from requests import Session

from tests.functional.features.context_utils import Actor


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
                  email_confirmation_link=None)
    context.add_actor(actor)
