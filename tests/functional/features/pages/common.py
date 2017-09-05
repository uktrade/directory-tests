# -*- coding: utf-8 -*-
"""Common data used across the functional tests"""
from enum import Enum

from tests.functional.features.pages import (
    fas_ui_creative_industry,
    fas_ui_creative_industry_summary,
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


class FAS_PAGE(Enum):
    """Selected FAS pages in a handy Enum form"""
    INDUSTRIES = (fas_ui_industries, "industries")
    HEALTH_INDUSTRY = (fas_ui_health_industry, "health industry")
    CREATIVE_INDUSTRY = (fas_ui_creative_industry, "creative industry")
    TECH_INDUSTRY = (fas_ui_tech_industry, "tech industry")
    FOOD_AND_DRINK_INDUSTRY = (fas_ui_food_and_drink_industry,
                               "food and drink industry")
    HEALTH_INDUSTRY_SUMMARY = (fas_ui_health_industry_summary,
                               "health industry summary")
    CREATIVE_INDUSTRY_SUMMARY = (fas_ui_creative_industry_summary,
                                 "creative industry summary")
    TECH_INDUSTRY_SUMMARY = (fas_ui_tech_industry_summary,
                             "tech industry summary")
    FOOD_AND_DRINK_INDUSTRY_SUMMARY = (fas_ui_food_and_drink_industry_summary,
                                       "food and drink industry summary")

    def __str__(self):
        return self.value[0]

    def __eq__(self, y: str):
        return self.value[1] == y.lower()

    @property
    def po(self):
        return self.value[0]
