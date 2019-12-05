#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tests.functional.utils.generic import (
    delete_test_buyers_from_directory_api,
    delete_test_companies_from_directory_api,
    delete_test_submissions_from_forms_api,
    delete_test_users_from_sso,
)

if __name__ == "__main__":
    print(f"Deleting test users...")
    delete_test_users_from_sso()
    print(f"Deleting test companies...")
    delete_test_companies_from_directory_api()
    print(f"Deleting test buyers...")
    delete_test_buyers_from_directory_api()
    print(f"Deleting test form submissions...")
    delete_test_submissions_from_forms_api()
    print(f"All requests to delete test data were successfully sent")
