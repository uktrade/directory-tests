# -*- coding: utf-8 -*-
"""SSO Common operations."""
import logging

from directory_tests_shared.clients import BASIC_AUTHENTICATOR, SSO_TEST_API_CLIENT


def verify_account(email: str):
    response = SSO_TEST_API_CLIENT.flag_user_email_as_verified_or_not(
        email, verified=True, authenticator=BASIC_AUTHENTICATOR
    )
    error = f"Something went wrong when trying to flag {email} email as verified"
    assert response.status_code == 204, error
    logging.debug(f"Successfully flagged '{email}' account as verified")


def delete_supplier_data_from_sso(email: str):
    response = SSO_TEST_API_CLIENT.delete_user_by_email(
        email, authenticator=BASIC_AUTHENTICATOR
    )
    if response.status_code == 204:
        logging.debug("Deleted %s data from SSO", email)
    else:
        logging.warning(
            "Something went wrong when trying to delete %s data from SSO", email
        )
