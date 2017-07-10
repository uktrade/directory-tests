# -*- coding: utf-8 -*-
"""FAB - Edit Company's Online Profiles page"""
import logging
import random

from faker import Factory

from tests import get_absolute_url
from tests.functional.features.pages import fab_ui_profile
from tests.functional.features.pages.utils import (
    extract_and_set_csrf_middleware_token
)
from tests.functional.features.utils import Method, check_response, make_request

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
FAKE = Factory.create()


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Edit Online Profiles page")


def go_to(context, supplier_alias):
    """Go to "Edit Company's Online Profiles" page.

    This requires:
     * Supplier to be logged in

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, URL, session=session, headers=headers,
                            allow_redirects=False, context=context)

    should_be_here(response)
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)
    logging.debug("%s is on the Edit Company's Online Profiles page",
                  supplier_alias)


def update_profiles(
        context, supplier_alias, *, facebook=True, linkedin=True, twitter=True,
        specific_facebook=None, specific_linkedin=None, specific_twitter=None):
    """Change Company's Sector of Interest.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param facebook: change Facebook URL if True, or use the current one if False
    :param linkedin: change LinkedIn URL if True, or use the current one if False
    :param twitter: change Twitter URL if True, or use the current one if False
    :param specific_facebook: use specific Facebook URL
    :param specific_linkedin: use specific LinkedIn URL
    :param specific_twitter: use specific Twitter URL
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    fake_fb = "http://facebook.com/{}".format(random.randint(9999, 999999999))
    fake_li = "http://linkedin.com/{}".format(random.randint(9999, 999999999))
    fake_tw = "http://twitter.com/{}".format(random.randint(9999, 999999999))
    new_facebook = specific_facebook or fake_fb if facebook else company.facebook
    new_linkedin = specific_linkedin or fake_li if linkedin else company.linkedin
    new_twitter = specific_twitter or fake_tw if twitter else company.twitter

    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": token,
            "supplier_company_social_links_edit_view-current_step": "social",
            "social-facebook_url": new_facebook,
            "social-linkedin_url": new_linkedin,
            "social-twitter_url": new_twitter
            }

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=True, context=context)

    fab_ui_profile.should_be_here(response)
    context.set_company_details(company.alias, facebook=new_facebook,
                                linkedin=new_linkedin, twitter=new_twitter)
    logging.debug("%s set Company's Online Profile links to: Facebook=%s, "
                  "LinkedId=%s, Twitter=%s", supplier_alias, new_facebook,
                  new_linkedin, new_twitter)


def update_profiles_w_invalid_urls(
        context, supplier_alias, *, facebook=True, linkedin=True, twitter=True,
        specific_facebook=None, specific_linkedin=None, specific_twitter=None):
    """Try to change Company's Online profiled using invalid URLs.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param facebook: change Facebook URL if True, or use the current one if False
    :param linkedin: change LinkedIn URL if True, or use the current one if False
    :param twitter: change Twitter URL if True, or use the current one if False
    :param specific_facebook: use specific Facebook URL
    :param specific_linkedin: use specific LinkedIn URL
    :param specific_twitter: use specific Twitter URL
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken

    fake = "http://{}".format(FAKE.domain_name())
    new_facebook = specific_facebook or fake if facebook else company.facebook
    new_linkedin = specific_linkedin or fake if linkedin else company.linkedin
    new_twitter = specific_twitter or fake if twitter else company.twitter

    headers = {"Referer": URL}
    data = {"csrfmiddlewaretoken": token,
            "supplier_company_social_links_edit_view-current_step": "social",
            "social-facebook_url": new_facebook,
            "social-linkedin_url": new_linkedin,
            "social-twitter_url": new_twitter
            }

    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, allow_redirects=True, context=context)
    # check whether we're still on the same page
    should_be_here(response)


def should_see_errors(context, supplier_alias, *, facebook=True, linkedin=True,
                      twitter=True):
    """Check if all required errors are visible.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param facebook: check for a Facebook URL error if True, or not if False
    :param linkedin: check for a LinkedIn URL error if True, or not if False
    :param twitter: check for a Twitter URL error if True, or not if False
    """
    content = context.response.content.decode("utf-8")
    if facebook:
        assert "Please provide a link to Facebook." in content
    if linkedin:
        assert "Please provide a link to LinkedIn." in content
    if twitter:
        assert "Please provide a link to Twitter." in content
    logging.debug("%s was not able to set Company's Online Profile links using"
                  " invalid URLs to: %s %s %s",
                  supplier_alias, "Facebook" if facebook else "",
                  "LinkedIn" if linkedin else "", "Twitter" if twitter else "")
