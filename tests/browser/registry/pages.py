# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import (
    exread_article_common,
    exread_article_list,
    external_british_council,
    external_events,
    exopps_home,
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
    fab_home,
    exread_footer,
    exread_get_finance,
    exread_header,
    exread_home,
    exread_interim_exporting_opportunities,
    international,
    invest_contact_us,
    invest_feedback,
    invest_footer,
    invest_guide,
    invest_header,
    invest_home,
    invest_industries,
    invest_industry,
    exread_personalised_journey,
    soo_home,
    exread_share_on_facebook,
    exread_share_on_linkedin,
    exread_share_on_twitter,
    sso_profile_about,
    sso_registration,
    sso_registration_confirmation,
    sso_sign_in,
    sso_sign_out,
    exread_triage_are_you_registered_with_companies_house,
    exread_triage_are_you_regular_exporter,
    exread_triage_company_name,
    exread_triage_create_your_export_journey,
    triage_do_you_use_online_marketplaces,
    triage_have_you_exported,
    triage_summary,
    triage_what_do_you_want_to_export,
    external_visit_britain,
)

EXRED_PAGE_REGISTRY = {
    "home": {"url": exread_home.URL, "po": exread_home},
    "home page": {"url": exread_home.URL, "po": exread_home},
    "triage - what do you want to export": {
        "url": triage_what_do_you_want_to_export.URL,
        "po": triage_what_do_you_want_to_export,
    },
    "triage - have you exported before": {
        "url": triage_have_you_exported.URL,
        "po": triage_have_you_exported,
    },
    "triage - are you regular exporter": {
        "url": exread_triage_are_you_regular_exporter.URL,
        "po": exread_triage_are_you_regular_exporter,
    },
    "triage - do you use online marketplaces": {
        "url": triage_do_you_use_online_marketplaces.URL,
        "po": triage_do_you_use_online_marketplaces,
    },
    "triage - are you registered with companies house": {
        "url": exread_triage_are_you_registered_with_companies_house.URL,
        "po": exread_triage_are_you_registered_with_companies_house,
    },
    "triage - what is your company name": {
        "url": exread_triage_company_name.URL,
        "po": exread_triage_company_name,
    },
    "triage - summary": {"url": triage_summary.URL, "po": triage_summary},
    "personalised journey": {
        "url": exread_personalised_journey.URL,
        "po": exread_personalised_journey,
    },
    "header menu": {"url": None, "po": exread_header},
    "footer links": {"url": None, "po": exread_footer},
    "interim export opportunities": {
        "url": exread_interim_exporting_opportunities.URL,
        "po": exread_interim_exporting_opportunities,
    },
    "find a buyer": {"url": fab_home.URL, "po": fab_home},
    "find a supplier": {"url": fas_ui_landing.URL, "po": fas_ui_landing},
    "create your export journey": {
        "url": exread_triage_create_your_export_journey.URL,
        "po": exread_triage_create_your_export_journey,
    },
    "british council": {"url": external_british_council.URL, "po": external_british_council},
    "visit britain": {"url": external_visit_britain.URL, "po": external_visit_britain},
    "selling online overseas": {
        "url": soo_home.URL,
        "po": soo_home,
    },
    "export opportunities": {
        "url": exopps_home.URL,
        "po": exopps_home,
    },
    "events": {"url": external_events.URL, "po": external_events},
    "get finance": {"url": exread_get_finance.URL, "po": exread_get_finance},
    "sso registration": {"url": sso_registration.URL, "po": sso_registration},
    "sso sign in": {"url": sso_sign_in.URL, "po": sso_sign_in},
    "sso sign out": {"url": sso_sign_out.URL, "po": sso_sign_out},
    "sso registration confirmation": {
        "url": sso_registration_confirmation.URL,
        "po": sso_registration_confirmation,
    },
    "sso profile about": {
        "url": sso_profile_about.URL,
        "po": sso_profile_about,
    },
    "article": {"url": None, "po": exread_article_common},
    "article list": {"url": None, "po": exread_article_list},
    "share on facebook": {
        "url": exread_share_on_facebook.URL,
        "po": exread_share_on_facebook,
    },
    "share on linkedin": {
        "url": exread_share_on_linkedin.URL,
        "po": exread_share_on_linkedin,
    },
    "share on twitter": {"url": exread_share_on_twitter.URL, "po": exread_share_on_twitter},
    "international": {"url": international.URL, "po": international},
}


FAS_PAGE_REGISTRY = {
    "fas landing": {"url": fas_ui_landing.URL, "po": fas_ui_landing},
    "fas empty search results": {
        "url": fas_ui_empty_search_results.URL,
        "po": fas_ui_empty_search_results,
    },
    "fas search results": {
        "url": fas_ui_search_results.URL,
        "po": fas_ui_search_results,
    },
    "fas contact us": {"url": fas_ui_contact_us.URL, "po": fas_ui_contact_us},
    "fas thank you for your message": {
        "url": fas_ui_thank_you_for_your_message.URL,
        "po": fas_ui_thank_you_for_your_message,
    },
    "fas industry": {"url": fas_ui_industry.URL, "po": fas_ui_industry},
    "fas industries": {"url": fas_ui_industries.URL, "po": fas_ui_industries},
    "fas aerospace industry": {
        "url": fas_ui_industry.URLS.AEROSPACE,
        "po": fas_ui_industry,
    },
    "fas agritech industry": {
        "url": fas_ui_industry.URLS.AGRITECH,
        "po": fas_ui_industry,
    },
    "fas automotive industry": {
        "url": fas_ui_industry.URLS.AUTOMOTIVE,
        "po": fas_ui_industry,
    },
    "fas business and government partnerships industry": {
        "url": fas_ui_industry.URLS.BUSINESS_AND_GOVERNMENT_PARTNERSHIPS,
        "po": fas_ui_industry,
    },
    "fas consumer retail industry": {
        "url": fas_ui_industry.URLS.CONSUMER_RETAIL,
        "po": fas_ui_industry,
    },
    "fas creative services industry": {
        "url": fas_ui_industry.URLS.CREATIVE_SERVICES,
        "po": fas_ui_industry,
    },
    "fas cyber security industry": {
        "url": fas_ui_industry.URLS.CYBER_SECURITY,
        "po": fas_ui_industry,
    },
    "fas education industry": {
        "url": fas_ui_industry.URLS.EDUCATION,
        "po": fas_ui_industry,
    },
    "fas energy industry": {
        "url": fas_ui_industry.URLS.ENERGY,
        "po": fas_ui_industry,
    },
    "fas engineering industry": {
        "url": fas_ui_industry.URLS.ENGINEERING,
        "po": fas_ui_industry,
    },
    "fas food and drink industry": {
        "url": fas_ui_industry.URLS.FOOD_AND_DRINK,
        "po": fas_ui_industry,
    },
    "fas healthcare industry": {
        "url": fas_ui_industry.URLS.HEALTHCARE,
        "po": fas_ui_industry,
    },
    "fas infrastructure industry": {
        "url": fas_ui_industry.URLS.INFRASTRUCTURE,
        "po": fas_ui_industry,
    },
    "fas innovation industry": {
        "url": fas_ui_industry.URLS.INNOVATION,
        "po": fas_ui_industry,
    },
    "fas legal services industry": {
        "url": fas_ui_industry.URLS.LEGAL_SERVICES,
        "po": fas_ui_industry,
    },
    "fas life sciences industry": {
        "url": fas_ui_industry.URLS.LIFE_SCIENCES,
        "po": fas_ui_industry,
    },
    "fas marine industry": {
        "url": fas_ui_industry.URLS.MARINE,
        "po": fas_ui_industry,
    },
    "fas professional and financial services industry": {
        "url": fas_ui_industry.URLS.PROFESSIONAL_AND_FINANCIAL_SERVICES,
        "po": fas_ui_industry,
    },
    "fas space industry": {
        "url": fas_ui_industry.URLS.SPACE,
        "po": fas_ui_industry,
    },
    "fas sports economy industry": {
        "url": fas_ui_industry.URLS.SPORTS_ECONOMY,
        "po": fas_ui_industry,
    },
    "fas technology industry": {
        "url": fas_ui_industry.URLS.TECHNOLOGY,
        "po": fas_ui_industry,
    },
    "fas company profile": {
        "url": fas_ui_company_profile.URL,
        "po": fas_ui_company_profile,
    },
    "fas article": {"url": fas_ui_article.URL, "po": fas_ui_article},
}

EXTERNAL_SITES_PAGE_REGISTRY = {
    "legal services landing": {
        "url": external_legal_services.URL,
        "po": external_legal_services,
    }
}

INVEST_PAGE_REGISTRY = {
    "invest - home": {"url": invest_home.URL, "po": invest_home},
    "invest - industry": {"url": invest_industry.URL, "po": invest_industry},
    "invest - header": {"url": None, "po": invest_header},
    "invest - footer": {"url": None, "po": invest_footer},
    "invest - contact us": {
        "url": invest_contact_us.URL,
        "po": invest_contact_us,
    },
    "invest - feedback": {"url": invest_feedback.URL, "po": invest_feedback},
    "invest - industries": {
        "url": invest_industries.URL,
        "po": invest_industries,
    },
    "invest - automotive industry": {
        "url": invest_industry.URLS.AUTOMOTIVE,
        "po": invest_industry,
    },
    "invest - capital investment industry": {
        "url": invest_industry.URLS.CAPITAL_INVESTMENT,
        "po": invest_industry,
    },
    "invest - creative industries industry": {
        "url": invest_industry.URLS.CREATIVE_INDUSTRIES,
        "po": invest_industry,
    },
    "invest - financial services industry": {
        "url": invest_industry.URLS.FINANCIAL_SERVICES,
        "po": invest_industry,
    },
    "invest - health and life sciences industry": {
        "url": invest_industry.URLS.HEALTH_AND_LIFE_SCIENCES,
        "po": invest_industry,
    },
    "invest - technology industry": {
        "url": invest_industry.URLS.TECHNOLOGY,
        "po": invest_industry,
    },
    "invest - advanced manufacturing industry": {
        "url": invest_industry.URLS.ADVANCED_MANUFACTURING,
        "po": invest_industry,
    },
    "invest - aerospace industry": {
        "url": invest_industry.URLS.AEROSPACE,
        "po": invest_industry,
    },
    "invest - agri-tech industry": {
        "url": invest_industry.URLS.AGRI_TECH,
        "po": invest_industry,
    },
    "invest - asset management industry": {
        "url": invest_industry.URLS.ASSET_MANAGEMENT,
        "po": invest_industry,
    },
    "invest - automotive research and development industry": {
        "url": invest_industry.URLS.AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT,
        "po": invest_industry,
    },
    "invest - automotive supply chain industry": {
        "url": invest_industry.URLS.AUTOMOTIVE_SUPPLY_CHAIN,
        "po": invest_industry,
    },
    "invest - chemicals industry": {
        "url": invest_industry.URLS.CHEMICALS,
        "po": invest_industry,
    },
    "invest - creative content and production industry": {
        "url": invest_industry.URLS.CREATIVE_CONTENT_AND_PRODUCTION,
        "po": invest_industry,
    },
    "invest - data analytics industry": {
        "url": invest_industry.URLS.DATA_ANALYTICS,
        "po": invest_industry,
    },
    "invest - digital media industry": {
        "url": invest_industry.URLS.DIGITAL_MEDIA,
        "po": invest_industry,
    },
    "invest - electrical networks industry": {
        "url": invest_industry.URLS.ELECTRICAL_NETWORKS,
        "po": invest_industry,
    },
    "invest - energy industry": {
        "url": invest_industry.URLS.ENERGY,
        "po": invest_industry,
    },
    "invest - energy from waste industry": {
        "url": invest_industry.URLS.ENERGY_FROM_WASTE,
        "po": invest_industry,
    },
    "invest - financial technology industry": {
        "url": invest_industry.URLS.FINANCIAL_TECHNOLOGY,
        "po": invest_industry,
    },
    "invest - food and drink industry": {
        "url": invest_industry.URLS.FOOD_AND_DRINK,
        "po": invest_industry,
    },
    "invest - free-from foods industry": {
        "url": invest_industry.URLS.FREE_FROM_FOODS,
        "po": invest_industry,
    },
    "invest - meat, poultry and dairy industry": {
        "url": invest_industry.URLS.MEAT_POULTRY_AND_DAIRY,
        "po": invest_industry,
    },
    "invest - medical technology industry": {
        "url": invest_industry.URLS.MEDICAL_TECHNOLOGY,
        "po": invest_industry,
    },
    "invest - motorsport industry": {
        "url": invest_industry.URLS.MOTORSPORT,
        "po": invest_industry,
    },
    "invest - nuclear energy industry": {
        "url": invest_industry.URLS.NUCLEAR_ENERGY,
        "po": invest_industry,
    },
    "invest - offshore wind energy industry": {
        "url": invest_industry.URLS.OFFSHORE_WIND_ENERGY,
        "po": invest_industry,
    },
    "invest - oil and gas industry": {
        "url": invest_industry.URLS.OIL_AND_GAS,
        "po": invest_industry,
    },
    "invest - pharmaceutical manufacturing industry": {
        "url": invest_industry.URLS.PHARMACEUTICAL_MANUFACTURING,
        "po": invest_industry,
    },
    "invest - retail industry": {
        "url": invest_industry.URLS.RETAIL,
        "po": invest_industry,
    },
    "invest - guide": {"url": invest_guide.URL, "po": invest_guide},
    "invest - uk setup guide": {"url": invest_guide.URL, "po": invest_guide},
    "invest - apply for a uk visa guide": {
        "url": invest_guide.URLS.APPLY_FOR_A_UK_VISA,
        "po": invest_guide,
    },
    "invest - establish a base for business in the uk guide": {
        "url": invest_guide.URLS.ESTABLISHED_A_BASE_FOR_BUSINESS_IN_THE_UK,
        "po": invest_guide,
    },
    "invest - hire skilled workers for your uk operations guide": {
        "url": invest_guide.URLS.HIRE_SKILLED_WORKERS_FOR_YOUR_UK_OPERATIONS,
        "po": invest_guide,
    },
    "invest - open a uk business bank account guide": {
        "url": invest_guide.URLS.OPEN_A_BUSINESS_BANK_ACCOUNT,
        "po": invest_guide,
    },
    "invest - set up a company in the uk guide": {
        "url": invest_guide.URLS.SET_UP_A_COMPANY_IN_THE_UK,
        "po": invest_guide,
    },
}

PAGES = {}
PAGES.update(EXRED_PAGE_REGISTRY)
PAGES.update(FAS_PAGE_REGISTRY)
PAGES.update(EXTERNAL_SITES_PAGE_REGISTRY)
PAGES.update(INVEST_PAGE_REGISTRY)


def get_page_url(page_name: str):
    return PAGES[page_name.lower()]["url"]


def get_page_object(page_name: str):
    return PAGES[page_name.lower()]["po"]
