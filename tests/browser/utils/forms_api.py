# -*- coding: utf-8 -*-
import logging

from directory_client_core.base import AbstractAPIClient

import settings


class FormsClient(AbstractAPIClient):
    version = "1"

    def __init__(self, base_url, api_key, sender_id, timeout, default_service_name):
        super().__init__(base_url, api_key, sender_id, timeout)
        self.default_service_name = default_service_name


client = FormsClient(
    base_url=settings.DIRECTORY_FORMS_API_URL,
    api_key=settings.DIRECTORY_FORMS_API_KEY,
    sender_id=settings.DIRECTORY_FORMS_API_SENDER_ID,
    timeout=30,
    default_service_name="testapi",
)


def find_form_submissions(email: str) -> dict:
    json = client.get(f"testapi/submissions-by-email/{email}/").json()
    logging.debug(f"Submissions for {email}: {json}")
    return json
