# -*- coding: utf-8 -*-
"""Various utils used across the project."""
import hashlib
import json
import logging
import os
import random
import re
import sys
import traceback
from collections import namedtuple
from contextlib import contextmanager
from email.mime.text import MIMEText
from enum import Enum
from pprint import pprint
from random import choice
from string import ascii_uppercase
from typing import List

import requests
from behave.runner import Context
from directory_api_client.testapiclient import DirectoryTestAPIClient
from directory_constants.constants import choices
from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient
from requests import Response
from retrying import retry
from termcolor import cprint
from tests import get_absolute_url
from tests.functional.schemas.Companies import COMPANIES
from tests.functional.utils.context_utils import (
    Actor,
    CaseStudy,
    Company,
    Feedback,
    Message
)
from tests.functional.utils.request import Method, check_response, make_request
from tests.settings import (
    DIRECTORY_API_CLIENT_KEY,
    DIRECTORY_API_URL,
    FAB_CONFIRM_COLLABORATION_SUBJECT,
    MAILGUN_DIRECTORY_API_USER,
    MAILGUN_DIRECTORY_EVENTS_URL,
    MAILGUN_DIRECTORY_SECRET_API_KEY,
    RARE_WORDS,
    SECTORS,
    SSO_PROXY_API_CLIENT_BASE_URL,
    SSO_PROXY_SIGNATURE_SECRET,
    TEST_IMAGES_DIR,
    JPEGs,
    JPGs,
    PNGs
)

import lxml
from bs4 import BeautifulSoup
from jsonschema import validate
from langdetect import DetectorFactory, detect_langs
from scrapy.selector import Selector

INDUSTRY_CHOICES = dict(choices.INDUSTRIES)

DIRECTORY_CLIENT = DirectoryTestAPIClient(
    DIRECTORY_API_URL, DIRECTORY_API_CLIENT_KEY)
SSO_CLIENT = DirectorySSOTestAPIClient(
    SSO_PROXY_API_CLIENT_BASE_URL, SSO_PROXY_SIGNATURE_SECRET
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


def get_file_log_handler(
        log_formatter, log_file=os.path.join(
            ".", "tests", "functional", "reports", "behave.log"),
        log_level=logging.DEBUG):
    """Configure the console logger.

    Will use DEBUG logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_file: specifies log file path relative to the project's root
    :param log_level: specifies logging level, e.g.: logging.ERROR
    :return: configured console log handler
    """
    print("Behave log file: {}".format(log_file))
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def init_loggers(context: Context):
    """Will initialize console and file loggers."""
    # configure the formatter
    fmt = ('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: '
           '%(message)s')
    log_formatter = logging.Formatter(fmt)
    log_file_handler = get_file_log_handler(log_formatter)
    # Add log file handler to Behave's logging
    context.config.setup_logging(handlers=[log_file_handler])


def decode_as_utf8(content):
    """Try to decode provided content as UTF-8

    :param content: bytes to decode as UTF-8
    :return: UTF-8 decoded content or the original content
    """
    if isinstance(content, bytes):
        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError:
            logging.debug("Could not decode content as utf-8")
            pass
    return content


class MailGunEvent(Enum):
    """Lists all of MailGun's event types.

    More info here:
    https://documentation.mailgun.com/en/latest/api-events.html#event-types
    """
    ACCEPTED = "accepted"
    DELIVERED = "delivered"
    REJECTED = "rejected"
    FAILED = "failed"
    OPENED = "opened"
    CLICKED = "clicked"
    UNSUBSCRIBED = "unsubscribed"
    COMPLAINED = "complained"
    STORED = "stored"

    def __str__(self):
        return self.value

    def __eq__(self, y):
        return self.value == y.value


class MailGunService(Enum):
    """Lists all MailGun's events states"""
    ServiceDetails = namedtuple('ServiceDetails', ['url', 'user', 'password'])
    DIRECTORY = ServiceDetails(
        url=MAILGUN_DIRECTORY_EVENTS_URL, user=MAILGUN_DIRECTORY_API_USER,
        password=MAILGUN_DIRECTORY_SECRET_API_KEY)

    def __str__(self):
        return self.value

    def __eq__(self, y):
        return self.value == y.value

    @property
    def url(self):
        return self.value.url

    @property
    def user(self):
        return self.value.user

    @property
    def password(self):
        return self.value.password


@retry(wait_fixed=15000, stop_max_attempt_number=9)
def find_mail_gun_events(
        context: Context, service: MailGunService, *, sender: str = None,
        recipient: str = None, to: str = None, subject: str = None,
        limit: int = None, event: MailGunEvent = None, begin: str = None,
        end: str = None, ascending: str = None) -> Response:
    """

    :param context: behave `context` object
    :param service: an object with MailGun service details
    :param sender: (optional) email address of the sender
    :param recipient: (optional) email address of the recipient
    :param to: (optional) email address of the recipient (from the MIME header)
    :param subject: (optional) subject of the message
    :param limit: (optional) Number of entries to return. (300 max)
    :param event: (optional) An event type
    :param begin: (optional)
    :param end: (optional)
    :param ascending: (optional) yes/no
    :return: a response object
    """
    params = {}

    if sender:
        params.update({"from": sender})
    if recipient:
        params.update({"recipient": recipient})
    if to:
        params.update({"to": to})
    if subject:
        params.update({"subject": subject})
    if limit:
        params.update({"limit": limit})
    if event:
        params.update({"event": str(event)})
    if begin:
        params.update({"begin": begin})
    if end:
        params.update({"end": end})
    if ascending:
        params.update({"ascending": ascending})

    response = make_request(
        Method.GET, service.url, auth=(service.user, service.password),
        params=params)
    context.response = response
    with assertion_msg(
            "Expected 200 OK from MailGun when searching for an event %s",
            response.status_code):
        assert response.status_code == 200
    number_of_events = len(response.json()["items"])
    if limit:
        with assertion_msg(
                "Expected (maximum) %d events but got %d instead.", limit,
                number_of_events):
            assert number_of_events <= limit
    with assertion_msg(
            "Expected to find at least 1 MailGun event, got 0 instead. User "
            "parameters: %s", params):
        assert number_of_events > 0
    logging.debug(
        "Found {} event(s) that matched following criteria: {}"
        .format(number_of_events, params))
    return response


def print_response(response: Response, *, trim: bool = True):
    """

    :param response:
    :param trim:
    :return:
    """
    request = response.request
    trim_offset = 2048  # define the length of logged response content

    if response.history:
        blue("REQ was redirected")
        for r in response.history:
            blue("Intermediate REQ: %s %s" % (r.request.method, r.url))
            blue("Intermediate REQ Headers:")
            if r.request.headers.get('Authorization'):
                r.request.headers['Authorization'] = 'STRIPPED_OUT'
            pprint(r.request.headers)
            if r.request.body:
                body = decode_as_utf8(r.request.body)
                if trim or len(body) > trim_offset:
                    blue("Intermediate REQ Body (trimmed):")
                    print(body[0:trim_offset])
                else:
                    blue("Intermediate REQ Body:")
                    print(body)
            else:
                blue("Intermediate REQ had no body")
            blue("Intermediate RESP: %d %s" % (r.status_code, r.reason))
            blue("Intermediate RESP Headers:")
            pprint(r.headers)
            if r.content:
                content = decode_as_utf8(r.content)
                if trim:
                    blue("Intermediate RESP Content (trimmed):")
                    print(content[0:trim_offset])
                else:
                    blue("Intermediate RESP Content:")
                    print(content)

        blue("Final destination: %s %s -> %d %s" % (
            request.method, request.url, response.status_code, response.url))
    else:
        green("REQ URL: %s %s" % (request.method, request.url))
        green("REQ Headers:")
        if request.headers.get('Authorization'):
            request.headers['Authorization'] = 'STRIPPED_OUT'
        pprint(request.headers)
        if request.headers.get('Set-Cookie'):
            green("REQ Cookies:")
            pprint(request.headers.get('Set-Cookie'))
        if request.body:
            body = decode_as_utf8(request.body)
            if trim:
                green("REQ Body (trimmed):")
                print(body[0:trim_offset])
            else:
                green("REQ Body:")
                print(body)
        else:
            green("REQ had no body")
        green("RSP Status: %s %s" % (response.status_code, response.reason))
        green("RSP URL: %s" % response.url)
        green("RSP Headers:")
        pprint(response.headers)
        green("RSP Cookies:")
        pprint(response.cookies)

    if response.content:
        content = decode_as_utf8(response.content)
        if trim:
            red("RSP Content (trimmed):")
            print(content[0:trim_offset])
        else:
            red("RSP Content:")
            print(content)


def log_response(response: Response, *, trim: bool = True):
    request = response.request
    trim_offset = 2048  # define the length of logged response content

    logging.debug(
        "RESPONSE TIME | %s | %s %s", str(response.elapsed), request.method,
        request.url)
    if response.history:
        logging.debug("REQ was redirected")
        for r in response.history:
            logging.debug("Intermediate REQ: %s %s", r.request.method, r.url)
            if r.request.headers.get('Authorization'):
                r.request.headers['Authorization'] = 'STRIPPED_OUT'
            logging.debug("Intermediate REQ Headers: %s", r.request.headers)
            if r.request.body:
                body = decode_as_utf8(r.request.body)
                if trim:
                    logging.debug(
                        "Intermediate REQ Body (trimmed): %s",
                        body[0:trim_offset])
                else:
                    logging.debug("Intermediate REQ Body: %s", body)
            else:
                logging.debug("Intermediate REQ had no body")
            logging.debug("Intermediate RESP: %d %s", r.status_code, r.reason)
            logging.debug("Intermediate RESP Headers: %s", r.headers)
            if r.content:
                content = decode_as_utf8(r.content)
                if trim or len(r.content) > trim_offset:
                    logging.debug(
                        "Intermediate RESP Content: %s", content[0:trim_offset])
                else:
                    logging.debug("Intermediate RSP Content: %s", content)
        logging.debug(
            "Final destination: %s %s -> %d %s", request.method, request.url,
            response.status_code, response.url)
    else:
        logging.debug("REQ URL: %s %s", request.method, request.url)
        if request.headers.get('Authorization'):
            request.headers['Authorization'] = 'STRIPPED_OUT'
        logging.debug("REQ Headers:", request.headers)

        if request.headers.get('Set-Cookie'):
            logging.debug("REQ Cookies:", request.headers.get('Set-Cookie'))

        if request.body:
            body = decode_as_utf8(request.body)
            if trim or len(body) > trim_offset:
                logging.debug("REQ Body (trimmed): %s", body[0:trim_offset])
            else:
                logging.debug("REQ Body: %s", body)
        else:
            logging.debug("REQ had no body")

        logging.debug(
            "RSP Status: %s %s", response.status_code, response.reason)
        logging.debug("RSP URL: %s", response.url)
        logging.debug("RSP Headers: %s", response.headers)
        logging.debug("RSP Cookies: %s", response.cookies)

    if response.content:
        content = decode_as_utf8(response.content)
        if trim:
            logging.debug("RSP Content (trimmed): %s", content[0:trim_offset])
        else:
            logging.debug("RSP Content: %s", content)


def int_api_ch_search(term: str) -> dict:
    """Will search for companies using provided term.

    NOTE:
    This will validate the response data against appropriate JSON Schema.

    :param term: search term, can be: company name or number, keywords etc.
    :type term: str
    :return: a JSON response from Companies House Search endpoint
    """
    url = get_absolute_url('internal-api:companies-house-search')
    params = {"term": term}
    response = make_request(
        Method.GET, url, params=params, allow_redirects=False)
    with assertion_msg(
            "Expected 200 OK from GET %s but instead got %s. In case you're "
            "getting 301 Redirect then check if you're using correct protocol "
            "https or http", response.url, response.status_code):
        assert response.status_code == 200
    logging.debug("Company House Search result: %s", response.json())
    validate(response.json(), COMPANIES)

    return response.json()


def extract_csrf_middleware_token(response: Response):
    """Extract CSRF middleware token from the response content.

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :type  response: requests.models.Response
    :return: CSRF middleware token extracted from the response content
    :rtype: str
    """
    with assertion_msg("Can't extract CSRF token as response has no content"):
        assert response.content
    css_selector = '#content input[type="hidden"]::attr(value)'
    token = extract_by_css(response, css_selector)
    logging.debug("Found CSRF token: %s", token)
    return token


def extract_registration_page_link(response: Response) -> str:
    with assertion_msg(
            "Can't extract link to the Registration page as the response has "
            "no content"):
        assert response.content
    css_selector = "#header-register-link::attr(href)"
    link = extract_by_css(response, css_selector)
    logging.debug("Found link to the Registration page token: %s", link)
    return link


def extract_form_action(response: Response) -> str:
    """Extract the form action (endpoint).

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :return: for action endpoint
    """
    with assertion_msg("Can't extract form action from an empty response!"):
        assert response.content
    css_selector = "#content form::attr(action)"
    action = extract_by_css(response, css_selector)
    logging.debug("Found confirm email form action value=%s", action)
    return action


def get_absolute_path_of_file(filename):
    """Returns absolute path to a file stored in ./tests/functional/files dir.

    Will fail if fail doesn't exists.

    :param filename: name of the file stored in ./tests/functional/files
    :return: an absolute path to the file
    """
    relative_path = os.path.join("tests", "functional", "files", filename)
    absolute_path = os.path.abspath(relative_path)
    with assertion_msg(
            "Could not find '%s' in ./tests/functional/files. Please check the "
            "filename!", filename):
        assert os.path.exists(absolute_path)

    return absolute_path


def get_md5_hash_of_file(absolute_path):
    """Calculate md5 hash of provided file.

    :param absolute_path: an absolute path to the file
    :type  absolute_path: str
    :return: md5 hash of the file
    :rtype:  str
    """
    with assertion_msg("File doesn't exist: %s", absolute_path):
        assert os.path.exists(absolute_path)
    return hashlib.md5(open(absolute_path, "rb").read()).hexdigest()


def extract_by_css(response, selector, *, first: bool = True):
    """Extract values from HTML response content using CSS selector.

    :param response: response containing HTML content
    :param selector: CSS selector
    :return: value of the 1st found element identified by the CSS selector
    """
    content = response.content.decode("utf-8")
    extracted = Selector(text=content).css(selector).extract()
    if first:
        result = extracted[0] if len(extracted) > 0 else ""
    else:
        result = extracted
    return result


def extract_logo_url(response, *, fas: bool = False):
    """Extract URL of the Company's logo picture from the Directory
    edit profile page content.

    :param response: response with the contents of edit profile page
    :param fas: Use FAS specific CSS selector if True, if False use FAB selector
    :return: a URL to the company's logo image
    """
    css_selector = ".logo-container img::attr(src)"
    if fas:
        css_selector = "#company-logo::attr(src)"
    logo_url = extract_by_css(response, css_selector)
    with assertion_msg("Could not find Company's logo URL in the response"):
        assert logo_url
    return logo_url


def check_hash_of_remote_file(expected_hash, file_url):
    """Check if the md5 hash of the file is the same as expected.

    :param expected_hash: expected md5 hash
    :param file_url: URL to the file to check
    """
    logging.debug("Fetching file: %s", file_url)
    response = requests.get(file_url)
    file_hash = hashlib.md5(response.content).hexdigest()
    with assertion_msg(
            "Expected hash of file downloaded from %s to be %s but got %s",
            file_url, expected_hash, file_hash):
        assert expected_hash == file_hash


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param message: a message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in message
                 like: %s, %d
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def red(x: str):
    cprint(x, 'red', attrs=['bold'])


def green(x: str):
    cprint(x, 'green', attrs=['bold'])


def blue(x: str):
    cprint(x, 'blue', attrs=['bold'])


def surround(text: str, tag: str):
    """Surround provided text with a tag.

    :param text: text to surround
    :param tag: tag to surround the text with
    :return: original text surrounded with tag
    """
    return "<{tag}>{text}</{tag}>".format(tag=tag, text=text)


def random_chars(size, *, chars=ascii_uppercase):
    res = ""
    while len(res) < size:
        res += random.choice(chars)
    return res


def sentence(
        *, max_length: int = 60, min_word_length: int = 9, max_words: int = 10,
        min_words: int = 3) -> str:
    """Generate a random string consisting of rare english words.

    NOTE:
    min_word_length is set to 9, because all words in RARE_WORDS are at least 9
    characters long

    :return: a sentence consisting of rare english words
    """
    words = []
    assert min_words <= max_words
    number_of_words = random.randint(min_words, max_words)
    while len(words) < number_of_words:
        word = random.choice(RARE_WORDS)
        if len(word) > min_word_length:
            words.append(word)
    while 0 < max_length < len(" ".join(words)):
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


def extract_and_set_csrf_middleware_token(
        context: Context, response: Response, supplier_alias: str):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param response: request with HTML content containing CSRF middleware token
    """
    token = extract_csrf_middleware_token(response)
    context.update_actor(supplier_alias, csrfmiddlewaretoken=token)


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
        country: str = None, comment: str = None,
        terms: str = None, g_recaptcha_response: str = None) -> Feedback:
    name = name or rare_word(min_length=12)
    email = email or ("test+buyer_{}@directory.uktrade.io"
                      .format(rare_word(min_length=15)))
    company_name = company_name or rare_word(min_length=12)
    country = country or rare_word(min_length=12)
    comment = comment or sentence(max_length=1000)
    g_recaptcha_response = g_recaptcha_response or "test mode"
    terms = terms or "on"

    feedback = Feedback(
        name=name, email=email, company_name=company_name,
        country=country, comment=comment, terms=terms,
        g_recaptcha_response=g_recaptcha_response)

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
    full_name = full_name or sentence(min_words=2, max_words=2)
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

        json = int_api_ch_search(random_company_number)

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
    return [find_active_company_without_fas_profile("test") for _ in
            range(number)]


def save_companies(companies: CompaniesList):
    """Save pre-selected Companies in a JSON file.

    :param companies: a list of named tuples with basic Company details
    """
    # convert `Company` named tuples into dictionaries
    list_dict = []
    for company in companies:
        list_dict.append(
            {key: getattr(company, key) for key in company._fields})

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
        ch_result = int_api_ch_search(company.number)
        if len(ch_result) == 1:
            exists = True
            if ch_result[0]["company_status"] == "active":
                active = True
                is_registered = already_registered(company.number)
                if is_registered:
                    registered_counter += 1
                    red("Company is already registered with FAB")
                    blue("Will remove company data from DIR & SSO DBs")
                    delete_supplier_data_from_dir(company.number)
                    email_address = get_company_email(company.number)
                    delete_supplier_data_from_sso(email_address)
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
    from tests.functional.registry import PAGE_REGISTRY
    selector = PAGE_REGISTRY[page_name.lower()]
    url = get_absolute_url(selector)
    if language_code:
        url += "?lang={}".format(language_code)
    return url


def get_fabs_page_url(page_name: str, *, language_code: str = None):
    from tests.functional.registry import PAGE_REGISTRY
    url = get_absolute_url(PAGE_REGISTRY[page_name.lower()])
    if language_code:
        url += "?lang={}".format(language_code)
    return url


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
    # strip out all of JS & CSS that might not be filtered out initially
    for element in soup.findAll(['script', 'style']):
        element.extract()

    if main:
        # ignore page header & footer
        logging.debug(
            "Will analyse only the main content of the page and ignore the "
            "page header & footer")
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


def get_company_email(number: str) -> str:
    """Get email address associated with company."""
    response = DIRECTORY_CLIENT.get_company_by_ch_id(number)
    check_response(response, 200)
    email = response.json()['company_email']
    logging.debug("Email for company %s is %s", number, email)
    return email


def get_published_companies(context: Context) -> list:
    """Get a List of dicts with published companies.

    :return: a list of dictionaries with published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies()
    context.response = response
    check_response(response, 200)
    return response.json()


def get_published_companies_with_n_sectors(
        context: Context, number_of_sectors: int) -> list:
    """Get a List of published companies with at least N associated sectors.

    :return: a list of dictionaries with matching published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies(
        minimal_number_of_sectors=number_of_sectors)
    context.response = response
    check_response(response, 200)
    return response.json()


def get_verification_code(context: Context, company_number: str):
    """Will get the verification code (sent by post) for specified company.

    :return: verification code sent by post
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    check_response(response, 200)
    verification_code = response.json()['letter_verification_code']
    return verification_code


def is_verification_letter_sent(
        context: Context, company_number: str) -> bool:
    """Check if verification letter was sent.

    :return: True if letter was sent and False if it wasn't
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    check_response(response, 200)
    result = response.json()['is_verification_letter_sent']
    return result


def delete_supplier_data_from_sso(
        email_address: str, *, context: Context = None):
    response = SSO_CLIENT.delete_user_by_email(email_address)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted %s user data from SSO DB", email_address)
    else:
        logging.error(
            "Something went wrong when trying to delete user data for %s from "
            "SSO DB", email_address)


def delete_supplier_data_from_dir(ch_id: str, *, context: Context = None):
    response = DIRECTORY_CLIENT.delete_company_by_ch_id(ch_id)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted supplier data for company %s from DIR DB",
            ch_id)
    else:
        msg = ("Something went wrong when trying to delete supplier data for "
               "company %s from DIR DB. Here's the response: \n%s", ch_id,
               response.content)
        red(msg)
        logging.error(msg)


def flag_sso_account_as_verified(context: Context, email_address: str):
    response = SSO_CLIENT.flag_user_email_as_verified_or_not(
        email_address, verified=True)
    context.response = response
    check_response(response, 204)


def filter_out_legacy_industries(company: dict) -> list:
    sectors = company['sectors']
    logging.error('Sectors before: %s', sectors)
    result = [sector for sector in sectors if sector in INDUSTRY_CHOICES]
    logging.error('Sectors after: %s', result)
    return result


@retry(wait_fixed=10000, stop_max_attempt_number=9)
def mailgun_get_directory_message(context: Context, message_url: str) -> dict:
    """Get message details from MailGun by its URL."""
    # this will help us to get the raw MIME
    headers = {"Accept": "message/rfc2822"}
    response = make_request(
        Method.GET, message_url, headers=headers,
        auth=("api", MAILGUN_DIRECTORY_SECRET_API_KEY))
    context.response = response

    with assertion_msg(
            "Expected to get 200 OK from MailGun when getting message details"
            " but got %s %s instead", response.status_code, response.reason):
        assert response.status_code == 200

    return response.json()


def mailgun_find_email_with_request_for_collaboration(
        context: Context, actor: Actor, company: Company) -> dict:
    logging.debug(
        "Trying to find email with a request for collaboration with company: "
        "%s", company.title)
    subject = FAB_CONFIRM_COLLABORATION_SUBJECT.format(company.title)
    response = find_mail_gun_events(
        context, service=MailGunService.DIRECTORY, recipient=actor.email,
        event=MailGunEvent.ACCEPTED, subject=subject)
    context.response = response
    with assertion_msg(
            "Expected to find an email with a request for collaboration with "
            "company: '%s'", company.alias):
        assert response.status_code == 200
    message_url = response.json()["items"][0]["storage"]["url"]
    return mailgun_get_directory_message(context, message_url)


def extract_plain_text_payload(msg: MIMEText) -> str:
    """Extract plain text payload (7bit) from email message."""
    res = None
    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_content_type() == "text/plain":
                res = part.get_payload()
    else:
        seven_bit = "Content-Transfer-Encoding: 7bit"
        payload = msg.get_payload()
        with assertion_msg("Could not find plain text msg in email payload"):
            assert seven_bit in payload
        start_7bit = payload.find(seven_bit)
        start = start_7bit + len(seven_bit)
        end = payload.find("--===============", start)
        res = payload[start:end]
    return res


def extract_link_with_invitation_for_collaboration(payload: str) -> str:
    start = payload.find("http")
    end = payload.find("\n", start) - 1  # `- 1` to skip the newline char
    invitation_link = payload[start:end]
    assert invitation_link
    logging.debug(
        "Found the link with invitation for collaboration %s", invitation_link)
    return invitation_link
