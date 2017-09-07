# -*- coding: utf-8 -*-
"""Common data used across the functional tests"""

from tests.functional.features.pages import (
    fas_ui_creative_industry,
    fas_ui_creative_industry_summary,
    fas_ui_find_supplier,
    fas_ui_food_and_drink_industry,
    fas_ui_food_and_drink_industry_summary,
    fas_ui_health_industry,
    fas_ui_health_industry_summary,
    fas_ui_industries,
    fas_ui_tech_industry,
    fas_ui_tech_industry_summary
)

DETAILS = {
    "TITLE": "business name",
    "KEYWORDS": "keywords",
    "WEBSITE": "website",
    "SIZE": "number of employees",
    "SECTOR": "sector of interest",
    "RECIPIENT": "letters recipient full name",
    "COUNTRIES": "countries to export to"
}


PROFILES = {
    "FACEBOOK": "Facebook",
    "LINKEDIN": "LinkedIn",
    "TWITTER": "Twitter"
}


FAS_PAGE_OBJECTS = {
    "find a supplier": fas_ui_find_supplier,
    "industries": fas_ui_industries,
    "health industry": fas_ui_health_industry,
    "creative industry": fas_ui_creative_industry,
    "tech industry": fas_ui_tech_industry,
    "food and drink industry": fas_ui_food_and_drink_industry,
    "health industry summary": fas_ui_health_industry_summary,
    "creative industry summary": fas_ui_creative_industry_summary,
    "tech industry summary": fas_ui_tech_industry_summary,
    "food and drink industry summary": fas_ui_food_and_drink_industry_summary,
}
