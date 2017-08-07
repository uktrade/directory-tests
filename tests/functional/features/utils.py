# -*- coding: utf-8 -*-
"""Various utils used across the project."""

import hashlib
import logging
import os
import sys
import traceback
from contextlib import contextmanager
from enum import Enum

import requests
from behave.runner import Context
from requests.models import Response
from retrying import retry
from scrapy.selector import Selector
from termcolor import cprint

from tests.functional.features.db_cleanup import get_dir_db_connection
from tests.settings import MAILGUN_EVENTS_URL, MAILGUN_SECRET_API_KEY


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


def make_request(method: Method, url, *, session=None, params=None,
                 headers=None, cookies=None, data=None, files=None,
                 allow_redirects=True, trim_response_content=True,
                 context=None):
    """Make a desired HTTP request using optional parameters, headers and data.

    NOTE:
    If you want to send a POST/PUT/PATCH request as "multipart/form-data;"
    rather than a default "application/x-www-form-urlencoded",
    then provide `data` as `files`.

    :param method: HTTP method, e.g.: GET, POST, PUT etc
    :type  method: tests.functional.features.utils.Method
    :param url: URL that request will be made against
    :type  url: str
    :param session: (optional) an instance of requests Session
    :type session: requests.Session
    :param params: (optional) query parameters
    :type  params: dict
    :param headers: (optional) extra request headers. Will not be persisted
                    across requests, even if using a session.
    :type  headers: dict
    :param cookies: (optional) extra request cookies. Will not be persisted
                    across requests, even if using a session.
    :type  cookies: dict
    :param data: (optional) data to send
    :type  data: dict
    :param files: (optional)
    :type  files: dict with a file. For more details please refer to:
                  http://docs.python-requests.org/en/master/user/quickstart/#post-a-multipart-encoded-file
    :param allow_redirects: Follow or do not follow redirects
    :type  allow_redirects: bool
    :param trim_response_content: decide whether you want to log only first 150
                                  characters of response content.
                                  Defaults to True.
    :type  trim_response_content: bool
    :param context: (optional) Behave's context object. If provided then this
                    Will store the response in `context.response`
    :return: a response object
    :rtype: requests.Response
    """
    with assertion_msg("Can't make a request without a valid URL!"):
        assert url is not None

    req = session or requests
    trim_offset = 150  # define the length of logged response content

    connect_timeout = 3.05
    read_timeout = 60
    request_kwargs = dict(url=url, params=params, headers=headers,
                          cookies=cookies, data=data, files=files,
                          allow_redirects=allow_redirects,
                          timeout=(connect_timeout, read_timeout))

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

    if not allow_redirects:
        logging.debug("REQ Follow redirects: disabled")

    logging.debug("REQ URL: %s %s", method, res.request.url)
    logging.debug("REQ Headers: %s", res.request.headers)
    if cookies:
        logging.debug("REQ Cookies: %s", cookies)
    if data:
        if files:
            if res.request.body:
                logging.debug("REQ Body (trimmed): %s",
                              res.request.body[0:trim_offset])
            else:
                logging.debug("REQ has no body just files")
        else:
            logging.debug("REQ Data: %s", res.request.body)
    logging.debug("RSP Status: %s %s", res.status_code, res.reason)
    logging.debug("RSP URL: %s", res.url)
    logging.debug("RSP Headers: %s", res.headers)
    logging.debug("RSP Cookies: %s", res.cookies)
    if res.history:
        logging.debug("REQ was redirected")
        for resp in res.history:
            logging.debug("Intermediate REQ: %s %s", resp.request.method, resp.url)
            logging.debug("Intermediate REQ Headers: %s", resp.request.headers)
            if files:
                logging.debug("Intermediate REQ Body (trimmed): %s",
                              resp.request.body[0:trim_offset])
            else:
                logging.debug("Intermediate REQ Body: %s", resp.request.body)
            logging.debug("Intermediate RESP: %d %s", resp.status_code, resp.reason)
            logging.debug("Intermediate RESP Headers: %s", resp.headers)
            logging.debug("Intermediate RESP Content: %s",
                          resp.content[0:trim_offset] or None)
        logging.debug("Final destination: %s %s -> %d %s",
                      res.request.method, res.request.url, res.status_code,
                      res.url)
    else:
        logging.debug("REQ was not redirected")
    if res.content:
        if trim_response_content:
            if len(res.content) > trim_offset:
                logging.debug("RSP Trimmed Content: %s",
                              res.content[0:trim_offset])
            else:
                logging.debug("RSP Content: %s", res.content)
        else:
            logging.debug("RSP Content: %s", res.content)

    if context:
        context.response = res
        logging.debug("Last response stored in context.response")

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
    content = response.content.decode("utf-8")

    csrf_tag_idx = content.find("name='csrfmiddlewaretoken'")
    value_property = "value='"
    search_offset = 70
    logging.debug("Looking for csrfmiddlewaretoken in: %s",
                  content[csrf_tag_idx:csrf_tag_idx + search_offset])
    csrf_token_idx = content.find(value_property,
                                  csrf_tag_idx,
                                  csrf_tag_idx + search_offset)
    csrf_token_end_idx = content.find("'",
                                      csrf_token_idx + len(value_property),
                                      csrf_tag_idx + search_offset)
    token = content[(csrf_token_idx + len(value_property)):csrf_token_end_idx]
    logging.debug("Found csrfmiddlewaretoken=%s", token)
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
    content = response.content.decode("utf-8")

    form_action = 'form method="post" action="'
    form_action_idx = content.find(form_action)
    start = form_action_idx + len(form_action)
    end = content.find('"', start)
    action = content[start:end]
    logging.debug("Found confirm email form action value=%s", action)
    return action


def extract_plain_text_payload(msg):
    """Extract plain text payload (7bit) from email message.

    :param msg: an email message
    :type msg: email.mime.text.MIMEText
    :return: a plain text message (no HTML)
    :rtype: str
    """
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
    return res or None


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


def get_verification_code(company_number):
    """Will get the verification code (sent by post) for specified company.

    :param company_number: company number given by Companies House
    :return: verification code sent by post
    """
    connection, cursor = get_dir_db_connection()
    sql = "SELECT verification_code FROM company_company WHERE number = %s;"
    data = (company_number, )
    cursor.execute(sql, data)
    res = None
    if cursor.description:
        res = cursor.fetchone()
        logging.debug("Verification code for company: %s is %s", company_number,
                      res)
    else:
        logging.debug("Did not find verification code for company %s. "
                      "Will return None", company_number)
    cursor.close()
    connection.close()
    return res


def check_response(response: Response, status_code: int, *,
                   location: str = None, locations: list = [],
                   location_starts_with: str = None, body_contains: list = [],
                   unexpected_strings: list = []):
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


def extract_by_css(response, selector):
    """Extract values from HTML response content using CSS selector.

    :param response: response containing HTML content
    :param selector: CSS selector
    :return: value of the 1st found element identified by the CSS selector
    """
    content = response.content.decode("utf-8")
    res = Selector(text=content).css(selector).extract()
    return res[0] if len(res) > 0 else ""


def extract_logo_url(response):
    """Extract URL of the Company's logo picture from the Directory
    edit profile page content.

    :param response: response with the contents of edit profile page
    :return: a URL to the company's logo image
    """
    css_selector = ".logo-container img::attr(src)"
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
    api_key = MAILGUN_SECRET_API_KEY
    # this will help us to get the raw MIME
    headers = {"Accept": "message/rfc2822"}
    response = requests.get(url, auth=("api", api_key), headers=headers)
    context.response = response

    with assertion_msg(
            "Expected 200 from MailGun when getting message details but got %s",
            response.status_code):
        assert response.status_code == 200
    return response.json()


@retry(wait_fixed=10000, stop_max_attempt_number=9)
def mailgun_get_message_url(context: Context, recipient: str) -> str:
    """Will try to find the message URL among 100 emails sent in last 1 hour.

    :param context: behave `context` object
    :param recipient: email address of the message recipient
    :return: mailgun message URL
    """
    url = MAILGUN_EVENTS_URL
    api_key = MAILGUN_SECRET_API_KEY
    message_limit = 1

    params = {
        "limit": message_limit,
        "recipient": recipient,
        "event": "accepted"
    }
    response = requests.get(url, auth=("api", api_key), params=params)
    context.response = response

    with assertion_msg(
            "Expected 200 OK from MailGun when searching for an event triggered"
            " by email verification message but got %s", response.status_code):
        assert response.status_code == 200
    no_of_items = len(response.json()["items"])
    with assertion_msg("Could not find MailGun event for %s", recipient):
        assert no_of_items == message_limit
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
