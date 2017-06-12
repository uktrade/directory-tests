# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging
import random

import requests
from jsonschema import validate

from tests import get_absolute_url
from tests.functional.features.ScenarioData import UnregisteredCompany
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
    response = requests.get(url=url, allow_redirects=False)
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
    response = requests.get(url=url, params=params)
    json = response.json()
    logging.debug("Company House Search result: {}".format(json))
    validate(json, COMPANIES)
    return response, response.json()


def select_random_company(context, alias):
    """Will try to find an active company that doesn't have a FAS profile.

    Steps (repeat until successful):
        1 - generate a random Companies House Number
        2 - check if there's a FAS profile for it
        3 - check if such company is registered with Companies House & is active

    Once a matching company is found, then it's data will be stored in:
        context.scenario_data.unregistered_companies[]

    :param context: behave `context` object
    :type context: behave.runner.Context
    :param alias: alias of the company used in the scope of the scenario
    :type alias: str
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

    company_json = json[0]
    logging.debug("It took {} attempt(s) to find an active Company without a "
                  "FAS profile: {} - {}".format(counter,
                                                company_json["title"],
                                                company_json["company_number"]))

    company = UnregisteredCompany(alias, company_json["title"],
                                  company_json["company_number"], company_json)
    context.add_unregistered_company(company)


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

