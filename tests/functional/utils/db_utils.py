# -*- coding: utf-8 -*-
"""Remove User & Accounts from FAB & SSO after test."""
import logging

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
    """Get email address associated with company.

    :param number: company number given by Companies House.
    :return: email address or None if couldn't find company or user associated
             with it
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(number)
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    email = response.json()['company_email']
    logging.debug("Email for company %s is %s", number, email)
    return email


def get_published_companies() -> list:
    """Get a List of dicts with published companies.

    :return: a list of dictionaries with published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies()
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    return response.json()


def get_published_companies_with_n_sectors(number_of_sectors: int) -> list:
    """Get a List of published companies with at least N associated sectors.

    :param number_of_sectors: minimal number of sectors associated with company
    :return: a list of dictionaries with matching published companies
    """
    response = DIRECTORY_CLIENT.get_published_companies(
        minimal_number_of_sectors=number_of_sectors)
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    return response.json()


def get_verification_code(company_number):
    """Will get the verification code (sent by post) for specified company.

    :param company_number: company number given by Companies House
    :return: verification code sent by post
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    verification_code = response.json()['letter_verification_code']
    return verification_code


def is_verification_letter_sent(company_number: str) -> bool:
    """Check if verification letter was sent.

    :param company_number: company number
    :return: True if letter was sent and False if it wasn't
    """
    response = DIRECTORY_CLIENT.get_company_by_ch_id(company_number)
    assert response.status_code == 200, (
        "Expected 200 but got {} with content: {}".format(
            response.status_code, response.content)
    )
    result = response.json()['is_verification_letter_sent']
    return result


def delete_supplier_data_from_sso(email_address):
    response = SSO_CLIENT.delete_user_by_email(email_address)
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted %s user data from SSO DB", email_address)
    else:
        logging.warning(
            "Something went wrong when trying to delete user data for %s from "
            "SSO DB", email_address)


def delete_supplier_data_from_dir(ch_id):
    response = DIRECTORY_CLIENT.delete_company_by_ch_id(ch_id)
    if response.status_code == 204:
        logging.debug(
            "Successfully deleted supplier data for company %s from DIR DB",
            ch_id)
    else:
        logging.warning(
            "Something went wrong when trying to delete supplier data for "
            "company %s from DIR DB", ch_id)


def flag_sso_account_as_verified(email_address):
    response = SSO_CLIENT.flag_user_email_as_verified_or_not(
        email_address, verified=True)
    if response.status_code == 204:
        logging.debug("Flagged '%s' account as verified", email_address)
    else:
        logging.warning(
            "Something went wrong when trying to flag %s email as verified",
            email_address)
