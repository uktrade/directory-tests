# -*- coding: utf-8 -*-
"""Various utils used across the project."""

import email
import logging
import os
from enum import Enum

import requests
from boto.s3 import connect_to_region
from boto.s3.connection import OrdinaryCallingFormat
from requests.models import Response

from tests.functional.features.db_cleanup import get_dir_db_connection
from tests.functional.features.settings import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET,
    S3_REGION,
    S3_SECRET_ACCESS_KEY
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
                 allow_redirects=True, trim_response_content=True):
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
    :return: a response object
    :rtype: requests.Response
    """
    assert url is not None, "Please provide the URL"

    req = session or requests

    if method == Method.DELETE:
        res = req.delete(url=url, params=params, headers=headers,
                         cookies=cookies, allow_redirects=allow_redirects)
    elif method == Method.GET:
        res = req.get(url=url, params=params, headers=headers, cookies=cookies,
                      allow_redirects=allow_redirects)
    elif method == Method.HEAD:
        res = req.head(url=url, params=params, headers=headers,
                       cookies=cookies, allow_redirects=allow_redirects)
    elif method == Method.OPTIONS:
        res = req.options(url=url, params=params, headers=headers,
                          cookies=cookies, allow_redirects=allow_redirects)
    elif method == Method.PATCH:
        res = req.patch(url=url, params=params, headers=headers, cookies=cookies,
                        data=data, files=files, allow_redirects=allow_redirects)
    elif method == Method.POST:
        res = req.post(url=url, params=params, headers=headers, cookies=cookies,
                       data=data, files=files, allow_redirects=allow_redirects)
    elif method == Method.PUT:
        res = req.put(url=url, params=params, headers=headers, cookies=cookies,
                      data=data, files=files, allow_redirects=allow_redirects)
    else:
        raise KeyError("Unrecognized Method: %s", method.name)

    if not allow_redirects:
        logging.debug("REQ Follow redirects: disabled")

    logging.debug("REQ URL: %s %s", method, res.request.url)
    logging.debug("REQ Headers: %s", res.request.headers)
    if cookies:
        logging.debug("REQ Cookies: %s", cookies)
    if data:
        logging.debug("REQ Data: %s", res.request.body)
    if files:
        logging.debug("REQ Files: %s", res.request.body)
    logging.debug("RSP Status: %s %s", res.status_code, res.reason)
    logging.debug("RSP URL: %s", res.url)
    logging.debug("RSP Headers: %s", res.headers)
    logging.debug("RSP Cookies: %s", res.cookies)
    if res.history:
        logging.debug("REQ was redirected")
        for resp in res.history:
            logging.debug("Intermediate REQ: %s %s", resp.request.method, resp.url)
            logging.debug("Intermediate REQ Headers: %s", resp.request.headers)
            logging.debug("Intermediate REQ Body: %s", resp.request.body)
            logging.debug("Intermediate RESP: %d %s", resp.status_code, resp.reason)
            logging.debug("Intermediate RESP Headers: %s", resp.headers)
            logging.debug("Intermediate RESP Content: %s", resp.content[0:150] or None)
        logging.debug("Final destination: %s %s -> %d %s",
                      res.request.method, res.request.url, res.status_code,
                      res.url)
    else:
        logging.debug("REQ was not redirected")
    if res.content:
        if trim_response_content:
            if len(res.content) > 150:
                logging.debug("RSP Trimmed Content: %s", res.content[0:150])
            else:
                logging.debug("RSP Content: %s", res.content)
        else:
            logging.debug("RSP Content: %s", res.content)

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


def extract_confirm_email_form_action(content):
    """Extract the form action (endpoint) from the Confirm Email page.

    Comes in handy when dealing with e.g. Django forms.

    :param content: response content decoded as utf-8
    :type  content: str
    :return: for action endpoint
    :rtype: str
    """
    assert content, "Expected a non-empty response content but got nothing"

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


def get_s3_bucket():
    """Get S3 bucket connection.

    NOTE:
    requires following environment variables to be set:
    * S3_ACCESS_KEY_ID
    * S3_SECRET_ACCESS_KEY
    * S3_BUCKET
    * S3_REGION

    :return: a S3 bucket connection
    :rtype: boto.s3.connection.S3Connection
    """
    conn = connect_to_region(region_name=S3_REGION,
                             aws_access_key_id=S3_ACCESS_KEY_ID,
                             aws_secret_access_key=S3_SECRET_ACCESS_KEY,
                             is_secure=True,
                             calling_format=OrdinaryCallingFormat())
    return conn.get_bucket(S3_BUCKET)


def find_confirmation_email_msg(bucket, actor, subject):
    """Will search for an email confirmation message stored in AWS S3.

    :param bucket: S3 bucket connection
    :param actor: Actor named tuple
    :param subject: expected subject of sought message
    :return: a plain text message payload
    """
    res = None
    found = False
    for key in bucket.list():
        if key.key != "AMAZON_SES_SETUP_NOTIFICATION":
            logging.debug("Processing email file: %s", key.key)
            try:
                msg_contents = key.get_contents_as_string().decode("utf-8")
                msg = email.message_from_string(msg_contents)
                if msg['To'] == actor.email:
                    logging.debug("Found an email addressed at: %s",
                                  msg['To'])
                    if msg['Subject'] == subject:
                        logging.debug("Found email confirmation message "
                                      "entitled: %s", subject)
                        res = extract_plain_text_payload(msg)
                        found = True
                        logging.debug("Deleting message %s", key.key)
                        bucket.delete_key(key.key)
                        logging.debug("Successfully deleted message %s from S3",
                                      key.key)
                    else:
                        logging.debug("Message from %s to %s had a non-matching"
                                      "subject: '%s'", msg['From'], msg['To'],
                                      msg['Subject'])
                else:
                    logging.debug("Message %s was addressed at: %s", key.key,
                                  msg['To'])
            except Exception as ex:
                logging.error("Something went wrong when getting an email msg "
                              "from S3: %s", ex)

    assert found, ("Could not find email confirmation message for {}"
                   .format(actor.email))
    return res


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
