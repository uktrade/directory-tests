# -*- coding: utf-8 -*-
"""Common operations for Gov Notify service"""
import logging

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


def filter_by_subject(notifications: list, subject: str) -> list:
    return list(filter(lambda x: x["subject"] == subject, notifications))


def filter_by_recipient(notifications: list, email: str) -> list:
    return list(filter(lambda x: x["email_address"] == email, notifications))


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmation_notification(
        email: str, *, subject: str = "Confirm your email address") -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(
        template_type="email")["notifications"]

    user_notifications = filter_by_recipient(notifications, email)
    email_confirmations = filter_by_subject(user_notifications, subject)

    logging.debug(notifications)
    logging.debug(user_notifications)
    logging.debug(email_confirmations)
    assert len(email_confirmations) == 1, (
        "Expected to find 1 email confirmation notification for {} but found "
        "{}".format(email, len(email_confirmations)))

    return email_confirmations[0]


def get_verification_link(email: str) -> str:
    logging.debug("Searching for verification email of: {}".format(email))
    notification = get_email_confirmation_notification(email)
    body = notification["body"]
    return extract_email_confirmation_link(body)
