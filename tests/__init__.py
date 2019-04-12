from functools import partial
import os
import uuid

from tests import settings


def urljoin(base_url: str, endpoint: str):
    if base_url.endswith("/"):
        return f"{base_url}{endpoint}"
    else:
        return f"{base_url}/{endpoint}"


join_api = partial(urljoin, settings.DIRECTORY_API_URL)
join_internal_api = partial(urljoin, settings.DIRECTORY_BUYER_API_URL)
join_ui_international = partial(urljoin, settings.DIRECTORY_UI_INTERNATIONAL_URL)
join_sso = partial(urljoin, settings.DIRECTORY_SSO_URL)
join_sso_api = partial(urljoin, settings.DIRECTORY_SSO_API_CLIENT_BASE_URL)
join_profile = partial(urljoin, settings.DIRECTORY_PROFILE_URL)
join_ui_buyer = partial(urljoin, settings.DIRECTORY_UI_BUYER_URL)
join_ui_supplier = partial(urljoin, settings.DIRECTORY_UI_SUPPLIER_URL)
join_ui_invest = partial(urljoin, settings.INVEST_UI_URL)
join_exred = partial(urljoin, settings.EXRED_UI_URL)
join_exopps = partial(urljoin, settings.EXPORT_OPPORTUNITIES_UI_URL)
join_contact_us = partial(urljoin, settings.DIRECTORY_CONTACT_US_UI_URL)
join_legacy_contact_us = partial(urljoin, settings.DIRECTORY_LEGACY_CONTACT_US_UI_URL)
join_soo = partial(urljoin, settings.SOO_UI_URL)
join_cms_url = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_api = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_ui = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_forms_api = partial(urljoin, settings.DIRECTORY_FORMS_API_URL)

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

    # SSO API
    "sso-api:landing": "",
    "sso-api:healthcheck": "api/v1/healthcheck/",
    "sso-api:healthcheck-ping": "api/v1/healthcheck/ping/",
    "sso-api:user": "api/v1/session-user/",

    # UI-BUYER
    "ui-buyer:landing": "",
    "ui-buyer:healthcheck": "healthcheck/",
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
    "ui-supplier:healthcheck": "healthcheck/",
    "ui-supplier:suppliers": "suppliers/",
    "ui-supplier:industries": "industries/",
    "ui-supplier:subscribe": "subscribe/",
    "ui-supplier:industries-health": "industries/healthcare/",
    "ui-supplier:industries-tech": "industries/technology/",
    "ui-supplier:industries-creative": "industries/creative-services/",
    "ui-supplier:industries-food": "industries/food-and-drink/",
    "ui-supplier:industries-health-summary": "industries/health/summary/",
    "ui-supplier:industries-tech-summary": "industries/tech/summary/",
    "ui-supplier:industries-creative-summary": "industries/creative/summary/",
    "ui-supplier:industries-food-summary": "industries/food-and-drink/summary/",
    "ui-supplier:feedback": "feedback/",
    "ui-supplier:search": "search/",

    # UI-INTERNATIONAL
    "ui-international:landing": "",
    "ui-international:industries": "industries/",
    "ui-international:industry": "industries/engineering-and-manufacturing/",
    "ui-international:healthcheck-sentry": "healthcheck/sentry/",

    # UI-INVEST
    "ui-invest:landing": "",
    "ui-invest:healthcheck": "healthcheck/",
    "ui-invest:contact": "contact/",
    "ui-invest:industries": "industries/",
    "ui-invest:uk-setup-guide": "uk-setup-guide/",
    "ui-invest:hpo-rail": "high-potential-opportunities/rail-infrastructure/",
    "ui-invest:hpo-rail-contact": "high-potential-opportunities/rail-infrastructure/contact/",
    "ui-invest:hpo-food": "high-potential-opportunities/food-production/",
    "ui-invest:hpo-food-contact": "high-potential-opportunities/food-production/contact/",
    "ui-invest:hpo-lightweight": "high-potential-opportunities/lightweight-structures/",
    "ui-invest:hpo-lightweight-contact": "high-potential-opportunities/lightweight-structures/contact/",
    "ui-invest:industries-advanced-manufacturing": "industries/advanced-manufacturing/",
    "ui-invest:industries-aerospace": "industries/aerospace/",
    "ui-invest:industries-agri-tech": "industries/agri-tech/",
    "ui-invest:industries-asset-management": "industries/asset-management/",
    "ui-invest:industries-automotive": "industries/automotive/",
    "ui-invest:industries-automotive-research-and-development": "industries/automotive-research-and-development/",
    "ui-invest:industries-automotive-supply-chain": "industries/automotive-supply-chain/",
    "ui-invest:industries-capital-investment": "industries/capital-investment/",
    "ui-invest:industries-chemicals": "industries/chemicals/",
    "ui-invest:industries-creative-content-and-production": "industries/creative-content-and-production/",
    "ui-invest:industries-creative-industries": "industries/creative-industries/",
    "ui-invest:industries-data-analytics": "industries/data-analytics/",
    "ui-invest:industries-digital-media": "industries/digital-media/",
    "ui-invest:industries-electrical-networks": "industries/electrical-networks/",
    "ui-invest:industries-energy": "industries/energy/",
    "ui-invest:industries-energy-waste": "industries/energy-waste/",
    "ui-invest:industries-financial-services": "industries/financial-services/",
    "ui-invest:industries-financial-technology": "industries/financial-technology/",
    "ui-invest:industries-food-and-drink": "industries/food-and-drink/",
    "ui-invest:industries-food-service-and-catering": "industries/food-service-and-catering/",
    "ui-invest:industries-free-foods": "industries/free-foods/",
    "ui-invest:industries-health-and-life-sciences": "industries/health-and-life-sciences/",
    "ui-invest:industries-meat-poultry-and-dairy": "industries/meat-poultry-and-dairy/",
    "ui-invest:industries-medical-technology": "industries/medical-technology/",
    "ui-invest:industries-motorsport": "industries/motorsport/",
    "ui-invest:industries-nuclear-energy": "industries/nuclear-energy/",
    "ui-invest:industries-offshore-wind-energy": "industries/offshore-wind-energy/",
    "ui-invest:industries-oil-and-gas": "industries/oil-and-gas/",
    "ui-invest:industries-pharmaceutical-manufacturing": "industries/pharmaceutical-manufacturing/",
    "ui-invest:industries-retail": "industries/retail/",
    "ui-invest:industries-technology": "industries/technology/",


    # API
    "api:healthcheck": "healthcheck/",
    "api:healthcheck-ping": "healthcheck/ping/",

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


    # INTERNAL API
    "internal-api:companies-house-search": "api/internal/companies-house-search/",

    # SSO-PROFILE
    "profile:healthcheck": "healthcheck/",
    "profile:healthcheck-ping": "healthcheck/ping/",
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
    "profile:edit-company-profile": "find-a-buyer/",
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
    "ui-exred:healthcheck": "healthcheck/",
    "ui-exred:healthcheck-ping": "healthcheck/ping/",
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

    # CMS API endpoints
    "cms-api:healthcheck": "healthcheck/",
    "cms-api:healthcheck-ping": "healthcheck/ping/",
    "cms-api:pages": "api/pages/",
    "cms-api:page-types": "api/pages/types/",
    "cms-api:images": "api/images/",
    "cms-api:documents": "api/documents/",
    "cms-api:pages-by-slug": "api/pages/lookup-by-slug/{}/",

    # Forms API endpoints
    "forms-api:healthcheck": "api/healthcheck/",
    "forms-api:healthcheck-ping": "api/healthcheck/ping/",
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
    elif name.startswith("internal-api:"):
        return join_internal_api(relative_url)
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
