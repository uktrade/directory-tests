# -*- coding: utf-8 -*-
"""Various utils used across the project."""

import logging
import os
from enum import Enum

import requests


def get_file_log_handler(log_formatter,
                         log_file=os.path.join(".", "tests", "functional",
                                               "reports", "behave.log"),
                         log_level=logging.DEBUG):
    """Configure the console logger.

    Will use DEBUG logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_file: specifies log file path relative to the root of the project
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
        res = req.head(url=url, params=params, headers=headers, cookies=cookies,
                       allow_redirects=allow_redirects)
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
        raise KeyError("Unrecognized Method: {}".format(method.name))

    if not allow_redirects:
        logging.debug("REQ Follow redirects: disabled")

    logging.debug("REQ URL: {}".format(res.request.url))
    logging.debug("REQ Headers: {}".format(res.request.headers))
    if cookies:
        logging.debug("REQ Cookies: {}".format(cookies))
    if data:
        logging.debug("REQ Data: {}".format(res.request.body))
    if files:
        logging.debug("REQ Files: {}".format(res.request.body))
    logging.debug("RSP Status: {} {}".format(res.status_code, res.reason))
    logging.debug("RSP URL: {}".format(res.url))
    logging.debug("RSP Headers: {}".format(res.headers))
    logging.debug("RSP Cookies: {}".format(res.cookies))
    if res.content:
        trim_response_content = len(res.content) > 150
        if trim_response_content:
            logging.debug("RSP Trimmed Content: {}".format(res.content[0:150]))
        else:
            logging.debug("RSP Content: {}".format(res.content))

    return res
