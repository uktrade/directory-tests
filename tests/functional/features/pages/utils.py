# -*- coding: utf-8 -*-
"""Common page helpers"""
import json
import logging
import os
import random
from random import choice
from typing import List

from behave.runner import Context
from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import CaseStudy, Company
from tests.functional.features.pages import int_api_ch_search
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    extract_csrf_middleware_token,
    make_request
)
from tests.settings import (
    RARE_WORDS,
    SECTORS,
    TEST_IMAGES_DIR,
    JPEGs,
    JPGs,
    PNGs
)

CompaniesList = List[Company]  # a type hint for a List of Company named tuples


def extract_and_set_csrf_middleware_token(
        context: Context, response: Response, supplier_alias: str):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param response: request with HTML content containing CSRF middleware token
    """
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def sentence(*, max_length: int = 60, min_word_length: int = 9, max_words: int = 10):
    """Generate a random string consisting of rare english words.

    NOTE:
    min_word_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a sentence consisting of rare english words
    """
    words = []
    while len(words) < max_words:
        word = random.choice(RARE_WORDS)
        if len(word) > min_word_length:
            words.append(word)
    while len(" ".join(words)) > max_length:
        words.pop()
    return " ".join(words)


def rare_word(*, min_length: int = 9, max_length: int = 20):
    """Get a random rare english word.

    NOTE:
    min_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a rare english word
    """
    assert min_length < max_length
    word = ""
    while min_length >= len(word) <= max_length:
        word = random.choice(RARE_WORDS)
    return word


def random_case_study_data(alias: str) -> CaseStudy:
    """Return a CaseStudy populated with randomly generated details.

    :param alias: alias of the Case Study
    :return: a CaseStudy namedtuple
    """
    sector = choice(SECTORS)
    images = PNGs + JPGs + JPEGs
    image_1, image_2, image_3 = (choice(images) for _ in range(3))
    (title, summary, description, caption_1, caption_2, caption_3, testimonial,
     source_name, source_job, source_company) = (sentence() for _ in range(10))
    website = "http://{}.{}".format(rare_word(), rare_word())
    keywords = ", ".join(sentence().split())

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
    is_registered = True
    exists = False
    active = False
    counter = 1
    while has_profile and is_registered and not exists and not active:
        random_company_number = str(random.randint(0, 9999999)).zfill(8)
        has_profile = has_fas_profile(random_company_number)
        if has_profile:
            logging.debug("Selected company has a FAS profile: %s. Will try a "
                          "different one.", random_company_number)
        else:
            logging.debug("Found a company without a FAS profile: %s.",
                          random_company_number)
        is_registered = already_registered(random_company_number)
        if is_registered:
            logging.debug("Company %s is already registered with FAB. Will try "
                          "a different one.", random_company_number)
        else:
            logging.debug("Company %s is not registered with FAB: Getting "
                          "it details from CH...", random_company_number)

        json = int_api_ch_search.search(random_company_number)

        if len(json) == 1:
            exists = True
            if json[0]["company_status"] == "active":
                active = True
                with assertion_msg(
                        "Expected to get details of company no.: %s but got %s",
                        random_company_number, json[0]["company_number"]):
                    assert json[0]["company_number"] == random_company_number
            else:
                counter += 1
                has_profile, is_registered, exists, active = True, True, False, False
                logging.debug("Company with number %s is not active. It's %s. "
                              "Trying a different one...",
                              random_company_number, json[0]["company_status"])
        else:
            counter += 1
            has_profile, is_registered, exists, active = True, True, False, False
            logging.debug("Company with number %s does not exist. Trying a "
                          "different one...", random_company_number)

    logging.debug("It took %s attempt(s) to find an active Company without a "
                  "FAS profile and not already registered with FAB: %s - %s",
                  counter, json[0]["title"], json[0]["company_number"])
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


def already_registered(company_number: str) -> bool:
    """Will check if Company is already registered with FAB.

    :param company_number:
    :return: True/False based on the presence of FAB profile
    """
    url = get_absolute_url('ui-buyer:landing')
    data = {"company_number": company_number}
    headers = {"Referer": url}

    response = make_request(Method.POST, url, headers=headers, data=data)
    return "Already registered" in response.content.decode("utf-8")


def get_companies(*, number: int = 100) -> CompaniesList:
    """Find a number of active companies without FAS profile.

    NOTE:
    The search is pretty slow. It takes roughly 10 minutes to find 100 companies

    :param number: (optional) expected number of companies to find
    :return: a list of Company named tuples (all with "test" alias)
    """
    return [find_active_company_without_fas_profile("test") for _ in range(number)]


def save_companies(companies: CompaniesList):
    """Save pre-selected Companies in a JSON file.

    :param companies: a list of named tuples with basic Company details
    """
    # convert `Company` named tuples into dictionaries
    list_dict = []
    for company in companies:
        list_dict.append({key: getattr(company, key) for key in company._fields})

    path = os.path.join(TEST_IMAGES_DIR, 'companies.json')
    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(list_dict, indent=4))


def load_companies() -> CompaniesList:
    """Load stored list of Companies from a JSON file.

    :return: a list of named tuples with basic Company details
    """
    path = os.path.join(TEST_IMAGES_DIR, 'companies.json')
    with open(path, 'r', encoding='utf8') as f:
        companies = json.load(f)
    return [Company(**company) for company in companies]


def escape_html(text: str, *, upper: bool = False) -> str:
    """Escape some of the special characters that are replaced by FAB/SSO.

    :param text: a string to escape
    :param upper: (optional) change to upper case before escaping the characters
    :return: a string with escaped characters
    """
    html_escape_table = {"&": "&amp;", "'": "&#39;"}
    if upper:
        text = text.upper()
    return "".join(html_escape_table.get(c, c) for c in text)


def get_active_company_without_fas_profile(alias: str) -> Company:
    """Randomly select one of predefined companies and set it alias.

    :param alias: alias of the company used withing the scope of the scenario
    :return: a Company named tuple with all basic company details
    """
    company = random.choice(load_companies())._replace(alias=alias)
    logging.debug("Selected company: %s", company)
    return company
