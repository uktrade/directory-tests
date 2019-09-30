# -*- coding: utf-8 -*-
from enum import Enum
from random import choice


class BusinessType(Enum):
    COMPANIES_HOUSE = "LTD, PLC or Royal Charter"
    INDIVIDUAL = "Individual"
    OVERSEAS_COMPANY = "Overseas company"

    SOLE_TRADER = "Sole trader"
    CHARITY = "Charity"
    PARTNERSHIP = "Partnership"
    OTHER = "Other UK business not registered in Companies House"

    ISD_ONLY = "ISD only"
    ISD_AND_TRADE = "ISD & Trade"
    UNPUBLISHED_ISD_AND_PUBLISHED_TRADE = "unpublished ISD & published Trade"

    @classmethod
    def random(cls):
        return choice(list(cls.__members__.values()))


class Account:
    published = False
    published_isd = False
    verified = False
    business_type = None
    description = None

    def __init__(self, account_description: str):
        self.description = account_description.lower()
        if self.description.startswith("published"):
            self.published = True
            self.verified = True
        elif self.description.startswith("unpublished verified"):
            self.published = False
            self.verified = True
        elif self.description.startswith("unpublished unverified"):
            self.published = False
            self.verified = False
        elif self.description == "verified individual":
            self.published = False
            self.verified = True
        elif self.description == "unverified individual":
            self.published = False
            self.verified = False
        elif self.description == f"published {BusinessType.ISD_ONLY.value}":
            self.published = False
            self.published_isd = True
            self.verified = True
        elif self.description == f"published {BusinessType.ISD_AND_TRADE.value}":
            self.published = True
            self.published_isd = True
            self.verified = True
        elif self.description == BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE.value:
            self.published = True
            self.published_isd = False
            self.verified = True
        elif self.description == BusinessType.OVERSEAS_COMPANY.value:
            self.business_type = BusinessType.OVERSEAS_COMPANY
        else:
            LookupError(f"Could not identify state of account in account description: '{self.description}'")

        if BusinessType.COMPANIES_HOUSE.value.lower() in self.description:
            self.business_type = BusinessType.COMPANIES_HOUSE
        elif BusinessType.SOLE_TRADER.value.lower() in self.description:
            self.business_type = BusinessType.SOLE_TRADER
        elif BusinessType.CHARITY.value.lower() in self.description:
            self.business_type = BusinessType.CHARITY
        elif BusinessType.PARTNERSHIP.value.lower() in self.description:
            self.business_type = BusinessType.PARTNERSHIP
        elif BusinessType.OTHER.value.lower() in self.description:
            self.business_type = BusinessType.OTHER
        elif BusinessType.INDIVIDUAL.value.lower() in self.description:
            self.business_type = BusinessType.INDIVIDUAL
        elif BusinessType.OVERSEAS_COMPANY.value.lower() in self.description:
            self.business_type = BusinessType.OVERSEAS_COMPANY
        elif BusinessType.ISD_ONLY.value.lower() in self.description:
            self.business_type = BusinessType.ISD_ONLY
        elif BusinessType.ISD_AND_TRADE.value.lower() in self.description:
            self.business_type = BusinessType.ISD_AND_TRADE
        elif BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE.value.lower() in self.description:
            self.business_type = BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE
        else:
            raise LookupError(f"Could not identify business type in account description: '{self.description}'")

    def __str__(self) -> str:
        return (
            f"Requested '{self.description}': business type: {self.business_type}, verified: {self.verified}, "
            f"published: {self.published}, published ISD: {self.published_isd}"
        )


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
