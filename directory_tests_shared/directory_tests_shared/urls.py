# -*- coding: utf-8 -*-
from enum import Enum, unique
from functools import partial
from typing import Union
from urllib.parse import urljoin

from .settings import (
    CMS_API_URL,
    CONTACT_US_URL,
    DIRECTORY_API_URL,
    DOMESTIC_URL,
    EXPORT_OPPORTUNITIES_URL,
    FIND_A_BUYER_URL,
    FIND_A_SUPPLIER_URL,
    FORMS_API_URL,
    INTERNATIONAL_URL,
    INVEST_URL,
    ISD_URL,
    LEGACY_CONTACT_US_URL,
    LEGACY_INVEST_URL,
    PROFILE_URL,
    SOO_URL,
    SSO_API_URL,
    SSO_URL,
)


class Url:
    def __init__(
        self, service_url: str, relative_endpoint: str, *, template: str = None
    ):
        join_endpoint = partial(urljoin, service_url)
        self.relative: str = relative_endpoint
        self.absolute: str = join_endpoint(relative_endpoint)
        self.template: Union[str, None] = template
        self.absolute_template: Union[str, None] = (
            join_endpoint(template) if template else None
        )


class CMSApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(CMS_API_URL, endpoint, template=template)


class ContactUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(CONTACT_US_URL, endpoint, template=template)


class DirectoryApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_API_URL, endpoint, template=template)


class DomesticUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DOMESTIC_URL, endpoint, template=template)


class ExOppsUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(EXPORT_OPPORTUNITIES_URL, endpoint, template=template)


class FABUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(FIND_A_BUYER_URL, endpoint, template=template)


class FABApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(FIND_A_BUYER_URL, endpoint, template=template)


class FASUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(FIND_A_SUPPLIER_URL, endpoint, template=template)


class LegacyFASUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DOMESTIC_URL + "trade/", endpoint, template=template)


class FormsApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(FORMS_API_URL, endpoint, template=template)


class InternationalUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(INTERNATIONAL_URL, endpoint, template=template)


class InvestUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(INVEST_URL, endpoint, template=template)


class LegacyInvestUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(LEGACY_INVEST_URL, endpoint, template=template)


class ISDUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(ISD_URL, endpoint, template=template)


class LegacyContactUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(LEGACY_CONTACT_US_URL, endpoint, template=template)


class ProfileUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(PROFILE_URL, endpoint, template=template)


class SOOUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(SOO_URL, endpoint, template=template)


class SSOUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(SSO_URL, endpoint, template=template)


class SSOApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(SSO_API_URL, endpoint, template=template)


@unique
class URLs(Enum):
    """This Enum is to help discover, refactor, find usage of URLs"""

    def __str__(self) -> str:
        return (
            f"{self._name_} absolute URL: {self.value.absolute} relative "
            f"URL: {self.value.relative}"
        )

    @property
    def absolute(self) -> str:
        return self.value.absolute

    @property
    def relative(self) -> str:
        return self.value.relative

    @property
    def template(self) -> Union[str, None]:
        return self.value.template

    @property
    def absolute_template(self) -> Union[str, None]:
        return self.value.absolute_template

    # Directory API
    DIR_API_HEALTHCHECK = DirectoryApiUrl("healthcheck/")
    DIR_API_HEALTHCHECK_PING = DirectoryApiUrl("healthcheck/ping/")
    DIR_API_ENROLMENT = DirectoryApiUrl("enrolment/")
    DIR_API_PRE_VERIFIED_ENROLMENT = DirectoryApiUrl("pre-verified-enrolment/")
    DIR_API_ENROLMENT_TRUSTED_CODE = DirectoryApiUrl("trusted-code/{code}/")
    DIR_API_NOTIFICATIONS_ANONYMOUS_UNSUBSCRIBE = DirectoryApiUrl(
        "notifications/anonymous-unsubscribe/"
    )
    DIR_API_BUYER = DirectoryApiUrl("buyer/")
    DIR_API_BUYER_CSV_DUMP = DirectoryApiUrl("buyer/csv-dump/")
    DIR_API_SUPPLIER_CSV_DUMP = DirectoryApiUrl("supplier/csv-dump/")
    DIR_API_VALIDATE_COMPANY_NUMBER = DirectoryApiUrl("validate/company-number/")
    DIR_API_COMPANIES_HOUSE_PROFILE = DirectoryApiUrl(
        "company/companies-house-profile/"
    )
    DIR_API_SUPPLIER = DirectoryApiUrl("supplier/")
    DIR_API_SUPPLIER_UNSUBSCRIBE = DirectoryApiUrl("supplier/unsubscribe/")
    DIR_API_EXPORT_READINESS_TRIAGE = DirectoryApiUrl("export-readiness/triage/")
    DIR_API_EXPORT_READINESS_ARTICLE_READ = DirectoryApiUrl(
        "export-readiness/article-read/"
    )
    DIR_API_EXPORT_READINESS_TASK_COMPLETED = DirectoryApiUrl(
        "export-readiness/task-completed/"
    )
    DIR_API_EXPORT_OPPORTUNITY_FOOD = DirectoryApiUrl("export-opportunity/food/")
    DIR_API_EXPORT_OPPORTUNITY_LEGAL = DirectoryApiUrl("export-opportunity/legal/")
    DIR_API_PUBLIC_COMPANY = DirectoryApiUrl("public/company/")
    DIR_API_PUBLIC_COMPANY_PROFILE = DirectoryApiUrl(
        "public/company/{companies_house_number}/"
    )
    DIR_API_PUBLIC_CASE_STUDY = DirectoryApiUrl("public/case-study/{id}/")
    DIR_API_SUPPLIER_COMPANY = DirectoryApiUrl("supplier/company/")
    DIR_API_SUPPLIER_COMPANY_CASE_STUDY = DirectoryApiUrl(
        "supplier/company/case-study/"
    )
    DIR_API_SUPPLIER_COMPANY_CASE_STUDY_BY_ID = DirectoryApiUrl(
        "supplier/company/case-study/{id}/"
    )
    DIR_API_SUPPLIER_COMPANY_VERIFY = DirectoryApiUrl("supplier/company/verify/")
    DIR_API_SUPPLIER_COMPANY_VERIFY_COMPANIES_HOUSE = DirectoryApiUrl(
        "supplier/company/verify/companies-house/"
    )
    DIR_API_CONTACT_SUPPLIER = DirectoryApiUrl("contact/supplier/")
    DIR_API_COMPANY_SEARCH = DirectoryApiUrl("company/search/")
    DIR_API_CASE_STUDY_SEARCH = DirectoryApiUrl("case-study/search/")
    DIR_API_SUPPLIER_COMPANY_COLLABORATORS = DirectoryApiUrl(
        "supplier/company/collaborators/"
    )
    DIR_API_SUPPLIER_COMPANY_COLLABORATION_INVITE = DirectoryApiUrl(
        "supplier/company/collaboration-invite/"
    )
    DIR_API_SUPPLIER_COMPANY_COLLABORATION_INVITE_BY_UUID = DirectoryApiUrl(
        "supplier/company/collaboration-invite/{uuid}/"
    )
    DIR_API_SUPPLIER_COMPANY_REMOVE_COLLABORATORS = DirectoryApiUrl(
        "supplier/company/remove-collaborators/"
    )
    DIR_API_SUPPLIER_COMPANY_TRANSFER_OWNERSHIP_INVITE = DirectoryApiUrl(
        "supplier/company/transfer-ownership-invite/"
    )
    DIR_API_SUPPLIER_COMPANY_TRANSFER_OWNERSHIP_INVITE_BY_UUID = DirectoryApiUrl(
        "supplier/company/transfer-ownership-invite/{uuid}/"
    )
    DIR_API_SUPPLIER_GECKO_TOTAL_REGISTERED = DirectoryApiUrl(
        "supplier/gecko/total-registered/"
    )
    DIR_API_ACTIVITY_STREAM = DirectoryApiUrl("activity-stream/")
    DIR_API_EXTERNAL_SUPPLIER_SSO = DirectoryApiUrl("external/supplier-sso/")
    DIR_API_EXTERNAL_SUPPLIER = DirectoryApiUrl("external/supplier/")
    DIR_API_TEST_API_COMPANY = DirectoryApiUrl(
        "/testapi/company/{ch_id_or_name}/",
        template="/testapi/company/{ch_id_or_name}/",
    )

    # SSO UI
    SSO_LANDING = SSOUrl("")
    SSO_EMAIL_CONFIRM = SSOUrl("accounts/confirm-email/")
    SSO_INACTIVE = SSOUrl("accounts/inactive/")
    SSO_LOGIN = SSOUrl("accounts/login/", template="accounts/login/?next={next}")
    SSO_LOGOUT = SSOUrl("accounts/logout/")
    SSO_PASSWORD_CHANGE = SSOUrl("accounts/password/change/")
    SSO_PASSWORD_RESET = SSOUrl("accounts/password/reset/")
    SSO_PASSWORD_SET = SSOUrl("accounts/password/set/")
    SSO_SIGNUP = SSOUrl("accounts/signup/")

    # SSO API
    SSO_API_LANDING = SSOApiUrl("")
    SSO_API_HEALTHCECK = SSOApiUrl("api/v1/healthcheck/")
    SSO_API_HEALTHCHECK_PING = SSOApiUrl("api/v1/healthcheck/ping/")
    SSO_API_USER = SSOApiUrl("api/v1/session-user/")

    # Find a Buyer
    FAB_LANDING = FABUrl("")
    FAB_SITEMAP = FABUrl("sitemap.xml")
    FAB_ACCOUNT_CONFIRM_OWNERSHIP_TRANSFER = FABUrl(
        "account/transfer/accept/?invite_key=",
        template="account/transfer/accept/?invite_key={invite_key}",
    )
    FAB_ACCOUNT_CONFIRM_PASSWORD = FABUrl("account/transfer/")
    FAB_ACCOUNT_REMOVE_COLLABORATOR = FABUrl("account/remove-collaborator/")
    FAB_CONFIRM_COMPANY_ADDRESS = FABUrl("verify/letter-confirm/")
    FAB_CONFIRM_IDENTITY = FABUrl("verify/")
    FAB_CONFIRM_IDENTITY_LETTER = FABUrl("verify/letter-send/")
    FAB_COMPANY_PROFILE = FABUrl("company-profile/")
    FAB_HEALTHCHECK = FABUrl("healthcheck/")
    FAB_REGISTER = FABUrl("register/")

    # Find a Supplier
    FAS_CASE_STUDY = FASUrl("case-study/", template="case-study/{number}/")
    FAS_CONTACT_SUPPLIER = FASUrl(
        "suppliers/", template="suppliers/{ch_number}/contact/"
    )
    FAS_FEEDBACK = FASUrl("feedback/")
    FAS_HEALTHCHECK = FASUrl("healthcheck/")
    FAS_INDUSTRIES = FASUrl("industries/", template="industries/{industry}/")
    FAS_INDUSTRY_CREATIVE_SERVICES = FASUrl("industries/creative-services/")
    FAS_INDUSTRY_FOOD_AND_DRINK = FASUrl("industries/food-and-drink/")
    FAS_INDUSTRY_HEALTHCARE = FASUrl("industries/healthcare/")
    FAS_INDUSTRY_TECHNOLOGY = FASUrl("industries/technology/")
    FAS_LANDING = FASUrl("")
    FAS_SEARCH = FASUrl("search/", template="search/?q={query}&industries={industries}")
    FAS_SITEMAP = FASUrl("sitemap.xml")
    FAS_SUBSCRIBE = FASUrl("subscribe/")
    FAS_SUPPLIER = FASUrl("suppliers/", template="suppliers/{ch_number}/")
    FAS_SUPPLIERS = FASUrl("suppliers/", template="suppliers/{ch_number}/{slug}/")
    FAS_INCOMING_REDIRECT = FASUrl("incoming/", template="incoming/{endpoint}")

    # Legacy FAS industry endpoints before slugs were changed to:
    # healthcare, technology & creative-services respectively
    FAS_INDUSTRIES_HEALTH = LegacyFASUrl("industries/health/")
    FAS_INDUSTRIES_TECH = LegacyFASUrl("industries/tech/")
    FAS_INDUSTRIES_CREATIVE = LegacyFASUrl("industries/creative/")

    # New International site
    INTERNATIONAL_LANDING = InternationalUrl("")
    INTERNATIONAL_SITEMAP = InternationalUrl("sitemap.xml")
    INTERNATIONAL_INDUSTRIES = InternationalUrl(
        "content/about-uk/industries/",
        template="content/about-uk/industries/{industry}/",
    )
    INTERNATIONAL_CAPITAL_INVEST = InternationalUrl("content/capital-invest/")
    INTERNATIONAL_INDUSTRY_ADVANCED_MANUFACTURING = InternationalUrl(
        "content/about-uk/industries/advanced-manufacturing/"
    )
    INTERNATIONAL_INDUSTRY_AEROSPACE = InternationalUrl(
        "content/about-uk/industries/aerospace/"
    )
    INTERNATIONAL_INDUSTRY_AGRI_TECH = InternationalUrl(
        "content/about-uk/industries/agri-tech/"
    )
    INTERNATIONAL_INDUSTRY_AGRICULTURAL_TECHNOLOGY = InternationalUrl(
        "content/about-uk/industries/agricultural-technology/"
    )
    INTERNATIONAL_INDUSTRY_ASSET_MANAGEMENT = InternationalUrl(
        "content/about-uk/industries/asset-management/"
    )
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE = InternationalUrl(
        "content/about-uk/industries/automotive/"
    )
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT = InternationalUrl(
        "content/about-uk/industries/automotive-research-and-development/"
    )
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE_SUPPLY_CHAIN = InternationalUrl(
        "content/about-uk/industries/automotive-supply-chain/"
    )
    INTERNATIONAL_INDUSTRY_CHEMICALS = InternationalUrl(
        "content/about-uk/industries/chemicals/"
    )
    INTERNATIONAL_INDUSTRY_CREATIVE_CONTENT_AND_PRODUCTION = InternationalUrl(
        "content/about-uk/industries/creative-content-and-production/"
    )
    INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES = InternationalUrl(
        "content/about-uk/industries/creative-industries/"
    )
    INTERNATIONAL_INDUSTRY_DATA_ANALYTICS = InternationalUrl(
        "content/about-uk/industries/data-analytics/"
    )
    INTERNATIONAL_INDUSTRY_DIGITAL_MEDIA = InternationalUrl(
        "content/about-uk/industries/digital-media/"
    )
    INTERNATIONAL_INDUSTRY_ELECTRICAL_NETWORKS = InternationalUrl(
        "content/about-uk/industries/electrical-networks/"
    )
    INTERNATIONAL_INDUSTRY_ENERGY = InternationalUrl(
        "content/about-uk/industries/energy/"
    )
    INTERNATIONAL_INDUSTRY_ENERGY_WASTE = InternationalUrl(
        "content/about-uk/industries/energy-waste/"
    )
    INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING = InternationalUrl(
        "content/about-uk/industries/engineering-and-manufacturing/"
    )
    INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES = InternationalUrl(
        "content/about-uk/industries/financial-services/"
    )
    INTERNATIONAL_INDUSTRY_FINANCIAL_TECHNOLOGY = InternationalUrl(
        "content/about-uk/industries/financial-technology/"
    )
    INTERNATIONAL_INDUSTRY_FOOD_AND_DRINK = InternationalUrl(
        "content/about-uk/industries/food-and-drink/"
    )
    INTERNATIONAL_INDUSTRY_FOOD_SERVICE_AND_CATERING = InternationalUrl(
        "content/about-uk/industries/food-service-and-catering/"
    )
    INTERNATIONAL_INDUSTRY_FREE_FOODS = InternationalUrl(
        "content/about-uk/industries/free-foods/"
    )
    INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES = InternationalUrl(
        "content/about-uk/industries/health-and-life-sciences/"
    )
    INTERNATIONAL_INDUSTRY_MEAT_POULTRY_AND_DAIRY = InternationalUrl(
        "content/about-uk/industries/meat-poultry-and-dairy/"
    )
    INTERNATIONAL_INDUSTRY_MEDICAL_TECHNOLOGY = InternationalUrl(
        "content/about-uk/industries/medical-technology/"
    )
    INTERNATIONAL_INDUSTRY_MOTORSPORT = InternationalUrl(
        "content/about-uk/industries/motorsport/"
    )
    INTERNATIONAL_INDUSTRY_NUCLEAR_ENERGY = InternationalUrl(
        "content/about-uk/industries/nuclear-energy/"
    )
    INTERNATIONAL_INDUSTRY_OFFSHORE_WIND_ENERGY = InternationalUrl(
        "content/about-uk/industries/offshore-wind-energy/"
    )
    INTERNATIONAL_INDUSTRY_OIL_AND_GAS = InternationalUrl(
        "content/about-uk/industries/oil-and-gas/"
    )
    INTERNATIONAL_INDUSTRY_PHARMACEUTICAL_MANUFACTURING = InternationalUrl(
        "content/about-uk/industries/pharmaceutical-manufacturing/"
    )
    INTERNATIONAL_INDUSTRY_RETAIL = InternationalUrl(
        "content/about-uk/industries/retail/"
    )
    INTERNATIONAL_INDUSTRY_TECHNOLOGY = InternationalUrl(
        "content/about-uk/industries/technology/"
    )
    INTERNATIONAL_HEALTHCHECK_FORMS_API = InternationalUrl("healthcheck/forms-api/")
    INTERNATIONAL_HEALTHCHECK_SENTRY = InternationalUrl("healthcheck/sentry/")
    INTERNATIONAL_REGIONS_MIDLANDS = InternationalUrl(
        "content/about-uk/regions/midlands/"
    )
    INTERNATIONAL_REGIONS_NORTHERN_IRELAND = InternationalUrl(
        "content/about-uk/regions/northern-ireland/"
    )
    INTERNATIONAL_REGIONS_SOUTH_ENGLAND = InternationalUrl(
        "content/about-uk/regions/south-england/"
    )
    INTERNATIONAL_REGIONS_NORTH_ENGLAND = InternationalUrl(
        "content/about-uk/regions/north-england/"
    )
    INTERNATIONAL_REGIONS_WALES = InternationalUrl("content/about-uk/regions/wales/")

    # Invest site
    INVEST_LANDING = InvestUrl("")
    INVEST_HEALTHCHECK = InvestUrl("healthcheck/")
    INVEST_CONTACT = InvestUrl("contact/")
    INVEST_SITEMAP = InvestUrl("sitemap.xml")
    INVEST_PIR = InvestUrl("perfectfit/")
    INVEST_HPO_CONTACT = InternationalUrl(
        "content/invest/high-potential-opportunities/contact/"
    )
    INVEST_HPO_RAIL = InternationalUrl(
        "content/invest/high-potential-opportunities/rail-infrastructure/"
    )
    INVEST_HPO_FOOD = InternationalUrl(
        "content/invest/high-potential-opportunities/food-production/"
    )
    INVEST_HPO_LIGHTWEIGHT = InternationalUrl(
        "content/invest/high-potential-opportunities/lightweight-structures/"
    )

    INVEST_INDUSTRIES = LegacyInvestUrl("industries/")
    INVEST_REGIONS_SCOTLAND = InternationalUrl("content/invest/uk-regions/scotland/")
    INVEST_LEGACY_UK_SETUP_GUIDE = LegacyInvestUrl("uk-setup-guide/")
    INVEST_LEGACY_UK_SETUP_GUIDE_UK_VISAS = LegacyInvestUrl(
        "uk-setup-guide/apply-uk-visa/"
    )
    INVEST_LEGACY_UK_SETUP_GUIDE_ESTABLISH_A_BASE = LegacyInvestUrl(
        "uk-setup-guide/establish-base-business-uk/"
    )
    INVEST_LEGACY_UK_SETUP_GUIDE_HIRE_SKILLED_WORKERS = LegacyInvestUrl(
        "uk-setup-guide/hire-skilled-workers-your-uk-operations/"
    )
    INVEST_LEGACY_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT = LegacyInvestUrl(
        "uk-setup-guide/open-uk-business-bank-account/"
    )
    INVEST_LEGACY_UK_SETUP_GUIDE_REGISTER_A_COMPANY = LegacyInvestUrl(
        "uk-setup-guide/setup-your-business-uk/"
    )
    INVEST_LEGACY_UK_SETUP_GUIDE_UK_TAX = LegacyInvestUrl(
        "uk-setup-guide/understand-uk-tax-and-incentives/"
    )

    INVEST_UK_SETUP_GUIDE = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/",
        template="content/invest/how-to-setup-in-the-uk/{guide}/",
    )
    INVEST_UK_SETUP_GUIDE_UK_VISAS = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/uk-visas-and-migration/"
    )
    INVEST_UK_SETUP_GUIDE_ACCESS_FINANCE = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/access-finance-in-the-uk/"
    )
    INVEST_UK_SETUP_GUIDE_ESTABLISH_A_BASE = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/"
    )
    INVEST_UK_SETUP_GUIDE_HIRE_SKILLED_WORKERS = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/"  # noqa
    )
    INVEST_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/"
    )
    INVEST_UK_SETUP_GUIDE_REGISTER_A_COMPANY = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/register-a-company-in-the-uk/"
    )
    INVEST_UK_SETUP_GUIDE_UK_TAX = InternationalUrl(
        "content/invest/how-to-setup-in-the-uk/uk-tax-and-incentives/"
    )

    INVEST_LEGACY_REGIONS_MIDLANDS = LegacyInvestUrl("uk-regions/midlands/")
    INVEST_LEGACY_REGIONS_NORTHERN_IRELAND = LegacyInvestUrl(
        "uk-regions/northern-ireland/"
    )
    INVEST_LEGACY_REGIONS_SOUTH_ENGLAND = LegacyInvestUrl("uk-regions/south-england/")
    INVEST_LEGACY_REGIONS_NORTH_ENGLAND = LegacyInvestUrl("uk-regions/north-england/")
    INVEST_LEGACY_REGIONS_LONDON = LegacyInvestUrl("uk-regions/london/")
    INVEST_LEGACY_REGIONS_WALES = LegacyInvestUrl("uk-regions/wales/")
    INVEST_LEGACY_REGIONS_SCOTLAND = LegacyInvestUrl("uk-regions/scotland/")

    INVEST_INDUSTRIES_ADVANCED_MANUFACTURING = LegacyInvestUrl(
        "industries/advanced-manufacturing/"
    )
    INVEST_INDUSTRIES_AEROSPACE = LegacyInvestUrl("industries/aerospace/")
    INVEST_INDUSTRIES_AGRI_TECH = LegacyInvestUrl("industries/agri-tech/")
    INVEST_INDUSTRIES_ASSET_MANAGEMENT = LegacyInvestUrl("industries/asset-management/")
    INVEST_INDUSTRIES_AUTOMOTIVE = LegacyInvestUrl("industries/automotive/")
    INVEST_INDUSTRIES_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT = LegacyInvestUrl(
        "industries/automotive-research-and-development/"
    )
    INVEST_INDUSTRIES_AUTOMOTIVE_SUPPLY_CHAIN = LegacyInvestUrl(
        "industries/automotive-supply-chain/"
    )
    INVEST_INDUSTRIES_CAPITAL_INVESTMENT = LegacyInvestUrl(
        "industries/capital-investment/"
    )
    INVEST_INDUSTRIES_CHEMICALS = LegacyInvestUrl("industries/chemicals/")
    INVEST_INDUSTRIES_CREATIVE_CONTENT_AND_PRODUCTION = LegacyInvestUrl(
        "industries/creative-content-and-production/"
    )
    INVEST_INDUSTRIES_CREATIVE_INDUSTRIES = LegacyInvestUrl(
        "industries/creative-industries/"
    )
    INVEST_INDUSTRIES_DATA_ANALYTICS = LegacyInvestUrl("industries/data-analytics/")
    INVEST_INDUSTRIES_DIGITAL_MEDIA = LegacyInvestUrl("industries/digital-media/")
    INVEST_INDUSTRIES_ELECTRICAL_NETWORKS = LegacyInvestUrl(
        "industries/electrical-networks/"
    )
    INVEST_INDUSTRIES_ENERGY = LegacyInvestUrl("industries/energy/")
    INVEST_INDUSTRIES_ENERGY_WASTE = LegacyInvestUrl("industries/energy-waste/")
    INVEST_INDUSTRIES_FINANCIAL_SERVICES = LegacyInvestUrl(
        "industries/financial-services/"
    )
    INVEST_INDUSTRIES_FINANCIAL_TECHNOLOGY = LegacyInvestUrl(
        "industries/financial-technology/"
    )
    INVEST_INDUSTRIES_FOOD_AND_DRINK = LegacyInvestUrl("industries/food-and-drink/")
    INVEST_INDUSTRIES_FOOD_SERVICE_AND_CATERING = LegacyInvestUrl(
        "industries/food-service-and-catering/"
    )
    INVEST_INDUSTRIES_FREE_FOODS = LegacyInvestUrl("industries/free-foods/")
    INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES = LegacyInvestUrl(
        "industries/health-and-life-sciences/"
    )
    INVEST_INDUSTRIES_MEAT_POULTRY_AND_DAIRY = LegacyInvestUrl(
        "industries/meat-poultry-and-dairy/"
    )
    INVEST_INDUSTRIES_MEDICAL_TECHNOLOGY = LegacyInvestUrl(
        "industries/medical-technology/"
    )
    INVEST_INDUSTRIES_MOTORSPORT = LegacyInvestUrl("industries/motorsport/")
    INVEST_INDUSTRIES_NUCLEAR_ENERGY = LegacyInvestUrl("industries/nuclear-energy/")
    INVEST_INDUSTRIES_OFFSHORE_WIND_ENERGY = LegacyInvestUrl(
        "industries/offshore-wind-energy/"
    )
    INVEST_INDUSTRIES_OIL_AND_GAS = LegacyInvestUrl("industries/oil-and-gas/")
    INVEST_INDUSTRIES_PHARMACEUTICAL_MANUFACTURING = LegacyInvestUrl(
        "industries/pharmaceutical-manufacturing/"
    )
    INVEST_INDUSTRIES_RETAIL = LegacyInvestUrl("industries/retail/")
    INVEST_INDUSTRIES_TECHNOLOGY = LegacyInvestUrl("industries/technology/")

    ISD_LANDING = ISDUrl("")
    ISD_SEARCH = ISDUrl("search/")

    # FAS/ISD Profile
    PROFILE_API_COMPANIES_HOUSE_SEARCH = ProfileUrl(
        "api/v1/companies-house-search/",
        template="api/v1/companies-house-search/?term={term}",
    )
    PROFILE_API_POSTCODE_SEARCH = ProfileUrl(
        "api/v1/postcode-search/?postcode={postcode}",
        template="api/v1/postcode-search/?postcode={postcode}",
    )
    PROFILE_HEALTHCHECK = ProfileUrl("healthcheck/")
    PROFILE_HEALTHCHECK_PING = ProfileUrl("healthcheck/ping/")
    PROFILE_SOO = ProfileUrl("selling-online-overseas/")
    PROFILE_BUSINESS_PROFILE = ProfileUrl("business-profile/")
    PROFILE_PERSONAL_PROFILE = ProfileUrl("personal-profile/")
    PROFILE_EXOPS_ALERTS = ProfileUrl("export-opportunities/email-alerts/")
    PROFILE_EXOPS_APPLICATIONS = ProfileUrl("export-opportunities/applications/")
    PROFILE_LANDING = ProfileUrl("")
    PROFILE_SITEMAP = ProfileUrl("sitemap.xml")
    PROFILE_ABOUT = ProfileUrl("about/")
    PROFILE_ADMIN_TRANSFER_OWNERSHIP = ProfileUrl("business-profile/admin/transfer/")
    PROFILE_ACCOUNT_ACCEPT_INVITATION = ProfileUrl(
        "account/collaborate/accept/?invite_key={invite_key}",
        template="account/collaborate/accept/?invite_key={invite_key}",
    )
    PROFILE_ACCOUNT_ADD_COLLABORATOR = ProfileUrl("business-profile/admin/invite/")
    PROFILE_ENROL = ProfileUrl("enrol/")
    PROFILE_ENROL_SELECT_BUSINESS_TYPE = ProfileUrl("enrol/business-type/")

    PROFILE_ENROL_USER_ACCOUNT = ProfileUrl(
        "enrol/business-type/companies-house/user-account/"
    )
    PROFILE_ENROL_EMAIL_VERIFICATION = ProfileUrl(
        "enrol/business-type/companies-house/verification/"
    )
    PROFILE_ENROL_COMPANIES_HOUSE_SEARCH = ProfileUrl(
        "enrol/business-type/companies-house/company-search/"
    )
    PROFILE_ENROL_BUSINESS_DETAILS = ProfileUrl(
        "enrol/business-type/companies-house/business-details/"
    )
    PROFILE_ENROL_PERSONAL_DETAILS = ProfileUrl(
        "enrol/business-type/companies-house/personal-details/"
    )
    PROFILE_ENROL_FINISHED = ProfileUrl("enrol/business-type/companies-house/finished/")

    PROFILE_ENROL_NON_CH_COMPANY_ENTER_USER_NAME_AND_PASSWORD = ProfileUrl(
        "enrol/business-type/non-companies-house-company/user-account/"
    )
    PROFILE_ENROL_NON_CH_COMPANY_EMAIL_VERIFICATION = ProfileUrl(
        "enrol/business-type/non-companies-house-company/verification/"
    )
    PROFILE_ENROL_NON_CH_COMPANY_ENTER_BUSINESS_DETAILS = ProfileUrl(
        "enrol/business-type/non-companies-house-company/address-search/"
    )
    PROFILE_ENROL_NON_CH_COMPANY_ENTER_PERSONAL_DETAILS = ProfileUrl(
        "enrol/business-type/non-companies-house-company/personal-details/"
    )
    PROFILE_ENROL_NON_CH_COMPANY_FINISHED = ProfileUrl(
        "enrol/business-type/non-companies-house-company/finished/"
    )
    PROFILE_ENROL_NON_CH_REQUEST_TO_VERIFY = ProfileUrl(
        "business-profile/verify/request/"
    )

    PROFILE_ENROL_INDIVIDUAL_START = ProfileUrl("enrol/business-type/individual/start/")
    PROFILE_ENROL_INDIVIDUAL_ENTER_YOUR_EMAIL_AND_PASSWORD = ProfileUrl(
        "enrol/business-type/individual/user-account/"
    )
    PROFILE_ENROL_INDIVIDUAL_EMAIL_VERIFICATION = ProfileUrl(
        "enrol/business-type/individual/verification/"
    )
    PROFILE_ENROL_INDIVIDUAL_UPDATE_YOUR_DETAILS = ProfileUrl(
        "enrol/?backfill-details-intent=true"
    )
    PROFILE_ENROL_INDIVIDUAL_ENTER_YOUR_PERSONAL_DETAILS = ProfileUrl(
        "enrol/business-type/individual/personal-details/"
    )
    PROFILE_ENROL_INDIVIDUAL_FINISHED = ProfileUrl(
        "enrol/business-type/individual/finished/"
    )

    PROFILE_ENROL_OVERSEAS_BUSINESS = ProfileUrl(
        "enrol/business-type/overseas-business/"
    )

    PROFILE_ADMIN = ProfileUrl("business-profile/admin/")
    PROFILE_ADMIN_REMOVE_PROFILE_FROM_ACCOUNT = ProfileUrl(
        "business-profile/admin/disconnect/"
    )
    PROFILE_EDIT_COMPANY_DESCRIPTION = ProfileUrl("business-profile/description/")
    PROFILE_EDIT_COMPANY_BUSINESS_DETAILS = ProfileUrl(
        "business-profile/business-details/"
    )
    PROFILE_PUBLISH_BUSINESS_PROFILE_TO_FAS = ProfileUrl("business-profile/publish/")
    PROFILE_ADD_PRODUCTS_AND_SERVICES = ProfileUrl(
        "business-profile/add-expertise/products-and-services/"
    )
    PROFILE_CASE_STUDY_EDIT = ProfileUrl(
        "business-profile/case-study/{case_number}/details/"
    )
    PROFILE_CASE_STUDY_DETAILS = ProfileUrl("business-profile/case-study/details/")
    PROFILE_CASE_STUDY_IMAGES = ProfileUrl("business-profile/case-study/images/")
    PROFILE_UPLOAD_LOGO = ProfileUrl("business-profile/logo/")
    PROFILE_COMPANY_EDIT_SOCIAL_MEDIA = ProfileUrl("business-profile/social-links/")

    # Domestic site
    DOMESTIC_API_COMPANY_HOUSE_SEARCH = DomesticUrl(
        "api/internal/companies-house-search/"
    )
    DOMESTIC_HEALTHCHECK = DomesticUrl("healthcheck/")
    DOMESTIC_HEALTHCHECK_PING = DomesticUrl("healthcheck/ping/")
    DOMESTIC_SEARCH = DomesticUrl("search/")
    DOMESTIC_SITEMAP = DomesticUrl("sitemap.xml")
    DOMESTIC_LANDING = DomesticUrl("")
    DOMESTIC_FEEDBACK = DomesticUrl("contact/feedback/")
    DOMESTIC_LANDING_UK = DomesticUrl("?lang=en-gb")
    DOMESTIC_INTERNATIONAL = DomesticUrl("international/")
    DOMESTIC_INTERNATIONAL_UK = DomesticUrl("international/?lang=en-gb")
    DOMESTIC_INTERNATIONAL_ZH = DomesticUrl("international/?lang=zh-hans")
    DOMESTIC_INTERNATIONAL_DE = DomesticUrl("international/?lang=de")
    DOMESTIC_INTERNATIONAL_JA = DomesticUrl("international/?lang=ja")
    DOMESTIC_INTERNATIONAL_ES = DomesticUrl("international/?lang=es")
    DOMESTIC_INTERNATIONAL_PT = DomesticUrl("international/?lang=pt")
    DOMESTIC_INTERNATIONAL_AR = DomesticUrl("international/?lang=ar")
    DOMESTIC_TRIAGE_SECTOR = DomesticUrl("triage/sector/")
    DOMESTIC_TRIAGE_EXPORTED_BEFORE = DomesticUrl("triage/exported-before/")
    DOMESTIC_TRIAGE_REGULAR_EXPORTER = DomesticUrl("triage/regular-exporter/")
    DOMESTIC_TRIAGE_ONLINE_MARKETPLACE = DomesticUrl("triage/online-marketplace/")
    DOMESTIC_TRIAGE_COMPANIES_HOUSE = DomesticUrl("triage/companies-house/")
    DOMESTIC_TRIAGE_COMPANY = DomesticUrl("triage/company/")
    DOMESTIC_TRIAGE_SUMMARY = DomesticUrl("triage/summary/")
    DOMESTIC_CUSTOM = DomesticUrl("custom/")
    DOMESTIC_NEW = DomesticUrl("new/")
    DOMESTIC_OCCASIONAL = DomesticUrl("occasional/")
    DOMESTIC_REGULAR = DomesticUrl("regular/")
    DOMESTIC_MARKET_RESEARCH = DomesticUrl("market-research/")
    DOMESTIC_CUSTOMER_INSIGHT = DomesticUrl("customer-insight/")
    DOMESTIC_FINANCE = DomesticUrl("finance/")
    DOMESTIC_BUSINESS_PLANNING = DomesticUrl("business-planning/")
    DOMESTIC_GETTING_PAID = DomesticUrl("getting-paid/")
    DOMESTIC_OPERATIONS_AND_COMPLIANCE = DomesticUrl("operations-and-compliance/")
    DOMESTIC_GET_FINANCE = DomesticUrl("get-finance/")
    DOMESTIC_STORY_FIRST = DomesticUrl("story/hello-babys-rapid-online-growth/")
    DOMESTIC_STORY_SECOND = DomesticUrl(
        "story/york-bag-retailer-goes-global-via-e-commerce/"
    )
    DOMESTIC_TERMS = DomesticUrl("terms-and-conditions/")
    DOMESTIC_PRIVACY = DomesticUrl("privacy-and-cookies/")

    # UNUSED DEFINITIONS
    # New Contact-Us UI - Domestic & International
    CONTACT_US_DOMESTIC = ContactUrl("contact/triage/domestic/")
    CONTACT_US_EXPORT_OPPORTUNITIES = ContactUrl("contact/triage/export-opportunities/")
    CONTACT_US_EXPORT_OPPORTUNITIES_NO_RESPONSE = ContactUrl(
        "contact/triage/export-opportunities/opportunity-no-response/"
    )
    CONTACT_US_EXPORT_OPPORTUNITIES_NOT_RELEVANT = ContactUrl(
        "contact/triage/export-opportunities/alerts-not-relevant/"
    )
    CONTACT_US_FORM_DOMESTIC = ContactUrl("contact/domestic/")
    CONTACT_US_FORM_DSO = ContactUrl("contact/defence-and-security-organisation/")
    CONTACT_US_FORM_EVENTS = ContactUrl("contact/events/")
    CONTACT_US_FORM_EXPORT_ADVICE = ContactUrl("contact/export-advice/comment/")
    CONTACT_US_FORM_INTERNATIONAL = ContactUrl("contact/international/")
    CONTACT_US_GREAT_ACCOUNT = ContactUrl("contact/triage/great-account/")
    CONTACT_US_GREAT_ACCOUNT_CH_LOGIN = ContactUrl(
        "contact/triage/great-account/companies-house-login/"
    )
    CONTACT_US_GREAT_ACCOUNT_NO_VERIFICATION_EMAIL = ContactUrl(
        "contact/triage/great-account/no-verification-email/"
    )
    CONTACT_US_GREAT_ACCOUNT_NO_VERIFICATION_LETTER = ContactUrl(
        "contact/triage/great-account/no-verification-letter/"
    )
    CONTACT_US_GREAT_ACCOUNT_PASSWORD_RESET = ContactUrl(
        "contact/triage/great-account/password-reset/"
    )
    CONTACT_US_GREAT_ACCOUNT_VERIFICATION_LETTER_CODE = ContactUrl(
        "contact/triage/great-account/verification-letter-code/"
    )
    CONTACT_US_GREAT_SERVICES = ContactUrl("contact/triage/great-services/")
    CONTACT_US_INTERNATIONAL = ContactUrl("contact/triage/international/")
    CONTACT_US_LANDING = ContactUrl("contact/triage/location/")
    CONTACT_US_OTHER_DOMESTIC_EU_EXIT = ContactUrl("eu-exit-news/contact/")
    CONTACT_US_OTHER_GET_FINANCE = ContactUrl("get-finance/contact/")
    CONTACT_US_OTHER_INTERNATIONAL_EU_EXIT = ContactUrl(
        "international/eu-exit-news/contact/"
    )

    # SOO Contact-Us pages
    CONTACT_US_SOO_ORGANISATION = ContactUrl("selling-online-overseas/organisation/")
    CONTACT_US_SOO_ORGANISATION_DETAILS = ContactUrl(
        "selling-online-overseas/organisation-details/"
    )
    CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE = ContactUrl(
        "selling-online-overseas/your-experience/"
    )
    CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS = ContactUrl(
        "selling-online-overseas/contact-details/"
    )
    CONTACT_US_SOO_ORGANISATION_SUCCESS = ContactUrl("selling-online-overseas/success/")

    # Legacy Contact-Us UI
    LEGACY_CONTACT_US_LANDING = LegacyContactUrl("")
    LEGACY_CONTACT_US_HELP = LegacyContactUrl("help/")
    LEGACY_CONTACT_US_FEEDBACK_FORM = LegacyContactUrl("help/FeedbackForm/")
    LEGACY_CONTACT_US_DIRECTORY_FEEDBACK_FORM = LegacyContactUrl(
        "directory/FeedbackForm"
    )

    # ExOpps UI - Export Opportunities
    EXOPPS_LANDING = ExOppsUrl("")
    EXOPPS_SITEMAP = ExOppsUrl("sitemap.xml")

    # SOO UI Selling Online Overseas
    SOO_LANDING = SOOUrl("")
    SOO_SITEMAP = SOOUrl("sitemap.xml")
    SOO_SEARCH_RESULTS = SOOUrl("markets/results/")
    SOO_MARKET_DETAILS = SOOUrl(
        "markets/details/", template="markets/details/{market}/"
    )

    # CMS API endpoints
    CMS_API_HEALTHCHECK = CMSApiUrl("healthcheck/")
    CMS_API_HEALTHCHECK_PING = CMSApiUrl("healthcheck/ping/")
    CMS_API_PAGES = CMSApiUrl("api/pages/")
    CMS_API_PAGE_BY_ID = CMSApiUrl(
        "api/pages/{page_id}/", template="api/pages/{page_id}/"
    )
    CMS_API_PAGE_BY_PATH = CMSApiUrl(
        "api/pages/lookup-by-path/{site_id}/{path}",
        template="api/pages/lookup-by-path/{site_id}/{path}",
    )
    CMS_API_PAGE_TYPES = CMSApiUrl("api/pages/types/")
    CMS_API_IMAGES = CMSApiUrl("api/images/")
    CMS_API_DOCUMENTS = CMSApiUrl("api/documents/")

    # Forms API endpoints
    FORMS_API_HEALTHCHECK = FormsApiUrl("api/healthcheck/")
    FORMS_API_HEALTHCHECK_PING = FormsApiUrl("api/healthcheck/ping/")
    FORMS_API_SUBMISSION = FormsApiUrl("api/submission/")
    FORMS_API_ADMIN = FormsApiUrl("admin/")
    FORMS_API_TESTAPI = FormsApiUrl("testapi/submissions-by-email/{email}/")

    # Trade Barriers
    TRADE_BARRIERS_LANDING = DomesticUrl("report-trade-barrier/")
    TRADE_BARRIERS_REPORT_FORM_ABOUT = DomesticUrl("report-trade-barrier/report/about/")
    TRADE_BARRIERS_REPORT_FORM_PROBLEM_DETAILS = DomesticUrl(
        "report-trade-barrier/report/problem-details/"
    )
    TRADE_BARRIERS_REPORT_FORM_SUMMARY = DomesticUrl(
        "report-trade-barrier/report/summary/"
    )
    TRADE_BARRIERS_REPORT_FORM_FINISHED = DomesticUrl(
        "report-trade-barrier/report/finished/"
    )
    TRADE_BARRIERS_REPORT_FORM_SUCCESS = DomesticUrl(
        "report-trade-barrier/report/success/"
    )
