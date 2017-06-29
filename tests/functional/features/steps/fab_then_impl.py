# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
import logging

from retrying import retry

from tests.functional.features.utils import (
    extract_email_confirmation_link,
    find_confirmation_email_msg,
    get_s3_bucket
)


def sso_account_should_be_created(context, alias):
    """Will verify if SSO account was successfully created.

    It's a very crude check, as it will only check if the response body
    contains selected phrases.

    NOTE:
    It expects that create SSO account response is stored in `context.response`

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the Actor used in the scope of the scenario
    :type alias: str
    """
    response = context.response
    msgs = ["Verify your email address",
            "if you do not receive an email within 10 minutes", (
                "We have sent you a confirmation email. Please follow the link"
                " in the email to verify your email address.")]

    content = response.content.decode("utf-8")
    for msg in msgs:
        err_msg = ("Could not find '{}' in the response".format(msg))
        assert msg in content, err_msg
    logging.debug("Successfully created new SSO account for %s", alias)


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def should_get_verification_email(context, alias, subject):
    """Will check if the Supplier received an email verification message.

    NOTE:
    The check is done by attempting to find a file with the email is Amazon S3.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the Actor used in the scope of the scenario
    :type alias: str
    :param subject: expected subject of the email verification message
    :type  subject: str
    """
    actor = context.get_actor(alias)
    bucket = get_s3_bucket()
    payload = find_confirmation_email_msg(bucket, actor, subject)
    link = extract_email_confirmation_link(payload)
    context.set_actor_email_confirmation_link(alias, link)
