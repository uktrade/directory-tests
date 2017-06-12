from urllib.parse import urljoin
from functools import partial
import os
import uuid

from tests import settings

join_api = partial(urljoin, settings.DIRECTORY_API_URL)
join_internal_api = partial(urljoin, settings.DIRECTORY_API_URL)
join_sso = partial(urljoin, settings.DIRECTORY_SSO_URL)
join_profile = partial(urljoin, settings.DIRECTORY_PROFILE_URL)
join_ui_buyer = partial(urljoin, settings.DIRECTORY_UI_BUYER_URL)
join_ui_supplier = partial(urljoin, settings.DIRECTORY_UI_SUPPLIER_URL)

urls = {
    # SSO
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
    'ui-buyer:register': 'register',
    'ui-buyer:register-confirm-company': 'register/company',
    'ui-buyer:company-profile': 'company-profile',
    'ui-buyer:upload-logo': 'company-profile/edit/logo',
    'ui-buyer:confirm-company-address': 'confirm-company-address',
    'ui-buyer:company-edit-address': 'company-profile/edit/address',
    'ui-buyer:company-edit-description': 'company-profile/edit/description',
    'ui-buyer:company-edit-key-facts': 'company-profile/edit/key-facts',
    'ui-buyer:company-edit-sectors': 'company-profile/edit/sectors',
    'ui-buyer:company-edit-contact': 'company-profile/edit/contact',
    'ui-buyer:company-edit-social-media': 'company-profile/edit/social-media',

    # UI-SUPPLIER
    'ui-supplier:landing': '',
    'ui-supplier:suppliers': 'suppliers',
    'ui-supplier:industries': 'industries',
    'ui-supplier:industries-health': 'industries/health',
    'ui-supplier:industries-tech': 'industries/tech',
    'ui-supplier:industries-creative': 'industries/creative',
    'ui-supplier:industries-food': 'industries/food-and-drink',
    'ui-supplier:terms': 'terms-and-conditions',
    'ui-supplier:privacy': 'privacy-policy',
    # NOTE: the URLS below require data from fixtures/supplier.json
    # to be loaded to the API db of the tested system
    'ui-supplier:suppliers-detail': 'suppliers/99999999',
    'ui-supplier:case-study': 'case-study/2147483647',

    # API
    'api:docs': 'docs/',
    'api:health': '',
    'api:enrolment': 'enrolment/',
    'api:company': 'supplier/{sso_id}/company/',
    'api:user': 'supplier/{sso_id}/',
    'api:validate-company-number': 'validate/company-number/',
    'api:companies-house-profile': 'company/companies-house-profile/',

    # INTERNAL API
    'internal-api:companies-house-search': 'internal/companies-house-search/',

    # SSO-PROFILE
    'profile:soo': 'selling-online-overseas/',
    'profile:fab': 'find-a-buyer/',
    'profile:exops-alerts': 'export-opportunities/email-alerts/',
    'profile:exops-applications': 'export-opportunities/applications/',
    'profile:landing': '',
    'profile:about': 'about/',
    'profile:directory-supplier': 'api/v1/directory/supplier/'
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
        "SSO_COMPANY_ALREADY_REGISTERED", '12345678'
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


def get_random_email_address():
    return '{}@example.com'.format(uuid.uuid4())
