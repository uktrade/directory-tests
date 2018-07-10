# -*- coding: utf-8 -*-
"""FAB - Confirm your will to collaborate to company's profile page"""
import logging

from requests import Response, Session
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

EXPECTED_STRINGS = [
    "Collaborate",
    "Do you want to be added as user to the profile for",
    "Yes",
    "No",
    "Is there anything wrong with this page?",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the FAB Confirm your collaboration page"
    )


def open(session: Session, link: str) -> Response:
    with assertion_msg("Expected a non-empty invitation link"):
        assert link
    return make_request(Method.GET, link, session=session)


def confirm(
    session: Session, csrf_middleware_token: str, invitation_link: str
) -> Response:
    """Confirm the invitation for collaboration.

    Example invitation link:
    https://dev.buyer.directory.uktrade.io/account/collaborate/accept/?invite_key=d1d04035-fb15-4bad-9903-452345234534
    """
    # in order to be redirected to the correct URL we have `unquote`
    # the form_action_value
    start = invitation_link.index("=") + 1
    invite_key = invitation_link[start:]
    headers = {"Referer": invitation_link}
    data = {
        "csrfmiddlewaretoken": csrf_middleware_token,
        "invite_key": invite_key,
    }

    return make_request(
        Method.POST,
        invitation_link,
        session=session,
        headers=headers,
        data=data,
    )
