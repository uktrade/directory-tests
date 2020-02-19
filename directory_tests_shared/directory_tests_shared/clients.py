# -*- coding: utf-8 -*-
import base64

from notifications_python_client import NotificationsAPIClient

from directory_api_client.testapiclient import url_company_by_ch_id  # noqa
from directory_api_client.testapiclient import url_published_companies  # noqa
from directory_api_client.testapiclient import DirectoryTestAPIClient
from directory_cms_client.client import cms_api_client as CMS_API_CLIENT  # noqa
from directory_forms_api_client.client import (  # noqa
    forms_api_client as FORMS_API_CLIENT,
)
from directory_sso_api_client.client import sso_api_client as SSO_API_CLIENT  # noqa
from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient
from .settings import (
    BASICAUTH_PASS,
    BASICAUTH_USER,
    CMS_API_DEFAULT_TIMEOUT,
    DIRECTORY_API_KEY,
    DIRECTORY_API_SENDER_ID,
    DIRECTORY_API_URL,
    GOV_NOTIFY_API_KEY,
    PIR_GOV_NOTIFY_API_KEY,
    SSO_API_DEFAULT_TIMEOUT,
    SSO_API_KEY,
    SSO_API_SENDER_ID,
    SSO_API_URL,
)

DIRECTORY_TEST_API_CLIENT = DirectoryTestAPIClient(
    DIRECTORY_API_URL,
    DIRECTORY_API_KEY,
    DIRECTORY_API_SENDER_ID,
    CMS_API_DEFAULT_TIMEOUT,
)

GOV_NOTIFY_CLIENT = NotificationsAPIClient(GOV_NOTIFY_API_KEY)
PIR_GOV_NOTIFY_CLIENT = NotificationsAPIClient(PIR_GOV_NOTIFY_API_KEY)

SSO_TEST_API_CLIENT = DirectorySSOTestAPIClient(
    SSO_API_URL, SSO_API_KEY, SSO_API_SENDER_ID, SSO_API_DEFAULT_TIMEOUT
)


class BasicAuthenticator:
    def __init__(self, username: str, password: str):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("ascii"))
        self.headers = {"Authorization": f"Basic {encoded_credentials.decode('ascii')}"}


BASIC_AUTHENTICATOR = BasicAuthenticator(BASICAUTH_USER, BASICAUTH_PASS)
