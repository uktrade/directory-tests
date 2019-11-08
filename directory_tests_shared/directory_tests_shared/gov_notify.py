# -*- coding: utf-8 -*-
"""Common operations for Gov Notify service"""
import logging
from pprint import pformat
from typing import List

from retrying import retry

from .clients import GOV_NOTIFY_CLIENT, PIR_GOV_NOTIFY_CLIENT
from .constants import (
    EMAIL_VERIFICATION_CODE_SUBJECT,
    EMAIL_VERIFICATION_MSG_SUBJECT,
    SSO_PASSWORD_RESET_MSG_SUBJECT,
)
from .utils import assertion_msg


def extract_email_confirmation_link(payload: str) -> str:
    """Find email confirmation link inside the plain text email payload."""
    start = payload.find("https")
    next_word = payload.find(" ", start)
    if next_word != -1:
        activation_link = payload[start:next_word]
    else:
        new_line = payload.find("\n", start)
        if new_line != -1:
            activation_link = payload[start:new_line]
        else:
            activation_link = payload[start:]
    with assertion_msg("activation link shouldn't contain new line character"):
        assert "\n" not in activation_link
    logging.debug(f"Found email confirmation link: {activation_link}")
    return activation_link


def extract_email_confirmation_code(payload: str) -> str:
    """Find email confirmation code inside the plain text email payload."""
    reference = "Your confirmation code is "
    start = payload.find(reference) + len(reference)
    end = start + 5
    confirmation_code = payload[start:end]
    logging.debug(f"Found email confirmation code: {confirmation_code}")
    return confirmation_code


def extract_password_reset_link(payload: str) -> str:
    """Find password reset link inside the plain text email payload."""
    start = payload.find("https")
    end = payload.find("\r\n", start)
    password_reset_link = payload[start:end]
    with assertion_msg(
        f"Extracted link is not a correct password reset link: {password_reset_link}"
    ):
        assert "accounts/password/reset/key/" in password_reset_link
    logging.debug(f"Found password reset link: {password_reset_link}")
    return password_reset_link


def filter_by_subject(notifications: list, subject: str) -> list:
    return list(filter(lambda x: subject in x["subject"], notifications))


def filter_by_recipient(notifications: list, email: str) -> list:
    return list(filter(lambda x: x["email_address"] == email, notifications))


def filter_by_content(notifications: list, substring: str) -> list:
    return list(filter(lambda x: substring in x["body"], notifications))


def filter_by_strings_in_body(notifications: list, strings: List[str]) -> list:
    return list(
        filter(lambda x: all(string in x["body"] for string in strings), notifications)
    )


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_notification(from_email: str, to_email: str, subject: str) -> dict:
    all_notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]

    recipient_notifications = filter_by_recipient(all_notifications, to_email)
    assert (
        len(recipient_notifications) > 0
    ), f"Expected to find at least 1 notification send to {to_email} but found 0"
    logging.debug(
        f"Found {len(recipient_notifications)} notifications send to: {to_email}"
    )

    notifications_with_matching_subject = filter_by_subject(
        recipient_notifications, subject
    )
    assert len(notifications_with_matching_subject) == 1, (
        f"Expected to find 1 notification entitled '{subject}' send to {to_email} but "
        f"found {len(notifications_with_matching_subject)}"
    )
    logging.debug(
        f"Found {len(notifications_with_matching_subject)} notifications send to: "
        f"{to_email} with matching subject: '{subject}'"
    )

    matching_notifications = filter_by_content(
        notifications_with_matching_subject, from_email
    )
    assert len(matching_notifications) == 1, (
        f"Expected to find 1 notification entitled '{subject}' send from {from_email} "
        f"to {to_email} but found {len(matching_notifications)}"
    )
    logging.debug(
        f"Found {len(matching_notifications)} notifications send from {from_email} to: "
        f"{to_email} with matching subject: '{subject}'"
    )

    return matching_notifications[0]


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmation_notification(
    email: str, *, subject: str = None, resent_code: bool = False, service: str = None
) -> dict:
    subject = subject or EMAIL_VERIFICATION_MSG_SUBJECT
    logging.debug(f"Looking for email sent to '{email}' with subject: '{subject}'")
    if service == "PIR":
        client = PIR_GOV_NOTIFY_CLIENT
    else:
        client = GOV_NOTIFY_CLIENT
    notifications = client.get_all_notifications(template_type="email")["notifications"]

    user_notifications = filter_by_recipient(notifications, email)
    email_confirmations = filter_by_subject(user_notifications, subject)

    if email_confirmations:
        logging.debug(pformat(email_confirmations))
    if resent_code:
        assert len(email_confirmations) > 1, (
            f"Expected to find more than 1 email confirmation notification for {email}"
            f" but found {len(email_confirmations)}"
        )

        result = max(email_confirmations, key=lambda x: x["created_at"])
    else:
        other_subjects = {mail["subject"] for mail in user_notifications}
        error = (
            f"Expected to find only 1 email confirmation notification for {email} but "
            f"found {len(email_confirmations)}. PS. I found {len(user_notifications)} "
            f"other emails to this user with following subjects: {other_subjects}"
        )
        assert len(email_confirmations) == 1, error
        result = min(email_confirmations, key=lambda x: x["created_at"])

    return result


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_password_reset_notification(
    email: str, *, subject: str = SSO_PASSWORD_RESET_MSG_SUBJECT
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]

    user_notifications = filter_by_recipient(notifications, email)
    password_reset_notifications = filter_by_subject(user_notifications, subject)

    assert len(password_reset_notifications) == 1, (
        f"Expected to find 1 password reset notification for {email} but found "
        f"{len(password_reset_notifications)}"
    )

    return password_reset_notifications[0]


def get_verification_link(email: str, *, subject: str = None) -> str:
    logging.debug(f"Searching for verification email of: {email}")
    notification = get_email_confirmation_notification(email, subject=subject)
    body = notification["body"]
    return extract_email_confirmation_link(body)


def get_password_reset_link(email: str) -> str:
    logging.debug(f"Searching for password reset email of: {email}")
    notification = get_password_reset_notification(email)
    body = notification["body"]
    return extract_password_reset_link(body)


@retry(wait_fixed=2000, stop_max_attempt_number=5)
def get_email_verification_code(email: str, *, resent_code: bool = False) -> str:
    """Find email confirmation code inside the plain text email payload."""
    subject = EMAIL_VERIFICATION_CODE_SUBJECT
    notification = get_email_confirmation_notification(
        email, subject=subject, resent_code=resent_code
    )
    body = notification["body"]
    activation_code = extract_email_confirmation_code(body)
    logging.debug(f"Found email confirmation code: {activation_code}")
    return activation_code


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_email_confirmations_with_matching_string(
    recipient_email: str, subject: str, strings: List[str]
) -> dict:
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]

    user_notifications = filter_by_recipient(notifications, recipient_email)
    email_confirmations = filter_by_subject(user_notifications, subject)
    with_matching_string = filter_by_strings_in_body(email_confirmations, strings)

    extra_message = ""
    if not with_matching_string and email_confirmations:
        extra_message = (
            f"BTW. Here are other notifications for '{recipient_email}': "
            f"{email_confirmations}"
        )

    logging.debug(pformat(with_matching_string))
    assert len(with_matching_string) == 1, (
        f"Expected to find 1 email confirmation notification containing "
        f"'{strings}' in message body send to {recipient_email} but found "
        f"{len(with_matching_string)}. Check if you're using correct email address for "
        f"the agent that supposed to receive it. {extra_message}"
    )

    return with_matching_string[0]


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def get_notifications_by_subject(email: str, subject: str) -> List[dict]:
    logging.debug(f"Looking for email sent to '{email}' with subject: '{subject}'")
    notifications = GOV_NOTIFY_CLIENT.get_all_notifications(template_type="email")[
        "notifications"
    ]
    user_notifications = filter_by_recipient(notifications, email)
    matching_notifications = filter_by_subject(user_notifications, subject)

    assert len(matching_notifications) >= 1, (
        f"Expected to find at least 1 notification for {email} with subject '{subject}'"
        f" but found {len(matching_notifications)}"
    )
    return matching_notifications
