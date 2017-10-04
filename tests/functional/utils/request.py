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
from urllib3.exceptions import HTTPError as BaseHTTPError

# a list of exceptions that can be thrown by `requests` (and urllib3)
REQUEST_EXCEPTIONS = (
    BaseHTTPError, RequestException, HTTPError, ConnectionError, ProxyError,
    SSLError, Timeout, ConnectTimeout, ReadTimeout, URLRequired,
    TooManyRedirects, MissingSchema, InvalidSchema, InvalidURL, InvalidHeader,
    ChunkedEncodingError, ContentDecodingError, StreamConsumedError, RetryError,
    UnrewindableBodyError
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
    from tests.functional.utils.generic import (
        assertion_msg,
        blue,
        log_response,
        red
    )

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
    from tests.functional.utils.generic import assertion_msg
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
                "Should redirect to one of these %d locations '%s' but instead"
                " was redirected to '%s'", len(locations), locations,
                new_location):
            assert new_location in locations

    if location_starts_with:
        new_location = response.headers.get("Location")
        with assertion_msg(
                "Expected Location header to start with: '%s' but got '%s' "
                "instead.", location_starts_with, new_location):
            assert new_location.startswith(location_starts_with)

