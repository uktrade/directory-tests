# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    article_common,
    article_list,
    british_council,
    events,
    export_opportunities,
    find_a_buyer,
    fas_ui_landing,
    footer,
    get_finance,
    header,
    home,
    interim_exporting_opportunities,
    international,
    invest_in_great,
    personalised_journey,
    selling_online_overseas,
    share_on_facebook,
    share_on_linkedin,
    share_on_twitter,
    sso_profile_about,
    sso_registration,
    sso_registration_confirmation,
    sso_sign_in,
    sso_sign_out,
    triage_are_you_registered_with_companies_house,
    triage_are_you_regular_exporter,
    triage_company_name,
    triage_create_your_export_journey,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_summary,
    visit_britain,
    triage_what_do_you_want_to_export,
    fas_ui_empty_search_results,
    fas_ui_search_results,
    fas_ui_contact_us,
    fas_ui_thank_you_for_your_message,
    fas_ui_industry
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
    "find a supplier": {
        "url": fas_ui_landing.URL,
        "po": fas_ui_landing
    },
    "invest in great": {
        "url": invest_in_great.URL,
        "po": invest_in_great
    },
    "create your export journey": {
        "url": triage_create_your_export_journey.URL,
        "po": triage_create_your_export_journey
    },
    "british council": {
        "url": british_council.URL,
        "po": british_council
    },
    "visit britain": {
        "url": visit_britain.URL,
        "po": visit_britain
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
    "sso profile about": {
        "url": sso_profile_about.URL,
        "po": sso_profile_about
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
    "international": {
        "url": international.URL,
        "po": international
    },
}


FAS_PAGE_REGISTRY = {
    "fas landing": {
        "url": fas_ui_landing.URL,
        "po": fas_ui_landing
    },
    "fas empty search results": {
        "url": fas_ui_empty_search_results.URL,
        "po": fas_ui_empty_search_results
    },
    "fas search results": {
        "url": fas_ui_search_results.URL,
        "po": fas_ui_search_results
    },
    "fas contact us": {
        "url": fas_ui_contact_us.URL,
        "po": fas_ui_contact_us
    },
    "fas thank you for your message": {
        "url": fas_ui_thank_you_for_your_message.URL,
        "po": fas_ui_thank_you_for_your_message
    },
    "fas industry": {
        "url": fas_ui_industry.URL,
        "po": fas_ui_industry
    }
}


PAGES = {}
PAGES.update(EXRED_PAGE_REGISTRY)
PAGES.update(FAS_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return PAGES[page_name.lower()]["url"]


def get_page_object(page_name: str):
    return PAGES[page_name.lower()]["po"]
