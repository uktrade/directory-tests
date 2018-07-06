# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
from requests import Response
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Welcome to your great.gov.uk profile",
    (
        "From now on, every time you sign in you’ll be able to quickly access all"
        " of our exporting tools in one place. The tools are here to help your "
        "business succeed internationally."
    ),
    (
        "You can start using any of our exporting tools by clicking on the tabs "
        "on your profile."
    ),
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def should_be_logged_out(response: Response):
    """Check if Supplier is logged out by checking the cookies."""
    with assertion_msg(
        "Found sso_display_logged_in cookie in the response. Maybe user is"
        " still logged in?"
    ):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
        "Found directory_sso_dev_session cookie in the response. Maybe "
        "user is still logged in?"
    ):
        assert "directory_sso_dev_session" not in response.cookies
