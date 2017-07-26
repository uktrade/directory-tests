# -*- coding: utf-8 -*-
"""Common page helpers"""
import logging
import random
from random import choice

from behave.runner import Context
from faker import Factory
from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import CaseStudy, Company
from tests.functional.features.pages import int_api_ch_search
from tests.functional.features.utils import (
    Method,
    extract_csrf_middleware_token,
    make_request
)
from tests.settings import SECTORS, JPEGs, JPGs, PNGs

FAKE = Factory.create()


def extract_and_set_csrf_middleware_token(
        context: Context, response: Response, supplier_alias: str):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param response: request with HTML content containing CSRF middleware token
    """
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def random_case_study_data(alias: str) -> CaseStudy:
    """Return a CaseStudy populated with randomly generated details.

    :param alias: alias of the Case Study
    :return: a CaseStudy namedtuple
    """
    images = PNGs + JPGs + JPEGs
    (title, summary, description, caption_1, caption_2, caption_3, testimonial,
     source_name, source_job, source_company) = (
        FAKE.sentence()[:60].strip() for _ in range(10))
    sector = choice(SECTORS)
    website = "http://{}/fake-case-study-url".format(FAKE.domain_name())
    keywords = ", ".join(FAKE.sentence().replace(".", "").split())
    image_1, image_2, image_3 = (choice(images) for _ in range(3))

    case_study = CaseStudy(
        alias=alias, title=title, summary=summary, description=description,
        sector=sector, website=website, keywords=keywords, image_1=image_1,
        image_2=image_2, image_3=image_3, caption_1=caption_1,
        caption_2=caption_2, caption_3=caption_3, testimonial=testimonial,
        source_name=source_name, source_job=source_job,
        source_company=source_company)

    return case_study


def find_active_company_without_fas_profile(alias: str) -> Company:
    """Will find an active company without a FAS profile.

    :param alias: alias that will be given to the found company
    :return: an Company named tuple
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

        json = int_api_ch_search.search(random_company_number)

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
        number=json[0]["company_number"], companies_house_details=json[0],
        case_studies={})
    return company


def has_fas_profile(company_number: str) -> bool:
    """Will check if company has an active FAS profile.

    It will do it by calling FAS /suppliers/{} UI endpoint. This endpoint
    returns:
     - 404 Not Found when there's no profile for selected company
     - and 301 with Location header pointing at the profile page

    :param company_number: Companies House number (8 digit long number padded
                                                   with zeroes)
    :return: True/False based on the presence of FAS profile
    """
    endpoint = get_absolute_url('ui-supplier:suppliers')
    url = "{}/{}".format(endpoint, company_number)
    response = make_request(Method.GET, url, allow_redirects=False)
    return response.status_code == 301
