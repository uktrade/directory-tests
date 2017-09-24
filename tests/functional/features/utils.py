# -*- coding: utf-8 -*-
"""Various utils used across the project."""

import hashlib
import logging
import os
import random
import sys
import traceback
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime, timedelta
from enum import Enum
from pprint import pprint
from string import ascii_uppercase

import requests
from behave.runner import Context
from requests import Session
from requests.exceptions import (
    ChunkedEncodingError,
    ConnectionError,
    ConnectTimeout,
    ContentDecodingError,
    HTTPError,
    InvalidHeader,
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    ProxyError,
    ReadTimeout,
    RequestException,
    RetryError,
    SSLError,
    StreamConsumedError,
    Timeout,
    TooManyRedirects,
    UnrewindableBodyError,
    URLRequired
)
from requests.models import Response
from retrying import retry
from scrapy.selector import Selector
from termcolor import cprint
from urllib3.exceptions import HTTPError as BaseHTTPError

from tests.settings import (
    MAILGUN_DIRECTORY_API_USER,
    MAILGUN_DIRECTORY_EVENTS_URL,
    MAILGUN_DIRECTORY_SECRET_API_KEY,
    MAILGUN_SSO_API_USER,
    MAILGUN_SSO_EVENTS_URL,
    MAILGUN_SSO_SECRET_API_KEY
)

# a list of exceptions that can be thrown by `requests` (and urllib3)
REQUEST_EXCEPTIONS = (
    BaseHTTPError, RequestException, HTTPError, ConnectionError, ProxyError,
    SSLError, Timeout, ConnectTimeout, ReadTimeout, URLRequired,
    TooManyRedirects, MissingSchema, InvalidSchema, InvalidURL, InvalidHeader,
    ChunkedEncodingError, ContentDecodingError, StreamConsumedError, RetryError,
    UnrewindableBodyError
)


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


class Method(Enum):
    """Lists all HTTP methods supported by `requests`."""
    DELETE = 0
    GET = 1
    HEAD = 2
    OPTIONS = 3
    PATCH = 4
    POST = 5
    PUT = 6

    def __str__(self):
        return self.name

    def __eq__(self, y):
        return self.value == y.value


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
    SSO = ServiceDetails(
        url=MAILGUN_SSO_EVENTS_URL, user=MAILGUN_SSO_API_USER,
        password=MAILGUN_SSO_SECRET_API_KEY)
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


def print_response(response: Response, *, trim: bool = True):
    """

    :param response:
    :param trim:
    :return:
    """
    request = response.request
    trim_offset = 1024  # define the length of logged response content

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
                if trim:
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
    trim_offset = 1024  # define the length of logged response content

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
                if trim:
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
            if trim:
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


def make_request(
        method: Method, url: str, *, session: Session = None,
        params: dict = None, headers: dict = None, cookies: dict = None,
        data: dict = None, files: dict = None,
        allow_redirects: bool = True, auth: tuple = None, trim: bool = True) \
        -> Response:
    """Make a desired HTTP request using optional parameters, headers and data.

    NOTE:
    If you want to send a POST/PUT/PATCH request as "multipart/form-data;"
    rather than a default "application/x-www-form-urlencoded",
    then provide `data` as `files`.

    :param method: HTTP method, e.g.: GET, POST, PUT etc
    :param url: URL that request will be made against
    :param session: (optional) an instance of requests Session
    :param params: (optional) query parameters
    :param headers: (optional) extra request headers. Will not be persisted
                    across requests, even if using a session.
    :param cookies: (optional) extra request cookies. Will not be persisted
                    across requests, even if using a session.
    :param data: (optional) data to send
    :param files: (optional) a dict with a file.
                  For more details please refer to:
                  http://docs.python-requests.org/en/master/user/quickstart/#post-a-multipart-encoded-file
    :param allow_redirects: Follow or do not follow redirects
    :param auth: (optional) authentication tuple, e.g.: ("username", "password")
    :param trim: (optional) trim long request body/response content if True
    :return: a response object
    """
    with assertion_msg("Can't make a request without a valid URL!"):
        assert url is not None

    req = session or requests

    connect_timeout = 3.05
    read_timeout = 60
    request_kwargs = dict(
        url=url, params=params, headers=headers, cookies=cookies, data=data,
        files=files, allow_redirects=allow_redirects,
        timeout=(connect_timeout, read_timeout), auth=auth)

    if not allow_redirects:
        msg = "REQ Follow redirects: disabled"
        blue(msg)
        logging.debug(msg)

    try:
        if method == Method.DELETE:
            res = req.delete(**request_kwargs)
        elif method == Method.GET:
            res = req.get(**request_kwargs)
        elif method == Method.HEAD:
            res = req.head(**request_kwargs)
        elif method == Method.OPTIONS:
            res = req.options(**request_kwargs)
        elif method == Method.PATCH:
            res = req.patch(**request_kwargs)
        elif method == Method.POST:
            res = req.post(**request_kwargs)
        elif method == Method.PUT:
            res = req.put(**request_kwargs)
        else:
            raise KeyError("Unrecognized Method: %s", method.name)
    except REQUEST_EXCEPTIONS as ex:
        red("Exception UTC datetime: %s" %
            datetime.isoformat(datetime.utcnow()))
        red("{} {}".format(method, url))
        red("Parameters: {}".format(params))
        if headers.get('Authorization'):
            headers['Authorization'] = 'STRIPPED_OUT'
        red("Headers: {}".format(headers))
        red("Cookies: {}".format(cookies))
        red("Data: {}".format(data))
        red("Files: {}".format(files))
        raise ex

    log_response(res, trim=trim)
    return res


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
    return token


def extract_confirm_email_form_action(response: Response):
    """Extract the form action (endpoint) from the Confirm Email page.

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :type  response: requests.models.Response
    :return: for action endpoint
    :rtype: str
    """
    with assertion_msg("Can't extract form action from an empty response!"):
        assert response.content
    css_selector = "#content form::attr(action)"
    action = extract_by_css(response, css_selector)
    logging.debug("Found confirm email form action value=%s", action)
    return action


def extract_plain_text_payload(msg):
    """Extract plain text payload (7bit) from email message.

    :param msg: an email message
    :type msg: email.mime.text.MIMEText
    :return: a plain text message (no HTML)
    :rtype: str
    """
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


def extract_email_confirmation_link(payload):
    """Find email confirmation link inside the plain text email payload.

    :param payload: plain text email message payload
    :type  payload: str
    :return: email confirmation link
    :rtype:  str
    """
    start = payload.find("http")
    end = payload.find("\n", start) - 1  # `- 1` to skip the newline char
    activation_link = payload[start:end]
    logging.debug("Found email confirmation link: %s", activation_link)
    return activation_link


def check_response(response: Response, status_code: int, *,
                   location: str = None, locations: list = None,
                   location_starts_with: str = None, body_contains: list = None,
                   unexpected_strings: list = None):
    """Check if SUT replied with an expected response.

    :param response: Response object return by `requests`
    :param status_code: expected status code
    :param location: (optional) expected value of Location header
    :param locations: (optional) in one of the Location list
    :param location_starts_with: (optional) expected leading part of
                                the Location header
    :param body_contains: (optional) a list of strings that should be present
                    in the response content
    :param unexpected_strings: (optional) a list of strings that should NOT be
                               present in the response content
    """
    with assertion_msg(
            "Expected %s but got %s", status_code, response.status_code):
        assert response.status_code == status_code

    if body_contains:
        with assertion_msg("Expected response with content, got an empty one!"):
            assert response.content
        content = response.content.decode("utf-8")
        for string in body_contains:
            with assertion_msg("Could not find '%s' in the response", string):
                assert string in content

    if unexpected_strings:
        with assertion_msg("Expected response with content, got an empty one!"):
            assert response.content
        content = response.content.decode("utf-8")
        for string in unexpected_strings:
            with assertion_msg("Found unexpected '%s' in response", string):
                assert string not in content

    if location:
        new_location = response.headers.get("Location")
        with assertion_msg("Expected Location header to be: '%s' but got '%s' "
                           "instead.", location, new_location):
            assert new_location == location

    if locations:
        new_location = response.headers.get("Location")
        with assertion_msg(
                "Should redirect to one of these %d locations '%s' but instead "
                "was redirected to '%s'", len(locations), locations,
                new_location):
            assert new_location in locations

    if location_starts_with:
        new_location = response.headers.get("Location")
        with assertion_msg(
                "Expected Location header to start with: '%s' but got '%s' "
                "instead.", location_starts_with, new_location):
            assert new_location.startswith(location_starts_with)


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
            expected_hash, file_hash):
        assert expected_hash == file_hash


@retry(wait_fixed=10000, stop_max_attempt_number=9)
def mailgun_get_message(context: Context, url: str) -> dict:
    """Get message detail by its URL.

    :param context: behave `context` object
    :param url: unique mailgun message URL
    :return: a dictionary with message details and message body
    """
    api_key = MAILGUN_SSO_SECRET_API_KEY
    # this will help us to get the raw MIME
    headers = {"Accept": "message/rfc2822"}
    response = make_request(
        Method.GET, url, headers=headers, auth=("api", api_key))
    context.response = response

    with assertion_msg(
            "Expected 200 from MailGun when getting message details but got %s",
            response.status_code):
        assert response.status_code == 200
    return response.json()


def mailgun_get_message_url(
        context: Context, recipient: str, *, subject: str = None) -> str:
    """Will try to find the message URL among 100 emails sent in last 1 hour.

    NOTE:
    More on MailGun's Event Polling:
    https://documentation.mailgun.com/en/latest/api-events.html#event-polling

    :param context: behave `context` object
    :param recipient: email address of the message recipient
    :return: mailgun message URL
    """
    message_limit = 1
    pattern = '%a, %d %b %Y %H:%M:%S GMT'
    begin = (datetime.utcnow() - timedelta(minutes=60)).strftime(pattern)

    response = find_mailgun_events(
        context, MailGunService.SSO, limit=message_limit, recipient=recipient,
        event=MailGunEvent.ACCEPTED, begin=begin, ascending="yes",
        subject=subject
    )
    context.response = response
    logging.debug("Found event with recipient: {}".format(recipient))
    return response.json()["items"][0]["storage"]["url"]


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


def get_verification_link(context: Context, recipient: str) -> str:
    """Get email verification link sent by SSO to specified recipient.

    :param context: behave `context` object
    :param recipient: email address of the message recipient
    :return: email verification link sent by SSO
    """
    logging.debug("Searching for verification email of: {}".format(recipient))
    message_url = mailgun_get_message_url(context, recipient)
    message = mailgun_get_message(context, message_url)
    body = message["body-mime"]
    return extract_email_confirmation_link(body)


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


@retry(wait_fixed=15000, stop_max_attempt_number=9)
def find_mailgun_events(
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


def random_chars(size, *, chars=ascii_uppercase):
    res = ""
    while len(res) < size:
        res += random.choice(chars)
    return res
