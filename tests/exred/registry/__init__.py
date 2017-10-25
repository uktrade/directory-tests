# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    home,
    triage_what_is_your_sector,
    triage_have_you_exported,
    triage_are_you_regular_exporter,
    triage_company_name_or_sole_trader,
    triage_result,
    personalised_journey,
    triage_do_you_use_online_marketplaces
)


EXRED_PAGE_REGISTRY = {
    "home": {
        "url": home.URL,
        "po": home
    },
    "triage - what is your sector": {
        "url": triage_what_is_your_sector.URL,
        "po": triage_what_is_your_sector
    },
    "triage - have you exported before": {
        "url": triage_have_you_exported.URL,
        "po": triage_have_you_exported
    },
    "triage - are you regular exporter": {
        "url": triage_are_you_regular_exporter.URL,
        "po": triage_are_you_regular_exporter
    },
    "triage - do you use online marketplaces": {
        "url": triage_do_you_use_online_marketplaces.URL,
        "po": triage_do_you_use_online_marketplaces
    },
    "triage - company name or sole trader": {
        "url": triage_company_name_or_sole_trader.URL,
        "po": triage_company_name_or_sole_trader
    },
    "triage - result": {
        "url": triage_result.URL,
        "po": triage_result
    },
    "personalised journey": {
        "url": personalised_journey.URL,
        "po": personalised_journey
    },
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(EXRED_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])


def get_page_object(page_name: str):
    return PAGE_REGISTRY[page_name.lower()]["po"]
