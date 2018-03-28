from urllib.parse import urljoin
from functools import partial
import os
import uuid

from tests import settings

join_api = partial(urljoin, settings.DIRECTORY_API_URL)
join_internal_api = partial(urljoin, settings.DIRECTORY_BUYER_API_URL)
join_sso = partial(urljoin, settings.DIRECTORY_SSO_URL)
join_profile = partial(urljoin, settings.DIRECTORY_PROFILE_URL)
join_ui_buyer = partial(urljoin, settings.DIRECTORY_UI_BUYER_URL)
join_ui_supplier = partial(urljoin, settings.DIRECTORY_UI_SUPPLIER_URL)
join_exred = partial(urljoin, settings.EXRED_UI_URL)

urls = {
    # SSO
    'sso:landing': '',
    'sso:healthcheck-database': 'api/v1/healthcheck/database/',
    'sso:login': 'accounts/login/',
    'sso:signup': 'accounts/signup/',
    'sso:logout': 'accounts/logout/',
    'sso:password_change': 'accounts/password/change/',
    'sso:password_set': 'accounts/password/set/',
    'sso:password_reset': 'accounts/password/reset/',
    'sso:email_confirm': 'accounts/confirm-email/',
    'sso:inactive': 'accounts/inactive/',
    'sso:health': 'api/v1/',
    'sso:user': 'api/v1/session-user/',

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
    'ui-buyer:confirm-identity': '/verify/',
    'ui-buyer:confirm-identity-letter': '/verify/letter-send/',
    'ui-buyer:company-profile': 'company-profile/',
    'ui-buyer:company-edit': 'company-profile/edit/',
    'ui-buyer:company-edit-address': 'company-profile/edit/address',
    'ui-buyer:company-edit-description': 'company-profile/edit/description/',
    'ui-buyer:company-edit-key-facts': 'company-profile/edit/key-facts/',
    'ui-buyer:company-edit-sectors': 'company-profile/edit/sectors/',
    'ui-buyer:company-edit-contact': 'company-profile/edit/contact/',
    'ui-buyer:company-edit-social-media': 'company-profile/edit/social-media/',
    'ui-buyer:account-add-collaborator': 'account/add-collaborator/',
    'ui-buyer:account-transfer-ownership': 'account/transfer/',
    'ui-buyer:account-confirm-password': 'account/transfer/',
    'ui-buyer:account-confirm-ownership-transfer': 'account/transfer/accept/?invite_key=',

    # UI-SUPPLIER
    'ui-supplier:landing': '',
    'ui-supplier:suppliers': 'suppliers/',
    'ui-supplier:industries': 'industries/',
    'ui-supplier:industries-health': 'industries/health/',
    'ui-supplier:industries-tech': 'industries/tech/',
    'ui-supplier:industries-creative': 'industries/creative/',
    'ui-supplier:industries-food': 'industries/food-and-drink/',
    'ui-supplier:industries-health-summary': 'industries/health/summary/',
    'ui-supplier:industries-tech-summary': 'industries/tech/summary/',
    'ui-supplier:industries-creative-summary': 'industries/creative/summary/',
    'ui-supplier:industries-food-summary': 'industries/food-and-drink/summary/',
    'ui-supplier:feedback': 'feedback/',
    'ui-supplier:search': 'search/',
    'ui-supplier:terms': 'terms-and-conditions/',
    'ui-supplier:privacy': 'privacy-policy/',
    # NOTE: the URLS below require data from fixtures/supplier.json
    # to be loaded to the API db of the tested system
    'ui-supplier:suppliers-detail': 'suppliers/99999999',
    'ui-supplier:case-study': 'case-study/2147483647',

    # API
    'api:docs': 'docs/',
    'api:healthcheck-database': 'healthcheck/database/',
    'api:healthcheck-cache': 'healthcheck/cache/',
    'api:healthcheck-elasticsearch': 'healthcheck/elasticsearch/',
    'api:enrolment': 'enrolment/',
    'api:company': 'supplier/{sso_id}/company/',
    'api:user': 'supplier/{sso_id}/',
    'api:validate-company-number': 'validate/company-number/',
    'api:companies-house-profile': 'company/companies-house-profile/',

    # INTERNAL API
    'internal-api:companies-house-search': 'api/internal/companies-house-search/',

    # SSO-PROFILE
    'profile:healthcheck-api': 'healthcheck/api/',
    'profile:healthcheck-sso-proxy': 'healthcheck/single-sign-on/',
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
    'ui-exred:story-thrid': 'story/york-bag-retailer-goes-global-via-e-commerce/',
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


def get_random_email_address():
    return '{}@example.com'.format(uuid.uuid4())
