# -*- coding: utf-8 -*-
"""ExRed Page Object Registry"""

from pages import exopps
from pages.external import (
    british_council_home,
    events_home,
    legal_services_home,
    visit_britain_home,
)
from pages import fab
from pages import fas
from pages import sso
from pages import invest
from pages import soo
from pages import exread


EXRED_PAGE_REGISTRY = {
    "home": {"url": exread.home.URL, "po": exread.home},
    "home page": {"url": exread.home.URL, "po": exread.home},
    "triage - what do you want to export": {
        "url": exread.triage_what_do_you_want_to_export.URL,
        "po": exread.triage_what_do_you_want_to_export,
    },
    "triage - have you exported before": {
        "url": exread.triage_have_you_exported.URL,
        "po": exread.triage_have_you_exported,
    },
    "triage - are you regular exporter": {
        "url": exread.triage_are_you_regular_exporter.URL,
        "po": exread.triage_are_you_regular_exporter,
    },
    "triage - do you use online marketplaces": {
        "url": exread.triage_do_you_use_online_marketplaces.URL,
        "po": exread.triage_do_you_use_online_marketplaces,
    },
    "triage - are you registered with companies house": {
        "url": exread.triage_are_you_registered_with_companies_house.URL,
        "po": exread.triage_are_you_registered_with_companies_house,
    },
    "triage - what is your company name": {
        "url": exread.triage_company_name.URL,
        "po": exread.triage_company_name,
    },
    "triage - summary": {"url": exread.triage_summary.URL, "po": exread.triage_summary},
    "personalised journey": {
        "url": exread.personalised_journey.URL,
        "po": exread.personalised_journey,
    },
    "header menu": {"url": None, "po": exread.header},
    "footer links": {"url": None, "po": exread.footer},
    "interim export opportunities": {
        "url": exread.interim_exporting_opportunities.URL,
        "po": exread.interim_exporting_opportunities,
    },
    "find a buyer": {"url": fab.home.URL, "po": fab.home},
    "find a supplier": {"url": fas.home.URL, "po": fas.home},
    "create your export journey": {
        "url": exread.triage_create_your_export_journey.URL,
        "po": exread.triage_create_your_export_journey,
    },
    "british council": {"url": british_council_home.URL, "po": british_council_home},
    "visit britain": {"url": visit_britain_home.URL, "po": visit_britain_home},
    "selling online overseas": {"url": soo.home.URL, "po": soo.home},
    "export opportunities": {
        "url": exopps.home.URL,
        "po": exopps.home,
    },
    "events": {"url": events_home.URL, "po": events_home},
    "get finance": {"url": exread.get_finance.URL, "po": exread.get_finance},
    "sso registration": {"url": sso.registration.URL, "po": sso.registration},
    "sso sign in": {"url": sso.sign_in.URL, "po": sso.sign_in},
    "sso sign out": {"url": sso.sign_out.URL, "po": sso.sign_out},
    "sso registration confirmation": {
        "url": sso.registration_confirmation.URL,
        "po": sso.registration_confirmation,
    },
    "sso profile about": {
        "url": sso.profile_about.URL,
        "po": sso.profile_about,
    },
    "article": {"url": None, "po": exread.article_common},
    "article list": {"url": None, "po": exread.article_list},
    "share on facebook": {
        "url": exread.share_on_facebook.URL,
        "po": exread.share_on_facebook,
    },
    "share on linkedin": {
        "url": exread.share_on_linkedin.URL,
        "po": exread.share_on_linkedin,
    },
    "share on twitter": {"url": exread.share_on_twitter.URL, "po": exread.share_on_twitter},
    "international": {"url": exread.international.URL, "po": exread.international},
}


FAS_PAGE_REGISTRY = {
    "fas landing": {"url": fas.home.URL, "po": fas.home},
    "fas empty search results": {
        "url": fas.empty_search_results.URL,
        "po": fas.empty_search_results,
    },
    "fas search results": {
        "url": fas.search_results.URL,
        "po": fas.search_results,
    },
    "fas contact us": {"url": fas.contact_us.URL, "po": fas.contact_us},
    "fas thank you for your message": {
        "url": fas.thank_you_for_your_message.URL,
        "po": fas.thank_you_for_your_message,
    },
    "fas industry": {"url": fas.industry.URL, "po": fas.industry},
    "fas industries": {"url": fas.industries.URL, "po": fas.industries},
    "fas aerospace industry": {
        "url": fas.industry.URLS.AEROSPACE,
        "po": fas.industry,
    },
    "fas agritech industry": {
        "url": fas.industry.URLS.AGRITECH,
        "po": fas.industry,
    },
    "fas automotive industry": {
        "url": fas.industry.URLS.AUTOMOTIVE,
        "po": fas.industry,
    },
    "fas business and government partnerships industry": {
        "url": fas.industry.URLS.BUSINESS_AND_GOVERNMENT_PARTNERSHIPS,
        "po": fas.industry,
    },
    "fas consumer retail industry": {
        "url": fas.industry.URLS.CONSUMER_RETAIL,
        "po": fas.industry,
    },
    "fas creative services industry": {
        "url": fas.industry.URLS.CREATIVE_SERVICES,
        "po": fas.industry,
    },
    "fas cyber security industry": {
        "url": fas.industry.URLS.CYBER_SECURITY,
        "po": fas.industry,
    },
    "fas education industry": {
        "url": fas.industry.URLS.EDUCATION,
        "po": fas.industry,
    },
    "fas energy industry": {
        "url": fas.industry.URLS.ENERGY,
        "po": fas.industry,
    },
    "fas engineering industry": {
        "url": fas.industry.URLS.ENGINEERING,
        "po": fas.industry,
    },
    "fas food and drink industry": {
        "url": fas.industry.URLS.FOOD_AND_DRINK,
        "po": fas.industry,
    },
    "fas healthcare industry": {
        "url": fas.industry.URLS.HEALTHCARE,
        "po": fas.industry,
    },
    "fas infrastructure industry": {
        "url": fas.industry.URLS.INFRASTRUCTURE,
        "po": fas.industry,
    },
    "fas innovation industry": {
        "url": fas.industry.URLS.INNOVATION,
        "po": fas.industry,
    },
    "fas legal services industry": {
        "url": fas.industry.URLS.LEGAL_SERVICES,
        "po": fas.industry,
    },
    "fas life sciences industry": {
        "url": fas.industry.URLS.LIFE_SCIENCES,
        "po": fas.industry,
    },
    "fas marine industry": {
        "url": fas.industry.URLS.MARINE,
        "po": fas.industry,
    },
    "fas professional and financial services industry": {
        "url": fas.industry.URLS.PROFESSIONAL_AND_FINANCIAL_SERVICES,
        "po": fas.industry,
    },
    "fas space industry": {
        "url": fas.industry.URLS.SPACE,
        "po": fas.industry,
    },
    "fas sports economy industry": {
        "url": fas.industry.URLS.SPORTS_ECONOMY,
        "po": fas.industry,
    },
    "fas technology industry": {
        "url": fas.industry.URLS.TECHNOLOGY,
        "po": fas.industry,
    },
    "fas company profile": {
        "url": fas.company_profile.URL,
        "po": fas.company_profile,
    },
    "fas article": {"url": fas.article.URL, "po": fas.article},
}

EXTERNAL_SITES_PAGE_REGISTRY = {
    "legal services landing": {
        "url": legal_services_home.URL,
        "po": legal_services_home,
    }
}

INVEST_PAGE_REGISTRY = {
    "invest - home": {"url": invest.home.URL, "po": invest.home},
    "invest - industry": {"url": invest.industry.URL, "po": invest.industry},
    "invest - header": {"url": None, "po": invest.header},
    "invest - footer": {"url": None, "po": invest.footer},
    "invest - contact us": {
        "url": invest.contact_us.URL,
        "po": invest.contact_us,
    },
    "invest - feedback": {"url": invest.feedback.URL, "po": invest.feedback},
    "invest - industries": {
        "url": invest.industries.URL,
        "po": invest.industries,
    },
    "invest - automotive industry": {
        "url": invest.industry.URLS.AUTOMOTIVE,
        "po": invest.industry,
    },
    "invest - capital investment industry": {
        "url": invest.industry.URLS.CAPITAL_INVESTMENT,
        "po": invest.industry,
    },
    "invest - creative industries industry": {
        "url": invest.industry.URLS.CREATIVE_INDUSTRIES,
        "po": invest.industry,
    },
    "invest - financial services industry": {
        "url": invest.industry.URLS.FINANCIAL_SERVICES,
        "po": invest.industry,
    },
    "invest - health and life sciences industry": {
        "url": invest.industry.URLS.HEALTH_AND_LIFE_SCIENCES,
        "po": invest.industry,
    },
    "invest - technology industry": {
        "url": invest.industry.URLS.TECHNOLOGY,
        "po": invest.industry,
    },
    "invest - advanced manufacturing industry": {
        "url": invest.industry.URLS.ADVANCED_MANUFACTURING,
        "po": invest.industry,
    },
    "invest - aerospace industry": {
        "url": invest.industry.URLS.AEROSPACE,
        "po": invest.industry,
    },
    "invest - agri-tech industry": {
        "url": invest.industry.URLS.AGRI_TECH,
        "po": invest.industry,
    },
    "invest - asset management industry": {
        "url": invest.industry.URLS.ASSET_MANAGEMENT,
        "po": invest.industry,
    },
    "invest - automotive research and development industry": {
        "url": invest.industry.URLS.AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT,
        "po": invest.industry,
    },
    "invest - automotive supply chain industry": {
        "url": invest.industry.URLS.AUTOMOTIVE_SUPPLY_CHAIN,
        "po": invest.industry,
    },
    "invest - chemicals industry": {
        "url": invest.industry.URLS.CHEMICALS,
        "po": invest.industry,
    },
    "invest - creative content and production industry": {
        "url": invest.industry.URLS.CREATIVE_CONTENT_AND_PRODUCTION,
        "po": invest.industry,
    },
    "invest - data analytics industry": {
        "url": invest.industry.URLS.DATA_ANALYTICS,
        "po": invest.industry,
    },
    "invest - digital media industry": {
        "url": invest.industry.URLS.DIGITAL_MEDIA,
        "po": invest.industry,
    },
    "invest - electrical networks industry": {
        "url": invest.industry.URLS.ELECTRICAL_NETWORKS,
        "po": invest.industry,
    },
    "invest - energy industry": {
        "url": invest.industry.URLS.ENERGY,
        "po": invest.industry,
    },
    "invest - energy from waste industry": {
        "url": invest.industry.URLS.ENERGY_FROM_WASTE,
        "po": invest.industry,
    },
    "invest - financial technology industry": {
        "url": invest.industry.URLS.FINANCIAL_TECHNOLOGY,
        "po": invest.industry,
    },
    "invest - food and drink industry": {
        "url": invest.industry.URLS.FOOD_AND_DRINK,
        "po": invest.industry,
    },
    "invest - free-from foods industry": {
        "url": invest.industry.URLS.FREE_FROM_FOODS,
        "po": invest.industry,
    },
    "invest - meat, poultry and dairy industry": {
        "url": invest.industry.URLS.MEAT_POULTRY_AND_DAIRY,
        "po": invest.industry,
    },
    "invest - medical technology industry": {
        "url": invest.industry.URLS.MEDICAL_TECHNOLOGY,
        "po": invest.industry,
    },
    "invest - motorsport industry": {
        "url": invest.industry.URLS.MOTORSPORT,
        "po": invest.industry,
    },
    "invest - nuclear energy industry": {
        "url": invest.industry.URLS.NUCLEAR_ENERGY,
        "po": invest.industry,
    },
    "invest - offshore wind energy industry": {
        "url": invest.industry.URLS.OFFSHORE_WIND_ENERGY,
        "po": invest.industry,
    },
    "invest - oil and gas industry": {
        "url": invest.industry.URLS.OIL_AND_GAS,
        "po": invest.industry,
    },
    "invest - pharmaceutical manufacturing industry": {
        "url": invest.industry.URLS.PHARMACEUTICAL_MANUFACTURING,
        "po": invest.industry,
    },
    "invest - retail industry": {
        "url": invest.industry.URLS.RETAIL,
        "po": invest.industry,
    },
    "invest - guide": {"url": invest.guide.URL, "po": invest.guide},
    "invest - uk setup guide": {"url": invest.guide.URL, "po": invest.guide},
    "invest - apply for a uk visa guide": {
        "url": invest.guide.URLS.APPLY_FOR_A_UK_VISA,
        "po": invest.guide,
    },
    "invest - establish a base for business in the uk guide": {
        "url": invest.guide.URLS.ESTABLISHED_A_BASE_FOR_BUSINESS_IN_THE_UK,
        "po": invest.guide,
    },
    "invest - hire skilled workers for your uk operations guide": {
        "url": invest.guide.URLS.HIRE_SKILLED_WORKERS_FOR_YOUR_UK_OPERATIONS,
        "po": invest.guide,
    },
    "invest - open a uk business bank account guide": {
        "url": invest.guide.URLS.OPEN_A_BUSINESS_BANK_ACCOUNT,
        "po": invest.guide,
    },
    "invest - set up a company in the uk guide": {
        "url": invest.guide.URLS.SET_UP_A_COMPANY_IN_THE_UK,
        "po": invest.guide,
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
