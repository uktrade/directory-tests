# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    article_common,
    article_list,
    events,
    export_opportunities,
    find_a_buyer,
    footer,
    get_finance,
    header,
    home,
    interim_exporting_opportunities,
    personalised_journey,
    selling_online_overseas,
    share_on_facebook,
    share_on_linkedin,
    share_on_twitter,
    sso_registration,
    sso_registration_confirmation,
    sso_sign_in,
    sso_sign_out,
    triage_are_you_registered_with_companies_house,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_summary,
    triage_what_do_you_want_to_export
)

EXRED_PAGE_REGISTRY = {
    "home": {
        "url": home.URL,
        "po": home
    },
    "home page": {
        "url": home.URL,
        "po": home
    },
    "triage - what do you want to export": {
        "url": triage_what_do_you_want_to_export.URL,
        "po": triage_what_do_you_want_to_export
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
    "triage - are you registered with companies house": {
        "url": triage_are_you_registered_with_companies_house.URL,
        "po": triage_are_you_registered_with_companies_house
    },
    "triage - what is your company name": {
        "url": triage_company_name.URL,
        "po": triage_company_name
    },
    "triage - summary": {
        "url": triage_summary.URL,
        "po": triage_summary
    },
    "personalised journey": {
        "url": personalised_journey.URL,
        "po": personalised_journey
    },
    "header menu": {
        "url": None,
        "po": header
    },
    "footer links": {
        "url": None,
        "po": footer
    },
    "interim export opportunities": {
        "url": interim_exporting_opportunities.URL,
        "po": interim_exporting_opportunities
    },
    "find a buyer": {
        "url": find_a_buyer.URL,
        "po": find_a_buyer
    },
    "selling online overseas": {
        "url": selling_online_overseas.URL,
        "po": selling_online_overseas
    },
    "export opportunities": {
        "url": export_opportunities.URL,
        "po": export_opportunities
    },
    "events": {
        "url": events.URL,
        "po": events
    },
    "get finance": {
        "url": get_finance.URL,
        "po": get_finance
    },
    "sso registration": {
        "url": sso_registration.URL,
        "po": sso_registration
    },
    "sso sign in": {
        "url": sso_sign_in.URL,
        "po": sso_sign_in
    },
    "sso sign out": {
        "url": sso_sign_out.URL,
        "po": sso_sign_out
    },
    "sso registration confirmation": {
        "url": sso_registration_confirmation.URL,
        "po": sso_registration_confirmation
    },
    "article": {
        "url": None,
        "po": article_common
    },
    "article list": {
        "url": None,
        "po": article_list
    },
    "share on facebook": {
        "url": share_on_facebook.URL,
        "po": share_on_facebook
    },
    "share on linkedin": {
        "url": share_on_linkedin.URL,
        "po": share_on_linkedin
    },
    "share on twitter": {
        "url": share_on_twitter.URL,
        "po": share_on_twitter
    },
}


def get_page_url(page_name: str):
    return EXRED_PAGE_REGISTRY[page_name.lower()]["url"]


def get_page_object(page_name: str):
    return EXRED_PAGE_REGISTRY[page_name.lower()]["po"]
