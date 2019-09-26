# -*- coding: utf-8 -*-
"""Profile - Edit Company's Online Profiles page"""
import logging
import random
import re

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.generic import assertion_msg
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Edit online profiles"
TYPE = PageType.FORM
URL = URLs.PROFILE_COMPANY_EDIT_SOCIAL_MEDIA.absolute
EXPECTED_STRINGS = [
    "Online profiles",
    "URL for your Facebook company page (optional):",
    "URL for your LinkedIn company profile (optional):",
    "URL for your Twitter company profile (optional):",
    "Use a full web address (URL) including http:// or https://",
    "Save and continue",
    "Back",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Edit Online Profiles page")


def go_to(session: Session) -> Response:
    """Go to "Edit Company's Online Profiles" page.

    This requires:
     * Supplier to be logged in
    """
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def update_profiles(
    actor: Actor,
    company: Company,
    *,
    facebook=True,
    linkedin=True,
    twitter=True,
    specific_facebook=None,
    specific_linkedin=None,
    specific_twitter=None,
) -> (Response, Company):
    """Change Company's Sector of Interest.

    NOTE:
    If any of `specific_*` arguments is set to an empty string, then this will
    remove existing link.
    """
    session = actor.session
    clean_name = re.sub('[|&"-_;# ]', "", company.title.lower())
    random_number = random.randint(9999, 999999999)
    profile_suffix = f"{clean_name}-{random_number}"

    fake_facebook = f"http://facebook.com/{profile_suffix}"
    fake_linkedin = f"http://linkedin.com/{profile_suffix}"
    fake_twitter = f"http://twitter.com/{profile_suffix}"

    if facebook:
        new_facebook = (
            specific_facebook if specific_facebook is not None else fake_facebook
        )
    else:
        new_facebook = company.facebook

    if linkedin:
        new_linkedin = (
            specific_linkedin if specific_linkedin is not None else fake_linkedin
        )
    else:
        new_linkedin = company.linkedin

    if twitter:
        new_twitter = specific_twitter if specific_twitter is not None else fake_twitter
    else:
        new_twitter = company.twitter

    headers = {"Referer": URL}
    data = {
        "facebook_url": new_facebook,
        "linkedin_url": new_linkedin,
        "twitter_url": new_twitter,
    }

    new_details = Company(
        facebook=new_facebook, linkedin=new_linkedin, twitter=new_twitter
    )

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )

    return response, new_details


def should_see_errors(
    response: Response, *, facebook=True, linkedin=True, twitter=True
):
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
    actor: Actor, company: Company, *, facebook=False, linkedin=False, twitter=False
) -> Response:
    """Remove links to all existing Online Profiles."""
    response, _ = update_profiles(
        actor,
        company,
        facebook=facebook,
        linkedin=linkedin,
        twitter=twitter,
        specific_facebook="",
        specific_linkedin="",
        specific_twitter="",
    )
    return response
