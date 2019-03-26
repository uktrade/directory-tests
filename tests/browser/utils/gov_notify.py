# -*- coding: utf-8 -*-
"""Common operations for Gov Notify service"""
import logging
from pprint import pformat
from typing import List

from notifications_python_client import NotificationsAPIClient
from retrying import retry

from settings import GOV_NOTIFY_API_KEY

GOV_NOTIFY_CLIENT = NotificationsAPIClient(GOV_NOTIFY_API_KEY)


def extract_email_confirmation_link(payload: str) -> str:
    """Find email confirmation link inside the plain text email payload."""
    start = payload.find("https")
    activation_link = payload[start:]
    logging.debug("Found email confirmation link: %s", activation_link)
    return activation_link


def extract_email_confirmation_code(payload: str) -> str:
    """Find email confirmation code inside the plain text email payload."""
    reference = "Your confirmation code is "
    start = payload.find(reference) + len(reference)
    end = start + 5
    confirmation_code = payload[start:end]
    logging.debug("Found email confirmation code: %s", confirmation_code)
    return confirmation_code


def filter_by_subject(notifications: list, subject: str) -> list:
    return list(filter(lambda x: x["subject"] == subject, notifications))


def filter_by_recipient(notifications: list, email: str) -> list:
    return list(filter(lambda x: x["email_address"] == email, notifications))


def filter_by_body_string(notifications: list, strings: List[str]) -> list:
    return list(
        filter(lambda x: all(string in x["body"] for string in strings), notifications)
    )


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmation_notification(
    email: str, *, subject: str = "Confirm your email address"
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]

    user_notifications = filter_by_recipient(notifications, email)
    email_confirmations = filter_by_subject(user_notifications, subject)

    if email_confirmations:
        logging.debug(pformat(email_confirmations))
    assert len(email_confirmations) == 1, (
        "Expected to find 1 email confirmation notification for {} but found "
        "{}".format(email, len(email_confirmations))
    )

    return email_confirmations[0]


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmations_with_matching_string(
    recipient_email: str, subject: str, strings: List[str]
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]

    user_notifications = filter_by_recipient(notifications, recipient_email)
    email_confirmations = filter_by_subject(user_notifications, subject)
    with_matching_string = filter_by_body_string(email_confirmations, strings)

    logging.debug(pformat(with_matching_string))
    assert len(with_matching_string) == 1, (
        f"Expected to find 1 email confirmation notification containing "
        f"'{strings}' in message body send to {recipient_email} but found "
        f"{len(email_confirmations)}. BTW. Check what's the agent's email "
        f"address used in the Invest application configuration"
    )

    return with_matching_string[0]


def get_verification_link(email: str) -> str:
    logging.debug("Searching for verification email of: {}".format(email))
    notification = get_email_confirmation_notification(email)
    body = notification["body"]
    return extract_email_confirmation_link(body)


def get_verification_code(email: str) -> str:
    """Find email confirmation code inside the plain text email payload."""
    subject = "Your confirmation code for great.gov.uk"
    notification = get_email_confirmation_notification(email, subject=subject)
    body = notification["body"]
    activation_code = extract_email_confirmation_code(body)
    logging.debug("Found email confirmation code: %s", activation_code)
    return activation_code
