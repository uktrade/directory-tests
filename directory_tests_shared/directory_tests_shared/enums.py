# -*- coding: utf-8 -*-
from enum import Enum
from random import choice


class BusinessType(Enum):
    COMPANIES_HOUSE = "companies-house-company"
    SOLE_TRADED = "non-companies-house-company"
    TAX_PAYER = "not-company"
    OVERSEAS_COMPANY = "overseas-company"

    @classmethod
    def random(cls):
        return choice(list(cls.__members__.values()))


class Service(Enum):
    BRITISH_COUNCIL = "British Council"
    DOMESTIC = "Domestic"
    EORI = "EORI"
    EVENTS = "Events"
    EXPORT_OPPORTUNITIES = "Export Opportunities"
    FAB = "Find a Buyer"
    FACEBOOK = "Facebook"
    FAS = "Find a Supplier"
    INTERNATIONAL = "International"
    INVEST = "Invest"
    ISD = "ISD"
    LINKEDIN = "LinkedIn"
    PIR = "PIR"
    PROFILE = "Profile"
    SOO = "Selling Online Overseas"
    SSO = "SSO"
    TWITTER = "Twitter"
    VISIT_BRITAIN = "Visit Britain"

    def __str__(self):
        return self.value


class PageType(Enum):
    ARTICLE = "article"
    ARTICLE_LIST = "article list"
    CONFIRMATION = "confirmation"
    CONTACT_US = "contact us"
    CONTENT = "content"
    ERROR = "error"
    EVENT = "event"
    FORM = "form"
    GUIDE = "guide"
    HOME = "home"
    HPO = "HPO"
    INDUSTRY = "industry"
    LANDING = "landing"
    LISTING = "listing"
    OPTION = "option"
    PROFILE = "profile"
    REGION = "region"
    SEARCH = "search"
    SEARCH_RESULTS = "search results"
    SHARE = "share"
    THANK_YOU = "thank you"

    def __str__(self):
        return self.value


class Language(Enum):
    ARABIC = "ar"
    CHINESE = "zh-hans"
    ENGLISH = "en-gb"
    FRENCH = "fr"
    GERMAN = "de"
    JAPANESE = "jp"
    PORTUGUESE = "pt"
    SPANISH = "es"

    def __str__(self):
        return self.value
