# -*- coding: utf-8 -*-
from notifications_python_client import NotificationsAPIClient

from .settings import (
    CMS_API_DEFAULT_TIMEOUT,
    DIRECTORY_API_KEY,
    DIRECTORY_API_SENDER_ID,
    DIRECTORY_API_URL,
    FORMS_API_URL,
    FORMS_API_KEY,
    FORMS_API_SENDER_ID,
    GOV_NOTIFY_API_KEY,
    SSO_API_DEFAULT_TIMEOUT,
    SSO_API_KEY,
    SSO_API_SENDER_ID,
    SSO_API_URL,
)

from directory_api_client.testapiclient import DirectoryTestAPIClient
from directory_client_core.base import AbstractAPIClient
from directory_cms_client.client import cms_api_client as CMS_API_CLIENT  # noqa
from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient
from directory_sso_api_client.client import sso_api_client as SSO_API_CLIENT  # noqa

DIRECTORY_TEST_API_CLIENT = DirectoryTestAPIClient(
    DIRECTORY_API_URL,
    DIRECTORY_API_KEY,
    DIRECTORY_API_SENDER_ID,
    CMS_API_DEFAULT_TIMEOUT,
)


class FormsAPIClient(AbstractAPIClient):
    version = "1"

    def __init__(self, base_url, api_key, sender_id, timeout):
        super().__init__(base_url, api_key, sender_id, timeout)


FORMS_API_CLIENT = FormsAPIClient(
    base_url=FORMS_API_URL,
    api_key=FORMS_API_KEY,
    sender_id=FORMS_API_SENDER_ID,
    timeout=30,
)

GOV_NOTIFY_CLIENT = NotificationsAPIClient(GOV_NOTIFY_API_KEY)

SSO_TEST_API_CLIENT = DirectorySSOTestAPIClient(
    SSO_API_URL,
    SSO_API_KEY,
    SSO_API_SENDER_ID,
    SSO_API_DEFAULT_TIMEOUT,
)
