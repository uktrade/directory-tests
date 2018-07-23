import logging
from datetime import datetime
from enum import Enum

import requests
from requests import Response, Session
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
from termcolor import cprint
from urllib3.exceptions import HTTPError as BaseHTTPError

from pages.common_actions import assertion_msg

# a list of exceptions that can be thrown by `requests` (and urllib3)
REQUEST_EXCEPTIONS = (
    BaseHTTPError, RequestException, HTTPError, ConnectionError, ProxyError,
    SSLError, Timeout, ConnectTimeout, ReadTimeout, URLRequired,
    TooManyRedirects, MissingSchema, InvalidSchema, InvalidURL, InvalidHeader,
    ChunkedEncodingError, ContentDecodingError, StreamConsumedError,
    RetryError, UnrewindableBodyError
)


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


def red(x: str):
    cprint(x, 'red', attrs=['bold'])


def green(x: str):
    cprint(x, 'green', attrs=['bold'])


def blue(x: str):
    cprint(x, 'blue', attrs=['bold'])


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
                        "Intermediate RESP Content: %s",
                        content[0:trim_offset])
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
        params: dict = None, headers: dict = None,
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
    :param auth: (optional) authentication tuple e.g.: ("username", "password")
    :param trim: (optional) trim long request body/response content if True
    :return: a response object
    """

    with assertion_msg("Can't make a request without a valid URL!"):
        assert url is not None

    if not session:
        logging.debug("Session object not provided. Will default to Requests")
    req = session or requests

    connect_timeout = 3.05
    read_timeout = 60
    request_kwargs = dict(
        url=url, params=params, headers=headers, data=data,
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
        red("Data: {}".format(data))
        red("Files: {}".format(files))
        raise ex

    log_response(res, trim=trim)
    return res
