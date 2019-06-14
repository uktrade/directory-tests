from enum import Enum, unique
from functools import partial
import os
import uuid
from typing import Union
from urllib.parse import urljoin

from tests.settings import (
    DIRECTORY_API_URL,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CONTACT_US_UI_URL,
    DIRECTORY_FORMS_API_URL,
    DIRECTORY_LEGACY_CONTACT_US_UI_URL,
    DIRECTORY_PROFILE_URL,
    DIRECTORY_SSO_API_CLIENT_BASE_URL,
    DIRECTORY_SSO_URL,
    DIRECTORY_UI_BUYER_URL,
    DIRECTORY_UI_INTERNATIONAL_URL,
    DIRECTORY_UI_SUPPLIER_URL,
    EXPORT_OPPORTUNITIES_UI_URL,
    EXRED_UI_URL,
    INVEST_UI_URL,
    ISD_UI_URL,
    SOO_UI_URL,
)

join_api = partial(urljoin, DIRECTORY_API_URL)
join_ui_international = partial(urljoin, DIRECTORY_UI_INTERNATIONAL_URL)
join_sso = partial(urljoin, DIRECTORY_SSO_URL)
join_sso_api = partial(urljoin, DIRECTORY_SSO_API_CLIENT_BASE_URL)
join_profile = partial(urljoin, DIRECTORY_PROFILE_URL)
join_ui_buyer = partial(urljoin, DIRECTORY_UI_BUYER_URL)
join_ui_supplier = partial(urljoin, DIRECTORY_UI_SUPPLIER_URL)
join_ui_invest = partial(urljoin, INVEST_UI_URL)
join_exred = partial(urljoin, EXRED_UI_URL)
join_exopps = partial(urljoin, EXPORT_OPPORTUNITIES_UI_URL)
join_contact_us = partial(urljoin, DIRECTORY_CONTACT_US_UI_URL)
join_legacy_contact_us = partial(urljoin, DIRECTORY_LEGACY_CONTACT_US_UI_URL)
join_soo = partial(urljoin, SOO_UI_URL)
join_cms_url = partial(urljoin, DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_api = partial(urljoin, DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_ui = partial(urljoin, DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_forms_api = partial(urljoin, DIRECTORY_FORMS_API_URL)

urls = {
    # SSO
    "sso:landing": "",
    "sso:login": "accounts/login/",
    "sso:signup": "accounts/signup/",
    "sso:logout": "accounts/logout/",
    "sso:password_change": "accounts/password/change/",
    "sso:password_set": "accounts/password/set/",
    "sso:password_reset": "accounts/password/reset/",
    "sso:email_confirm": "accounts/confirm-email/",
    "sso:inactive": "accounts/inactive/",

    # UI-BUYER
    "ui-buyer:landing": "",
    "ui-buyer:register": "register",
    "ui-buyer:register-confirm-company": "register/company/",
    "ui-buyer:register-confirm-export-status": "register/exports/",
    "ui-buyer:register-finish": "register/finished/",
    "ui-buyer:register-submit-account-details": "register-submit/",
    "ui-buyer:confirm-company-address": "verify/letter-confirm/",
    "ui-buyer:confirm-identity": "verify/",
    "ui-buyer:confirm-identity-letter": "verify/letter-send/",
    "ui-buyer:company-profile": "company-profile/",
    "ui-buyer:company-edit": "company-profile/edit/",
    "ui-buyer:company-edit-address": "company-profile/edit/address",
    "ui-buyer:company-edit-description": "company-profile/edit/description/",
    "ui-buyer:company-edit-key-facts": "company-profile/edit/key-facts/",
    "ui-buyer:company-edit-sectors": "company-profile/edit/sectors/",
    "ui-buyer:company-edit-contact": "company-profile/edit/contact/",
    "ui-buyer:account-add-collaborator": "account/add-collaborator/",
    "ui-buyer:account-remove-collaborator": "account/remove-collaborator/",
    "ui-buyer:account-transfer-ownership": "account/transfer/",
    "ui-buyer:account-confirm-password": "account/transfer/",
    "ui-buyer:account-confirm-ownership-transfer": "account/transfer/accept/?invite_key=",
    "ui-buyer:account-accept-invitation": "account/collaborate/accept/?invite_key={invite_key}",

    # UI-SUPPLIER
    "ui-supplier:landing": "",
    "ui-supplier:suppliers": "suppliers/",
    "ui-supplier:industries": "industries/",
    "ui-supplier:subscribe": "subscribe/",
    "ui-supplier:industries-health": "industries/healthcare/",
    "ui-supplier:industries-tech": "industries/technology/",
    "ui-supplier:industries-creative": "industries/creative-services/",
    "ui-supplier:industries-food": "industries/food-and-drink/",
    "ui-supplier:feedback": "feedback/",
    "ui-supplier:search": "search/",

    # UI-INTERNATIONAL
    "ui-international:landing": "",
    "ui-international:industries": "content/industries/",
    "ui-international:industry": "content/industries/",

    # API
    "api:enrolment": "enrolment/",
    "api:pre-verified-enrolment": "pre-verified-enrolment",
    "api:enrolment-trusted-code": "trusted-code/{code}/",

    "api:notifications-anonymous-unsubscribe": "notifications/anonymous-unsubscribe/",

    "api:buyer": "buyer/",
    "api:buyer-csv-dump": "buyer/csv-dump/",
    "api:supplier-csv-dump": "supplier/csv-dump/",

    "api:validate-company-number": "validate/company-number/",
    "api:companies-house-profile": "company/companies-house-profile/",

    "api:supplier": "supplier/",
    "api:supplier-unsubscribe": "supplier/unsubscribe/",

    "api:export-readiness-triage": "export-readiness/triage/",
    "api:export-readiness-article-read": "export-readiness/article-read/",
    "api:export-readiness-task-completed": "export-readiness/task-completed/",

    "api:export-opportunity-food": "export-opportunity/food/",
    "api:export-opportunity-legal": "export-opportunity/legal/",

    "api:public-company": "public/company/",
    "api:public-company-profile": "public/company/{companies_house_number}/",
    "api:public-case-study": "public/case-study/{id}/",


    "api:supplier-company": "supplier/company/",
    "api:supplier-company-case-study": "supplier/company/case-study/",
    "api:supplier-company-case-study-by-id": "supplier/company/case-study/{id}/",
    "api:supplier-company-verify": "supplier/company/verify/",
    "api:supplier-company-verify-companies-house": "supplier/company/verify/companies-house/",
    "api:contact-supplier": "contact/supplier/",
    "api:company-search": "company/search/",
    "api:case-study-search": "case-study/search/",

    "api:supplier-company-collaborators": "supplier/company/collaborators/",
    "api:supplier-company-collaboration-invite": "supplier/company/collaboration-invite/",
    "api:supplier-company-collaboration-invite-by-uuid": "supplier/company/collaboration-invite/{uuid}/",
    "api:supplier-company-remove-collaborators": "supplier/company/remove-collaborators/",

    "api:supplier-company-transfer-ownership-invite": "supplier/company/transfer-ownership-invite/",
    "api:supplier-company-transfer-ownership-invite-by-uuid": "supplier/company/transfer-ownership-invite/{uuid}/",
    "api:supplier-gecko-total-registered": "supplier/gecko/total-registered/",
    "api:activity-stream": "activity-stream/",
    "api:external-supplier-sso": "external/supplier-sso/",
    "api:external-supplier": "external/supplier/",

    # SSO-PROFILE
    "profile:soo": "selling-online-overseas/",
    "profile:fab": "find-a-buyer/",
    "profile:exops-alerts": "export-opportunities/email-alerts/",
    "profile:exops-applications": "export-opportunities/applications/",
    "profile:landing": "",
    "profile:about": "about/",
    "profile:enrol": "enrol/",
    "profile:enrol-user-account": "enrol/business-type/companies-house/user-account/",
    "profile:enrol-email-verification": "enrol/business-type/companies-house/verification/",
    "profile:enrol-companies-house-search": "enrol/business-type/companies-house/search/",
    "profile:enrol-business-details": "enrol/business-type/companies-house/business-details/",
    "profile:enrol-personal-details": "enrol/business-type/companies-house/personal-details/",
    "profile:enrol-finished": "enrol/business-type/companies-house/finished/",
    "profile:edit-company-description": "find-a-buyer/description/",
    "profile:edit-company-business-details": "find-a-buyer/business-details/",
    "profile:publish-business-profile-to-fas": "find-a-buyer/publish/",
    "profile:add-products-and-services": "find-a-buyer/add-expertise/products-and-services/",
    "profile:case-study-edit": "find-a-buyer/case-study/{case_number}/details/",
    "profile:case-study-details": "find-a-buyer/case-study/details/",
    "profile:case-study-images": "find-a-buyer/case-study/images/",
    "profile:upload-logo": "find-a-buyer/logo/",
    "profile:company-edit-social-media": "find-a-buyer/social-links/",

    # ExRed UI
    "ui-exred:search": "search/",
    "ui-exred:landing": "",
    "ui-exred:landing-uk": "?lang=en-gb",
    "ui-exred:international": "international/",
    "ui-exred:international-uk": "international/?lang=en-gb",
    "ui-exred:international-zh": "international/?lang=zh-hans",
    "ui-exred:international-de": "international/?lang=de",
    "ui-exred:international-ja": "international/?lang=ja",
    "ui-exred:international-es": "international/?lang=es",
    "ui-exred:international-pt": "international/?lang=pt",
    "ui-exred:international-ar": "international/?lang=ar",
    "ui-exred:triage-sector": "triage/sector/",
    "ui-exred:triage-exported-before": "triage/exported-before/",
    "ui-exred:triage-regular-exporter": "triage/regular-exporter/",
    "ui-exred:triage-online-marketplace": "triage/online-marketplace/",
    "ui-exred:triage-companies-house": "triage/companies-house/",
    "ui-exred:triage-company": "triage/company/",
    "ui-exred:triage-summary": "triage/summary/",
    "ui-exred:custom": "custom/",
    "ui-exred:new": "new/",
    "ui-exred:occasional": "occasional/",
    "ui-exred:regular": "regular/",
    "ui-exred:market-research": "market-research/",
    "ui-exred:customer-insight": "customer-insight/",
    "ui-exred:finance": "finance/",
    "ui-exred:business-planning": "business-planning/",
    "ui-exred:getting-paid": "getting-paid/",
    "ui-exred:operations-and-compliance": "operations-and-compliance/",
    "ui-exred:get-finance": "get-finance/",
    "ui-exred:story-first": "story/online-marketplaces-propel-freestyle-xtreme-sales/",
    "ui-exred:story-second": "story/hello-babys-rapid-online-growth/",
    "ui-exred:story-third": "story/york-bag-retailer-goes-global-via-e-commerce/",
    "ui-exred:terms": "terms-and-conditions/",
    "ui-exred:privacy": "privacy-and-cookies/",

    # New Contact-Us UI - Domestic & International
    "ui-contact-us:triage-landing": "contact/triage/location/",
    "ui-contact-us:triage-domestic": "contact/triage/domestic/",
    "ui-contact-us:triage-international": "contact/triage/international/",
    "ui-contact-us:triage-great-services": "contact/triage/great-services/",
    "ui-contact-us:triage-export-opportunities": "contact/triage/export-opportunities/",
    "ui-contact-us:triage-export-opportunities-no-response": "contact/triage/export-opportunities/opportunity-no-response/",
    "ui-contact-us:triage-export-opportunities-not-relevant": "contact/triage/export-opportunities/alerts-not-relevant/",
    "ui-contact-us:triage-great-account": "contact/triage/great-account/",
    "ui-contact-us:triage-great-account-password-reset": "contact/triage/great-account/password-reset/",
    "ui-contact-us:triage-great-account-ch-login": "contact/triage/great-account/companies-house-login/",
    "ui-contact-us:triage-great-account-verification-letter-code": "contact/triage/great-account/verification-letter-code/",
    "ui-contact-us:triage-great-account-no-verification-email": "contact/triage/great-account/no-verification-email/",
    "ui-contact-us:triage-great-account-no-verification-letter": "contact/triage/great-account/no-verification-letter/",

    # New Contact-Us UI - forms
    "ui-contact-us:form-domestic": "contact/domestic/",
    "ui-contact-us:form-international": "contact/international/",
    "ui-contact-us:form-dso": "contact/defence-and-security-organisation/",
    "ui-contact-us:form-events": "contact/events/",
    "ui-contact-us:form-export-advice": "contact/export-advice/comment/",

    # Other Contact-Us pages
    "ui-contact-us:other-domestic-eu-exit": "eu-exit-news/contact/",
    "ui-contact-us:other-international-eu-exit": "international/eu-exit-news/contact/",
    "ui-contact-us:other-get-finance": "get-finance/contact/",
    "ui-contact-us:soo:organisation": "selling-online-overseas/organisation",
    "ui-contact-us:soo:organisation:details": "selling-online-overseas/organisation-details",
    "ui-contact-us:soo:organisation:your-experience": "selling-online-overseas/your-experience",
    "ui-contact-us:soo:organisation:contact-details": "selling-online-overseas/contact-details",
    "ui-contact-us:soo:organisation:success": "selling-online-overseas/success",

    # Legacy Contact-Us UI
    "legacy-ui-contact-us:help": "help/",
    "legacy-ui-contact-us:feedback-form": "help/FeedbackForm/",
    "legacy-ui-contact-us:directory": "directory/",
    "legacy-ui-contact-us:directory-feedback-form": "directory/FeedbackForm/",
    "legacy-ui-contact-us:soo-triage": "triage/",
    "legacy-ui-contact-us:soo-triage-form": "triage/soo/",
    "legacy-ui-contact-us:soo-triage-feedback-form": "FeedbackForm/TriageForm/",

    # ExOpps UI - Export Opportunities
    "ui-exopps:landing": "",

    # SOO UI Selling Online Overseas
    "ui-soo:landing": "",
    "ui-soo:search-results": "markets/results/",
    "ui-soo:market-details": "markets/details/",

    # Forms API endpoints
    "forms-api:submission": "api/submission/",
    "forms-api:admin": "admin/",
    "forms-api:testapi": "testapi/submissions-by-email/{email}/",
}

# these user credentials are hard-coded in `directory-sso`. The users
# are created when `manage.py create_test_users` is ran on sso.
users = {
    "verified": {
        "username": os.environ["SSO_USER_USERNAME"],
        "password": os.environ["SSO_USER_PASSWORD"],
        "token": os.environ["SSO_USER_TOKEN"],
        "sso_id": int(os.environ["SSO_USER_SSO_ID"])
    },
    "unverified": {
        "token": os.environ["SSO_UNVERIFIED_USER_TOKEN"]
    }
}


companies = {
    "not_active": os.getenv(
        "SSO_COMPANY_NOT_ACTIVE", "06542942"
    ),
    "already_registered": os.getenv(
        "SSO_COMPANY_ALREADY_REGISTERED", "10416664"
    ),
    "active_not_registered": os.getenv(
        "SSO_COMPANY_ACTIVE_NOT_REGISTERED", "01624297"
    ),
}


def get_relative_url(name):
    return urls[name]


def get_absolute_url(name):
    relative_url = get_relative_url(name)
    if name.startswith("sso:"):
        return join_sso(relative_url)
    elif name.startswith("sso-api:"):
        return join_sso_api(relative_url)
    elif name.startswith("ui-buyer:"):
        return join_ui_buyer(relative_url)
    elif name.startswith("ui-supplier:"):
        return join_ui_supplier(relative_url)
    elif name.startswith("ui-invest:"):
        return join_ui_invest(relative_url)
    elif name.startswith("api:"):
        return join_api(relative_url)
    elif name.startswith("profile:"):
        return join_profile(relative_url)
    elif name.startswith("ui-exred:"):
        return join_exred(relative_url)
    elif name.startswith("ui-contact-us:"):
        return join_contact_us(relative_url)
    elif name.startswith("legacy-ui-contact-us:"):
        return join_legacy_contact_us(relative_url)
    elif name.startswith("ui-soo:"):
        return join_soo(relative_url)
    elif name.startswith("cms-api:"):
        return join_cms_api(relative_url)
    elif name.startswith("cms-healthcheck:"):
        return join_cms_url(relative_url)
    elif name.startswith("cms-ui:"):
        return join_cms_ui(relative_url)
    elif name.startswith("forms-api:"):
        return join_forms_api(relative_url)
    elif name.startswith("ui-international"):
        return join_ui_international(relative_url)
    elif name.startswith("ui-exopps:"):
        return join_exopps(relative_url)


def get_random_email_address():
    return "{}@example.com".format(uuid.uuid4())


def retriable_error(exception):
    """Return True if test should be re-run based on the Exception"""
    return isinstance(exception, (AssertionError, ))


def is_500(exception):
    """Return True exception message contains 500"""
    return "500" in str(exception)


class Url:

    def __init__(
            self, service_url: str, relative_endpoint: str, *,
            template: str = None
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
        super().__init__(
            DIRECTORY_CMS_API_CLIENT_BASE_URL, endpoint, template=template
        )


class ContactUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(
            DIRECTORY_CONTACT_US_UI_URL, endpoint, template=template
        )


class DirectoryApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_API_URL, endpoint, template=template)


class DomesticUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(EXRED_UI_URL, endpoint, template=template)


class ExOppsUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(
            EXPORT_OPPORTUNITIES_UI_URL, endpoint, template=template
        )


class FABUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_UI_BUYER_URL, endpoint, template=template)


class FABApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_UI_BUYER_URL, endpoint, template=template)


class FASUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_UI_SUPPLIER_URL, endpoint, template=template)


class FormsApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_FORMS_API_URL, endpoint, template=template)


class InternationalUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(
            DIRECTORY_UI_INTERNATIONAL_URL, endpoint, template=template
        )


class InvestUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(INVEST_UI_URL, endpoint, template=template)


class ISDUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(ISD_UI_URL, endpoint, template=template)


class LegacyContactUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(
            DIRECTORY_LEGACY_CONTACT_US_UI_URL, endpoint, template=template
        )


class ProfileUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_PROFILE_URL, endpoint, template=template)


class SOOUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(SOO_UI_URL, endpoint, template=template)


class SSOUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(DIRECTORY_SSO_URL, endpoint, template=template)


class SSOApiUrl(Url):
    def __init__(self, endpoint: str, *, template: str = None):
        super().__init__(
            DIRECTORY_SSO_API_CLIENT_BASE_URL, endpoint, template=template
        )


@unique
class URLs(Enum):
    """This Enum is to help discover, refactor, find usage of URLs"""

    def __str__(self) -> str:
        return (f"{self._name_} absolute URL: {self.value.absolute} relative "
                f"URL: {self.value.relative}")

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
    DIR_API_NOTIFICATIONS_ANONYMOUS_UNSUBSCRIBE = DirectoryApiUrl("notifications/anonymous-unsubscribe/")
    DIR_API_BUYER = DirectoryApiUrl("buyer/")
    DIR_API_BUYER_CSV_DUMP = DirectoryApiUrl("buyer/csv-dump/")
    DIR_API_SUPPLIER_CSV_DUMP = DirectoryApiUrl("supplier/csv-dump/")
    DIR_API_VALIDATE_COMPANY_NUMBER = DirectoryApiUrl("validate/company-number/")
    DIR_API_COMPANIES_HOUSE_PROFILE = DirectoryApiUrl("company/companies-house-profile/")
    DIR_API_SUPPLIER = DirectoryApiUrl("supplier/")
    DIR_API_SUPPLIER_UNSUBSCRIBE = DirectoryApiUrl("supplier/unsubscribe/")
    DIR_API_EXPORT_READINESS_TRIAGE = DirectoryApiUrl("export-readiness/triage/")
    DIR_API_EXPORT_READINESS_ARTICLE_READ = DirectoryApiUrl("export-readiness/article-read/")
    DIR_API_EXPORT_READINESS_TASK_COMPLETED = DirectoryApiUrl("export-readiness/task-completed/")
    DIR_API_EXPORT_OPPORTUNITY_FOOD = DirectoryApiUrl("export-opportunity/food/")
    DIR_API_EXPORT_OPPORTUNITY_LEGAL = DirectoryApiUrl("export-opportunity/legal/")
    DIR_API_PUBLIC_COMPANY = DirectoryApiUrl("public/company/")
    DIR_API_PUBLIC_COMPANY_PROFILE = DirectoryApiUrl("public/company/{companies_house_number}/")
    DIR_API_PUBLIC_CASE_STUDY = DirectoryApiUrl("public/case-study/{id}/")
    DIR_API_SUPPLIER_COMPANY = DirectoryApiUrl("supplier/company/")
    DIR_API_SUPPLIER_COMPANY_CASE_STUDY = DirectoryApiUrl("supplier/company/case-study/")
    DIR_API_SUPPLIER_COMPANY_CASE_STUDY_BY_ID = DirectoryApiUrl("supplier/company/case-study/{id}/")
    DIR_API_SUPPLIER_COMPANY_VERIFY = DirectoryApiUrl("supplier/company/verify/")
    DIR_API_SUPPLIER_COMPANY_VERIFY_COMPANIES_HOUSE = DirectoryApiUrl("supplier/company/verify/companies-house/")
    DIR_API_CONTACT_SUPPLIER = DirectoryApiUrl("contact/supplier/")
    DIR_API_COMPANY_SEARCH = DirectoryApiUrl("company/search/")
    DIR_API_CASE_STUDY_SEARCH = DirectoryApiUrl("case-study/search/")
    DIR_API_SUPPLIER_COMPANY_COLLABORATORS = DirectoryApiUrl("supplier/company/collaborators/")
    DIR_API_SUPPLIER_COMPANY_COLLABORATION_INVITE = DirectoryApiUrl("supplier/company/collaboration-invite/")
    DIR_API_SUPPLIER_COMPANY_COLLABORATION_INVITE_BY_UUID = DirectoryApiUrl("supplier/company/collaboration-invite/{uuid}/")
    DIR_API_SUPPLIER_COMPANY_REMOVE_COLLABORATORS = DirectoryApiUrl("supplier/company/remove-collaborators/")
    DIR_API_SUPPLIER_COMPANY_TRANSFER_OWNERSHIP_INVITE = DirectoryApiUrl("supplier/company/transfer-ownership-invite/")
    DIR_API_SUPPLIER_COMPANY_TRANSFER_OWNERSHIP_INVITE_BY_UUID = DirectoryApiUrl("supplier/company/transfer-ownership-invite/{uuid}/")
    DIR_API_SUPPLIER_GECKO_TOTAL_REGISTERED = DirectoryApiUrl("supplier/gecko/total-registered/")
    DIR_API_ACTIVITY_STREAM = DirectoryApiUrl("activity-stream/")
    DIR_API_EXTERNAL_SUPPLIER_SSO = DirectoryApiUrl("external/supplier-sso/")
    DIR_API_EXTERNAL_SUPPLIER = DirectoryApiUrl("external/supplier/")

    # SSO UI
    SSO_LANDING = SSOUrl("")
    SSO_EMAIL_CONFIRM = SSOUrl("accounts/confirm-email/")
    SSO_INACTIVE = SSOUrl("accounts/inactive/")
    SSO_LOGIN = SSOUrl("accounts/login/")
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
    FAB_API_COMPANIES_HOUSE_SEARCH = FABApiUrl("api/internal/companies-house-search/", template="api/internal/companies-house-search/?term={term}")
    FAB_LANDING = FABUrl("")
    FAB_ACCOUNT_ACCEPT_INVITATION = FABUrl("account/collaborate/accept/?invite_key={invite_key}", template="account/collaborate/accept/?invite_key={invite_key}")
    FAB_ACCOUNT_ADD_COLLABORATOR = FABUrl("account/add-collaborator/")
    FAB_ACCOUNT_CONFIRM_OWNERSHIP_TRANSFER = FABUrl("account/transfer/accept/?invite_key=", template="account/transfer/accept/?invite_key={invite_key}")
    FAB_ACCOUNT_CONFIRM_PASSWORD = FABUrl("account/transfer/")
    FAB_ACCOUNT_REMOVE_COLLABORATOR = FABUrl("account/remove-collaborator/")
    FAB_ACCOUNT_TRANSFER_OWNERSHIP = FABUrl("account/transfer/")
    FAB_COMPANY_EDIT = FABUrl("company-profile/edit/")
    FAB_COMPANY_EDIT_ADDRESS = FABUrl("company-profile/edit/address/")
    FAB_COMPANY_EDIT_CONTACT = FABUrl("company-profile/edit/contact/")
    FAB_COMPANY_EDIT_DESCRIPTION = FABUrl("company-profile/edit/description/")
    FAB_COMPANY_EDIT_KEY_FACTS = FABUrl("company-profile/edit/key-facts/")
    FAB_COMPANY_EDIT_SECTORS = FABUrl("company-profile/edit/sectors/")
    FAB_COMPANY_PROFILE = FABUrl("company-profile/")
    FAB_CONFIRM_COMPANY_ADDRESS = FABUrl("verify/letter-confirm/")
    FAB_CONFIRM_IDENTITY = FABUrl("verify/")
    FAB_CONFIRM_IDENTITY_LETTER = FABUrl("verify/letter-send/")
    FAB_HEALTHCHECK = FABUrl("healthcheck/")
    FAB_REGISTER = FABUrl("register/")
    FAB_REGISTER_CONFIRM_COMPANY = FABUrl("register/company/")
    FAB_REGISTER_CONFIRM_EXPORT_STATUS = FABUrl("register/exports/")
    FAB_REGISTER_FINISH = FABUrl("register/finished/")
    FAB_REGISTER_SUBMIT_ACCOUNT_DETAILS = FABUrl("register-submit/")

    # Find a Supplier
    FAS_LANDING = FASUrl("")
    FAS_HEALTHCHECK = FASUrl("healthcheck/")
    FAS_SUPPLIERS = FASUrl("suppliers/")
    FAS_INDUSTRIES = FASUrl("industries/", template="industries/{industry}/")
    FAS_SUBSCRIBE = FASUrl("subscribe/")
    FAS_FEEDBACK = FASUrl("feedback/")
    FAS_SEARCH = FASUrl("search/")

    # Legacy FAS industry endpoints before slugs were changed to:
    # healthcare, technology & creative-services respectively
    FAS_INDUSTRIES_HEALTH = FASUrl("industries/health/")
    FAS_INDUSTRIES_TECH = FASUrl("industries/tech/")
    FAS_INDUSTRIES_CREATIVE = FASUrl("industries/creative/")

    # New International site
    INTERNATIONAL_LANDING = InternationalUrl("")
    INTERNATIONAL_INDUSTRIES = InternationalUrl("content/industries/", template="content/industries/{industry}/")
    INTERNATIONAL_INDUSTRY_ADVANCED_MANUFACTURING = InternationalUrl("content/industries/advanced-manufacturing/")
    INTERNATIONAL_INDUSTRY_AEROSPACE = InternationalUrl("content/industries/aerospace/")
    INTERNATIONAL_INDUSTRY_AGRI_TECH = InternationalUrl("content/industries/agri-tech/")
    INTERNATIONAL_INDUSTRY_ASSET_MANAGEMENT = InternationalUrl("content/industries/asset-management/")
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE = InternationalUrl("content/industries/automotive/")
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT = InternationalUrl("content/industries/automotive-research-and-development/")
    INTERNATIONAL_INDUSTRY_AUTOMOTIVE_SUPPLY_CHAIN = InternationalUrl("content/industries/automotive-supply-chain/")
    INTERNATIONAL_INDUSTRY_CAPITAL_INVESTMENT = InternationalUrl("content/industries/capital-investment/")
    INTERNATIONAL_INDUSTRY_CHEMICALS = InternationalUrl("content/industries/chemicals/")
    INTERNATIONAL_INDUSTRY_CREATIVE_CONTENT_AND_PRODUCTION = InternationalUrl("content/industries/creative-content-and-production/")
    INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES = InternationalUrl("content/industries/creative-industries/")
    INTERNATIONAL_INDUSTRY_DATA_ANALYTICS = InternationalUrl("content/industries/data-analytics/")
    INTERNATIONAL_INDUSTRY_DIGITAL_MEDIA = InternationalUrl("content/industries/digital-media/")
    INTERNATIONAL_INDUSTRY_ELECTRICAL_NETWORKS = InternationalUrl("content/industries/electrical-networks/")
    INTERNATIONAL_INDUSTRY_ENERGY = InternationalUrl("content/industries/energy/")
    INTERNATIONAL_INDUSTRY_ENERGY_WASTE = InternationalUrl("content/industries/energy-waste/")
    INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING = InternationalUrl("content/industries/engineering-and-manufacturing/")
    INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES = InternationalUrl("content/industries/financial-services/")
    INTERNATIONAL_INDUSTRY_FINANCIAL_TECHNOLOGY = InternationalUrl("content/industries/financial-technology/")
    INTERNATIONAL_INDUSTRY_FOOD_AND_DRINK = InternationalUrl("content/industries/food-and-drink/")
    INTERNATIONAL_INDUSTRY_FOOD_SERVICE_AND_CATERING = InternationalUrl("content/industries/food-service-and-catering/")
    INTERNATIONAL_INDUSTRY_FREE_FOODS = InternationalUrl("content/industries/free-foods/")
    INTERNATIONAL_INDUSTRY_HEALTH_AND_LIFE_SCIENCES = InternationalUrl("content/industries/health-and-life-sciences/")
    INTERNATIONAL_INDUSTRY_MEAT_POULTRY_AND_DAIRY = InternationalUrl("content/industries/meat-poultry-and-dairy/")
    INTERNATIONAL_INDUSTRY_MEDICAL_TECHNOLOGY = InternationalUrl("content/industries/medical-technology/")
    INTERNATIONAL_INDUSTRY_MOTORSPORT = InternationalUrl("content/industries/motorsport/")
    INTERNATIONAL_INDUSTRY_NUCLEAR_ENERGY = InternationalUrl("content/industries/nuclear-energy/")
    INTERNATIONAL_INDUSTRY_OFFSHORE_WIND_ENERGY = InternationalUrl("content/industries/offshore-wind-energy/")
    INTERNATIONAL_INDUSTRY_OIL_AND_GAS = InternationalUrl("content/industries/oil-and-gas/")
    INTERNATIONAL_INDUSTRY_PHARMACEUTICAL_MANUFACTURING = InternationalUrl("content/industries/pharmaceutical-manufacturing/")
    INTERNATIONAL_INDUSTRY_RETAIL = InternationalUrl("content/industries/retail/")
    INTERNATIONAL_INDUSTRY_TECHNOLOGY = InternationalUrl("content/industries/technology/")
    INTERNATIONAL_HEALTHCHECK_FORMS_API = InternationalUrl("healthcheck/forms-api/")
    INTERNATIONAL_HEALTHCHECK_SENTRY = InternationalUrl("healthcheck/sentry/")
    INTERNATIONAL_UK_SETUP_GUIDE = InternationalUrl("content/how-to-setup-in-the-uk/", template="content/how-to-setup-in-the-uk/{guide}/")
    INTERNATIONAL_UK_SETUP_GUIDE_UK_VISAS = InternationalUrl("content/how-to-setup-in-the-uk/uk-visas-and-migration/")
    INTERNATIONAL_UK_SETUP_GUIDE_ESTABLISH_A_BASE = InternationalUrl("content/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk/")
    INTERNATIONAL_UK_SETUP_GUIDE_HIRE_SKILLED_WORKERS = InternationalUrl("content/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/")
    INTERNATIONAL_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT = InternationalUrl("content/how-to-setup-in-the-uk/open-a-uk-business-bank-account/")
    INTERNATIONAL_UK_SETUP_GUIDE_REGISTER_A_COMPANY = InternationalUrl("content/how-to-setup-in-the-uk/register-a-company-in-the-uk/")
    INTERNATIONAL_UK_SETUP_GUIDE_UK_TAX = InternationalUrl("content/how-to-setup-in-the-uk/uk-tax-and-incentives/")

    # Invest site
    INVEST_LANDING = InvestUrl("")
    INVEST_HEALTHCHECK = InvestUrl("healthcheck/")
    INVEST_CONTACT = InvestUrl("contact/")
    INVEST_INDUSTRIES = InvestUrl("industries/")
    INVEST_UK_SETUP_GUIDE = InvestUrl("uk-setup-guide/")
    INVEST_HPO_RAIL = InvestUrl("high-potential-opportunities/rail-infrastructure/")
    INVEST_HPO_RAIL_CONTACT = InvestUrl("high-potential-opportunities/rail-infrastructure/contact/")
    INVEST_HPO_FOOD = InvestUrl("high-potential-opportunities/food-production/")
    INVEST_HPO_FOOD_CONTACT = InvestUrl("high-potential-opportunities/food-production/contact/")
    INVEST_HPO_LIGHTWEIGHT = InvestUrl("high-potential-opportunities/lightweight-structures/")
    INVEST_HPO_LIGHTWEIGHT_CONTACT = InvestUrl("high-potential-opportunities/lightweight-structures/contact/")
    INVEST_INDUSTRIES_ADVANCED_MANUFACTURING = InvestUrl("industries/advanced-manufacturing/")
    INVEST_INDUSTRIES_AEROSPACE = InvestUrl("industries/aerospace/")
    INVEST_INDUSTRIES_AGRI_TECH = InvestUrl("industries/agri-tech/")
    INVEST_INDUSTRIES_ASSET_MANAGEMENT = InvestUrl("industries/asset-management/")
    INVEST_INDUSTRIES_AUTOMOTIVE = InvestUrl("industries/automotive/")
    INVEST_INDUSTRIES_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT = InvestUrl("industries/automotive-research-and-development/")
    INVEST_INDUSTRIES_AUTOMOTIVE_SUPPLY_CHAIN = InvestUrl("industries/automotive-supply-chain/")
    INVEST_INDUSTRIES_CAPITAL_INVESTMENT = InvestUrl("industries/capital-investment/")
    INVEST_INDUSTRIES_CHEMICALS = InvestUrl("industries/chemicals/")
    INVEST_INDUSTRIES_CREATIVE_CONTENT_AND_PRODUCTION = InvestUrl("industries/creative-content-and-production/")
    INVEST_INDUSTRIES_CREATIVE_INDUSTRIES = InvestUrl("industries/creative-industries/")
    INVEST_INDUSTRIES_DATA_ANALYTICS = InvestUrl("industries/data-analytics/")
    INVEST_INDUSTRIES_DIGITAL_MEDIA = InvestUrl("industries/digital-media/")
    INVEST_INDUSTRIES_ELECTRICAL_NETWORKS = InvestUrl("industries/electrical-networks/")
    INVEST_INDUSTRIES_ENERGY = InvestUrl("industries/energy/")
    INVEST_INDUSTRIES_ENERGY_WASTE = InvestUrl("industries/energy-waste/")
    INVEST_INDUSTRIES_FINANCIAL_SERVICES = InvestUrl("industries/financial-services/")
    INVEST_INDUSTRIES_FINANCIAL_TECHNOLOGY = InvestUrl("industries/financial-technology/")
    INVEST_INDUSTRIES_FOOD_AND_DRINK = InvestUrl("industries/food-and-drink/")
    INVEST_INDUSTRIES_FOOD_SERVICE_AND_CATERING = InvestUrl("industries/food-service-and-catering/")
    INVEST_INDUSTRIES_FREE_FOODS = InvestUrl("industries/free-foods/")
    INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES = InvestUrl("industries/health-and-life-sciences/")
    INVEST_INDUSTRIES_MEAT_POULTRY_AND_DAIRY = InvestUrl("industries/meat-poultry-and-dairy/")
    INVEST_INDUSTRIES_MEDICAL_TECHNOLOGY = InvestUrl("industries/medical-technology/")
    INVEST_INDUSTRIES_MOTORSPORT = InvestUrl("industries/motorsport/")
    INVEST_INDUSTRIES_NUCLEAR_ENERGY = InvestUrl("industries/nuclear-energy/")
    INVEST_INDUSTRIES_OFFSHORE_WIND_ENERGY = InvestUrl("industries/offshore-wind-energy/")
    INVEST_INDUSTRIES_OIL_AND_GAS = InvestUrl("industries/oil-and-gas/")
    INVEST_INDUSTRIES_PHARMACEUTICAL_MANUFACTURING = InvestUrl("industries/pharmaceutical-manufacturing/")
    INVEST_INDUSTRIES_RETAIL = InvestUrl("industries/retail/")
    INVEST_INDUSTRIES_TECHNOLOGY = InvestUrl("industries/technology/")

    ISD_LANDING = ISDUrl("")
    ISD_SEARCH = ISDUrl("search/")

    # FAS/ISD Profile 
    PROFILE_HEALTHCHECK = ProfileUrl("healthcheck/")
    PROFILE_HEALTHCHECK_PING = ProfileUrl("healthcheck/ping/")
    PROFILE_SOO = ProfileUrl("selling-online-overseas/")
    PROFILE_FAB = ProfileUrl("find-a-buyer/")
    PROFILE_EXOPS_ALERTS = ProfileUrl("export-opportunities/email-alerts/")
    PROFILE_EXOPS_APPLICATIONS = ProfileUrl("export-opportunities/applications/")
    PROFILE_LANDING = ProfileUrl("")
    PROFILE_ABOUT = ProfileUrl("about/")
    PROFILE_ENROL = ProfileUrl("enrol/")
    PROFILE_ENROL_USER_ACCOUNT = ProfileUrl("enrol/business-type/companies-house/user-account/")
    PROFILE_ENROL_EMAIL_VERIFICATION = ProfileUrl("enrol/business-type/companies-house/verification/")
    PROFILE_ENROL_COMPANIES_HOUSE_SEARCH = ProfileUrl("enrol/business-type/companies-house/search/")
    PROFILE_ENROL_BUSINESS_DETAILS = ProfileUrl("enrol/business-type/companies-house/business-details/")
    PROFILE_ENROL_PERSONAL_DETAILS = ProfileUrl("enrol/business-type/companies-house/personal-details/")
    PROFILE_ENROL_FINISHED = ProfileUrl("enrol/business-type/companies-house/finished/")
    PROFILE_EDIT_COMPANY_DESCRIPTION = ProfileUrl("find-a-buyer/description/")
    PROFILE_EDIT_COMPANY_BUSINESS_DETAILS = ProfileUrl("find-a-buyer/business-details/")
    PROFILE_PUBLISH_BUSINESS_PROFILE_TO_FAS = ProfileUrl("find-a-buyer/publish/")
    PROFILE_ADD_PRODUCTS_AND_SERVICES = ProfileUrl("find-a-buyer/add-expertise/products-and-services/")
    PROFILE_CASE_STUDY_EDIT = ProfileUrl("find-a-buyer/case-study/{case_number}/details/")
    PROFILE_CASE_STUDY_DETAILS = ProfileUrl("find-a-buyer/case-study/details/")
    PROFILE_CASE_STUDY_IMAGES = ProfileUrl("find-a-buyer/case-study/images/")
    PROFILE_UPLOAD_LOGO = ProfileUrl("find-a-buyer/logo/")
    PROFILE_COMPANY_EDIT_SOCIAL_MEDIA = ProfileUrl("find-a-buyer/social-links/")

    # Domestic site
    DOMESTIC_HEALTHCHECK = DomesticUrl("healthcheck/")
    DOMESTIC_HEALTHCHECK_PING = DomesticUrl("healthcheck/ping/")
    DOMESTIC_SEARCH = DomesticUrl("search/")
    DOMESTIC_LANDING = DomesticUrl("")
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
    DOMESTIC_STORY_FIRST = DomesticUrl("story/online-marketplaces-propel-freestyle-xtreme-sales/")
    DOMESTIC_STORY_SECOND = DomesticUrl("story/hello-babys-rapid-online-growth/")
    DOMESTIC_STORY_THIRD = DomesticUrl("story/york-bag-retailer-goes-global-via-e-commerce/")
    DOMESTIC_TERMS = DomesticUrl("terms-and-conditions/")
    DOMESTIC_PRIVACY = DomesticUrl("privacy-and-cookies/")

    # New Contact-Us UI - Domestic & International
    CONTACT_US_LANDING = ContactUrl("contact/triage/location/")
    CONTACT_US_DOMESTIC = ContactUrl("contact/triage/domestic/")
    CONTACT_US_INTERNATIONAL = ContactUrl("contact/triage/international/")
    CONTACT_US_GREAT_SERVICES = ContactUrl("contact/triage/great-services/")
    CONTACT_US_EXPORT_OPPORTUNITIES = ContactUrl("contact/triage/export-opportunities/")
    CONTACT_US_EXPORT_OPPORTUNITIES_NO_RESPONSE = ContactUrl("contact/triage/export-opportunities/opportunity-no-response/")
    CONTACT_US_EXPORT_OPPORTUNITIES_NOT_RELEVANT = ContactUrl("contact/triage/export-opportunities/alerts-not-relevant/")
    CONTACT_US_GREAT_ACCOUNT = ContactUrl("contact/triage/great-account/")
    CONTACT_US_GREAT_ACCOUNT_PASSWORD_RESET = ContactUrl("contact/triage/great-account/password-reset/")
    CONTACT_US_GREAT_ACCOUNT_CH_LOGIN = ContactUrl("contact/triage/great-account/companies-house-login/")
    CONTACT_US_GREAT_ACCOUNT_VERIFICATION_LETTER_CODE = ContactUrl("contact/triage/great-account/verification-letter-code/")
    CONTACT_US_GREAT_ACCOUNT_NO_VERIFICATION_EMAIL = ContactUrl("contact/triage/great-account/no-verification-email/")
    CONTACT_US_GREAT_ACCOUNT_NO_VERIFICATION_LETTER = ContactUrl("contact/triage/great-account/no-verification-letter/")

    # New Contact-Us UI - forms
    CONTACT_US_FORM_DOMESTIC = ContactUrl("contact/domestic/")
    CONTACT_US_FORM_INTERNATIONAL = ContactUrl("contact/international/")
    CONTACT_US_FORM_DSO = ContactUrl("contact/defence-and-security-organisation/")
    CONTACT_US_FORM_EVENTS = ContactUrl("contact/events/")
    CONTACT_US_FORM_EXPORT_ADVICE = ContactUrl("contact/export-advice/comment/")
    
    # Other Contact-Us pages
    CONTACT_US_OTHER_DOMESTIC_EU_EXIT = ContactUrl("eu-exit-news/contact/")
    CONTACT_US_OTHER_INTERNATIONAL_EU_EXIT = ContactUrl("international/eu-exit-news/contact/")
    CONTACT_US_OTHER_GET_FINANCE = ContactUrl("get-finance/contact/")
    CONTACT_US_SOO_ORGANISATION = ContactUrl("selling-online-overseas/organisation/")
    CONTACT_US_SOO_ORGANISATION_DETAILS = ContactUrl("selling-online-overseas/organisation-details/")
    CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE = ContactUrl("selling-online-overseas/your-experience/")
    CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS = ContactUrl("selling-online-overseas/contact-details/")
    CONTACT_US_SOO_ORGANISATION_SUCCESS = ContactUrl("selling-online-overseas/success/")

    # Legacy Contact-Us UI
    LEGACY_CONTACT_US_HELP = LegacyContactUrl("help/")
    LEGACY_CONTACT_US_FEEDBACK_FORM = LegacyContactUrl("help/FeedbackForm/")
    LEGACY_CONTACT_US_DIRECTORY = LegacyContactUrl("directory/")
    LEGACY_CONTACT_US_DIRECTORY_FEEDBACK_FORM = LegacyContactUrl("directory/FeedbackForm/")
    LEGACY_CONTACT_US_SOO_TRIAGE = LegacyContactUrl("triage/")
    LEGACY_CONTACT_US_SOO_TRIAGE_FORM = LegacyContactUrl("triage/soo/")
    LEGACY_CONTACT_US_SOO_TRIAGE_FEEDBACK_FORM = LegacyContactUrl("FeedbackForm/TriageForm/")

    # ExOpps UI - Export Opportunities
    EXOPPS_LANDING = ExOppsUrl("")

    # SOO UI Selling Online Overseas
    SOO_LANDING = SOOUrl("")
    SOO_SEARCH_RESULTS = SOOUrl("markets/results/")
    SOO_MARKET_DETAILS = SOOUrl("markets/details/", template="markets/details/{market}/")

    # CMS API endpoints
    CMS_API_HEALTHCHECK = CMSApiUrl("healthcheck/")
    CMS_API_HEALTHCHECK_PING = CMSApiUrl("healthcheck/ping/")
    CMS_API_PAGES = CMSApiUrl("api/pages/")
    CMS_API_PAGE_TYPES = CMSApiUrl("api/pages/types/")
    CMS_API_IMAGES = CMSApiUrl("api/images/")
    CMS_API_DOCUMENTS = CMSApiUrl("api/documents/")

    # Forms API endpoints
    FORMS_API_HEALTHCHECK = FormsApiUrl("api/healthcheck/")
    FORMS_API_HEALTHCHECK_PING = FormsApiUrl("api/healthcheck/ping/")
    FORMS_API_SUBMISSION = FormsApiUrl("api/submission/")
    FORMS_API_ADMIN = FormsApiUrl("admin/")
    FORMS_API_TESTAPI = FormsApiUrl("testapi/submissions-by-email/{email}/")
