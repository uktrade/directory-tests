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
    FAB = "FAB"
    FAS = "FAS"
    INTERNATIONAL = "International"
    ISD = "ISD"
    PROFILE = "Profile"
    SSO = "SSO"

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
