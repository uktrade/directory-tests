# -*- coding: utf-8 -*-
"""SSO Common operations."""
import logging
from collections import namedtuple
from datetime import datetime, timedelta
from enum import Enum

from behave.runner import Context
from requests import Response
from retrying import retry

from settings import (
    MAILGUN_SSO_API_USER,
    MAILGUN_SSO_EVENTS_URL,
    MAILGUN_SSO_SECRET_API_KEY
)
from utils import assertion_msg
from utils.request import Method, make_request


class MailGunEvent(Enum):
    """Lists all of MailGun's event types.

    More info here:
    https://documentation.mailgun.com/en/latest/api-events.html#event-types
    """
    ACCEPTED = "accepted"
    DELIVERED = "delivered"
    REJECTED = "rejected"
    FAILED = "failed"
    OPENED = "opened"
    CLICKED = "clicked"
    UNSUBSCRIBED = "unsubscribed"
    COMPLAINED = "complained"
    STORED = "stored"

    def __str__(self):
        return self.value

    def __eq__(self, y):
        return self.value == y.value


class MailGunService(Enum):
    """Lists all MailGun's events states"""
    ServiceDetails = namedtuple('ServiceDetails', ['url', 'user', 'password'])
    SSO = ServiceDetails(
        url=MAILGUN_SSO_EVENTS_URL, user=MAILGUN_SSO_API_USER,
        password=MAILGUN_SSO_SECRET_API_KEY)

    def __str__(self):
        return self.value

    def __eq__(self, y):
        return self.value == y.value

    @property
    def url(self):
        return self.value.url

    @property
    def user(self):
        return self.value.user

    @property
    def password(self):
        return self.value.password


def extract_email_confirmation_link(payload):
    """Find email confirmation link inside the plain text email payload.

    :param payload: plain text email message payload
    :type  payload: str
    :return: email confirmation link
    :rtype:  str
    """
    start = payload.find("http")
    end = payload.find("\n", start) - 1  # `- 1` to skip the newline char
    activation_link = payload[start:end]
    logging.debug("Found email confirmation link: %s", activation_link)
    return activation_link


@retry(wait_fixed=15000, stop_max_attempt_number=9)
def find_mailgun_events(
        context: Context, service: MailGunService, *, sender: str = None,
        recipient: str = None, to: str = None, subject: str = None,
        limit: int = None, event: MailGunEvent = None, begin: str = None,
        end: str = None, ascending: str = None) -> Response:
    """

    :param context: behave `context` object
    :param service: an object with MailGun service details
    :param sender: (optional) email address of the sender
    :param recipient: (optional) email address of the recipient
    :param to: (optional) email address of the recipient (from the MIME header)
    :param subject: (optional) subject of the message
    :param limit: (optional) Number of entries to return. (300 max)
    :param event: (optional) An event type
    :param begin: (optional)
    :param end: (optional)
    :param ascending: (optional) yes/no
    :return: a response object
    """
    params = {}

    if sender:
        params.update({"from": sender})
    if recipient:
        params.update({"recipient": recipient})
    if to:
        params.update({"to": to})
    if subject:
        params.update({"subject": subject})
    if limit:
        params.update({"limit": limit})
    if event:
        params.update({"event": str(event)})
    if begin:
        params.update({"begin": begin})
    if end:
        params.update({"end": end})
    if ascending:
        params.update({"ascending": ascending})

    response = make_request(
        Method.GET, service.url, auth=(service.user, service.password),
        params=params)
    context.response = response
    with assertion_msg(
            "Expected 200 OK from MailGun when searching for an event %s",
            response.status_code):
        assert response.status_code == 200
    number_of_events = len(response.json()["items"])
    if limit:
        with assertion_msg(
                "Expected (maximum) %d events but got %d instead.", limit,
                number_of_events):
            assert number_of_events <= limit
    with assertion_msg(
            "Expected to find at least 1 MailGun event, got 0 instead. User "
            "parameters: %s", params):
        assert number_of_events > 0
    logging.debug(
        "Found {} event(s) that matched following criteria: {}"
        .format(number_of_events, params))
    return response


@retry(wait_fixed=10000, stop_max_attempt_number=9)
def mailgun_get_message(context: Context, url: str) -> dict:
    """Get message detail by its URL.

    :param context: behave `context` object
    :param url: unique mailgun message URL
    :return: a dictionary with message details and message body
    """
    api_key = MAILGUN_SSO_SECRET_API_KEY
    # this will help us to get the raw MIME
    headers = {"Accept": "message/rfc2822"}
    response = make_request(
        Method.GET, url, headers=headers, auth=("api", api_key))
    context.response = response

    with assertion_msg(
            "Expected 200 from MailGun when getting message but got %s",
            response.status_code):
        assert response.status_code == 200
    return response.json()


def mailgun_get_message_url(
        context: Context, recipient: str, *, subject: str = None) -> str:
    """Will try to find the message URL among 100 emails sent in last 1 hour.

    NOTE:
    More on MailGun's Event Polling:
    https://documentation.mailgun.com/en/latest/api-events.html#event-polling

    :param context: behave `context` object
    :param recipient: email address of the message recipient
    :param subject: (optional) subject of sought email
    :return: mailgun message URL
    """
    message_limit = 1
    pattern = '%a, %d %b %Y %H:%M:%S GMT'
    begin = (datetime.utcnow() - timedelta(minutes=60)).strftime(pattern)

    response = find_mailgun_events(
        context, MailGunService.SSO, limit=message_limit, recipient=recipient,
        event=MailGunEvent.ACCEPTED, begin=begin, ascending="yes",
        subject=subject
    )
    context.response = response
    logging.debug("Found event with recipient: {}".format(recipient))
    return response.json()["items"][0]["storage"]["url"]


def get_verification_link(context: Context, recipient: str) -> str:
    """Get email verification link sent by SSO to specified recipient.

    :param context: behave `context` object
    :param recipient: email address of the message recipient
    :return: email verification link sent by SSO
    """
    logging.debug("Searching for verification email of: {}".format(recipient))
    message_url = mailgun_get_message_url(context, recipient)
    message = mailgun_get_message(context, message_url)
    body = message["body-mime"]
    return extract_email_confirmation_link(body)
