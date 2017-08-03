# -*- coding: utf-8 -*-
"""FAB - Edit Company's Online Profiles page"""
import logging
import random

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import Actor, Company
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    check_response,
    make_request
)

URL = get_absolute_url("ui-buyer:company-edit-social-media")
EXPECTED_STRINGS = [
    "Add your social media pages",
    "URL for your LinkedIn company profile (optional):",
    "Use a full web address (URL) including http:// or https://",
    "URL for your Twitter company profile (optional):",
    "Use a full web address (URL) including http:// or https://",
    "URL for your Facebook company page (optional):",
    "Use a full web address (URL) including http:// or https://",
    "Save", "Cancel"
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Edit Online Profiles page")


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Online Profiles" page.

    This requires:
     * Supplier to be logged in

    :param session: Supplier session object
    :return: response object
    """
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, URL, session=session, headers=headers)
    should_be_here(response)
    return response


def update_profiles(
        actor: Actor, company: Company, *, facebook=True, linkedin=True,
        twitter=True, specific_facebook=None, specific_linkedin=None,
        specific_twitter=None) -> (Response, Company):
    """Change Company's Sector of Interest.

    NOTE:
    If any of `specific_*` arguments is set to an empty string, then this will
    remove existing link.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :param facebook: change Facebook URL if True, or use the current one if False
    :param linkedin: change LinkedIn URL if True, or use the current one if False
    :param twitter: change Twitter URL if True, or use the current one if False
    :param specific_facebook: use specific Facebook URL
    :param specific_linkedin: use specific LinkedIn URL
    :param specific_twitter: use specific Twitter URL
    :return: a tuple consisting of a Response object & a namedtuple with Company
             details used in the update request.
    """
    session = actor.session
    token = actor.csrfmiddlewaretoken

    fake_fb = "http://facebook.com/{}".format(random.randint(9999, 999999999))
    fake_li = "http://linkedin.com/{}".format(random.randint(9999, 999999999))
    fake_tw = "http://twitter.com/{}".format(random.randint(9999, 999999999))

    if facebook:
        new_fb = specific_facebook if specific_facebook is not None else fake_fb
    else:
        new_fb = company.facebook

    if linkedin:
        new_li = specific_linkedin if specific_linkedin is not None else fake_li
    else:
        new_li = company.linkedin

    if twitter:
        new_tw = specific_twitter if specific_twitter is not None else fake_tw
    else:
        new_tw = company.twitter

    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": token,
        "company_social_links_edit_view-current_step": "social",
        "social-facebook_url": new_fb,
        "social-linkedin_url": new_li,
        "social-twitter_url": new_tw
    }

    new_details = Company(facebook=new_fb, linkedin=new_li, twitter=new_tw)

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response, new_details


def should_see_errors(
        response: Response, *, facebook=True, linkedin=True, twitter=True):
    """Check if all required errors are visible.

    :param response: a Response object
    :param facebook: check for a Facebook URL error if True, or not if False
    :param linkedin: check for a LinkedIn URL error if True, or not if False
    :param twitter: check for a Twitter URL error if True, or not if False
    """
    content = response.content.decode("utf-8")
    if facebook:
        with assertion_msg("Could't find link to Facebook profile"):
            assert "Please provide a link to Facebook." in content
    if linkedin:
        with assertion_msg("Could't find link to LinkedIn profile"):
            assert "Please provide a link to LinkedIn." in content
    if twitter:
        with assertion_msg("Could't find link to Twitter profile"):
            assert "Please provide a link to Twitter." in content


def remove_links(
        actor: Actor, company: Company, *, facebook=False, linkedin=False,
        twitter=False) -> Response:
    """Remove links to all existing Online Profiles.

    :param actor: a namedtuple with Actor details
    :param company: a namedtuple with Company details
    :param facebook: remove link to Facebook profile if True, or not if False
    :param linkedin: remove link to LinkedIn profile if True, or not if False
    :param twitter: remove link to Twitter profile if True, or not if False
    :return: a Response object
    """
    response, _ = update_profiles(
        actor, company, facebook=facebook, linkedin=linkedin,
        twitter=twitter, specific_facebook="", specific_linkedin="",
        specific_twitter="")
    return response
