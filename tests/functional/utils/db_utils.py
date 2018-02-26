# -*- coding: utf-8 -*-
"""Remove User & Accounts from FAB & SSO after test."""
import logging

from behave.runner import Context
from directory_api_client.testapiclient import DirectoryTestAPIClient
from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient

from tests.settings import (
    DIRECTORY_API_URL,
    DIRECTORY_API_CLIENT_KEY,
    SSO_PROXY_SIGNATURE_SECRET,
    SSO_PROXY_API_CLIENT_BASE_URL
)

DIRECTORY_CLIENT = DirectoryTestAPIClient(
    DIRECTORY_API_URL, DIRECTORY_API_CLIENT_KEY)
SSO_CLIENT = DirectorySSOTestAPIClient(
    SSO_PROXY_API_CLIENT_BASE_URL, SSO_PROXY_SIGNATURE_SECRET
)


def get_company_email(number: str) -> str:
    """Get email address associated with company."""
    response = DIRECTORY_CLIENT.get_company_by_ch_id(number)
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    email = response.json()['company_email']
    logging.debug("Email for company %s is %s", number, email)
    return email


def get_published_companies(context: Context) -> list:
    """Get a List of dicts with published companies.

    :return: a list of dictionaries with published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies()
    context.response = response
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    return response.json()


def get_published_companies_with_n_sectors(
        context: Context, number_of_sectors: int) -> list:
    """Get a List of published companies with at least N associated sectors.

    :return: a list of dictionaries with matching published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies(
        minimal_number_of_sectors=number_of_sectors)
    context.response = response
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    return response.json()


def get_verification_code(context: Context, company_number: str):
    """Will get the verification code (sent by post) for specified company.

    :return: verification code sent by post
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    verification_code = response.json()['letter_verification_code']
    return verification_code


def is_verification_letter_sent(
        context: Context, company_number: str) -> bool:
    """Check if verification letter was sent.

    :return: True if letter was sent and False if it wasn't
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    context.response = response
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    result = response.json()['is_verification_letter_sent']
    return result


def delete_supplier_data_from_sso(
        email_address: str, *, context: Context = None):
    response = SSO_CLIENT.delete_user_by_email(email_address)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted %s user data from SSO DB", email_address)
    else:
        logging.warning(
            "Something went wrong when trying to delete user data for %s from "
            "SSO DB", email_address)


def delete_supplier_data_from_dir(ch_id: str, *, context: Context = None):
    response = DIRECTORY_CLIENT.delete_company_by_ch_id(ch_id)
    if context:
        context.response = response
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted supplier data for company %s from DIR DB",
            ch_id)
    else:
        logging.warning(
            "Something went wrong when trying to delete supplier data for "
            "company %s from DIR DB", ch_id)


def flag_sso_account_as_verified(context: Context, email_address: str):
    response = SSO_CLIENT.flag_user_email_as_verified_or_not(
        email_address, verified=True)
    context.response = response
    if response.status_code == 204:
        logging.debug("Flagged '%s' account as verified", email_address)
    else:
        logging.warning(
            "Something went wrong when trying to flag %s email as verified",
            email_address)
