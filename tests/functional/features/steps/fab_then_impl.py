# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
import logging

from retrying import retry

from tests.functional.features.pages import fab_ui_edit_online_profiles
from tests.functional.features.utils import (
    check_hash_of_remote_file,
    check_response,
    extract_csrf_middleware_token,
    extract_logo_url,
    get_verification_link
)


def reg_sso_account_should_be_created(context, alias):
    """Will verify if SSO account was successfully created.

    It's a very crude check, as it will only check if the response body
    contains selected phrases.

    NOTE:
    It expects that create SSO account response is stored in `context.response`

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the Actor used in the scope of the scenario
    :type alias: str
    """
    response = context.response
    msgs = ["Verify your email address",
            "if you do not receive an email within 10 minutes",
            ("We have sent you a confirmation email. Please follow the link"
             " in the email to verify your email address.")]
    content = response.content.decode("utf-8")
    for msg in msgs:
        err_msg = ("Could not find '{}' in the response".format(msg))
        assert msg in content, err_msg
    logging.debug("Successfully created new SSO account for %s", alias)


@retry(wait_fixed=5000, stop_max_attempt_number=18)
def reg_should_get_verification_email(context, alias, subject):
    """Will check if the Supplier received an email verification message.

    NOTE:
    The check is done by attempting to find a file with the email is Amazon S3.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the Actor used in the scope of the scenario
    :type alias: str
    :param subject: expected subject of the email verification message
    :type  subject: str
    """
    logging.debug("Searching for an email verification message...")
    actor = context.get_actor(alias)
    link = get_verification_link(actor.email)
    context.set_actor_email_confirmation_link(alias, link)


def bp_should_be_prompted_to_build_your_profile(context, supplier_alias):
    content = context.response.content.decode("utf-8")
    assert "Build and improve your profile" in content
    assert "To set up your Find a Buyer profile" in content
    assert "Your company details" in content
    assert "Company name" in content
    assert "Website (optional)" in content
    assert "Enter up to 10 keywords that describe your company" in content
    assert "How many employees are in your company" in content
    logging.debug("%s is on the 'Build and improve your profile' page",
                  supplier_alias)
    token = extract_csrf_middleware_token(context.response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def prof_should_be_on_profile_page(context, supplier_alias):
    content = context.response.content.decode("utf-8")
    assert "Facts &amp; details" in content
    assert "Number of employees" in content
    assert "Registration number" in content
    assert "Company description" in content
    assert "Online profiles" in content
    assert "Recent projects" in content
    assert "+ Add a case study" in content
    assert "Sectors of interest" in content
    assert "Keywords" in content
    logging.debug("%s is on the company profile page", supplier_alias)


def prof_should_be_told_about_missing_description(context, supplier_alias):
    content = context.response.content.decode("utf-8")
    assert "Your company has no description." in content
    assert "Your profile can't be published until your company has a" in content
    assert "Set your description" in content
    logging.debug("%s was told that the company profile has no description",
                  supplier_alias)


def prof_should_be_told_that_company_is_not_verified_yet(context, supplier_alias):
    content = context.response.content.decode("utf-8")
    assert "Your company has not yet been verified." in content
    assert "Your profile can't be published until your company is verified" in content
    assert "Verify your company" in content
    logging.debug("%s was told that the company is not verified yet",
                  supplier_alias)


def prof_should_be_told_that_company_is_published(context, supplier_alias):
    content = context.response.content.decode("utf-8")
    assert "Your company is published" in content
    assert "Your profile is visible to international buyers" in content
    assert "View published profile" in content
    logging.debug("%s was told that the company profile is published",
                  supplier_alias)


def fas_should_be_on_profile_page(context, supplier_alias, company_alias):
    content = context.response.content.decode("utf-8")
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    assert "Contact" in content
    assert "Company description" in content
    assert "Facts &amp; details" in content
    assert "Industries of interest" in content
    assert "Keywords" in content
    assert "Contact company" in content
    assert company.number in content
    assert company.summary in content
    logging.debug("Supplier %s is on the %s company's FAS page",
                  supplier_alias, company_alias)


def reg_supplier_is_not_appropriate_for_fab(context, supplier_alias):
    expected = [
        "Try our other business services",
        "The Find a Buyer service promotes companies that are currently "
        "exporting or looking to export in the near future. The answers you "
        "gave suggest that your company is currently not appropriate to feature"
        " in the Find a Buyer service.",
        "Exporting is GREAT advice for new exporters"
    ]
    check_response(context.response, 200, body_contains=expected)
    logging.debug("%s was told that her/his business is not appropriate "
                  "to feature in the Find a Buyer service", supplier_alias)


def reg_supplier_has_to_verify_email_first(context, supplier_alias):
    expected = ["Verify your email address",
                ("We have sent you a confirmation email. Please follow the link"
                 " in the email to verify your email address."),
                "if you do not receive an email within 10 minutes."]
    check_response(context.response, 200, body_contains=expected)
    logging.debug("%s was told that her/his email address has to be verified "
                  "first before being able to Sign In", supplier_alias)


def sso_should_be_on_landing_page(context, supplier_alias):
    expected = ["Welcome to your great.gov.uk profile",
                ("From now on, every time you sign in you’ll be able to quickly"
                 " access all of our exporting tools in one place. The tools "
                 "are here to help your business succeed internationally."),
                ("You can start using any of our exporting tools by clicking "
                 "on the tabs on your profile."), "Export opportunities",
                "Find a buyer", "Selling online overseas",
                ("Find thousands of exporting opportunities, search and apply "
                 "within your industry or a specific country, and sign up for "
                 "email alerts so you’re the first to know of new "
                 "opportunities."),
                ("Promote your business to overseas buyers with your own trade "
                 "profile, add case studies of your company’s best work, and "
                 "let buyers contact your sales team directly."),
                ("Join major online marketplaces in other countries and access"
                 " special offers negotiated by the Department for "
                 "International Trade.")]
    check_response(context.response, 200, body_contains=expected)
    logging.debug("%s is on the SSO Profile landing page", supplier_alias)


def sso_should_be_signed_in_to_sso_account(context, supplier_alias):
    response = context.response
    assert response.cookies.get("sessionid") is not None
    assert "Sign out" in response.content.decode("utf-8")
    logging.debug("%s is logged in to the SSO account".format(supplier_alias))


def prof_should_be_told_about_invalid_links(context, supplier_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    fab_ui_edit_online_profiles.should_see_errors(
        context, supplier_alias, facebook=facebook, linkedin=linkedin,
        twitter=twitter)


def prof_should_see_logo_picture(context, supplier_alias):
    """Will check if Company's Logo visible on FAB profile page is the same as
    the uploaded one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    logo_url = company.logo_url
    logo_hash = company.logo_hash
    logo_picture = company.logo_picture

    logging.debug("Fetching logo image visible on the %s's FAB profile page",
                  company.title)
    check_hash_of_remote_file(logo_hash, logo_url)
    logging.debug("The Logo visible on the %s's FAB profile page is the same "
                  "as uploaded %s", company.title, logo_picture)


def fas_should_see_logo_picture(context, supplier_alias):
    """Will check if Company's Logo visible on FAS profile page is the same as
    the one uploaded on FAB.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    logo_hash = company.logo_hash
    logo_url = company.logo_url
    logo_picture = company.logo_picture

    # had to do an inline import as there was a problem with circular imports
    from tests.functional.features.steps.fab_when_impl import (
        prof_view_published_profile
    )
    # Go to the FAS profile page & extract the URL of visible logo image
    prof_view_published_profile(context, supplier_alias)
    response = context.response
    visible_logo_url = extract_logo_url(response)

    # Check if FAS shows the correct Logo image
    assert visible_logo_url == logo_url
    logging.debug("Fetching logo image visible on the %s's FAS profile page",
                  company.title)
    check_hash_of_remote_file(logo_hash, logo_url)
    logging.debug("The Logo visible on the %s's FAS profile page is the same "
                  "as uploaded %s", company.title, logo_picture)


def prof_all_unsupported_files_should_be_rejected(context, supplier_alias):
    """Check if all unsupported files were rejected upon upload as company logo.

    NOTE:
    This require `context.rejections` to be set.
    It should be a list of bool values.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    assert hasattr(context, "rejections")
    assert all(context.rejections), (
        "Some of the uploaded files that should be marked as unsupported were "
        "actually accepted. Please check the logs for more details")
    logging.debug("All files of unsupported types uploaded by %s were rejected"
                  .format(supplier_alias))
