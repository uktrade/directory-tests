# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
import logging


def verify_response_sso_account_was_created(context):
    """Will verify if SSO account was successfully created.

    It's a very crude check, as it will only check if the response body contains
    selected phrases.

    NOTE:
    It expects that create SSO account response is stored in `context.response`

    :param context: behave `context` object
    :type context: behave.runner.Context
    """
    response = context.response
    msgs = ["Verify your email address",
            "if you do not receive an email within 10 minutes", (
                "We have sent you a confirmation email. Please follow the link "
                "in the email to verify your email address.")
            ]

    content = response.content.decode("utf-8")
    for msg in msgs:
        err_msg = ("Could not find '{}' in the response".format(msg))
        assert content.find(msg) > -1, err_msg
    logging.debug("Successfully created new SSO account")

