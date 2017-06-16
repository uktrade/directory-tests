# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random
from urllib.parse import quote

import requests
from jsonschema import validate

from tests import get_absolute_url
from tests.functional.features.ScenarioData import UnregisteredCompany
from tests.functional.features.utils import make_request
from tests.functional.features.utils import Method
from tests.functional.schemas import COMPANIES


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
    json = response.json()
    logging.debug("Company House Search result: {}".format(json))
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
        logging.debug("Found a company without a FAS profile: {}. Getting "
                      "it details...".format(random_company_number))

        response, json = search_company_house(random_company_number)

        if len(json) == 1:
            exists = True
            if json[0]["company_status"] == "active":
                active = True
                assert json[0]["company_number"] == random_company_number, (
                    "Expected to get details of company no.: {} but got {}"
                        .format(random_company_number, json[0]["company_number"]))
            else:
                counter += 1
                has_profile, exists, active = True, False, False
                logging.debug("Company with number {} is not active. It's {}. "
                              "Trying a different one..."
                              .format(random_company_number,
                                      json[0]["company_status"]))
        else:
            counter += 1
            has_profile, exists, active = True, False, False
            logging.debug("Company with number {} does not exist. Trying a "
                          "different one...".format(random_company_number))

    logging.debug("It took {} attempt(s) to find an active Company without a "
                  "FAS profile: {} - {}".format(counter,
                                                json[0]["title"],
                                                json[0]["company_number"]))
    company = UnregisteredCompany(alias, json[0]["title"].strip(),
                                  json[0]["company_number"], json[0])
    return company


def select_random_company(context, supplier_alias, alias):
    """Will try to find an active company that doesn't have a FAS profile.

    Steps (repeat until successful):
        1 - generate a random Companies House Number
        2 - check if there's a FAS profile for it
        3 - check if such company is registered with Companies House & is active

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
                            allow_redirects=False)
    assert response.status_code == 302
    exp_location = "/register/company?company_number={}".format(company.number)
    assert response.headers.get("Location") == exp_location
    logging.debug("Successfully selected company {} - {} for registration"
                  .format(company.title, company.number))

    # go to the Confirm Company page
    url = get_absolute_url('ui-buyer:register-confirm-company')
    headers = {"Referer": get_absolute_url('ui-buyer:landing')}
    params = {"company_number": company.number}
    response = make_request(Method.GET, url, session=session, params=params,
                            headers=headers)
    assert response.status_code == 200
    assert "Create your company’s profile" in response.content.decode("utf-8")
    assert company.title in response.content.decode("utf-8")
    assert company.number in response.content.decode("utf-8")
    logging.debug("Successfully got to the Confirm your Company page")


def confirm_company_selection(context, alias):
    """Will confirm that the selected company is the right one.

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
    """
    company = context.get_unregistered_company(alias)
    url_confirm = get_absolute_url('ui-buyer:register-confirm-company')
    params = {"company_number": company.number}
    response = requests.get(url=url_confirm, params=params)
    assert response.status_code == 200
    error_msg = "Company not found. Please check the number."
    error_idx = response.content.decode("utf-8").find(error_msg)
    assert error_idx == -1, ("Response contains an error '{}':\n{}"
                             .format(error_msg, response.content))
    logging.debug("Confirmed selection of Company: {}".format(company.number))

    # Once on the "Confirm Company" page, we have to go to the
    # "Confirm Export Status" page with "Referer" header set to this page
    url_export = get_absolute_url('ui-buyer:register-confirm-export-status')
    headers = {"Referer": "{}?company_number={}".format(url_confirm,
                                                        company.number)}
    response = requests.get(url=url_export, headers=headers)
    assert response.status_code == 200
    logging.debug("Confirmed selection of Company: {}".format(company.number))


def confirm_export_status(context, supplier_alias, alias, export_status):
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
    company = context.get_unregistered_company(alias)
    url = get_absolute_url('sso:signup')
    next_param = ("{}/register-submit?company_number={}&export_status={}"
                  .format(DIRECTORY_SSO_URL, company.number, export_status))
    params = {"next": quote(next_param)}
    response = make_request(Method.GET, url, session=session, params=params)
    assert response.status_code == 200
    logging.debug("Confirmed Export Status of '{}'. We're now on SSO signup "
                  "page.".format(alias))

    content = response.content.decode("utf-8")
    csrf_tag_idx = content.find("name='csrfmiddlewaretoken'")
    value_property = "value='"
    logging.debug("Looking for csrfmiddlewaretoken in: {}"
                  .format(content[csrf_tag_idx:csrf_tag_idx + 150]))
    csrf_token_idx = content.find(value_property, csrf_tag_idx, csrf_tag_idx + 60)
    csrf_token_end_idx = content.find("'", csrf_token_idx + len(value_property), csrf_tag_idx + 150)
    token = content[(csrf_token_idx+len(value_property)):csrf_token_end_idx]
    logging.debug("Found csrfmiddlewaretoken={}".format(token))
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
    context.export_status = export_status


def create_sso_account_for_selected_company(context, supplier_alias, alias):
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
    next_url = get_absolute_url("ui-buyer:register-submit-account-details")
    # Encode `next` URL
    next_link = quote("{}?company_number={}&export_status={}"
                      .format(next_url, company.number, export_status))

    url_signup = get_absolute_url("sso:signup")
    headers = {"Referer": "{}?next={}".format(url_signup,
                                              next_link)}
    cookies = {"sso_display_logged_in": "false"}
    data = {"csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
            "email": actor.email,
            "email2": actor.email,
            "password1": actor.password,
            "password2": actor.password,
            "terms_agreed": "on",
            "next": next_link}
    response = make_request(Method.POST, url_signup, session=session,
                            headers=headers, cookies=cookies, data=data)
    context.response = response

