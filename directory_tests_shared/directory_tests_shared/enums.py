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
    publish = False
    publish_isd = False
    verify = False
    verify_email = False
    business_type = None
    description = None

    def __init__(self, account_description: str):
        self.description = account_description.lower()
        if self.description.startswith("published"):
            self.publish = True
            self.verify = True
            self.verify_email = True
        elif self.description.startswith("unpublished verified"):
            self.publish = False
            self.verify = True
            self.verify_email = True
        elif self.description.startswith("unpublished unverified"):
            self.publish = False
            self.verify = False
            self.verify_email = True
        elif self.description == "verified individual":
            self.publish = False
            self.verify = True
            self.verify_email = True
        elif self.description == "unverified individual":
            self.publish = False
            self.verify = False
            self.verify_email = False
        elif self.description.startswith("verified sso/great.gov.uk account for"):
            self.publish = False
            self.verify = False
            self.verify_email = True
        elif self.description.startswith("unverified sso/great.gov.uk account for"):
            self.publish = False
            self.verify = False
            self.verify_email = False
        elif self.description == f"published {BusinessType.ISD_ONLY.value}":
            self.publish = False
            self.publish_isd = True
            self.verify = True
            self.verify_email = True
        elif self.description == f"published {BusinessType.ISD_AND_TRADE.value}":
            self.publish = True
            self.publish_isd = True
            self.verify = True
        elif self.description == BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE.value:
            self.publish = True
            self.publish_isd = False
            self.verify = True
            self.verify_email = True
        elif self.description == BusinessType.OVERSEAS_COMPANY.value:
            self.business_type = BusinessType.OVERSEAS_COMPANY
        else:
            LookupError(
                f"Could not identify state of account in account description: '{self.description}'"
            )

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
        elif (
            BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE.value.lower()
            in self.description
        ):
            self.business_type = BusinessType.UNPUBLISHED_ISD_AND_PUBLISHED_TRADE
        else:
            raise LookupError(
                f"Could not identify business type in account description: '{self.description}'"
            )

    def __str__(self) -> str:
        return (
            f"Requested '{self.description}': business type: {self.business_type}, verified: {self.verify}, "
            f"published: {self.publish}, published ISD: {self.publish_isd}"
        )


class Service(Enum):
    BRITISH_COUNCIL = "British Council"
    CHECK_DUTIES_CUSTOMS = "Check duties and customs"
    DOMESTIC = "Domestic"
    EORI = "EORI"
    EVENTS = "Events"
    EXPORT_OPPORTUNITIES = "Export Opportunities"
    ERP = "ERP"
    FAB = "Find a Buyer"
    FACEBOOK = "Facebook"
    FAS = "Find a Supplier"
    GENERIC = "Generic"
    GOVUK = "GOV.UK"
    INTERNATIONAL = "International"
    INVEST = "Invest"
    ISD = "ISD"
    LINKEDIN = "LinkedIn"
    MADDB = "Market Access Database"
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
    DEDICATED_SUPPORT_CONTENT = "Dedicated Support Content"
    DOMESTIC_CONTACT_US = "Domestic Contact us"
    ERROR = "error"
    EVENT = "event"
    FORM = "form"
    GUIDE = "guide"
    HOME = "home"
    HPO = "HPO"
    INDUSTRY = "industry"
    INTERNATIONAL_CONTACT_US = "International Contact us"
    LANDING = "landing"
    LISTING = "listing"
    OPTION = "option"
    OPPORTUNITY = "opportunity"
    PROFILE = "profile"
    REGION = "region"
    SEARCH = "search"
    SEARCH_RESULTS = "search results"
    SHARE = "share"
    SHORT_DOMESTIC_CONTACT_US = "Short Domestic Contact us"
    UKEF_CONTACT_US = "UKEF Contact us"
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
