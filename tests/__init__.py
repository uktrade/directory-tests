from __future__ import absolute_import

from urlparse import urljoin
from functools import partial
import uuid

from tests import settings

join_api = partial(urljoin, settings.DIRECTORY_API_URL)
join_sso = partial(urljoin, settings.DIRECTORY_SSO_URL)
join_buyer_ui = partial(urljoin, settings.DIRECTORY_BUYER_UI_URL)
join_supplier_ui = partial(urljoin, settings.DIRECTORY_SUPPLIER_UI_URL)
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
    # UI-SUPPLIER
    # API
    'api:docs': 'docs/',
    'api:health': '',
    'api:enrolment': 'enrolment/',
    'api:sms-verify': 'enrolment/verification-sms/',
    'api:company': 'supplier/{sso_id}/company/',
    'api:user': 'supplier/{sso_id}/',
    'api:confirm-company-email': 'enrolment/confirm/',
    'api:validate-company-number': 'validate/company-number/',
    'api:companies-house-profile': 'company/companies-house-profile/',
}

# these user credentials are hard-coded in `directory-sso`. The users
# are created when `manage.py create_test_users` is ran on sso.
users = {
    'verified': {
        'username': 'verified@example.com',
        'password': 'passwordpassword',
    }
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


def get_random_email_address():
    return '{}@example.com'.format(uuid.uuid4())
