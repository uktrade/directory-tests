# -*- coding: utf-8 -*-
"""Various utils used across the project."""

import hashlib
import logging
import os
import random
from enum import Enum

import requests
from requests.models import Response
from scrapy.selector import Selector

from tests.functional.features.db_cleanup import get_dir_db_connection
from tests.settings import (
    EXPORT_STATUSES,
    MAILGUN_EVENTS_URL,
    MAILGUN_SECRET_API_KEY,
    NO_EXPORT_INTENT_LABEL
)


def get_file_log_handler(log_formatter,
                         log_file=os.path.join(".", "tests", "functional",
                                               "reports", "behave.log"),
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


def get_console_log_handler(log_formatter, log_level=logging.ERROR):
    """Configure the console logger.

    Will use ERROR logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_level: specifies logging level, e.g.: logging.ERROR
    :return: configured console log handler
    """
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(log_level)
    return console_handler


def init_loggers():
    """Will initialize console and file loggers."""
    # get the root logger
    root_logger = logging.getLogger()
    # "disable" `urllib3` logger, which is used by `requests`
    logging.getLogger("boto").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # configure the formatter
    fmt = ('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: '
           '%(message)s')
    log_formatter = logging.Formatter(fmt)

    # configure the file & console loggers
    root_logger.addHandler(get_file_log_handler(log_formatter))
    root_logger.addHandler(get_console_log_handler(log_formatter))


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
    assert url is not None, "Please provide the URL"

    req = session or requests
    trim_offset = 150  # define the length of logged response content

    request_kwargs = dict(url=url, params=params, headers=headers,
                          cookies=cookies, data=data, files=files,
                          allow_redirects=allow_redirects)

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
    assert response.content, "Response has no content"
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
    assert response.content, "Response has no content"
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
    :type  response: requests.models.Response
    :param status_code: expected status code
    :type  status_code: int
    :param location: (optional) expected value of Location header
    :type  location: str
    :param locations: (optional) in one of the Location list
    :type  locations: list
    :param location_starts_with: (optional) expected leading part of
                                the Location header
    :type  location_starts_with: str
    :param body_contains: (optional) a list of strings that should be present
                    in the response content
    :type  body_contains: list
    :param unexpected_strings: (optional) a list of strings that should NOT be
                               present in the response content
    :type  unexpected_strings: list
    """
    assert response.status_code == status_code

    if body_contains:
        assert response.content, "Response has no content!"
        content = response.content.decode("utf-8")
        for string in body_contains:
            assert string in content

    if unexpected_strings:
        assert response.content, "Response has no content!"
        content = response.content.decode("utf-8")
        for string in unexpected_strings:
            assert string in content

    if location:
        assert response.headers.get("Location") == location, (
            "Expected Location header to be: '{}' but got '{}' instead."
            .format(location, response.headers.get("Location")))

    if locations:
        assert response.headers.get("Location") in locations, (
            "Should be redirected to one of these {} locations '{}' but instead"
            " was redirected to '{}'".format(len(locations), locations,
                                             response.headers.get("Location")))

    if location_starts_with:
        new_location = response.headers.get("Location")
        assert new_location.startswith(location_starts_with), (
            "Expected Location header to start with: '{}' but got '{}' instead."
            .format(location_starts_with, response.headers.get("Location")))


def get_positive_exporting_status():
    """Select random Exporting Status that allows you to register with
    Find a Buyer service.

    :return: an exporting status accepted by Find a Buyer service
    :rtype: str
    """
    with_export_intent = [EXPORT_STATUSES[s] for s in EXPORT_STATUSES if
                          s != NO_EXPORT_INTENT_LABEL]
    return random.choice(with_export_intent)


def get_absolute_path_of_file(filename):
    """Returns absolute path to a file stored in ./tests/functional/files dir.

    Will fail if fail doesn't exists.

    :param filename: name of the file stored in ./tests/functional/files
    :return: an absolute path to the file
    """
    relative_path = os.path.join("tests", "functional", "files", filename)
    absolute_path = os.path.abspath(relative_path)
    error_message = ("Could not find '{}' in ./tests/functional/files. Please "
                     "check the filename!")
    assert os.path.exists(absolute_path), error_message

    return absolute_path


def get_md5_hash_of_file(absolute_path):
    """Calculate md5 hash of provided file.

    :param absolute_path: an absolute path to the file
    :type  absolute_path: str
    :return: md5 hash of the file
    :rtype:  str
    """
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
    assert logo_url, "Could not find Company's logo URL"
    return logo_url


def check_hash_of_remote_file(expected_hash, file_url):
    """Check if the md5 hash of the file is the same as expected.

    :param expected_hash: expected md5 hash
    :param file_url: URL to the file to check
    """
    logging.debug("Fetching file: %s", file_url)
    response = requests.get(file_url)
    file_hash = hashlib.md5(response.content).hexdigest()
    assert expected_hash == file_hash, (
        "Expected hash of file downloaded from %s to be %s but got %s"
        .format(expected_hash, file_hash))


def mailgun_get_message(url: str) -> dict:
    """Get message detail by its URL.

    :param url: unique mailgun message URL
    :return: a dictionary with message details and message body
    """
    api_key = MAILGUN_SECRET_API_KEY
    # this will help us to get the raw MIME
    headers = {"Accept": "message/rfc2822"}
    r = requests.get(url, auth=("api", api_key), headers=headers)

    if r.status_code == 200:
        return r.json()
    else:
        raise LookupError("Oops! Something went wrong: {}".format(r.content))


def mailgun_get_message_url(recipient: str) -> str:
    """Will try to find the message URL among 100 emails sent in last 1 hour.

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

    assert response.status_code == 200
    assert len(response.json()["items"]) == message_limit
    logging.debug("Found event with recipient: {}".format(recipient))
    return response.json()["items"][0]["storage"]["url"]


def get_verification_link(recipient: str) -> str:
    """Get email verification link sent by SSO to specified recipient.

    :param recipient: email address of the message recipient
    :return: email verification link sent by SSO
    """
    logging.debug("Searching for verification email of: {}".format(recipient))
    message_url = mailgun_get_message_url(recipient)
    message = mailgun_get_message(message_url)
    body = message["body-mime"]
    return extract_email_confirmation_link(body)
