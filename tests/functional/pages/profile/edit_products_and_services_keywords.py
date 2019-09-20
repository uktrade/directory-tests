# -*- coding: utf-8 -*-
"""Profile - Edit Company's products and services keywords"""
from typing import List
from urllib.parse import urljoin

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_url, make_request

SERVICE = Service.PROFILE
NAME = "Edit company's products and services (keywords)"
TYPE = PageType.FORM
URL = URLs.PROFILE_ADD_PRODUCTS_AND_SERVICES.absolute
EXPECTED_STRINGS = ["Choose the products and services"]


def should_be_here(response: Response, *, industry: str = None):
    if industry:
        url = urljoin(URL, industry + "/")
    else:
        url = URL
    check_url(response, url)


def submit(
    session: Session,
    industry: str,
    keywords: List[str],
    *,
    separator: str = "|",
    send_as_data: bool = True,
    send_as_files: bool = False,
) -> Response:
    error = f"Can send data only as data or as files"
    assert (send_as_data and not send_as_files) or (
        send_as_files and not send_as_data
    ), error
    headers = {"Referer": URL}
    data = {
        "input-autocomplete": f"{separator}".join(keywords),
        "expertise_products_services": f"{separator}".join(keywords),
    }
    url = urljoin(URL, industry + "/")
    if send_as_data and not send_as_files:
        return make_request(
            Method.POST, url, session=session, headers=headers, data=data
        )
    elif send_as_files and not send_as_data:
        return make_request(
            Method.POST, url, session=session, headers=headers, files=data
        )
