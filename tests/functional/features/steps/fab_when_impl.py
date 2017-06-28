# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random
from urllib.parse import quote, unquote

from faker import Factory
from jsonschema import validate
from requests.models import Response
from scrapy.selector import Selector

from tests import get_absolute_url
from tests.functional.features.context_utils import UnregisteredCompany
from tests.functional.features.settings import NO_OF_EMPLOYEES, SECTORS
from tests.functional.features.steps.fab_then_impl import (
    prof_should_be_on_profile_page,
    prof_should_be_told_that_company_is_not_verified_yet,
    prof_should_be_told_that_company_is_published
)
from tests.functional.features.utils import (
    Method,
    check_response,
    extract_confirm_email_form_action,
    extract_csrf_middleware_token,
    get_verification_code,
    make_request
)
from tests.functional.schemas.Companies import COMPANIES


def has_fas_profile(company_number):
    """Will check if company has an active FAS profile.

    It will do it by calling FAS /suppliers/{} UI endpoint. This endpoint
    returns:
     - 404 Not Found when there's no profile for selected company
     - and 301 with Location header pointing at the profile page

    :param company_number: Companies House number (8 digit long number padded
                                                   with zeroes)
    :type: str
    :return: True/False based on the presence of FAS profile
    :rtype bool
    """
    endpoint = get_absolute_url('ui-supplier:suppliers')
    url = "{}/{}".format(endpoint, company_number)
    response = make_request(Method.GET, url, allow_redirects=False)
    return response.status_code == 301


def search_company_house(term):
    """Will search for companies using provided term.

    NOTE:
    This will validate the response data against appropriate JSON Schema.

    :param term: search term, can be: company name or number, keywords etc.
    :type term: str
    :return: a tuple consisting of raw Requests response & response JSON
    :rtype: tuple
    """
    url = get_absolute_url('internal-api:companies-house-search')
    params = {"term": term}
    response = make_request(Method.GET, url, params=params,
                            allow_redirects=False)
    assert response.status_code == 200, (
        "Expected 200 but got {}. In case you're getting 301 Redirect then "
        "check if you're using correct protocol https or http"
        .format(response.status_code))
    json = response.json()
    logging.debug("Company House Search result: %s", json)
    validate(json, COMPANIES)
    return response, response.json()


def find_active_company_without_fas_profile(alias):
    """Will find an active company without a FAS profile.

    :param alias: alias that will be given to the found company
    :return: an UnregisteredCompany named tuple
    :rtype: test.functional.features.ScenarioData.UnregisteredCompany
    """
    has_profile = True
    exists = False
    active = False
    counter = 1
    while has_profile and not exists and not active:
        random_company_number = str(random.randint(0, 9999999)).zfill(8)
        has_profile = has_fas_profile(random_company_number)
        logging.debug("Found a company without a FAS profile: %s. Getting "
                      "it details...", random_company_number)

        _, json = search_company_house(random_company_number)

        if len(json) == 1:
            exists = True
            if json[0]["company_status"] == "active":
                active = True
                assert json[0]["company_number"] == random_company_number, (
                    "Expected to get details of company no.: %s but got %s",
                    random_company_number, json[0]["company_number"])
            else:
                counter += 1
                has_profile, exists, active = True, False, False
                logging.debug("Company with number %s is not active. It's %s. "
                              "Trying a different one...",
                              random_company_number, json[0]["company_status"])
        else:
            counter += 1
            has_profile, exists, active = True, False, False
            logging.debug("Company with number %s does not exist. Trying a "
                          "different one...", random_company_number)

    logging.debug("It took %s attempt(s) to find an active Company without a "
                  "FAS profile: %s - %s", counter, json[0]["title"],
                  json[0]["company_number"])
    company = UnregisteredCompany(alias=alias,
                                  title=json[0]["title"].strip(),
                                  number=json[0]["company_number"],
                                  details=json[0],
                                  summary=None,
                                  description=None)
    return company


def select_random_company(context, supplier_alias, alias):
    """Will try to find an active company that doesn't have a FAS profile.

    Steps (repeat until successful):
        1 - generate a random Companies House Number
        2 - check if there's a FAS profile for it
        3 - check if such company is registered at Companies House & is active

    Once a matching company is found, then it's data will be stored in:
        context.scenario_data.unregistered_companies[]

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    """
    company = find_active_company_without_fas_profile(alias)
    context.add_unregistered_company(company)

    # Once we have company's details, we can select it for registration
    session = context.get_actor(supplier_alias).session
    url = get_absolute_url('ui-buyer:landing')
    data = {"company_name": company.title, "company_number": company.number}
    response = make_request(Method.POST, url, session=session,
                            headers={"Referer": url}, data=data,
                            allow_redirects=True, context=context)
    html_escape_table = {"&": "&amp;", "'": "&#39;"}
    escaped_company_title = "".join(html_escape_table.get(c, c) for c in
                                    company.title.upper())
    exp_strings = ["Create your company’s profile", escaped_company_title,
                   company.number]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Successfully got to the Confirm your Company page")

    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    context.set_company_for_actor(supplier_alias, alias)


def reg_confirm_company_selection(context, supplier_alias, alias):
    """Will confirm that the selected company is the right one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    """
    actor = context.get_actor(supplier_alias)
    token = actor.csrfmiddlewaretoken
    session = actor.session
    company = context.get_unregistered_company(alias)
    url = ("{}?company_number={}"
           .format(get_absolute_url('ui-buyer:register-confirm-company'),
                   company.number))
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": token,
            "enrolment_view-current_step": "company",
            "company-company_name": company.title,
            "company-company_number": company.number,
            "company-company_address": company.details["address_snippet"]}

    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    check_response(response, 302, location="/register/exports")
    logging.debug("Confirmed selection of Company: %s", company.number)

    # Once on the "Confirm Company" page, we have to go to the
    # "Confirm Export Status" page with "Referer" header set to this page
    url_export = get_absolute_url('ui-buyer:register-confirm-export-status')
    headers = {"Referer": url}
    response = make_request(Method.GET, url_export, session=session,
                            headers=headers, context=context)
    exp_strings = ["Your company's previous exports"]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Confirmed selection of Company: %s", company.number)

    # Now, we've landed on the Export Status page, so we have extract the
    # csrfmiddlewaretoken from the response content
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def reg_confirm_export_status(context, supplier_alias, alias, export_status):
    """Will confirm the current export status of selected unregistered company.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    :param export_status: current Export Status of selected company
    :type export_status: str
    """
    if export_status == "Yes, in the last year":
        export_status = "YES"
    elif export_status == "Yes, 1 to 2 years ago":
        export_status = "ONE_TWO_YEARS_AGO"
    elif export_status == "Yes, but more than 2 years ago":
        export_status = "OVER_TWO_YEARS_AGO"
    elif export_status == "No, but we are preparing to":
        export_status = "NOT_YET"
    elif export_status == "No, we are not planning to sell overseas":
        export_status = "NO_INTENTION"
    else:
        raise LookupError("Could not recognize provided Export Status: {}"
                          .format(export_status))
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    company = context.get_unregistered_company(alias)

    referer = get_absolute_url("ui-buyer:register-confirm-export-status")

    # Step 1: POST /register/exports
    url = get_absolute_url("ui-buyer:register-confirm-export-status")
    headers = {"Referer": referer}
    data = {"csrfmiddlewaretoken": token,
            "enrolment_view-current_step": "exports",
            "exports-export_status": export_status,
            "exports-terms_agreed": "on"}
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    check_response(response, 302, location="/register/finished")

    # Step 2: GET /register/finished
    url = get_absolute_url("ui-buyer:register-finish")
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    location = ("/register-submit?company_number={}&export_status={}"
                .format(company.number, export_status))
    check_response(response, 302, location=location)

    # Step 3: GET /register-submit?company_number={}&export_status={}
    url = get_absolute_url("ui-buyer:register-submit-account-details")
    params = {"company_number": company.number,
              "export_status": export_status}
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, allow_redirects=False,
                            context=context)
    next_1 = quote("{}?export_status={}&company_number={}"
                   .format(url, export_status, company.number))
    location_1 = "{}?next={}".format(get_absolute_url("sso:signup"), next_1)
    next_2 = quote("{}?company_number={}&export_status={}"
                   .format(url, company.number, export_status))
    location_2 = "{}?next={}".format(get_absolute_url("sso:signup"), next_2)
    locations = [location_1, location_2]
    check_response(response, 302, locations=locations)
    logging.debug("Confirmed Export Status of '%s'. We're now going to the "
                  "SSO signup page.", alias)

    # Step 4: GET SSO /accounts/signup/?next=...
    # don't use FAB UI Cookies
    url = get_absolute_url("sso:signup")
    params = {"next": next_1}
    headers = {"Referer": referer}
    # context.reset_actor_session(supplier_alias)
    session = context.get_actor(supplier_alias).session
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, context=context)
    exp_strings = ["Create a great.gov.uk account and you can"]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Successfully landed on SSO signup page")

    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    context.export_status = export_status


def reg_create_sso_account(context, supplier_alias, alias):
    """Will create a SSO account for selected company.

    NOTE:
    Will use credentials randomly generated at Actor's initialization.
    It will also store final response in `context`

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_unregistered_company(alias)
    export_status = context.export_status
    # Step 1: POST SSO accounts/signup/
    next_url = get_absolute_url("ui-buyer:register-submit-account-details")
    next_link = quote("{}?company_number={}&export_status={}"
                      .format(next_url, company.number, export_status))
    url_signup = get_absolute_url("sso:signup")
    headers = {"Referer": "{}?next={}".format(url_signup,
                                              next_link)}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "email": actor.email,
            "email2": actor.email,
            "password1": actor.password,
            "password2": actor.password,
            "terms_agreed": "on",
            "next": next_link}
    response = make_request(Method.POST, url_signup, session=session,
                            headers=headers, data=data,
                            allow_redirects=False, context=context)
    check_response(response, 302, location="/accounts/confirm-email/")

    # Steps 2: GET SSO /accounts/confirm-email/
    url = get_absolute_url("sso:email_confirm")
    response = make_request(Method.GET, url, session=session,
                            headers=headers, allow_redirects=False,
                            context=context)
    check_response(response, 200)


def reg_open_email_confirmation_link(context, supplier_alias):
    """Given Supplier has received a message with email confirmation link
    Then Supplier has to click on that link.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    # context.reset_actor_session(supplier_alias)
    actor = context.get_actor(supplier_alias)
    session = actor.session
    confirmation_link = actor.email_confirmation_link
    assert confirmation_link, "Expected a non-empty email confirmation link"
    response = make_request(Method.GET, confirmation_link, session=session,
                            context=context)
    exp_strings = ["Confirm email Address"]
    unexp_strings = ["This e-mail confirmation link expired or is invalid"]
    check_response(response, 200, strings=exp_strings,
                   unexp_strings=unexp_strings)
    logging.debug("Supplier is on the Confirm your email address page")

    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    form_action_value = extract_confirm_email_form_action(response)
    context.form_action_value = form_action_value


def reg_supplier_confirms_email_address(context, supplier_alias):
    """Given Supplier has clicked on the email confirmation link, Suppliers has
    to confirm that the provided email address is the correct one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    # STEP 1 - Submit "Confirm your email address" form
    actor = context.get_actor(supplier_alias)
    session = actor.session
    csrfmiddlewaretoken = actor.csrfmiddlewaretoken
    form_action_value = context.form_action_value
    url = "{}{}".format(get_absolute_url("sso:landing"), form_action_value)
    referer = actor.email_confirmation_link
    headers = {"Referer": referer}
    data = {"csrfmiddlewaretoken": csrfmiddlewaretoken}
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    new_location = response.headers.get("Location")
    assert new_location.startswith("/accounts/login/?next=")
    assert "register-submit%253Fcompany_number%253D" in new_location
    check_response(response, 302)

    # Step 2 - Follow redirect - go to SSO /accounts/login/
    # use the same Referer as in previous request
    headers = {"Referer": referer}
    url = "{}{}".format(get_absolute_url("sso:landing"), new_location)
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    new_location = response.headers.get("Location")
    register_submit = get_absolute_url("ui-buyer:register-submit-account-details")
    assert new_location.startswith(quote(register_submit)), (
        "Expected new Location to start with: '{}' but got '{}'"
        .format(register_submit, new_location))
    assert "company_number" in new_location
    assert "export_status" in new_location
    check_response(response, 302)

    # Step 3 - Follow redirect - go to DIR /company-profile/edit
    # use the same Referer as in previous request
    headers = {"Referer": referer}
    url = unquote(new_location)
    response = make_request(Method.GET, url, session=session, headers=headers,
                            context=context)
    exp_strings = ["Build and improve your profile"]
    check_response(response, 200, strings=exp_strings)


def bp_provide_company_details(context, supplier_alias):
    """Build Profile - Provide company details: website (optional), keywords
    and number of employees.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    fake = Factory.create()
    actor = context.get_actor(supplier_alias)
    company = context.get_unregistered_company(actor.company_alias)
    session = actor.session
    csrfmiddlewaretoken = actor.csrfmiddlewaretoken
    url = get_absolute_url("ui-buyer:company-edit")
    headers = {"Referer": url}
    employees = random.choice(NO_OF_EMPLOYEES)
    website = "https://{}".format(fake.domain_name())
    keywords = ", ".join(fake.sentence().replace(".", "").split())
    data = {"csrfmiddlewaretoken": csrfmiddlewaretoken,
            "supplier_company_profile_edit_view-current_step": "basic",
            "basic-name": company.title,
            "basic-website": website,
            "basic-keywords": keywords,
            "basic-employees": employees}
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    exp_strings = ["Your company sector",
                   "What sector is your company interested in working in?"]
    exp_strings += SECTORS
    check_response(response, 200, strings=exp_strings)
    logging.debug("Supplier is on the Select Sector page")
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def bp_extract_company_details(response: Response):
    """Build Profile - extract company details from Your company address page

    :param response: requests response
    :type  response: requests.models.Response
    :return: named tuple containing all extracted company details
    """
    assert response.content, "Response has no content"
    content = response.content.decode("utf-8")

    from collections import namedtuple

    Details = namedtuple("Details", ["address_signature", "address_line_1",
                                     "address_line_2", "locality", "country",
                                     "postal_code", "po_box"])

    def extract(selector):
        res = Selector(text=content).css(selector).extract()
        return res[0] if len(res) > 0 else ""

    address_signature = extract("#id_address-signature::attr(value)")
    address_line_1 = extract("#id_address-address_line_1::attr(value)")
    address_line_2 = extract("#id_address-address_line_2::attr(value)")
    locality = extract("#id_address-locality::attr(value)")
    country = extract("#id_address-country::attr(value)")
    postal_code = extract("#id_address-postal_code::attr(value)")
    po_box = extract("#id_address-po_box::attr(value)")

    details = Details(address_signature, address_line_1, address_line_2,
                      locality, country, postal_code, po_box)

    logging.debug("Extracted company details: %s", details)
    return details


def bp_select_random_sector(context, supplier_alias):
    """Build Profile - Randomly select one of available sectors our company is
    interested in working in.

    NOTE:
    This will set `context.details` which will contain company details extracted
    from the page displayed after Supplier selects the sector.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    csrfmiddlewaretoken = actor.csrfmiddlewaretoken
    url = get_absolute_url("ui-buyer:company-edit")
    headers = {"Referer": url}
    sector = random.choice(SECTORS)
    data = {"csrfmiddlewaretoken": csrfmiddlewaretoken,
            "supplier_company_profile_edit_view-current_step": "classification",
            "classification-sectors": sector,
            }
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    exp_strings = [
        "We need to send a letter containing a verification code ",
        "Your company address", "Full name", "Address line 1", "Address line 2",
        "City", "Country", "Postcode", "PO box"
    ]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Supplier is on the Your company address page")
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    context.details = bp_extract_company_details(response)


def bp_provide_full_name(context, supplier_alias):
    """Build Profile - Provide Supplier's full name, which will be use when
    sending verification letter.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    details = context.details
    session = actor.session
    csrfmiddlewaretoken = actor.csrfmiddlewaretoken
    url = get_absolute_url("ui-buyer:company-edit")
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": csrfmiddlewaretoken,
            "supplier_company_profile_edit_view-current_step": "address",
            "address-signature": details.address_signature,
            "address-postal_full_name": actor.alias,
            "address-address_line_1": details.address_line_1,
            "address-address_line_2": details.address_line_2,
            "address-locality": details.locality,
            "address-country": details.country,
            "address-postal_code": details.postal_code,
            "address-po_box": details.po_box
            }
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    exp_strings = [
        actor.alias, "Thank you",
        "The letter will be sent to your registered business address",
        "You can change the name of the person who will receive this letter",
    ]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Supplier is on the Thank You page")
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def bp_confirm_registration_and_send_letter(context, supplier_alias):
    """Build Profile - Supplier has to finally confirm registration and is
    informed about verification letter.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    # STEP 1 - Confirm registration
    actor = context.get_actor(supplier_alias)
    session = actor.session
    csrfmiddlewaretoken = actor.csrfmiddlewaretoken
    url = get_absolute_url("ui-buyer:company-edit")
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": csrfmiddlewaretoken,
            "supplier_company_profile_edit_view-current_step": "confirm"
            }
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    msg = ("You should receive your verification letter within a week. When you"
           " receive the letter, please log in to GREAT.gov.uk to enter your "
           "verification profile to publish your company profile.")
    exp_strings = [msg, "We've sent your verification letter"]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Supplier is on the We've sent your verification letter page")

    # STEP 2 - Click on the "View or amend your company profile" link
    # use previous url as the referer link
    referer = url
    url = get_absolute_url("ui-buyer:company-profile")
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    exp_strings = [
        "Your company has no description.", "Set your description",
        "Your profile can't be published until your company has a",
    ]
    check_response(response, 200, strings=exp_strings)
    logging.debug("Supplier is on the Edit Company Profile page")


def prof_set_company_description(context, supplier_alias):
    """Edit Profile - Will set company description.

    This is quasi-mandatory (*) step before Supplier can verify the company with
    the code sent in a letter.

    (*) it's quasi mandatory, because Supplier can actually go to the company
    verification page using the link provided in the letter without the need
    to set company description.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    # STEP 1 - go to the "Set Company Description" page
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = get_absolute_url("ui-buyer:company-edit-description")
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    exp_strings = [
        "About your company", "Describe your business to overseas buyers",
        "Brief summary to make your company stand out to buyers"
    ]
    check_response(response, 200, strings=exp_strings)
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    logging.debug("Supplier is on the Set Company Description page")

    # STEP 2 - Submit company description
    fake = Factory.create()
    url = get_absolute_url("ui-buyer:company-edit-description")
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    summary = fake.sentence()
    description = fake.sentence()
    data = {"csrfmiddlewaretoken": token,
            "supplier_company_description_edit_view-current_step": "description",
            "description-summary": summary,
            "description-description": description
            }
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    check_response(response, 302, location="/company-profile")
    context.set_company_description(actor.company_alias, summary, description)

    # STEP 3 - follow the redirect
    url = get_absolute_url("ui-buyer:company-profile")
    headers = {"Referer": get_absolute_url("ui-buyer:company-edit-description")}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    check_response(response, 200)
    prof_should_be_on_profile_page(context, supplier_alias)
    prof_should_be_told_that_company_is_not_verified_yet(context, supplier_alias)
    logging.debug("Supplier is back to the Profile Page")


def prof_verify_company(context, supplier_alias):
    """Will verify the company by submitting the verification code that is sent
    by post to the company's address.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_unregistered_company(actor.company_alias)

    # STEP 0 - get the verification code from DB
    verification_code = get_verification_code(company.number)

    # STEP 1 - go to the "Set Company Description" page
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = get_absolute_url("ui-buyer:confirm-company-address")
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    exp_strings = [
        "Verify your company",
        ("Enter the verification code from the letter we sent to you after  "
         "you created your company profile"),
        ("We sent you a letter through the mail containing a twelve digit "
         "code.")]
    check_response(response, 200, strings=exp_strings)
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    logging.debug("Supplier is on the Verify Company page")

    # STEP 2 - Submit the verification code
    url = get_absolute_url("ui-buyer:confirm-company-address")
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    data = {"csrfmiddlewaretoken": token,
            "supplier_company_address_verification_view-current_step": "address",
            "address-code": verification_code
            }
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    exp_strings = [
        "Your con has re verified",
        "View or amend your company profile"
    ]
    check_response(response, 200, strings=exp_strings)

    # STEP 3 - click on the "View or amend your company profile" link
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = get_absolute_url("ui-buyer:company-profile")
    headers = {"Referer": get_absolute_url("ui-buyer:confirm-company-address")}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    check_response(response, 200)
    prof_should_be_on_profile_page(context, supplier_alias)
    prof_should_be_told_that_company_is_published(context, supplier_alias)
    logging.debug("%s is on the Verified & Published Company Profile page",
                  supplier_alias)


def prof_view_published_profile(context, supplier_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_unregistered_company(actor.company_alias)

    # STEP 1 - go to the "View published profile" page
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = "{}/{}".format(get_absolute_url("ui-supplier:suppliers"), company.number)
    response = make_request(Method.GET, url, session=session,
                            allow_redirects=False, context=context)
    location = "/suppliers/{}/".format(company.number)
    check_response(response, 301, location=location)

    # STEP 2 - follow the redirect from last response
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = "{}{}".format(get_absolute_url("ui-supplier:landing"),
                        response.headers.get("Location"))
    response = make_request(Method.GET, url, session=session,
                            allow_redirects=False, context=context)
    check_response(response, 200, strings=[company.number])
    logging.debug("Supplier is on the company's FAS page")
