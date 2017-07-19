# -*- coding: utf-8 -*-
"""FAB - Build and improve your profile page"""
import logging

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:company-edit")
EXPECTED_STRINGS = [
    "Thank you", "Basic", "Industries", "Address", "Confirm",
    "The letter will be sent to your registered business address",
    "You can change the name of the person who will receive this letter",
    "< Back to previous step", "Send"
]


def should_be_here(response: Response):
    """Check if Supplier is on FAB Build your profile - Confirm page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the FAB Build your profile - Confirm page")


def submit(session: Session, token: str) -> Response:
    """Build Profile - Supplier has to finally confirm registration and is
    informed about verification letter.

    :param session: Supplier session object
    :param token: CSRF token required to submit the form
    :return: response object
    """
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": token,
        "supplier_company_profile_edit_view-current_step": "confirm"
    }
    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response
