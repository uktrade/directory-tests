#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from retrying import retry

from tests.functional.utils.generic import (
    delete_test_buyers_from_directory_api,
    delete_test_companies_from_directory_api,
    delete_test_submissions_from_forms_api,
    delete_test_users_from_sso,
)


@retry(stop_max_attempt_number=5)
def sso():
    print(f"Deleting test users...")
    delete_test_users_from_sso()


@retry(stop_max_attempt_number=5)
def companies():
    print(f"Deleting test companies...")
    delete_test_companies_from_directory_api()


@retry(stop_max_attempt_number=5)
def buyers():
    print(f"Deleting test buyers...")
    delete_test_buyers_from_directory_api()


@retry(stop_max_attempt_number=5)
def forms():
    print(f"Deleting test form submissions...")
    delete_test_submissions_from_forms_api()


if __name__ == "__main__":
    sso()
    companies()
    buyers()
    forms()
    print(f"All requests to delete test data were successfully sent")
