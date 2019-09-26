# -*- coding: utf-8 -*-
"""Find a Buyer - Remove Collaborator page"""
from typing import List, Tuple

from requests import Response, Session
from scrapy import Selector

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.generic import Method, make_request
from tests.functional.utils.request import check_response

SERVICE = Service.FAB
NAME = "Remove collaborator"
TYPE = PageType.FORM
URL = URLs.FAB_ACCOUNT_REMOVE_COLLABORATOR.absolute
EXPECTED_STRINGS = [
    "Remove user from account",
    "Select the emails you would like to remove",
    "Confirm",
    "Cancel",
]

EXPECTED_STRINGS_NO_COLLABORATORS = [
    "Your company has no collaborators",
    "Click",
    "here",
    "to go back",
]


def should_be_here(response: Response, *, have_collaborators: bool = True):
    if have_collaborators:
        check_response(response, 200, body_contains=EXPECTED_STRINGS)
    else:
        check_response(response, 200, body_contains=EXPECTED_STRINGS_NO_COLLABORATORS)


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.PROFILE_BUSINESS_PROFILE.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def extract_email_to_id_mapping(label: str) -> Tuple[str, str]:
    element_id = Selector(text=label).css("label::attr(for)").extract()[0]
    email = Selector(text=label).css("label::text").extract()[0]
    return email, element_id


def extract_sso_id(html: str, email_to_element_id: Tuple[str, str]):
    email, element_id = email_to_element_id
    css_selector = f"#{element_id}::attr(value)"
    value = Selector(text=html).css(css_selector).extract()
    return email, value[0] if value else None


def extract_email_to_sso_id(html: str, mapping: dict) -> dict:
    return dict(
        map(
            lambda email_to_element_id: extract_sso_id(html, email_to_element_id),
            mapping.items(),
        )
    )


def extract_sso_ids(response: Response) -> dict:
    content = response.content.decode("utf-8")
    label_css = "label[for]"
    labels = Selector(text=content).css(label_css).extract()
    email_to_element_id_map = dict(map(extract_email_to_id_mapping, labels))
    return extract_email_to_sso_id(content, email_to_element_id_map)


def remove(session: Session, token: str, sso_ids: List[str]) -> Response:
    data = {"csrfmiddlewaretoken": token, "sso_ids": sso_ids}
    headers = {"Referer": URL}
    return make_request(Method.POST, URL, session=session, data=data, headers=headers)


def should_not_see_collaborator(response: Response, collaborator_email: str):
    check_response(response, 200, unexpected_strings=[collaborator_email])
