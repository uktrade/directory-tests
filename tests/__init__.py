from urlparse import urljoin
import uuid

from tests import settings

urls = {
    'sso:login': '/accounts/login/',
    'sso:signup': '/accounts/signup/',
}


def get_url(name):
    return urljoin(settings.DIRECTORY_SSO_URL, urls[name])


def get_random_email_address():
    return '{}@example.com'.format(uuid.uuid4())
