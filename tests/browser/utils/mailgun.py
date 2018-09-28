import logging

from collections import namedtuple
from enum import Enum

from behave.runner import Context
from requests import Response
from retrying import retry

from pages.common_actions import assertion_msg
from settings import (
    INVEST_CONTACT_CONFIRMATION_SUBJECT,
    MAILGUN_API_USER,
    MAILGUN_INVEST_EVENTS_URL,
    MAILGUN_INVEST_SECRET_API_KEY,
)
from utils.request import make_request, Method


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

    ServiceDetails = namedtuple("ServiceDetails", ["url", "user", "secret"])
    INVEST = ServiceDetails(
        url=MAILGUN_INVEST_EVENTS_URL,
        user=MAILGUN_API_USER,
        secret=MAILGUN_INVEST_SECRET_API_KEY,
    )

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
    def secret(self):
        return self.value.secret


@retry(wait_fixed=15000, stop_max_attempt_number=9)
def find_mailgun_events(
        context: Context,
        service: MailGunService,
        *,
        sender: str = None,
        recipient: str = None,
        to: str = None,
        subject: str = None,
        limit: int = None,
        event: MailGunEvent = None,
        begin: str = None,
        end: str = None,
        ascending: str = None
) -> Response:
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
        Method.GET,
        service.url,
        auth=(service.user, service.secret),
        params=params,
    )
    context.response = response
    with assertion_msg(
            "Expected 200 OK from MailGun when searching for an event %s",
            response.status_code,
    ):
        assert response.status_code == 200
    number_of_events = len(response.json()["items"])
    if limit:
        with assertion_msg(
                "Expected (maximum) %d events but got %d instead.",
                limit,
                number_of_events,
        ):
            assert number_of_events <= limit
    with assertion_msg(
            "Expected to find at least 1 MailGun event, got 0 instead. User "
            "parameters: %s",
            params,
    ):
        assert number_of_events > 0
    logging.debug(
        "Found {} event(s) that matched following criteria: {}".format(
            number_of_events, params
        )
    )
    return response


def mailgun_invest_find_contact_confirmation_email(
        context: Context, sender: str, recipient: str, *,
        subject: str = INVEST_CONTACT_CONFIRMATION_SUBJECT):
    logging.debug(
        "Trying to find contact confirmation email sent to: "
        "%s",
        recipient,
    )
    response = find_mailgun_events(
        context,
        sender=sender,
        service=MailGunService.INVEST,
        recipient=recipient,
        event=MailGunEvent.ACCEPTED,
        subject=subject,
    )
    context.response = response
    with assertion_msg(
            "Expected to find a contact confirmation email sent to: %s",
            recipient
    ):
        assert response.status_code == 200
