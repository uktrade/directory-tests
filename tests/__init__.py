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
join_sso = partial(urljoin, settings.DIRECTORY_SSO_URL)
join_sso_api = partial(urljoin, settings.DIRECTORY_SSO_API_CLIENT_BASE_URL)
join_profile = partial(urljoin, settings.DIRECTORY_PROFILE_URL)
join_ui_buyer = partial(urljoin, settings.DIRECTORY_UI_BUYER_URL)
join_ui_supplier = partial(urljoin, settings.DIRECTORY_UI_SUPPLIER_URL)
join_exred = partial(urljoin, settings.EXRED_UI_URL)
join_contact_us = partial(urljoin, settings.DIRECTORY_CONTACT_US_UI_URL)
join_soo = partial(urljoin, settings.SOO_UI_URL)
join_cms_url = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_api = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)
join_cms_ui = partial(urljoin, settings.DIRECTORY_CMS_API_CLIENT_BASE_URL)

urls = {
    # SSO
    'sso:landing': '',
    'sso:login': 'accounts/login/',
    'sso:signup': 'accounts/signup/',
    'sso:logout': 'accounts/logout/',
    'sso:password_change': 'accounts/password/change/',
    'sso:password_set': 'accounts/password/set/',
    'sso:password_reset': 'accounts/password/reset/',
    'sso:email_confirm': 'accounts/confirm-email/',
    'sso:inactive': 'accounts/inactive/',
    # Legacy SSO API healthcheck endpoint
    'sso:health': 'api/v1/',

    # SSO API
    'sso-api:landing': '',
    'sso-api:healthcheck-database': 'api/v1/healthcheck/database/',
    'sso-api:healthcheck-ping': 'api/v1/healthcheck/ping/',
    'sso-api:healthcheck-sentry': 'api/v1/healthcheck/sentry/',
    'sso-api:user': 'api/v1/session-user/',

    # UI-BUYER
    'ui-buyer:landing': '',
    'ui-buyer:healthcheck-api': 'healthcheck/api/',
    'ui-buyer:healthcheck-sso': 'healthcheck/single-sign-on/',
    'ui-buyer:register': 'register',
    'ui-buyer:register-confirm-company': 'register/company/',
    'ui-buyer:register-confirm-export-status': 'register/exports/',
    'ui-buyer:register-finish': 'register/finished/',
    'ui-buyer:register-submit-account-details': 'register-submit/',
    'ui-buyer:upload-logo': 'company-profile/edit/logo/',
    'ui-buyer:case-study-create': 'company/case-study/create/',
    'ui-buyer:case-study-edit': 'company/case-study/edit/',
    'ui-buyer:confirm-company-address': 'verify/letter-confirm/',
    'ui-buyer:confirm-identity': 'verify/',
    'ui-buyer:confirm-identity-letter': 'verify/letter-send/',
    'ui-buyer:company-profile': 'company-profile/',
    'ui-buyer:company-edit': 'company-profile/edit/',
    'ui-buyer:company-edit-address': 'company-profile/edit/address',
    'ui-buyer:company-edit-description': 'company-profile/edit/description/',
    'ui-buyer:company-edit-key-facts': 'company-profile/edit/key-facts/',
    'ui-buyer:company-edit-sectors': 'company-profile/edit/sectors/',
    'ui-buyer:company-edit-contact': 'company-profile/edit/contact/',
    'ui-buyer:company-edit-social-media': 'company-profile/edit/social-media/',
    'ui-buyer:account-add-collaborator': 'account/add-collaborator/',
    'ui-buyer:account-remove-collaborator': 'account/remove-collaborator/',
    'ui-buyer:account-transfer-ownership': 'account/transfer/',
    'ui-buyer:account-confirm-password': 'account/transfer/',
    'ui-buyer:account-confirm-ownership-transfer': 'account/transfer/accept/?invite_key=',

    # UI-SUPPLIER
    'ui-supplier:landing': '',
    'ui-supplier:suppliers': 'suppliers/',
    'ui-supplier:industries': 'industries/',
    'ui-supplier:subscribe': 'subscribe/',
    'ui-supplier:industries-health': 'industries/healthcare/',
    'ui-supplier:industries-tech': 'industries/technology/',
    'ui-supplier:industries-creative': 'industries/creative-services/',
    'ui-supplier:industries-food': 'industries/food-and-drink/',
    'ui-supplier:industries-health-summary': 'industries/health/summary/',
    'ui-supplier:industries-tech-summary': 'industries/tech/summary/',
    'ui-supplier:industries-creative-summary': 'industries/creative/summary/',
    'ui-supplier:industries-food-summary': 'industries/food-and-drink/summary/',
    'ui-supplier:feedback': 'feedback/',
    'ui-supplier:search': 'search/',
    # NOTE: the URLS below require data from fixtures/supplier.json
    # to be loaded to the API db of the tested system
    'ui-supplier:suppliers-detail': 'suppliers/03074910/ft-solutions-limited/',
    'ui-supplier:case-study': 'case-study/172/how-a-major-airport-rewards-its-loyal-passengers/',

    # UI-INVEST
    'ui-invest:landing': '',
    'ui-invest:industries': 'industries/',
    'ui-invest:uk-setup-guide': 'uk-setup-guide/',

    # API
    'api:healthcheck-cache': 'healthcheck/cache/',
    'api:healthcheck-database': 'healthcheck/database/',
    'api:healthcheck-elasticsearch': 'healthcheck/elasticsearch/',
    'api:healthcheck-single-sign-on': 'healthcheck/single-sign-on/',
    'api:healthcheck-sentry': 'healthcheck/sentry/',
    'api:healthcheck-ping': 'healthcheck/ping/',
    'api:healthcheck-stannp': 'healthcheck/stannp/',

    'api:enrolment': 'enrolment/',
    'api:pre-verified-enrolment': 'pre-verified-enrolment',
    'api:enrolment-trusted-code': 'trusted-code/{code}/',

    'api:notifications-anonymous-unsubscribe': 'notifications/anonymous-unsubscribe/',

    'api:buyer': 'buyer/',
    'api:buyer-csv-dump': 'buyer/csv-dump/',
    'api:supplier-csv-dump': 'supplier/csv-dump/',

    'api:validate-company-number': 'validate/company-number/',
    'api:companies-house-profile': 'company/companies-house-profile/',

    'api:supplier': 'supplier/',
    'api:supplier-unsubscribe': 'supplier/unsubscribe/',

    'api:export-readiness-triage': 'export-readiness/triage/',
    'api:export-readiness-article-read': 'export-readiness/article-read/',
    'api:export-readiness-task-completed': 'export-readiness/task-completed/',

    'api:export-opportunity-food': 'export-opportunity/food/',
    'api:export-opportunity-legal': 'export-opportunity/legal/',

    'api:public-company': 'public/company/',
    'api:public-company-profile': 'public/company/{companies_house_number}/',
    'api:public-case-study': 'public/case-study/{id}/',


    'api:supplier-company': 'supplier/company/',
    'api:supplier-company-case-study': 'supplier/company/case-study/',
    'api:supplier-company-case-study-by-id': 'supplier/company/case-study/{id}/',
    'api:supplier-company-verify': 'supplier/company/verify/',
    'api:supplier-company-verify-companies-house': 'supplier/company/verify/companies-house/',
    'api:contact-supplier': 'contact/supplier/',
    'api:company-search': 'company/search/',
    'api:case-study-search': 'case-study/search/',

    'api:supplier-company-collaborators': 'supplier/company/collaborators/',
    'api:supplier-company-collaboration-invite': 'supplier/company/collaboration-invite/',
    'api:supplier-company-collaboration-invite-by-uuid': 'supplier/company/collaboration-invite/{uuid}/',
    'api:supplier-company-remove-collaborators': 'supplier/company/remove-collaborators/',

    'api:supplier-company-transfer-ownership-invite': 'supplier/company/transfer-ownership-invite/',
    'api:supplier-company-transfer-ownership-invite-by-uuid': 'supplier/company/transfer-ownership-invite/{uuid}/',
    'api:supplier-gecko-total-registered': 'supplier/gecko/total-registered/',
    'api:activity-stream': 'activity-stream/',
    'api:external-supplier-sso': 'external/supplier-sso/',
    'api:external-supplier': 'external/supplier/',


    # INTERNAL API
    'internal-api:companies-house-search': 'api/internal/companies-house-search/',

    # SSO-PROFILE
    'profile:healthcheck-ping': 'healthcheck/ping/',
    'profile:healthcheck-sentry': 'healthcheck/sentry/',
    'profile:healthcheck-sso': 'healthcheck/single-sign-on/',
    'profile:soo': 'selling-online-overseas/',
    'profile:fab': 'find-a-buyer/',
    'profile:exops-alerts': 'export-opportunities/email-alerts/',
    'profile:exops-applications': 'export-opportunities/applications/',
    'profile:landing': '',
    'profile:about': 'about/',
    'profile:directory-supplier': 'api/v1/directory/supplier/',

    # ExRed UI
    'ui-exred:healthcheck-api': 'healthcheck/api/',
    'ui-exred:healthcheck-sso-proxy': 'healthcheck/single-sign-on/',
    'ui-exred:landing': '',
    'ui-exred:landing-uk': '?lang=en-gb',
    'ui-exred:international': 'international/',
    'ui-exred:international-uk': 'international/?lang=en-gb',
    'ui-exred:international-zh': 'international/?lang=zh-hans',
    'ui-exred:international-de': 'international/?lang=de',
    'ui-exred:international-ja': 'international/?lang=ja',
    'ui-exred:international-es': 'international/?lang=es',
    'ui-exred:international-pt': 'international/?lang=pt',
    'ui-exred:international-ar': 'international/?lang=ar',
    'ui-exred:triage-sector': 'triage/sector/',
    'ui-exred:triage-exported-before': 'triage/exported-before/',
    'ui-exred:triage-regular-exporter': 'triage/regular-exporter/',
    'ui-exred:triage-online-marketplace': 'triage/online-marketplace/',
    'ui-exred:triage-companies-house': 'triage/companies-house/',
    'ui-exred:triage-company': 'triage/company/',
    'ui-exred:triage-summary': 'triage/summary/',
    'ui-exred:custom': 'custom/',
    'ui-exred:new': 'new/',
    'ui-exred:occasional': 'occasional/',
    'ui-exred:regular': 'regular/',
    'ui-exred:market-research': 'market-research/',
    'ui-exred:customer-insight': 'customer-insight/',
    'ui-exred:finance': 'finance/',
    'ui-exred:business-planning': 'business-planning/',
    'ui-exred:getting-paid': 'getting-paid/',
    'ui-exred:operations-and-compliance': 'operations-and-compliance/',
    'ui-exred:get-finance': 'get-finance/',
    'ui-exred:export-opportunities': 'export-opportunities/',
    'ui-exred:story-first': 'story/online-marketplaces-propel-freestyle-xtreme-sales/',
    'ui-exred:story-second': 'story/hello-babys-rapid-online-growth/',
    'ui-exred:story-third': 'story/york-bag-retailer-goes-global-via-e-commerce/',
    'ui-exred:terms': 'terms-and-conditions/',
    'ui-exred:privacy': 'privacy-and-cookies/',

    # Contact-Us UI
    'ui-contact-us:help': 'help/',
    'ui-contact-us:feedback-form': 'help/FeedbackForm/',
    'ui-contact-us:directory': 'directory/',
    'ui-contact-us:directory-feedback-form': 'directory/FeedbackForm/',
    'ui-contact-us:soo-triage': 'triage/',
    'ui-contact-us:soo-triage-form': 'triage/soo/',
    'ui-contact-us:soo-triage-feedback-form': 'FeedbackForm/TriageForm/',

    # SOO UI Selling Online Overseas
    'ui-soo:landing': '',
    'ui-soo:search-results': 'markets/results/',
    'ui-soo:market-details': 'markets/details/',

    # CMS API endpoints
    'cms-healthcheck:landing': '',
    'cms-healthcheck:ping': 'healthcheck/ping/',
    'cms-healthcheck:database': 'healthcheck/database/',
    'cms-api:pages': 'api/pages/',
    'cms-api:images': 'api/images/',
    'cms-api:documents': 'api/documents/',
    'cms-api:pages-by-slug': 'api/pages/lookup-by-slug/{}/',
}

# these user credentials are hard-coded in `directory-sso`. The users
# are created when `manage.py create_test_users` is ran on sso.
users = {
    'verified': {
        'username': os.environ['SSO_USER_USERNAME'],
        'password': os.environ['SSO_USER_PASSWORD'],
        'token': os.environ['SSO_USER_TOKEN'],
        'sso_id': int(os.environ['SSO_USER_SSO_ID'])
    },
    'unverified': {
        'token': os.environ['SSO_UNVERIFIED_USER_TOKEN']
    }
}


companies = {
    'not_active': os.getenv(
        "SSO_COMPANY_NOT_ACTIVE", '06542942'
    ),
    'already_registered': os.getenv(
        "SSO_COMPANY_ALREADY_REGISTERED", '10416664'
    ),
    'active_not_registered': os.getenv(
        "SSO_COMPANY_ACTIVE_NOT_REGISTERED", '01624297'
    ),
}


def get_relative_url(name):
    return urls[name]


def get_absolute_url(name):
    relative_url = get_relative_url(name)
    if name.startswith('sso:'):
        return join_sso(relative_url)
    elif name.startswith('sso-api:'):
        return join_sso_api(relative_url)
    elif name.startswith('ui-buyer:'):
        return join_ui_buyer(relative_url)
    elif name.startswith('ui-supplier:'):
        return join_ui_supplier(relative_url)
    elif name.startswith('api:'):
        return join_api(relative_url)
    elif name.startswith('internal-api:'):
        return join_internal_api(relative_url)
    elif name.startswith('profile:'):
        return join_profile(relative_url)
    elif name.startswith('ui-exred:'):
        return join_exred(relative_url)
    elif name.startswith('ui-contact-us:'):
        return join_contact_us(relative_url)
    elif name.startswith('ui-soo:'):
        return join_soo(relative_url)
    elif name.startswith('cms-api:'):
        return join_cms_api(relative_url)
    elif name.startswith('cms-healthcheck:'):
        return join_cms_url(relative_url)
    elif name.startswith('cms-ui:'):
        return join_cms_ui(relative_url)


def get_random_email_address():
    return '{}@example.com'.format(uuid.uuid4())


def retriable_error(exception):
    """Return True if test should be re-run based on the Exception"""
    return isinstance(exception, (AssertionError, ))


def is_500(exception):
    """Return True exception message contains 500"""
    return "500" in str(exception)
