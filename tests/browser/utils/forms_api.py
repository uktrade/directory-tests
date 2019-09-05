# -*- coding: utf-8 -*-
import logging
from typing import List

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


def filter_by_action(submissions: List[dict], action: str) -> list:
    return list(filter(lambda x: x["meta"]["action_name"] == action, submissions))


def filter_by_sender_email(submissions: List[dict], email: str) -> list:
    return list(
        filter(lambda x:
               "sender" in x["meta"] and x["meta"]["sender"]["email_address"] == email,
               submissions)
    )


def filter_by_subject(submissions: List[dict], action: str) -> list:
    return list(filter(lambda x: x["meta"]["subject"] == action, submissions))


def filter_by_uuid_last_name(submissions: List[dict], uuid: str) -> list:
    result = []
    for x in submissions:
        if "full_name" in x["data"]:
            if x["data"]["full_name"] == uuid:
                result.append(x)
        if "family_name" in x["data"]:
            if x["data"]["family_name"] == uuid:
                result.append(x)
        if "last_name" in x["data"]:
            if x["data"]["last_name"] == uuid:
                result.append(x)
        if "lastname" in x["data"]:
            if x["data"]["lastname"] == uuid:
                result.append(x)
        if "html_body" in x["data"]:
            if uuid in x["data"]["html_body"]:
                result.append(x)
    return result


def find_form_submissions(email: str) -> List[dict]:
    json = client.get(f"testapi/submissions-by-email/{email}/").json()
    logging.debug(f"Submissions for {email}: {json}")
    return json


def find_form_submissions_by_subject_and_action(
        email: str, subject: str, action: str
) -> List[dict]:
    submissions = find_form_submissions(email)
    by_subject = filter_by_subject(submissions, subject)
    return filter_by_action(by_subject, action)


def find_form_submissions_for_dit_office(mailbox: str, sender: str) -> List[dict]:
    submissions = find_form_submissions(mailbox)
    return filter_by_sender_email(submissions, sender)
