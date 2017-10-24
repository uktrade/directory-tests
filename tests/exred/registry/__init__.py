# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""
from pages import (
    home,
    triage_1st_question,
    triage_2nd_question,
    triage_3rd_question,
    triage_4th_question,
    triage_result,
    personalised_journey
)

from utils import get_absolute_url

EXRED_PAGE_REGISTRY = {
    "home": {
        "url": "ExRed Home",
        "po": home
    },
    "triage - what is your sector": {
        "url": "ExRed Triage - what is your sector",
        "po": triage_what_is_your_sector
    },
    "triage - have you exported before": {
        "url": "ExRed Triage - have you exported before",
        "po": triage_have_you_exported
    },
    "triage - are you regular exporter": {
        "url": "ExRed Triage - are you regular exporter",
        "po": triage_are_you_regular_exporter
    },
    "triage - do you use online marketplaces": {
        "url": "ExRed Triage - do you use online marketplaces",
        "po": triage_do_you_use_online_marketplaces
    },
    "triage - company name or sole trader": {
        "url": "ExRed Triage - company name or sole trader",
        "po": triage_company_name_or_sole_trader
    },
    "triage - result": {
        "url": "ExRed Triage - result",
        "po": triage_result
    },
    "personalised journey": {
        "url": "ExRed Personalised Journey",
        "po": personalised_journey
    },
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(EXRED_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])


def get_page_object(page_name: str):
    return PAGE_REGISTRY[page_name.lower()]["po"]
