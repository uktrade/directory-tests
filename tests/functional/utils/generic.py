# -*- coding: utf-8 -*-
"""Various utils used across the project."""
import hashlib
import logging
import os
import random
import re
import sys
import traceback
from collections import defaultdict
from contextlib import contextmanager
from pprint import pprint
from random import choice
from string import ascii_uppercase
from typing import DefaultDict, List

import lxml
import requests
from behave.runner import Context
from bs4 import BeautifulSoup
from langdetect import DetectorFactory, detect_langs
from requests import Response

from directory_constants import choices
from directory_tests_shared import URLs
from directory_tests_shared.clients import (
    DIRECTORY_TEST_API_CLIENT,
    FORMS_API_CLIENT,
    SSO_TEST_API_CLIENT,
    BasicAuthenticator,
)
from directory_tests_shared.constants import SECTORS, TEST_IMAGES_DIR, JPEGs, PNGs
from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER
from directory_tests_shared.utils import (
    blue,
    extract_by_css,
    green,
    rare_word,
    red,
    sentence,
)
from tests.functional.utils.context_utils import (
    CaseStudy,
    Company,
    Feedback,
    Message,
    update_actor,
)
from tests.functional.utils.request import Method, check_response, make_request

INDUSTRY_CHOICES = dict(choices.INDUSTRIES)

# a type hint for a List of Company named tuples
CompaniesList = List[Company]
# make `langdetect` results deterministic
DetectorFactory.seed = 0  # noqa
# A dict with currently supported languages on FAS and their short codes
ERROR_INDICATORS = [
    "error",
    "errors",
    "problem",
    "problems",
    "fail",
    "failed",
    "failure",
    "required",
    "missing",
]

BASIC_AUTHENTICATOR = BasicAuthenticator(BASICAUTH_USER, BASICAUTH_PASS)


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


def extract_page_contents(
    content: str,
    *,
    ignored_characters: str = "[ا]",
    strip_js: bool = True,
    strip_css: bool = True,
    strip_header: bool = True,
    strip_cookie_notice: bool = True,
    strip_country_dialog: bool = True,
    strip_skip_to_main_content: bool = True,
    strip_image_captions: bool = True,
    strip_companies_list: bool = True,
    strip_footer: bool = True,
    strip_select_menus: bool = True,
    strip_unordered_lists: bool = False,
    strip_fas_search_result_summary: bool = True,
    strip_industry_last_updated: bool = True,
    strip_report_this_page: bool = True,
) -> str:
    soup = BeautifulSoup(content, "lxml")

    if strip_js:
        for element in soup.findAll(["script"]):
            element.extract()
    if strip_css:
        for element in soup.findAll(["style"]):
            element.extract()
    if strip_header:
        for element in soup.findAll(["header"]):
            element.extract()
        for element in soup.select("#great-header"):
            element.extract()
    if strip_country_dialog:
        for element in soup.select("#country-selector-dialog"):
            element.extract()
    if strip_cookie_notice:
        for element in soup.select("#header-cookie-notice"):
            element.extract()
    if strip_skip_to_main_content:
        for element in soup.select("#skip-link"):
            element.extract()
    if strip_image_captions:
        for element in soup.select(".image-caption"):
            element.extract()
    if strip_companies_list:
        for element in soup.select("#companies-section ul"):
            element.extract()
    if strip_footer:
        for element in soup.findAll(["footer"]):
            element.extract()
    if strip_select_menus:
        for element in soup.findAll(["select"]):
            element.extract()
    if strip_unordered_lists:
        for element in soup.findAll(["ul"]):
            element.extract()
    if strip_fas_search_result_summary:
        for element in soup.select("#hero-container"):
            element.extract()
    if strip_industry_last_updated:
        for element in soup.select("p.description.subheading"):
            element.extract()
    if strip_report_this_page:
        for element in soup.select("#error-reporting-section-contact-us"):
            element.extract()

    text = soup.get_text()

    # clear the page content from the specified characters
    if ignored_characters:
        text = re.sub(ignored_characters, "", text)

    # remove empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def print_response(
    response: Response,
    *,
    trim: bool = True,
    content_only: bool = True,
    trim_offset: int = 2048,
):
    request = response.request

    if response.history:
        blue("REQ was redirected")
        for r in response.history:
            blue("Intermediate REQ: %s %s" % (r.request.method, r.url))
            blue("Intermediate REQ Headers:")
            if r.request.headers.get("Authorization"):
                r.request.headers["Authorization"] = "STRIPPED_OUT"
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
                content_only_msg = ""
                if content_only:
                    content_only_msg = " & without HTML markup"
                    content = extract_page_contents(content)
                if trim:
                    blue(
                        "Intermediate RESP Content (trimmed{}):".format(
                            content_only_msg
                        )
                    )
                    print(content[0:trim_offset])
                else:
                    blue("Intermediate RESP Content{}:".format(content_only_msg))
                    print(content)

        blue(
            "Final destination: %s %s -> %d %s"
            % (request.method, request.url, response.status_code, response.url)
        )
    else:
        green("REQ URL: %s %s" % (request.method, request.url))
        green("REQ Headers:")
        if request.headers.get("Authorization"):
            request.headers["Authorization"] = "STRIPPED_OUT"
        pprint(request.headers)
        if request.headers.get("Set-Cookie"):
            green("REQ Cookies:")
            pprint(request.headers.get("Set-Cookie"))
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
        content_only_msg = ""
        if content_only:
            content_only_msg = " & without HTML markup"
            content = extract_page_contents(content)
        if trim:
            red("RSP Content (trimmed){}:".format(content_only_msg))
            print(content[0:trim_offset])
        else:
            red("RSP Content: {}".format(content_only_msg))
            print(content)


def log_response(
    response: Response,
    *,
    trim: bool = True,
    trim_offset: int = 2048,
    content_only: bool = True,
):
    request = response.request

    logging.debug(
        "RESPONSE TIME | %s | %s %s", str(response.elapsed), request.method, request.url
    )
    if response.history:
        logging.debug("REQ was redirected")
        for r in response.history:
            logging.debug("Intermediate REQ: %s %s", r.request.method, r.url)
            if r.request.headers.get("Authorization"):
                r.request.headers["Authorization"] = "STRIPPED_OUT"
            logging.debug("Intermediate REQ Headers: %s", r.request.headers)
            if r.request.body:
                body = decode_as_utf8(r.request.body)
                if trim:
                    logging.debug(
                        "Intermediate REQ Body (trimmed): %s", body[0:trim_offset]
                    )
                else:
                    logging.debug("Intermediate REQ Body: %s", body)
            else:
                logging.debug("Intermediate REQ had no body")
            logging.debug("Intermediate RESP: %d %s", r.status_code, r.reason)
            logging.debug("Intermediate RESP Headers: %s", r.headers)
            if r.content:
                content = decode_as_utf8(r.content)
                content_only_msg = ""
                if content_only:
                    content_only_msg = " & without HTML markup"
                    content = extract_page_contents(content)
                if trim or len(r.content) > trim_offset:
                    logging.debug(
                        "Intermediate RESP Content (trimmed%s): %s",
                        content[0:trim_offset],
                        content_only_msg,
                    )
                else:
                    logging.debug(
                        "Intermediate RSP Content%s: %s", content, content_only_msg
                    )
        logging.debug(
            "Final destination: %s %s -> %d %s\n%s",
            request.method,
            request.url,
            response.status_code,
            response.url,
            response.headers,
        )
    else:
        logging.debug("REQ URL: %s %s", request.method, request.url)
        if request.headers.get("Authorization"):
            request.headers["Authorization"] = "STRIPPED_OUT"
        logging.debug("REQ Headers: %s", request.headers)

        if request.headers.get("Set-Cookie"):
            logging.debug("REQ Cookies: %s", request.headers.get("Set-Cookie"))

        if request.body:
            body = decode_as_utf8(request.body)
            if trim or len(body) > trim_offset:
                logging.debug("REQ Body (trimmed): %s", body[0:trim_offset])
            else:
                logging.debug("REQ Body: %s", body)
        else:
            logging.debug("REQ had no body")

        logging.debug("RSP Status: %s %s", response.status_code, response.reason)
        logging.debug("RSP URL: %s", response.url)
        logging.debug("RSP Headers: %s", response.headers)
        logging.debug("RSP Cookies: %s", response.cookies)

    if response.content:
        content = decode_as_utf8(response.content)
        content_only_msg = ""
        if content_only:
            content_only_msg = " without HTML markup"
            content = extract_page_contents(content)
        if trim:
            logging.debug(
                "RSP Content (trimmed &%s): %s",
                content_only_msg,
                content[0:trim_offset],
            )
        else:
            logging.debug("RSP Content%s:\n %s", content_only_msg, content)


def extract_csrf_middleware_token(response: Response) -> str:
    """Extract CSRF middleware token from the response content.

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :type  response: requests.models.Response
    :return: CSRF middleware token extracted from the response content
    :rtype: str
    """
    with assertion_msg("Can't extract CSRF token as response has no content"):
        assert response.content
    css_selector = "input[type=hidden][name=csrfmiddlewaretoken]::attr(value)"
    token = extract_by_css(response.content.decode("UTF-8"), css_selector)
    with assertion_msg(f"Couldn't find csrfmiddlewaretoken on {response.url}"):
        assert token
    logging.debug("Found CSRF token: %s", token)
    return token


def extract_form_action(response: Response) -> str:
    """Extract the form action (endpoint).

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :return: for action endpoint
    """
    with assertion_msg("Can't extract form action from an empty response!"):
        assert response.content
    css_selector = "#content form::attr(action)"
    action = extract_by_css(response.content.decode("UTF-8"), css_selector)
    logging.debug("Found confirm email form action value=%s", action)
    return action


def get_absolute_path_of_file(filename):
    """Returns absolute path to a file stored in ./tests/functional/files dir.

    Will fail if fail doesn't exists.

    :param filename: name of the file stored in ./tests/functional/files
    :return: an absolute path to the file
    """
    relative_path = os.path.join(TEST_IMAGES_DIR, filename)
    absolute_path = os.path.abspath(relative_path)
    with assertion_msg(
        f"Could not find '{filename}' in ./tests/files. Please check the filename!"
    ):
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


def extract_logo_url(response: Response):
    """Extract URL of the Company's logo picture from the Directory
    edit profile page content.

    :param response: response with the contents of edit profile page
    :param fas: Use FAS specific CSS selector if True, else use FAB selector
    :return: a URL to the company's logo image
    """
    css_selector = "#logo-container img::attr(src)"
    logo_url = extract_by_css(response.content.decode("UTF-8"), css_selector)
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
        file_url,
        expected_hash,
        file_hash,
    ):
        assert expected_hash == file_hash


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        if len(sys._current_frames()) == 1:
            print(f"Found 'shallow' Traceback, will inspect outer traceback frames")
            import inspect

            for f in inspect.getouterframes(sys._getframe(0)):
                print(f"{f.filename} +{f.lineno} - in {f.function}")
                if "_def.py" in f.filename:
                    break
        traceback.print_tb(tb)
        raise


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


def extract_and_set_csrf_middleware_token(
    context: Context, response: Response, supplier_alias: str
):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param response: request with HTML content containing CSRF middleware token
    """
    token = extract_csrf_middleware_token(response)
    update_actor(context, supplier_alias, csrfmiddlewaretoken=token)


def random_case_study_data(alias: str) -> CaseStudy:
    """Return a CaseStudy populated with randomly generated details.

    :param alias: alias of the Case Study
    :return: a CaseStudy namedtuple
    """
    sector = choice(SECTORS)
    images = PNGs + JPEGs
    image_1, image_2, image_3 = (choice(images) for _ in range(3))
    (
        title,
        summary,
        description,
        caption_1,
        caption_2,
        caption_3,
        testimonial,
        source_name,
        source_job,
        source_company,
    ) = (sentence() for _ in range(10))
    website = "http://{}.{}".format(rare_word(), rare_word())
    keywords = ", ".join(sentence().split())

    case_study = CaseStudy(
        alias=alias,
        title=title,
        summary=summary,
        description=description,
        sector=sector,
        website=website,
        keywords=keywords,
        image_1=image_1,
        image_2=image_2,
        image_3=image_3,
        caption_1=caption_1,
        caption_2=caption_2,
        caption_3=caption_3,
        testimonial=testimonial,
        source_name=source_name,
        source_job=source_job,
        source_company=source_company,
    )

    return case_study


def random_feedback_data(
    *,
    name: str = None,
    email: str = None,
    company_name: str = None,
    country: str = None,
    comment: str = None,
    terms: str = None,
    g_recaptcha_response: str = None,
) -> Feedback:
    name = name or rare_word()
    email = email or ("test+buyer_{}@directory.uktrade.digital".format(rare_word()))
    company_name = company_name or f"{rare_word()} AUTOTESTS"
    country = country or rare_word()
    comment = comment or sentence(max_length=1000)
    g_recaptcha_response = g_recaptcha_response or "test mode"
    terms = terms or "on"

    feedback = Feedback(
        name=name,
        email=email,
        company_name=company_name,
        country=country,
        comment=comment,
        terms=terms,
        g_recaptcha_response=g_recaptcha_response,
    )

    return feedback


def assert_that_captcha_is_in_dev_mode(response: Response):
    content = response.content.decode("UTF-8")
    dev_site_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    if dev_site_key not in content:
        raise NotImplementedError(f"Captcha is not in Dev Mode on {response.url} !!!")


def random_message_data(
    *,
    alias: str = None,
    body: str = None,
    company_name: str = None,
    country: str = None,
    email_address: str = None,
    family_name: str = None,
    given_name: str = None,
    g_recaptcha_response: str = None,
    sector: str = None,
    subject: str = None,
    terms: str = None,
) -> Feedback:
    alias = alias or "test message"
    body = body or sentence(max_length=1000)
    company_name = company_name or f"{rare_word()} AUTOTESTS"
    country = country or rare_word()
    email_address = email_address or (
        "test+buyer_{}@directory.uktrade.digital".format(rare_word())
    )
    family_name = family_name or sentence(min_words=2, max_words=2)
    given_name = given_name or sentence(min_words=2, max_words=2)
    sector = sector or random.choice(SECTORS)
    subject = subject or sentence(max_length=200)
    g_recaptcha_response = g_recaptcha_response or "test mode"
    terms = terms or "on"

    message = Message(
        alias=alias,
        body=body,
        company_name=company_name,
        country=country,
        email_address=email_address,
        family_name=family_name,
        given_name=given_name,
        g_recaptcha_response=g_recaptcha_response,
        sector=sector,
        subject=subject,
        terms=terms,
    )

    return message


def escape_html(text: str, *, upper: bool = False) -> str:
    """Escape some of the special characters that are replaced by FAB/SSO.

    :param text: a string to escape
    :param upper: (optional) change to upper case before escaping characters
    :return: a string with escaped characters
    """
    html_escape_table = {"&": "&amp;", "'": "&#39;"}
    if upper:
        text = text.upper()
    return "".join(html_escape_table.get(c, c) for c in text)


def extract_main_error(content: str) -> str:
    """Extract error from page `main` block.

    :param content: a raw HTML content
    :return: error message or None is no error was detected
    """
    soup = BeautifulSoup(content, "lxml")
    sections = soup.find_all("main")
    lines = [
        line.strip()
        for section in sections
        for line in section.text.splitlines()
        if line
    ]
    has_errors = any(
        indicator in line.lower() for line in lines for indicator in ERROR_INDICATORS
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
    sections = soup.find_all("section")
    lines = [
        line.strip()
        for section in sections
        for line in section.text.splitlines()
        if line
    ]
    has_errors = any(
        indicator in line.lower() for line in lines for indicator in ERROR_INDICATORS
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
        for indicator in ERROR_INDICATORS
    )
    return form_errors if has_errors else ""


def detect_page_language(
    name: str, url: str, content: str, *, main: bool = False, rounds: int = 15
) -> DefaultDict[str, List]:
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

    :param name: human friendly page name
    :param url: URL to the HTML page with some content
    :param content: use explicit content rather than downloading it from URL
    :param main: use only the main part of the content (ignore header & footer)
    :param rounds: number of detection rounds.
    :return: language code detected by langdetect
    """
    assert rounds > 0, "Rounds can't be lower than 1"
    if url:
        content = make_request(Method.GET, url).content.decode("utf-8")

    if main:
        logging.debug(
            "Will analyse only the main content of the page and ignore the "
            "page header & footer"
        )
        text = extract_page_contents(content)
    else:
        logging.debug(
            "Will analyse the contents of the whole page, including page "
            "header & footer"
        )
        text = extract_page_contents(
            content, strip_header=False, strip_footer=False, strip_unordered_lists=False
        )

    raw_results = {}
    logging.debug("Text used to detect the page language(s):")
    logging.debug(text)
    for x in range(rounds):
        raw_results[x] = detect_langs(text)

    flattened_results = defaultdict(list)
    for detections in raw_results.values():
        for detection in detections:
            flattened_results[detection.lang].append(detection.prob)

    logging.debug(
        f"Language detection results for '{name}' -> {url} after {rounds} "
        f"rounds: {flattened_results}"
    )
    return flattened_results


def get_number_of_search_result_pages(response: Response) -> int:
    """Will extract the last search result page number from provided response.

    The CSS selector will return string like: `page 1 of 2`.
    Then we extract the numbers from it and return the last one.
    In case of lack of thereof a 0 is returned.

    :param response: FAS Search Result response
    :return: a number of FAS Search Result pages or 0 if couldn't find
             information about number of pages
    """
    last_page_css_selector = "#paginator ol li.active-blue-text ~ li a::text"
    last_page = extract_by_css(
        response.content.decode("UTF-8"), last_page_css_selector
    ).strip()
    last_page = int(last_page) if last_page.isdigit() else 0
    logging.debug(f"Number of search result pages: {last_page}")
    return last_page


def get_company_by_id_or_title(number_or_title: str) -> dict:
    """Get email address associated with company."""
    response = DIRECTORY_TEST_API_CLIENT.get_company_by_ch_id(number_or_title)
    return response.json() if response.status_code == 200 else None


def get_published_companies(context: Context) -> list:
    """Get a List of dicts with published companies.

    :return: a list of dictionaries with published companies
    """
    response = DIRECTORY_TEST_API_CLIENT.get_published_companies()
    context.response = response
    check_response(response, 200)
    return response.json()


def get_published_companies_with_n_sectors(
    context: Context, number_of_sectors: int
) -> list:
    """Get a List of published companies with at least N associated sectors.

    :return: a list of dictionaries with matching published companies
    """
    response = DIRECTORY_TEST_API_CLIENT.get_published_companies(
        minimal_number_of_sectors=number_of_sectors
    )
    context.response = response
    check_response(response, 200)
    return response.json()


def get_verification_code(context: Context, company_number: str):
    """Will get the verification code (sent by post) for specified company.

    :return: verification code sent by post
    """
    response = DIRECTORY_TEST_API_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    check_response(response, 200)
    verification_code = response.json()["letter_verification_code"]
    logging.debug(f"GET verification code: {response.json()}")
    return verification_code


def verify_non_ch_company(context: Context, company: Company):
    """Verify company which requested manual verification."""
    url = URLs.DIR_API_TEST_API_COMPANY.absolute_template.format(
        ch_id_or_name=company.title
    )
    data = {"verified_with_identity_check": True}
    context.response = DIRECTORY_TEST_API_CLIENT.patch(url, data)
    check_response(context.response, 204)
    logging.debug(
        f"Successfully flagged '{company.title}' as verified with identity check"
    )


def is_verification_letter_sent(context: Context, company_number: str) -> bool:
    """Check if verification letter was sent.

    :return: True if letter was sent and False if it wasn't
    """
    response = DIRECTORY_TEST_API_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    check_response(response, 200)
    result = response.json()["is_verification_letter_sent"]
    return result


def delete_supplier_data_from_sso(email_address: str, *, context: Context = None):
    response = SSO_TEST_API_CLIENT.delete_user_by_email(email_address)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug("Successfully deleted %s user data from SSO DB", email_address)
    else:
        logging.error(
            "Something went wrong when trying to delete user data for %s from "
            "SSO DB",
            email_address,
        )


def delete_test_buyers_from_directory_api():
    response = DIRECTORY_TEST_API_CLIENT.delete(
        "testapi/test-buyers/", authenticator=BASIC_AUTHENTICATOR
    )
    with assertion_msg(
        f"Expected 204 or 404 from DIRECTORY-API but got:"
        f"{response.status_code} → {response.content}"
    ):
        assert response.status_code in [204, 404]
    logging.debug(
        f"Successfully issued a request to delete test buyers from DIRECTORY-API: "
        f"{response.status_code}"
    )


def delete_test_companies_from_directory_api():
    response = DIRECTORY_TEST_API_CLIENT.delete(
        "testapi/test-companies/", authenticator=BASIC_AUTHENTICATOR
    )
    with assertion_msg(
        f"Expected 204 or 404 from DIRECTORY-API but got:"
        f"{response.status_code} → {response.content}"
    ):
        assert response.status_code in [204, 404]
    logging.debug(
        f"Successfully issued a request to delete test companies from DIRECTORY-API: "
        f"{response.status_code}"
    )


def delete_test_users_from_sso():
    response = SSO_TEST_API_CLIENT.delete(
        "testapi/test-users/", authenticator=BASIC_AUTHENTICATOR
    )
    with assertion_msg(
        f"Expected 204 or 404 from SSO-API but got: {response.status_code} → "
        f"{response.content}"
    ):
        assert response.status_code in [204, 404]
    logging.debug(
        f"Successfully issued a request to delete test users from SSO-API: "
        f"{response.status_code}"
    )


def delete_test_submissions_from_forms_api():
    response = FORMS_API_CLIENT.delete(
        "testapi/test-submissions/", authenticator=BASIC_AUTHENTICATOR
    )
    with assertion_msg(
        f"Expected 204 or 404 from FORMS-API but got: {response.status_code} → "
        f"{response.content}"
    ):
        assert response.status_code in [204, 404]
    logging.debug(
        f"Successfully issued a request to delete test submissions from FORMS-API: "
        f"{response.status_code}"
    )


def delete_supplier_data_from_dir(ch_id_or_name: str, *, context: Context = None):
    response = DIRECTORY_TEST_API_CLIENT.delete_company_by_ch_id(ch_id_or_name)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted supplier data for company %s from DIR DB",
            ch_id_or_name,
        )
    else:
        msg = (
            "INFO: Could not delete company {} from DIR DB!\n"
            "Most likely it's because a FAB profile wasn't created for the "
            "company used in the scenario or if in the scenario there is "
            "more than one supplier actor associated with the same company,"
            " then you're seeing this message because company data was "
            "already deleted when the data for the first supplier actor was"
            " deleted.\nJust in case, here's the response from the server: "
            "\n{}".format(ch_id_or_name, response.content)
        )
        blue(msg)
        logging.error(msg)


def flag_sso_account_as_verified(context: Context, email_address: str):
    response = SSO_TEST_API_CLIENT.flag_user_email_as_verified_or_not(
        email_address, verified=True
    )
    context.response = response
    check_response(response, 204)
    logging.debug(f"Account for {email_address} was flagged as verified")


def filter_out_legacy_industries(company: dict) -> list:
    sectors = company["sectors"]
    logging.error("Sectors before: %s", sectors)
    result = [sector for sector in sectors if sector in INDUSTRY_CHOICES]
    logging.error("Sectors after: %s", result)
    return result


def create_test_isd_company(context: Context) -> dict:
    """Creates an unpublished test ISD company"""
    response = DIRECTORY_TEST_API_CLIENT.post("testapi/isd_company/")
    context.response = response
    check_response(response, 201)
    return response.json()
