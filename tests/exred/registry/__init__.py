# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""
from pages import (
    exred_home,
    exred_triage_1st_question
)

from utils import get_absolute_url

EXRED_PAGE_REGISTRY = {
    "home": {
        "url": "exred:home",
        "po": exred_home
    },
    "triage - 1st question": {
        "url": "exred:triage-1st-question",
        "po": exred_triage_1st_question
    }
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(EXRED_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])


def get_page_object(page_name: str):
    return PAGE_REGISTRY[page_name.lower()]["po"]
