# -*- coding: utf-8 -*-
"""Common operations for Gov Notify service"""
import logging

from notifications_python_client import NotificationsAPIClient
from retrying import retry
from tests.functional.utils.generic import assertion_msg
from tests.settings import (
    EMAIL_VERIFICATION_MSG_SUBJECT,
    GOV_NOTIFY_API_KEY,
    SSO_PASSWORD_RESET_MSG_SUBJECT,
)

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


def extract_password_reset_link(payload: str) -> str:
    """Find password reset link inside the plain text email payload."""
    start = payload.find("https")
    end = payload.find("\r\n", start)
    password_reset_link = payload[start:end]
    with assertion_msg(
        "Extracted link is not a correct password reset link: %s",
        password_reset_link,
    ):
        assert "accounts/password/reset/key/" in password_reset_link
    logging.debug("Found password reset link: %s", password_reset_link)
    return password_reset_link


def filter_by_subject(notifications: list, subject: str) -> list:
    return list(filter(lambda x: x["subject"] == subject, notifications))


def filter_by_recipient(notifications: list, email: str) -> list:
    return list(filter(lambda x: x["email_address"] == email, notifications))


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmation_notification(
    email: str, *, subject: str = EMAIL_VERIFICATION_MSG_SUBJECT
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(
        template_type="email"
    )["notifications"]

    user_notifications = filter_by_recipient(notifications, email)
    email_confirmations = filter_by_subject(user_notifications, subject)

    assert len(email_confirmations) == 1, (
        "Expected to find 1 email confirmation notification for {} but found "
        "{}".format(email, len(email_confirmations))
    )

    return email_confirmations[0]


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_password_reset_notification(
    email: str, *, subject: str = SSO_PASSWORD_RESET_MSG_SUBJECT
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(
        template_type="email"
    )["notifications"]

    user_notifications = filter_by_recipient(notifications, email)
    password_reset_notifications = filter_by_subject(
        user_notifications, subject
    )

    assert len(password_reset_notifications) == 1, (
        "Expected to find 1 password reset notification for {} but found "
        "{}".format(email, len(password_reset_notifications))
    )

    return password_reset_notifications[0]


def get_verification_link(email: str) -> str:
    logging.debug("Searching for verification email of: %s", email)
    notification = get_email_confirmation_notification(email)
    body = notification["body"]
    return extract_email_confirmation_link(body)


def get_password_reset_link(email: str) -> str:
    logging.debug("Searching for password reset email of: %s", email)
    notification = get_password_reset_notification(email)
    body = notification["body"]
    return extract_password_reset_link(body)


@retry(wait_fixed=2000, stop_max_attempt_number=5)
def get_email_verification_code(email: str) -> str:
    """Find email confirmation code inside the plain text email payload."""
    subject = "Your confirmation code for great.gov.uk"
    notification = get_email_confirmation_notification(email, subject=subject)
    body = notification["body"]
    return extract_email_confirmation_code(body)
