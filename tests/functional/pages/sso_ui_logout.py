# -*- coding: utf-8 -*-
"""SSO - Logout page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("sso:logout")
EXPECTED_STRINGS = [
    "Sign out", "Are you sure you want to sign out?"
]


def go_to(session: Session, *, next_param: str = None) -> Response:
    """Go to the SSO Logout page.

    :param session: Supplier session object
    :param next_param: (optional) URL to redirect to after successful login
    :return: response object
    """
    fab_landing = get_absolute_url("ui-buyer:landing")
    params = {"next": next_param or fab_landing}
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(
        Method.GET, URL, session=session, params=params, headers=headers)
    return response


def should_be_here(response: Response):
    """Check if Supplier is on SSO logout page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO logout page")


def logout(session: Session, token: str, *, next_param: str = None) -> Response:
    """Sign out from SSO/FAB.

    :param session: Supplier session object
    :param token: CSRF token required to submit the login form
    :param next_param: (optional) URL to redirect to after logging out
    :return: response object
    """
    fab_landing = get_absolute_url("ui-buyer:landing")
    data = {
        "csrfmiddlewaretoken": token,
        "next": next_param or fab_landing
    }
    query = "?next={}".format(URL, fab_landing)
    headers = {"Referer": urljoin(URL, query)}
    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response
