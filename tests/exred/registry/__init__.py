# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""
from pages import (
    home,
    triage_1st_question,
    triage_2nd_question,
    triage_3rd_question,
    triage_4th_question,
    triage_result,
)

from utils import get_absolute_url

EXRED_PAGE_REGISTRY = {
    "home": {
        "url": "ExRed Home",
        "po": home
    },
    "triage - 1st question": {
        "url": "ExRed Triage - 1st question",
        "po": triage_1st_question
    },
    "triage - 2nd question": {
        "url": "ExRed Triage - 2nd question",
        "po": triage_2nd_question
    },
    "triage - 3rd question": {
        "url": "ExRed Triage - 3rd question",
        "po": triage_3rd_question
    },
    "triage - 4th question": {
        "url": "ExRed Triage - 4th question",
        "po": triage_4th_question
    },
    "triage - result": {
        "url": "ExRed Triage - result",
        "po": triage_result
    },
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(EXRED_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])


def get_page_object(page_name: str):
    return PAGE_REGISTRY[page_name.lower()]["po"]
