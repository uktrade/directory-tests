# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
import email
import logging

from boto.s3 import connect_to_region
from boto.s3.connection import OrdinaryCallingFormat
from retrying import retry

from tests.functional.features.settings import S3_ACCESS_KEY_ID
from tests.functional.features.settings import S3_SECRET_ACCESS_KEY
from tests.functional.features.settings import S3_BUCKET
from tests.functional.features.settings import S3_REGION
from tests.functional.features.utils import \
    extract_plain_text_payload
from tests.functional.features.utils import extract_email_confirmation_link


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
def should_get_verification_email(context, alias, title):
    """Will check if the Supplier received an email verification message.

    NOTE:
    The check is done by attempting to find a file with the email is Amazon S3.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the Actor used in the scope of the scenario
    :type alias: str
    :param title: expected title of the email verification message
    :type  title: str
    """
    actor = context.get_actor(alias)
    title = title or ("Your great.gov.uk account: Please Confirm Your E-mail "
                      "Address")
    conn = connect_to_region(region_name=S3_REGION,
                             aws_access_key_id=S3_ACCESS_KEY_ID,
                             aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                             is_secure=True,
                             calling_format=OrdinaryCallingFormat())
    bucket = conn.get_bucket(S3_BUCKET)
    found = False
    for key in bucket.list():
        if key.key != "AMAZON_SES_SETUP_NOTIFICATION":
            logging.debug("Processing email file: %s", key.key)
            try:
                msg_contents = key.get_contents_as_string().decode("utf-8")
                msg = email.message_from_string(msg_contents)
                if msg['To'] == actor.email:
                    logging.debug("Found an email addressed at: %s",
                                  msg['To'])
                    if msg['Subject'] == title:
                        logging.debug("Found email confirmation message "
                                      "entitled: %s", title)
                        payload = extract_plain_text_payload(msg)
                        link = extract_email_confirmation_link(payload)
                        context.set_actor_email_confirmation_link(alias, link)
                        found = True
                logging.debug("Deleting message %s", key.key)
                bucket.delete_key(key.key)
                logging.debug("Successfully deleted message %s from S3",
                              key.key)
            except Exception as ex:
                logging.error("Something went wrong when getting an email msg "
                              "from S3: %s", ex)

    assert found, ("Could not find email confirmation message for {}"
                   .format(actor.email))
