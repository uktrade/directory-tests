# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""
from tests.exred.pages import (
    exred_home
)

from tests import get_absolute_url

EXRED_PAGE_REGISTRY = {
    "home": {
        "url": "ui-supplier:landing",
        "po": exred_home
    },
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(EXRED_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])


def get_page_object(page_name: str):
    return PAGE_REGISTRY[page_name.lower()]["po"]
