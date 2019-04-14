# -*- coding: utf-8 -*-
"""Profile - Edit Company's products and services keywords"""
from typing import List
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_url, make_request

SERVICE = Services.PROFILE
NAME = "Edit company's products and services (keywords)"
TYPE = "form"
URL = get_absolute_url("profile:add-products-and-services")
EXPECTED_STRINGS = [
    "Add publicity services",
    "Choose the products and services"
]


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
        separator: str = "|"
) -> Response:
    headers = {"Referer": URL}
    data = {
        "input-autocomplete": f"{separator}".join(keywords),
        "expertise_products_services": f"{separator}".join(keywords),
    }
    url = urljoin(URL, industry + "/")
    return make_request(
        Method.POST, url, session=session, headers=headers, data=data
    )
