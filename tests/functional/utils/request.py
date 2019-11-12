# -*- coding: utf-8 -*-
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
    URLRequired,
)
from urllib3.exceptions import HTTPError as BaseHTTPError

# a list of exceptions that can be thrown by `requests` (and urllib3)
from directory_tests_shared.settings import (
    BASICAUTH_PASS,
    BASICAUTH_USER,
    USE_BASIC_AUTH,
)
from directory_tests_shared.utils import red

REQUEST_EXCEPTIONS = (
    BaseHTTPError,
    RequestException,
    HTTPError,
    ConnectionError,
    ProxyError,
    SSLError,
    Timeout,
    ConnectTimeout,
    ReadTimeout,
    URLRequired,
    TooManyRedirects,
    MissingSchema,
    InvalidSchema,
    InvalidURL,
    InvalidHeader,
    ChunkedEncodingError,
    ContentDecodingError,
    StreamConsumedError,
    RetryError,
    UnrewindableBodyError,
)


def basic_auth() -> tuple:
    return BASICAUTH_USER, BASICAUTH_PASS


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
    method: Method,
    url: str,
    *,
    session: Session = None,
    params: dict = None,
    headers: dict = None,
    data: dict = None,
    files: dict = None,
    allow_redirects: bool = True,
    auth: tuple = None,
    trim: bool = True,
    cookies: dict = None,
    connect_timeout: float = 3.05,
    read_timeout: int = 60,
    use_basic_auth: bool = USE_BASIC_AUTH,
    no_filename_in_multipart_form_data: bool = False,
) -> Response:
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
    :param data: (optional) data to send
    :param files: (optional) a dict with a file.
                  For more details please refer to:
                  https://requests.kennethreitz.org//en/master/user/quickstart/#post-a-multipart-encoded-file
    :param allow_redirects: Follow or do not follow redirects
    :param auth: (optional) authentication tuple, e.g. ("username", "password")
    :param trim: (optional) trim long request body/response content if True
    :param cookies: (optional) extra request cookies. Will not be persisted
                    across requests, even if using a session.
    :param connect_timeout: (optional) the number of seconds Requests will wait for your client to establish
                            a connection to a remote machine
    :param read_timeout: (optional) the number of seconds the client will wait for the server to send a response
    :param use_basic_auth: (optional) use default basic auth credentials
    :param no_filename_in_multipart_form_data: (optional) remove filename parameter from multipart form data
    :return: Response
    """
    from tests.functional.utils.generic import assertion_msg, log_response

    with assertion_msg("Can't make a request without a valid URL!"):
        assert url is not None

    if not session:
        logging.warning("Session object not provided. Will default to Requests")
    req = session or requests

    if no_filename_in_multipart_form_data:
        # in order to remove the "filename" parameter from "multipart/form-data;" request, every item from the
        # dictionary has to have a tuple value, where the first item represents filename. If it's set to None, then
        # no filename is sent.
        # see: https://stackoverflow.com/a/23131823
        files = {key: (None, value) for key, value in files.items()}

    if use_basic_auth:
        auth = basic_auth()
    request_kwargs = dict(
        url=url,
        params=params,
        headers=headers,
        data=data,
        files=files,
        allow_redirects=allow_redirects,
        timeout=(connect_timeout, read_timeout),
        auth=auth,
        cookies=cookies,
    )

    logging.debug(f"{method} {url}")
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
        red("Exception UTC datetime: %s" % datetime.isoformat(datetime.utcnow()))
        red("{} {}".format(method, url))
        red("Parameters: {}".format(params))
        if headers.get("Authorization"):
            headers["Authorization"] = "STRIPPED_OUT"
        red("Headers: {}".format(headers))
        red("Data: {}".format(data))
        if files:
            meta = [(k, v[0], v[2]) for k, v in files.items()]
            red("Files: {}".format(meta))
        raise ex

    blocked = "Unfortunately your IP address does not appear to come from"
    if blocked in res.content.decode("UTF-8"):
        logging.debug(f"Looks like we're blocked, will retry")
        res = make_request(Method.GET, res.url, session=session)

    log_response(res, trim=trim)
    return res


def check_url(response: Response, expected_url: str, *, startswith: bool = False):
    # avoid circular imports
    from tests.functional.utils.generic import assertion_msg

    if startswith:
        error = (
            f"Expected response URL to start with {expected_url} but got "
            f"{response.url} instead"
        )
        with assertion_msg(error):
            assert response.url.startswith(expected_url)
    else:
        error = f"Expected {expected_url} but got {response.url} instead"
        with assertion_msg(error):
            assert response.url == expected_url


def check_response(
    response: Response,
    status_code: int,
    *,
    location: str = None,
    locations: list = None,
    location_starts_with: str = None,
    body_contains: list = None,
    unexpected_strings: list = None,
):
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
    # avoid circular imports
    from tests.functional.utils.generic import assertion_msg

    with assertion_msg(
        f"Expected {status_code} from {response.url} but got " f"{response.status_code}"
    ):
        assert response.status_code == status_code

    if body_contains:
        with assertion_msg("Expected response with content, got an empty one"):
            assert response.content
        content = response.content.decode("utf-8").lower()
        for string in body_contains:
            with assertion_msg(
                f"Could not find '{string}' in the response from: {response.request.url}"
            ):
                assert string.lower() in content

    if unexpected_strings:
        with assertion_msg("Expected response with content, got an empty one"):
            assert response.content
        content = response.content.decode("utf-8")
        for string in unexpected_strings:
            with assertion_msg("Found unexpected '%s' in response", string):
                assert string not in content

    if location:
        new_location = response.headers.get("Location")
        with assertion_msg(
            "Expected Location header to be: '%s' but got '%s' " "instead.",
            location,
            new_location,
        ):
            assert new_location == location

    if locations:
        new_location = response.headers.get("Location")
        with assertion_msg(
            "Should redirect to one of these %d locations '%s' but instead"
            " was redirected to '%s'",
            len(locations),
            locations,
            new_location,
        ):
            assert new_location in locations

    if location_starts_with:
        new_location = response.headers.get("Location")
        with assertion_msg(
            "Expected Location header to start with: '%s' but got '%s' " "instead.",
            location_starts_with,
            new_location,
        ):
            assert new_location.startswith(location_starts_with)
