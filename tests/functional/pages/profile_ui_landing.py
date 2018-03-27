# -*- coding: utf-8 -*-
"""SSO - Verify your email page"""
from requests import Response
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Welcome to your great.gov.uk profile",
    ("From now on, every time you sign in you’ll be able to quickly access all "
     "of our exporting tools in one place. The tools are here to help your "
     "business succeed internationally."),
    ("You can start using any of our exporting tools by clicking on the tabs on"
     " your profile."), "Export opportunities", "Find a buyer",
    "Selling online overseas",
    ("Find thousands of exporting opportunities, search and apply within your "
     "industry or a specific country, and sign up for email alerts so you’re "
     "the first to know of new opportunities."),
    ("Promote your business to overseas buyers with your own trade profile, add"
     " case studies of your company’s best work, and let buyers contact your "
     "sales team directly."),
    ("Join major online marketplaces in other countries and access special "
     "offers negotiated by the Department for International Trade.")
]


def should_be_here(response: Response):
    """Check if Supplier is on SSO landing page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def should_be_logged_out(response: Response):
    """Check if Supplier is logged out by checking the cookies.

    :param response: response object
    """
    with assertion_msg(
            "Found sso_display_logged_in cookie in the response. Maybe user is "
            "still logged in?"):
        assert "sso_display_logged_in" not in response.cookies
    with assertion_msg(
            "Found directory_sso_dev_session cookie in the response. Maybe user"
            " is still logged in?"):
        assert "directory_sso_dev_session" not in response.cookies
