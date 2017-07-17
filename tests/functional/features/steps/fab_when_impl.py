# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random
from urllib.parse import quote, unquote

from behave.runner import Context
from behave.model import Table
from faker import Factory
from jsonschema import validate
from requests.models import Response
from scrapy.selector import Selector

from tests import get_absolute_url
from tests.functional.features.context_utils import Company
from tests.functional.features.pages import (
    fab_ui_edit_details,
    fab_ui_edit_online_profiles,
    fab_ui_edit_sector
)
from tests.functional.features.pages.common import DETAILS, PROFILES
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
    extract_logo_url,
    get_absolute_path_of_file,
    get_md5_hash_of_file,
    get_verification_code,
    make_request
)
from tests.functional.schemas.Companies import COMPANIES
from tests.settings import EXPORT_STATUSES, NO_OF_EMPLOYEES, SECTORS


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
    :return: an Company named tuple
    :rtype: test.functional.features.ScenarioData.Company
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
    company = Company(
        alias=alias, title=json[0]["title"].strip(),
        number=json[0]["company_number"], companies_house_details=json[0])
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
    context.add_company(company)

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
    expected = ["Create your company’s profile", escaped_company_title,
                company.number]
    check_response(response, 200, body_contains=expected)
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
    company = context.get_company(alias)
    url = ("{}?company_number={}"
           .format(get_absolute_url('ui-buyer:register-confirm-company'),
                   company.number))
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": token,
            "enrolment_view-current_step": "company",
            "company-company_name": company.title,
            "company-company_number": company.number,
            "company-company_address":
                company.companies_house_details["address_snippet"]}

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
    expected = ["Your company's previous exports"]
    check_response(response, 200, body_contains=expected)
    logging.debug("Confirmed selection of Company: %s", company.number)

    # Now, we've landed on the Export Status page, so we have extract the
    # csrfmiddlewaretoken from the response content
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def reg_supplier_is_not_ready_to_export(context, supplier_alias):
    """Supplier decides that her/his company is not ready to export.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    export_status = "NO_INTENTION"
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
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
    check_response(response, 200)


def submit_export_status_form(context, supplier_alias, export_status):
    """Submit the Export Status form.

    NOTE:
    This won't run any assertions once the last request is made, it's because
    that there are 2 possible results depending whether Supplier already has
    a SSO/great.gov.uk account or not.
    Moreover the last response will be stored in `context.response`, which can
    be used in further verification.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param export_status: any export status that allows Suppliers to create
                          a Directory profile.
    :type  export_status: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
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
    make_request(Method.GET, url, session=session, params=params,
                 headers=headers, allow_redirects=False, context=context)


def supplier_should_get_to_build_your_profile(context, supplier_alias):
    """Assert last response based on the fact that Supplier has
    a SSO/great.gov.uk account

    NOTE:
    Will use `context.response` to assert the contents of last response.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company_alias = actor.company_alias
    session = actor.session
    response = context.response
    check_response(response, 302, location="/company-profile/edit")
    assert response.cookies.get("sessionid") is not None
    logging.debug("Confirmed Export Status of '%s'. We're now going to the "
                  "FAB edit company profile page.", company_alias)

    # GET FAB /company-profile/edit
    url = get_absolute_url("ui-buyer:company-edit")
    headers = {
        "Referer":
            get_absolute_url("ui-buyer:register-confirm-export-status")
    }
    response = make_request(Method.GET, url, session=session,
                            headers=headers, context=context)
    expected = ["Build and improve your profile"]
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully got to Build your Profile page")


def supplier_should_get_to_sso_registration_page(
        context, supplier_alias, export_status):
    """Assert last response based on the fact that Supplier doesn't have
    a SSO/great.gov.uk account

    NOTE:
    Will use `context.response` to assert the contents of last response.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param export_status: any export status that allows Suppliers to create
                          a Directory profile.
    :type  export_status: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    company_alias = actor.company_alias
    session = actor.session
    response = context.response
    referer = get_absolute_url("ui-buyer:register-confirm-export-status")
    url = get_absolute_url("ui-buyer:register-submit-account-details")
    # assert last response based on the fact that Supplier doesn't have
    # a SSO account
    next_1 = quote("{}?export_status={}&company_number={}"
                   .format(url, export_status, company.number))
    location_1 = "{}?next={}".format(get_absolute_url("sso:signup"), next_1)
    next_2 = quote("{}?company_number={}&export_status={}"
                   .format(url, company.number, export_status))
    location_2 = "{}?next={}".format(get_absolute_url("sso:signup"), next_2)
    locations = [location_1, location_2]
    check_response(response, 302, locations=locations)
    logging.debug("Confirmed Export Status of '%s'. We're now going to the "
                  "SSO signup page.", company_alias)

    # GET SSO /accounts/signup/?next=...
    url = get_absolute_url("sso:signup")
    params = {"next": next_1}
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, context=context)
    expected = ["Create a great.gov.uk account and you can"]
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully landed on SSO signup page")

    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def reg_confirm_export_status(context, supplier_alias, export_status):
    """Will confirm the current export status of selected unregistered company.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param export_status: current Export Status of selected company
    :type export_status: str
    """
    export_status = EXPORT_STATUSES[export_status]
    context.export_status = export_status
    has_sso_account = context.get_actor(supplier_alias).has_sso_account

    submit_export_status_form(context, supplier_alias, export_status)

    if has_sso_account:
        logging.debug("Supplier already has a SSO account")
        supplier_should_get_to_build_your_profile(context, supplier_alias)
    else:
        logging.debug("Supplier doesn't have a SSO account")
        supplier_should_get_to_sso_registration_page(
            context, supplier_alias, export_status)


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
    company = context.get_company(alias)
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
    actor = context.get_actor(supplier_alias)
    session = actor.session
    confirmation_link = actor.email_confirmation_link
    assert confirmation_link, "Expected a non-empty email confirmation link"
    response = make_request(Method.GET, confirmation_link, session=session,
                            context=context)
    expected = ["Confirm email Address"]
    unexpected = ["This e-mail confirmation link expired or is invalid"]
    check_response(response, 200, body_contains=expected,
                   unexpected_strings=unexpected)
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
    expected = ["Build and improve your profile"]
    check_response(response, 200, body_contains=expected)
    context.set_actor_has_sso_account(supplier_alias, True)


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
    company = context.get_company(actor.company_alias)
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
    expected = ["Your company sector",
                "What sector is your company interested in working in?"]
    expected += SECTORS
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on the Select Sector page")
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def bp_extract_company_address_details(response: Response):
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
    expected = [
        "We need to send a letter containing a verification code ",
        "Your company address", "Full name", "Address line 1", "Address line 2",
        "City", "Country", "Postcode", "PO box"
    ]
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on the Your company address page")
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    details = bp_extract_company_address_details(response)
    context.set_company_details(actor.company_alias, address_details=details)


def bp_provide_full_name(context, supplier_alias):
    """Build Profile - Provide Supplier's full name, which will be use when
    sending verification letter.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    details = company.address_details
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
    expected = [
        actor.alias, "Thank you",
        "The letter will be sent to your registered business address",
        "You can change the name of the person who will receive this letter",
    ]
    check_response(response, 200, body_contains=expected)
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
    expected = [msg, "We've sent your verification letter"]
    check_response(response, 200, body_contains=expected)
    logging.debug("Supplier is on the We've sent your verification letter page")

    # STEP 2 - Click on the "View or amend your company profile" link
    # use previous url as the referer link
    referer = url
    url = get_absolute_url("ui-buyer:company-profile")
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    expected = [
        "Your company has no description.", "Set your description",
        "Your profile can't be published until your company has a",
    ]
    check_response(response, 200, body_contains=expected)
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
    expected = [
        "About your company", "Describe your business to overseas buyers",
        "Brief summary to make your company stand out to buyers"
    ]
    check_response(response, 200, body_contains=expected)
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
    company = context.get_company(actor.company_alias)

    # STEP 0 - get the verification code from DB
    verification_code = get_verification_code(company.number)

    # STEP 1 - go to the "Set Company Description" page
    actor = context.get_actor(supplier_alias)
    session = actor.session
    url = get_absolute_url("ui-buyer:confirm-company-address")
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    expected = [
        "Verify your company",
        ("Enter the verification code from the letter we sent to you after  "
         "you created your company profile"),
        ("We sent you a letter through the mail containing a twelve digit "
         "code.")]
    check_response(response, 200, body_contains=expected)
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
    expected = [
        "Your company has been verified",
        "View or amend your company profile"
    ]
    check_response(response, 200, body_contains=expected)

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
    """Whilst being of FAB company profile page it will `click` on
    the `View published profile` link.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)

    # STEP 1 - go to the "View published profile" page
    url = "{}/{}".format(get_absolute_url("ui-supplier:suppliers"),
                         company.number)
    response = make_request(Method.GET, url, session=session,
                            allow_redirects=False, context=context)
    location = "/suppliers/{}/".format(company.number)
    check_response(response, 301, location_starts_with=location)

    # STEP 2 - follow the redirect from last response
    url = "{}{}".format(get_absolute_url("ui-supplier:landing"),
                        response.headers.get("Location"))
    response = make_request(Method.GET, url, session=session,
                            allow_redirects=False, context=context)
    check_response(response, 200, body_contains=[company.number])
    logging.debug("Supplier is on the company's FAS page")


def prof_attempt_to_sign_in_to_fab(context, supplier_alias):
    """Try to sign in to FAB as a Supplier without verified email address.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    # Step 1 - Get to the Sign In page
    url = get_absolute_url("sso:login")
    params = {"next": fab_landing}
    headers = {"Referer": fab_landing}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = []
    check_response(response, 200, body_contains=expected)
    assert response.cookies.get("sso_display_logged_in") == "false"
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 2 - submit the login form
    url = get_absolute_url("sso:login")
    data = {"next": fab_landing,
            "csrfmiddlewaretoken": token,
            "login": actor.email,
            "password": actor.password,
            "remember": "on"}
    # Referer is the same as the final URL from the previous request
    referer = response.request.url
    headers = {"Referer": referer}
    response = make_request(Method.POST, url, session=session, data=data,
                            headers=headers, allow_redirects=False,
                            context=context)
    location = "/accounts/confirm-email/"
    check_response(response, 302, location=location)
    cookies = response.cookies
    assert cookies.get("sso_display_logged_in") == "false"
    assert cookies.get("directory_sso_dev_session") is not None
    # extra check - validate the cookie Domain
    assert "sso_display_logged_in" in cookies.get_dict(domain='.uktrade.io')
    assert "directory_sso_dev_session" in cookies.get_dict(domain='.uktrade.io')

    # Step 3 - follow the redirect
    url = get_absolute_url("sso:email_confirm")
    # Referer is the same as in the previous request
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    check_response(response, 200)


def prof_sign_out_from_fab(context, supplier_alias):
    """Sign out from Find a Buyer.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    # Step 1 - Get to the Sign Out confirmation page
    url = get_absolute_url("sso:logout")
    params = {"next": fab_landing}
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = ["Sign out", "Are you sure you want to sign out?"]
    check_response(response, 200, body_contains=expected)
    assert response.cookies.get("sso_display_logged_in") == "true"
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 2 - log out
    url = get_absolute_url("sso:logout")
    data = {"csrfmiddlewaretoken": token,
            "next": fab_landing}
    # Referer header is the final URL of the previous request
    referer = response.request.url
    headers = {"Referer": referer}
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, allow_redirects=False, context=context)
    check_response(response, 302, location=fab_landing)
    assert response.cookies.get("sso_display_logged_in") == "false"
    # It looks like `requests` is ignoring empty cookies, so to check whether
    # `directory_sso_dev_session` was unset, we have to check
    # the "Set-Cookie" header
    cookies_hdr = response.headers.get("Set-Cookie")
    assert 'directory_sso_dev_session="\\"\\"";' in cookies_hdr

    # Step 3 - follow the redirect to FAB's landing page
    url = response.headers.get("Location")
    # Referer header is the same one as in the previous request
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = ["Find a Buyer - GREAT.gov.uk", "Get promoted internationally",
                "with a great.gov.uk trade profile",
                "Enter your Companies House number"]
    check_response(response, 200, body_contains=expected)
    assert "sso_display_logged_in" not in response.cookies
    assert "directory_sso_dev_session" not in response.cookies


def prof_sign_in_to_fab(context, supplier_alias):
    """Sign in to Find a Buyer.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    fab_landing = get_absolute_url("ui-buyer:landing")

    # Step 1 - Get to the Sign In page
    url = get_absolute_url("sso:login")
    params = {"next": fab_landing}
    headers = {"Referer": fab_landing}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = []
    check_response(response, 200, body_contains=expected)
    assert response.cookies.get("sso_display_logged_in") == "false"
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)

    # Step 2 - submit the login form
    url = get_absolute_url("sso:login")
    data = {"next": fab_landing,
            "csrfmiddlewaretoken": token,
            "login": actor.email,
            "password": actor.password,
            "remember": "on"}
    # Referer is the same as the final URL from the previous request
    referer = response.request.url
    headers = {"Referer": referer}
    response = make_request(Method.POST, url, session=session, data=data,
                            headers=headers, allow_redirects=False,
                            context=context)
    check_response(response, 302, location=fab_landing)
    cookies = response.cookies
    assert cookies.get("sso_display_logged_in") == "true"
    assert cookies.get("directory_sso_dev_session") is not None
    # extra check - validate the cookie Domain
    assert "sso_display_logged_in" in cookies.get_dict(domain='.uktrade.io')
    assert "directory_sso_dev_session" in cookies.get_dict(domain='.uktrade.io')

    # Step 3 - follow the redirect
    url = fab_landing
    # Referer is the same as in the previous request
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    check_response(response, 302, location="/company-profile")
    assert "sso_display_logged_in" not in response.cookies
    assert "directory_sso_dev_session" not in response.cookies

    # Step 4 - go the company profile page
    url = get_absolute_url("ui-buyer:company-profile")
    # Referer is the same as the final URL from the previous request
    referer = response.request.url
    headers = {"Referer": referer}
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    check_response(response, 200)
    assert "sso_display_logged_in" not in response.cookies
    assert "directory_sso_dev_session" not in response.cookies


def reg_create_standalone_sso_account(context, supplier_alias):
    """Will create a standalone SSO/great.gov.uk account.

    NOTE:
    There will be no association between this account and any company.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1: Go to the SSO/great.gov.uk registration page
    url = get_absolute_url("sso:signup")
    headers = {"Referer": get_absolute_url("ui-buyer:landing")}
    response = make_request(Method.GET, url, session=session,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = ["Register", "Create a great.gov.uk account and you can",
                "gain access to worldwide exporting opportunities",
                "promote your business to international buyers",
                "Email:", "Confirm email:", "Password:", "Confirm password:",
                "Tick this box to accept the", "of the great.gov.uk service."]
    check_response(response, 200, body_contains=expected)
    assert response.cookies.get("sso_display_logged_in") == "false"

    # Step 2: POST SSO accounts/signup/
    url = get_absolute_url("sso:signup")
    headers = {"Referer": url}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "email": actor.email,
            "email2": actor.email,
            "password1": actor.password,
            "password2": actor.password,
            "terms_agreed": "on"
            }
    response = make_request(Method.POST, url, session=session,
                            headers=headers, data=data,
                            allow_redirects=False, context=context)
    check_response(response, 302, location="/accounts/confirm-email/")
    assert response.cookies.get("sso_display_logged_in") == "false"
    assert response.cookies.get("directory_sso_dev_session") is not None

    # Steps 3: GET SSO /accounts/confirm-email/
    url = get_absolute_url("sso:email_confirm")
    response = make_request(Method.GET, url, session=session,
                            headers=headers, allow_redirects=False,
                            context=context)
    expected = ["Verify your email address"]
    check_response(response, 200, body_contains=expected)
    assert response.cookies.get("sso_display_logged_in") == "false"


def sso_supplier_confirms_email_address(context, supplier_alias):
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
    assert "%2Fabout%2F" in new_location
    check_response(response, 302)

    # Step 2 - Follow redirect - go to
    # SSO_HOST/accounts/login/?next=https://SSO_HOST/about/
    # use the same Referer as in previous request
    headers = {"Referer": referer}
    url = "{}{}".format(get_absolute_url("sso:landing"), new_location)
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    new_location = response.headers.get("Location")
    expected_locations = [get_absolute_url("profile:about"),
                          get_absolute_url("profile:about")
                          .replace("http://", "https://")]
    check_response(response, 302, locations=expected_locations)
    assert response.cookies.get("sso_display_logged_in") == "true"

    # Step 3 - Follow the redirect - go to PROFILE /about
    # use the same Referer as in previous request
    headers = {"Referer": referer}
    url = unquote(new_location)
    response = make_request(Method.GET, url, session=session, headers=headers,
                            context=context)
    expected = ["Welcome to your great.gov.uk profile"]
    check_response(response, 200, body_contains=expected)
    context.set_actor_has_sso_account(supplier_alias, True)


def sso_go_to_create_trade_profile(context, supplier_alias):
    """Follow the 'Create a trade profile' button on the "Find a Buyer" tab.

    NOTE:
    It's assumed that Supplier already has a standalone SSO/great.gov.uk account

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Step 1 - Go to "Find a Buyer" tab
    headers = {"Referer": get_absolute_url("profile:about")}
    url = get_absolute_url("profile:fab")
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    expected = ["Get a trade profile", "Create a trade profile",
                "Get a trade profile for your company and you can:",
                "generate new sales leads",
                "promote your business to thousands of overseas buyers",
                ("add case studies of your best work to make your company "
                 "stand out"),
                ("have buyers contact your sales team directly to get deals "
                 "moving"),
                ]
    check_response(response, 200, body_contains=expected)

    # Step 2 - Click on "Create a trade profile" button
    url = get_absolute_url("ui-buyer:landing")
    response = make_request(Method.GET, url, session=session,
                            allow_redirects=False, context=context)
    expected = ["Get promoted internationally",
                "with a great.gov.uk trade profile",
                "Connect directly with international buyers"
                ]
    check_response(response, 200, body_contains=expected)


def prof_go_to_edit_logo_page(context, supplier_alias):
    """Go to the 'Upload your company's logo' page & extract CSRF token.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    # Go to "Upload your company's logo" page
    headers = {"Referer": get_absolute_url("ui-buyer:company-profile")}
    url = get_absolute_url("ui-buyer:upload-logo")
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    expected = ["Upload your company's logo", "Logo:", "Upload file",
                ("For best results this should be a transparent PNG file of "
                 "600 x 600 pixels and no more than 2MB")
                ]
    check_response(response, 200, body_contains=expected)
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def prof_upload_logo(context, supplier_alias, picture: str):
    """Upload Company's logo & extract newly uploaded logo image URL.

    NOTE:
    picture must represent file stored in ./tests/functional/files

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param picture: name of the picture file stored in ./tests/functional/files
    :type  picture: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    company = context.get_company(actor.company_alias)
    filename = get_absolute_path_of_file(picture)

    # Upload company's logo
    headers = {"Referer": get_absolute_url("ui-buyer:upload-logo")}
    url = get_absolute_url("ui-buyer:upload-logo")
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "supplier_company_profile_logo_edit_view-current_step": "logo",
            }
    with open(filename, "rb") as f:
        picture = f.read()
    files = {"logo-logo": picture}
    response = make_request(
        Method.POST, url, session=session, headers=headers, data=data,
        files=files, allow_redirects=False, context=context)
    check_response(response, 302, location="/company-profile")
    assert response.cookies.get("sessionid") is not None

    # Follow the redirect
    headers = {"Referer": get_absolute_url("ui-buyer:upload-logo")}
    url = get_absolute_url("ui-buyer:company-profile")
    response = make_request(Method.GET, url, session=session, headers=headers,
                            allow_redirects=False, context=context)
    expected = ["Your company is published"]
    check_response(response, 200, body_contains=expected)

    logging.debug("Successfully uploaded logo picture: %s", picture)

    # Keep logo details in Company's scenario data
    logo_url = extract_logo_url(response)
    md5_hash = get_md5_hash_of_file(filename)
    context.set_company_logo_detail(
        company.alias, picture=picture, hash=md5_hash, url=logo_url)


def prof_upload_unsupported_file_as_logo(context, supplier_alias, file):
    """Try to upload unsupported file type as Company's logo.

    NOTE:
    file must exist in ./tests/functional/files

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param file: name of the file stored in ./tests/functional/files
    :type  file: str
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    filename = get_absolute_path_of_file(file)

    logging.debug("Attempting to upload %s as company logo", filename)
    # Try to upload a file of unsupported type as company's logo
    headers = {"Referer": get_absolute_url("ui-buyer:upload-logo")}
    url = get_absolute_url("ui-buyer:upload-logo")
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "supplier_company_profile_logo_edit_view-current_step": "logo",
            }
    with open(filename, "rb") as f:
        picture = f.read()
    files = {"logo-logo": picture}
    response = make_request(Method.POST, url, session=session, headers=headers,
                            data=data, files=files,
                            allow_redirects=False, context=context)

    content = response.content.decode("utf-8")
    # There are 2 different error message that you can get, depending of the
    # type of uploaded file.
    # Here, we're checking if `any` of these 2 message is visible.
    error_messages = ["Invalid image format, allowed formats: PNG, JPG, JPEG",
                      ("Upload a valid image. The file you uploaded was either "
                       "not an image or a corrupted image.")]
    has_error = any([message in content for message in error_messages])
    is_200 = response.status_code == 200
    if is_200 and has_error:
        logging.debug("%s was rejected", file)
    else:
        logging.error("%s was accepted", file)

    return is_200 and has_error


def prof_supplier_uploads_logo(context, supplier_alias, picture):
    """Upload a picture and set it as Company's logo.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param picture: name of the picture file stored in ./tests/functional/files
    """
    prof_go_to_edit_logo_page(context, supplier_alias)
    prof_upload_logo(context, supplier_alias, picture)


def prof_to_upload_unsupported_logos(context, supplier_alias, table):
    """Upload a picture and set it as Company's logo.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type supplier_alias: str
    :param table: context.table containing data table
                  see: https://pythonhosted.org/behave/gherkin.html#table
    """
    files = [row['file'] for row in table]
    rejections = []
    for file in files:
        prof_go_to_edit_logo_page(context, supplier_alias)
        rejected = prof_upload_unsupported_file_as_logo(context, supplier_alias, file)
        rejections.append(rejected)
    context.rejections = rejections


def prof_update_company_details(context, supplier_alias, table_of_details):
    """Update selected Company's details.

    NOTE:
    `table_of_details` contains names of details to update.
    Passing `table_of_details` can be avoided as we already have access to
    `context` object, yet in order to be more explicit, we're making it
    a mandatory argument.

    :param table_of_details: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
    """
    details_to_update = [row["detail"] for row in table_of_details]

    title = DETAILS["TITLE"] in details_to_update
    keywords = DETAILS["KEYWORDS"] in details_to_update
    website = DETAILS["WEBSITE"] in details_to_update
    size = DETAILS["SIZE"] in details_to_update
    sector = DETAILS["SECTOR"] in details_to_update

    fab_ui_edit_details.go_to(context, supplier_alias)
    fab_ui_edit_details.update_details(context, supplier_alias,
                                       title=title, keywords=keywords,
                                       website=website, size=size)
    fab_ui_edit_sector.update_sector(context, supplier_alias, update=sector)


def prof_add_online_profiles(context, supplier_alias, online_profiles):
    """Update links to Company's Online Profiles.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param online_profiles: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
    """
    profiles = [row["online profile"] for row in online_profiles]
    facebook = PROFILES["FACEBOOK"] in profiles
    linkedin = PROFILES["LINKEDIN"] in profiles
    twitter = PROFILES["TWITTER"] in profiles
    fab_ui_edit_online_profiles.go_to(context, supplier_alias)
    fab_ui_edit_online_profiles.update_profiles(
        context, supplier_alias, facebook=facebook, linkedin=linkedin,
        twitter=twitter)


def prof_add_invalid_online_profiles(
        context: Context, supplier_alias: str, online_profiles: Table):
    """Attempt to update links to Company's Online Profiles using invalid URLs.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param online_profiles: context.table containing data table
            see: https://pythonhosted.org/behave/gherkin.html#table
    """
    facebook = False
    linkedin = False
    twitter = False
    facebook_url = "http://notfacebook.com"
    linkedin_url = "http://notlinkedin.com"
    twitter_url = "http://nottwitter.com"
    for row in online_profiles:
        if row["online profile"] == PROFILES["FACEBOOK"]:
            facebook = True
            facebook_url = row.get("invalid link", facebook_url)
        if row["online profile"] == PROFILES["LINKEDIN"]:
            linkedin = True
            linkedin_url = row.get("invalid link", linkedin_url)
        if row["online profile"] == PROFILES["TWITTER"]:
            twitter = True
            twitter_url = row.get("invalid link", twitter_url)
    fab_ui_edit_online_profiles.go_to(context, supplier_alias)
    logging.debug(
        "Will use following invalid URLs to Online Profiles: %s %s %s",
        facebook_url if facebook else "", linkedin_url if linkedin else "",
        twitter_url if twitter else "")
    fab_ui_edit_online_profiles.update_profiles(
        context, supplier_alias, facebook=facebook, linkedin=linkedin,
        twitter=twitter, specific_facebook=facebook_url,
        specific_linkedin=linkedin_url, specific_twitter=twitter_url)


def prof_remove_links_to_online_profiles(context, supplier_alias):
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)

    facebook = True if company.facebook else False
    linkedin = True if company.linkedin else False
    twitter = True if company.twitter else False

    fab_ui_edit_online_profiles.remove_links(
        context, supplier_alias, facebook=facebook, linkedin=linkedin,
        twitter=twitter)
