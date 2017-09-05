# -*- coding: utf-8 -*-
"""Common page helpers"""
import json
import logging
import os
import random
import re
from random import choice
from typing import List

import lxml
import requests
from behave.runner import Context
from bs4 import BeautifulSoup
from langdetect import DetectorFactory, detect_langs
from requests import Response

from tests import get_absolute_url
from tests.functional.features.context_utils import (
    CaseStudy,
    Company,
    Feedback,
    Message
)
from tests.functional.features.db_cleanup import (
    delete_supplier_data,
    get_company_email
)
from tests.functional.features.pages import int_api_ch_search
from tests.functional.features.pages.common import FAS_PAGE
from tests.functional.features.utils import (
    Method,
    assertion_msg,
    blue,
    extract_by_css,
    extract_csrf_middleware_token,
    green,
    make_request,
    red
)
from tests.settings import (
    RARE_WORDS,
    SECTORS,
    TEST_IMAGES_DIR,
    JPEGs,
    JPGs,
    PNGs
)

# a type hint for a List of Company named tuples
CompaniesList = List[Company]
# make `langdetect` results deterministic
DetectorFactory.seed = 0
# A dict with currently supported languages on FAS and their short codes
ERROR_INDICATORS = [
    'error', 'errors', 'problem', 'problems', 'fail', 'failed', 'failure',
    'required', 'missing'
]
FAS_SUPPORTED_LANGUAGES = {
    "arabic": "ar",
    "english": "en",
    "chinese": "zh-hans",
    "german": "de",
    "japanese": "ja",
    "portuguese": "pt",
    "portuguese-brazilian": "pt-br",
    "spanish": "es"
}
FAS_PAGE_SELECTORS = {
    "landing": "ui-supplier:landing",
    'industries': 'ui-supplier:industries',
    'search': 'ui-supplier:search',
    'health industry': 'ui-supplier:industries-health',
    'tech industry': 'ui-supplier:industries-tech',
    'creative industry': 'ui-supplier:industries-creative',
    'food-and-drink industry': 'ui-supplier:industries-food',
    'health industry summary': 'ui-supplier:industries-health-summary',
    'tech industry summary': 'ui-supplier:industries-tech-summary',
    'creative industry summary': 'ui-supplier:industries-creative-summary',
    'food-and-drink industry summary': 'ui-supplier:industries-food-summary',
    'terms-and-conditions': 'ui-supplier:terms',
    'privacy-policy': 'ui-supplier:privacy',
}


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
    website = "http://{}.{}".format(rare_word(min_length=15), rare_word())
    keywords = ", ".join(sentence().split())

    case_study = CaseStudy(
        alias=alias, title=title, summary=summary, description=description,
        sector=sector, website=website, keywords=keywords, image_1=image_1,
        image_2=image_2, image_3=image_3, caption_1=caption_1,
        caption_2=caption_2, caption_3=caption_3, testimonial=testimonial,
        source_name=source_name, source_job=source_job,
        source_company=source_company)

    return case_study


def random_feedback_data(
        *, name: str = None, email: str = None, company_name: str = None,
        country: str = None, comment: str = None, terms: str = None) -> Feedback:
    name = name or rare_word(min_length=12)
    email = email or ("test+buyer_{}@directory.uktrade.io"
                      .format(rare_word(min_length=15)))
    company_name = company_name or rare_word(min_length=12)
    country = country or rare_word(min_length=12)
    comment = comment or sentence(max_length=1000)
    terms = terms or "on"

    feedback = Feedback(
        name=name, email=email, company_name=company_name,
        country=country, comment=comment, terms=terms)

    return feedback


def random_message_data(
        *, alias: str = None, body: str = None, company_name: str = None,
        country: str = None, email_address: str = None, full_name: str = None,
        g_recaptcha_response: str = None, sector: str = None,
        subject: str = None, terms: str = None) -> Feedback:
    alias = alias or "test message"
    body = body or sentence(max_length=1000)
    company_name = company_name or rare_word(min_length=12)
    country = country or rare_word(min_length=12)
    email_address = email_address or ("test+buyer_{}@directory.uktrade.io"
                                      .format(rare_word(min_length=15)))
    full_name = full_name or sentence(max_words=2)
    sector = sector or random.choice(SECTORS)
    subject = subject or sentence(max_length=200)
    g_recaptcha_response = g_recaptcha_response or "test mode"
    terms = terms or "on"

    message = Message(
        alias=alias, body=body, company_name=company_name, country=country,
        email_address=email_address, full_name=full_name,
        g_recaptcha_response=g_recaptcha_response, sector=sector,
        subject=subject, terms=terms)

    return message


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


def is_already_registered(response: Response) -> bool:
    """Will check if response contains information that Company is already
    registered with FAB.

    :param response: requests response
    :return: True/False based on the presence of FAB profile
    """
    return "Already registered" in response.content.decode("utf-8")


def is_inactive(response: Response) -> bool:
    """Will check if response contains information that Company is inactive.

    :param response: requests response
    :return: True/False based on the Company's Status in Companies House
    """
    return "Company not active." in response.content.decode("utf-8")


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


def update_companies():
    """Update existing pre-defined list of Companies."""
    companies = load_companies()
    updated_companies = []
    companies_number = len(companies)
    doesnt_exit_counter = 0
    inactive_counter = 0
    registered_counter = 0
    for index, company in enumerate(companies):
        progress_message = ("Updating company {} out of {}: {} - {}".format(
            index + 1, companies_number, company.number, company.title))
        blue(progress_message)
        exists, active, is_registered = False, False, False
        ch_result = int_api_ch_search.search(company.number)
        if len(ch_result) == 1:
            exists = True
            if ch_result[0]["company_status"] == "active":
                active = True
                is_registered = already_registered(company.number)
                if is_registered:
                    registered_counter += 1
                    red("Company is already registered with FAB")
                    blue("Will remove company data from DIR & SSO DBs")
                    email = get_company_email(company.number)
                    delete_supplier_data("DIRECTORY", email)
                    delete_supplier_data("SSO", email)
                    blue("Successfully deleted company data from DIR & SSO DBs")
                    is_registered = False
            else:
                inactive_counter += 1
                red("Company %s - %s is not active any more" % (company.number,
                                                                company.title))
        else:
            doesnt_exit_counter += 1
            red("Company %s - %s does not exist any more" % (company.number,
                                                             company.title))
        if not exists or (exists and not active):
            blue("Searching for a new replacement company")
            new = find_active_company_without_fas_profile("test")
            updated_companies.append(new)
            blue("Found company %s - %s" % (new.number, new.title))

        if exists and active and not is_registered:
            green("Company %s - %s is still active, it's not registered with "
                  "FAB" % (company.number, company.title))
            updated_company = Company(
                alias="test", title=ch_result[0]["title"].strip(),
                number=ch_result[0]["company_number"],
                companies_house_details=ch_result[0],
                case_studies={})
            updated_companies.append(updated_company)

    blue("Number of already registered companies %d" % registered_counter)
    blue("Number of replaced inactive companies %d" % inactive_counter)
    blue("Number of non-existent companies %d" % doesnt_exit_counter)
    green("Saving updated list of companies")
    save_companies(updated_companies)


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


def get_language_code(language: str):
    return FAS_SUPPORTED_LANGUAGES[language.lower()]


def get_fas_page_url(page_name: str, *, language_code: str = None):
    selector = FAS_PAGE_SELECTORS[page_name.lower()]
    url = get_absolute_url(selector)
    if language_code:
        url += "?lang={}".format(language_code)
    return url


def get_fas_page_object(page_name: str):
    if page_name == FAS_PAGE.CREATIVE_INDUSTRY:
        page = FAS_PAGE.CREATIVE_INDUSTRY.po
    elif page_name == FAS_PAGE.FOOD_AND_DRINK_INDUSTRY:
        page = FAS_PAGE.FOOD_AND_DRINK_INDUSTRY.po
    elif page_name == FAS_PAGE.HEALTH_INDUSTRY:
        page = FAS_PAGE.HEALTH_INDUSTRY.po
    elif page_name == FAS_PAGE.TECH_INDUSTRY:
        page = FAS_PAGE.TECH_INDUSTRY.po
    elif page_name == FAS_PAGE.CREATIVE_INDUSTRY_SUMMARY:
        page = FAS_PAGE.CREATIVE_INDUSTRY_SUMMARY.po
    elif page_name == FAS_PAGE.FOOD_AND_DRINK_INDUSTRY_SUMMARY:
        page = FAS_PAGE.FOOD_AND_DRINK_INDUSTRY_SUMMARY.po
    elif page_name == FAS_PAGE.HEALTH_INDUSTRY_SUMMARY:
        page = FAS_PAGE.HEALTH_INDUSTRY_SUMMARY.po
    elif page_name == FAS_PAGE.TECH_INDUSTRY_SUMMARY:
        page = FAS_PAGE.TECH_INDUSTRY_SUMMARY.po
    elif page_name == FAS_PAGE.INDUSTRIES:
        page = FAS_PAGE.INDUSTRIES.po
    else:
        raise KeyError("Unknown FAS page: '{}'".format(page_name))

    return page


def extract_main_error(content: str) -> str:
    """Extract error from page `main` block.

    :param content: a raw HTML content
    :return: error message or None is no error was detected
    """
    soup = BeautifulSoup(content, "lxml")
    sections = soup.find_all('main')
    lines = [
        line.strip().lower()
        for section in sections
        for line in section.text.splitlines()
        if line
    ]
    has_errors = any(
        indicator in line
        for line in lines
        for indicator in ERROR_INDICATORS
    )
    return "\n".join(lines) if has_errors else ""


def extract_section_error(content: str) -> str:
    """Extract error from 'section'.

    :param content: a raw HTML content
    :return: error message or None is no error was detected
    """
    if not content:
        return None
    soup = BeautifulSoup(content, "lxml")
    sections = soup.find_all('section')
    lines = [
        line.strip().lower()
        for section in sections
        for line in section.text.splitlines()
        if line
    ]
    has_errors = any(
        indicator in line
        for line in lines
        for indicator in ERROR_INDICATORS
    )
    return "\n".join(lines) if has_errors else ""


def extract_form_errors(content: str) -> str:
    """Extract form errors if any is present.

    :param content: a raw HTML content
    :return: form error or None is no form error was detected
    """
    if not content:
        return None
    tree = lxml.html.fromstring(content)
    elements = tree.find_class("input-field-container has-error")

    form_errors = ""
    for element in elements:
        string_element = lxml.html.tostring(element).decode("utf-8")
        form_errors += string_element.replace("\t", "").replace("\n\n", "")

    has_errors = any(
        indicator in line.lower()
        for line in form_errors.splitlines()
        for indicator in ERROR_INDICATORS)
    return form_errors if has_errors else ""


def detect_page_language(
        *, url: str = None, content: str = None, main: bool = False,
        rounds: int = 15) -> dict:
    """Detect the language of the page.

    NOTE:
    `langdetect` uses a non-deterministic algorithm. By setting the
    `DetectorFactory.seed` to 0 we can force the library to give consistent
    results.
    In order to ensure that the page language detection is consistent, we can
    run the detection process N times (by default it's 15 times) and compare
    all the results using statistics like: median or average.

    langdetect supports 55 languages out of the box:
        af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he,
        hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl,
        pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi,
        zh-cn, zh-tw

    :param url: URL to the HTML page with some content
    :param content: use explicit content rather than downloading it from URL
    :param main: use only the main part of the content (ignore header & footer)
    :param rounds: number of detection rounds.
    :return: language code detected by langdetect
    """
    assert rounds > 0, "Rounds can't be lower than 1"
    ignored_characters = '[ا]'
    if url:
        content = requests.get(url).content.decode("utf-8")

    soup = BeautifulSoup(content, "lxml")
    # strip out all of JavaScript & CSS that might not be filtered out initially
    for element in soup.findAll(['script', 'style']):
        element.extract()

    if main:
        # ignore page header & footer
        logging.debug(
            "Will analyse only the main content of the page and ignore the page"
            " header & footer")
        for element in soup.findAll(['header', 'footer']):
            element.extract()

    # clear the page content from the specified characters
    text = re.sub(ignored_characters, '', soup.get_text())
    lines = [line.strip().lower() for line in text.splitlines() if line.strip()]
    results = {}
    for x in range(rounds):
        results[x] = detect_langs('\n'.join(lines))
    logging.debug(
        "Language detection results after %d rounds: %s", rounds, results)
    return results


def get_number_of_search_result_pages(response: Response) -> int:
    """Will extract the last search result page number from provided response.

    The CSS selector will return string like: `page 1 of 2`.
    Then we extract the numbers from it and return the last one.
    In case of lack of thereof a 0 is returned.

    :param response: FAS Search Result response
    :return: a number of FAS Search Result pages or 0 if couldn't find
             information about number of pages
    """
    no_page_counter = 0
    css_selector = (".company-profile-details-body-toolbar-bottom"
                    " span.current::text")
    pages = extract_by_css(response, css_selector).strip()
    page_numbers = [int(word) for word in pages.split() if word.isdigit()]
    last_page = page_numbers[-1] if len(page_numbers) == 2 else no_page_counter
    return last_page
