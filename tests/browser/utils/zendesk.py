# -*- coding: utf-8 -*-
import datetime
import logging
from typing import List

from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket

from settings import ZENDESK_EMAIL, ZENDESK_SUBDOMAIN, ZENDESK_TOKEN

credentials = {
    "email": ZENDESK_EMAIL,
    "token": ZENDESK_TOKEN,
    "subdomain": ZENDESK_SUBDOMAIN,
}

ZENPY_CLIENT = Zenpy(**credentials)


def get_tickets(*, start_time: datetime.datetime = None) -> List[Ticket]:
    if not start_time:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start_time = now - datetime.timedelta(days=1)
    return [t for t in ZENPY_CLIENT.tickets.incremental(start_time=start_time)]


def filter_by_brand(tickets: List[Ticket], brand: str) -> List[Ticket]:
    return list(filter(lambda x: x.brand.name == brand, tickets))


def filter_by_email(tickets: List[Ticket], email: str) -> List[Ticket]:
    return list(filter(lambda x: x.requester.email == email, tickets))


def filter_by_subject(tickets: List[Ticket], subject: str) -> List[Ticket]:
    return list(filter(lambda x: x.subject.lower() == subject.lower(), tickets))


def filter_by_content(tickets: List[Ticket], strings: List[str]) -> List[Ticket]:
    return list(
        filter(lambda x: all(string in x.description for string in strings), tickets)
    )


def find_tickets(email: str, subject: str) -> List[Ticket]:
    tickets = get_tickets()
    logging.debug(f"Found {len(tickets)} Zendesk tickets")
    by_email = filter_by_email(tickets, email)
    logging.debug(f"Found {len(by_email)} emails for {email}")
    return filter_by_subject(by_email, subject)
