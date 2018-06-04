# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    article_common,
    article_list,
    british_council,
    events,
    export_opportunities,
    external_legal_services,
    fas_ui_article,
    fas_ui_company_profile,
    fas_ui_contact_us,
    fas_ui_empty_search_results,
    fas_ui_industries,
    fas_ui_industry,
    fas_ui_landing,
    fas_ui_search_results,
    fas_ui_thank_you_for_your_message,
    find_a_buyer,
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
    triage_what_do_you_want_to_export,
    visit_britain,
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
    },
    "fas industries": {
        "url": fas_ui_industries.URL,
        "po": fas_ui_industries
    },
    "fas aerospace industry": {
        "url": fas_ui_industry.URLS.AEROSPACE,
        "po": fas_ui_industry
    },
    "fas agritech industry": {
        "url": fas_ui_industry.URLS.AGRITECH,
        "po": fas_ui_industry
    },
    "fas automotive industry": {
        "url": fas_ui_industry.URLS.AUTOMOTIVE,
        "po": fas_ui_industry
    },
    "fas business and government partnerships industry": {
        "url": fas_ui_industry.URLS.BUSINESS_AND_GOVERNMENT_PARTNERSHIPS,
        "po": fas_ui_industry
    },
    "fas consumer retail industry": {
        "url": fas_ui_industry.URLS.CONSUMER_RETAIL,
        "po": fas_ui_industry
    },
    "fas creative services industry": {
        "url": fas_ui_industry.URLS.CREATIVE_SERVICES,
        "po": fas_ui_industry
    },
    "fas cyber security industry": {
        "url": fas_ui_industry.URLS.CYBER_SECURITY,
        "po": fas_ui_industry
    },
    "fas education industry": {
        "url": fas_ui_industry.URLS.EDUCATION,
        "po": fas_ui_industry
    },
    "fas energy industry": {
        "url": fas_ui_industry.URLS.ENERGY,
        "po": fas_ui_industry
    },
    "fas engineering industry": {
        "url": fas_ui_industry.URLS.ENGINEERING,
        "po": fas_ui_industry
    },
    "fas food and drink industry": {
        "url": fas_ui_industry.URLS.FOOD_AND_DRINK,
        "po": fas_ui_industry
    },
    "fas healthcare industry": {
        "url": fas_ui_industry.URLS.HEALTHCARE,
        "po": fas_ui_industry
    },
    "fas infrastructure industry": {
        "url": fas_ui_industry.URLS.INFRASTRUCTURE,
        "po": fas_ui_industry
    },
    "fas innovation industry": {
        "url": fas_ui_industry.URLS.INNOVATION,
        "po": fas_ui_industry
    },
    "fas legal services industry": {
        "url": fas_ui_industry.URLS.LEGAL_SERVICES,
        "po": fas_ui_industry
    },
    "fas life sciences industry": {
        "url": fas_ui_industry.URLS.LIFE_SCIENCES,
        "po": fas_ui_industry
    },
    "fas marine industry": {
        "url": fas_ui_industry.URLS.MARINE,
        "po": fas_ui_industry
    },
    "fas professional and financial services industry": {
        "url": fas_ui_industry.URLS.PROFESSIONAL_AND_FINANCIAL_SERVICES,
        "po": fas_ui_industry
    },
    "fas space industry": {
        "url": fas_ui_industry.URLS.SPACE,
        "po": fas_ui_industry
    },
    "fas sports economy industry": {
        "url": fas_ui_industry.URLS.SPORTS_ECONOMY,
        "po": fas_ui_industry
    },
    "fas technology industry": {
        "url": fas_ui_industry.URLS.TECHNOLOGY,
        "po": fas_ui_industry
    },
    "fas company profile": {
        "url": fas_ui_company_profile.URL,
        "po": fas_ui_company_profile
    },
    "fas article": {
        "url": fas_ui_article.URL,
        "po": fas_ui_article
    }
}

EXTERNAL_SITES_PAGE_REGISTRY = {
    "legal services landing": {
        "url": external_legal_services.URL,
        "po": external_legal_services
    }

}

PAGES = {}
PAGES.update(EXRED_PAGE_REGISTRY)
PAGES.update(FAS_PAGE_REGISTRY)
PAGES.update(EXTERNAL_SITES_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return PAGES[page_name.lower()]["url"]


def get_page_object(page_name: str):
    return PAGES[page_name.lower()]["po"]
