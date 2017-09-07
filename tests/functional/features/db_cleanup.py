# -*- coding: utf-8 -*-
"""Remove User & Accounts from FAB & SSO after test."""
import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from tests.settings import (
    DIR_DB_HOST,
    DIR_DB_NAME,
    DIR_DB_PASSWORD,
    DIR_DB_PORT,
    DIR_DB_USER,
    SSO_DB_HOST,
    SSO_DB_NAME,
    SSO_DB_PASSWORD,
    SSO_DB_PORT,
    SSO_DB_USER
)


SSO_CLEAN_UP = """
DO $$
DECLARE
actor_email TEXT;
userid INTEGER;
BEGIN
    -- STEP 0 - get user ID (need to explicitly cast it to Integer)
    actor_email := %s;
    userid := (SELECT id::INTEGER FROM user_user WHERE email = actor_email);
    -- STEP 1 - delete account email address
    DELETE FROM account_emailaddress WHERE user_id = userid;
    -- STEP 2 - delete user account
    DELETE FROM user_user WHERE id = userid;
END $$;
"""

SSO_EXPIRED_SESSION_CLEAN_UP = """
DELETE FROM django_session WHERE age(expire_date, NOW()) < '1 day';
"""

DIRECTORY_CLEAN_UP = """
DO $$
DECLARE
actor_email TEXT;
companyID INTEGER;
BEGIN
    -- STEP 0 - get company ID (need to explicitly cast it to Integer)
    actor_email := %s;
    companyID := (SELECT company_id::INTEGER FROM user_user WHERE company_email = actor_email);
    -- STEP 1 - delete all possible notifications
    DELETE FROM notifications_supplieremailnotification WHERE supplier_id = companyID;
    DELETE FROM notifications_anonymousunsubscribe WHERE email = actor_email;
    DELETE FROM notifications_anonymousemailnotification WHERE email = actor_email;
    -- STEP 2 - delete messages sent to the Supplier
    DELETE FROM contact_messagetosupplier WHERE recipient_id = companyID;
    -- STEP 3 - delete all case studies
    DELETE FROM company_companycasestudy WHERE company_id = companyID;
    -- STEP 4 - delete user details
    DELETE FROM user_user WHERE company_id = companyID;
    -- STEP 5 - and finally delete company details
    DELETE FROM company_company WHERE id = companyID;
END $$;
"""

DIRECTORY_COMPANY_EMAIL = """
SELECT company_email
FROM user_user u, company_company c
WHERE c.number = %s
AND u.company_id = c.id;
"""


def get_dir_db_connection(*, dict_cursor: bool = False):
    try:
        connection = psycopg2.connect(
            dbname=DIR_DB_NAME, user=DIR_DB_USER, password=DIR_DB_PASSWORD,
            host=DIR_DB_HOST, port=DIR_DB_PORT)
    except psycopg2.OperationalError as e:
        logging.error('Unable to connect to Directory DB!\n%s', e)
        raise
    else:
        logging.debug('Connected to Directory DB: %s!', DIR_DB_NAME)
    if dict_cursor:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = connection.cursor()
    return connection, cursor


def get_sso_db_connection(*, dict_cursor: bool = False):
    try:
        connection = psycopg2.connect(
            dbname=SSO_DB_NAME, user=SSO_DB_USER, password=SSO_DB_PASSWORD,
            host=SSO_DB_HOST, port=SSO_DB_PORT)
    except psycopg2.OperationalError as e:
        logging.error('Unable to connect to SSO DB!\n%s', e)
        raise
    else:
        logging.debug('Connected to Directory DB: %s!', DIR_DB_NAME)
    if dict_cursor:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = connection.cursor()
    return connection, cursor


def get_company_email(number: str) -> str:
    """Get email address associated with company.

    :param number: company number given by Companies House.
    :return: email address or None if couldn't find company or user associated
             with it
    """
    connection, cursor = get_dir_db_connection()
    data = (number, )
    cursor.execute(DIRECTORY_COMPANY_EMAIL, data)
    result_set = cursor.fetchone()
    cursor.close()
    connection.close()
    email = result_set[0] if result_set is not None else None
    return email


def delete_supplier_data(service_name, email_address):
    if service_name == "DIRECTORY":
        sql = DIRECTORY_CLEAN_UP
        connection, cursor = get_dir_db_connection()
    elif service_name == "SSO":
        sql = SSO_CLEAN_UP
        connection, cursor = get_sso_db_connection()
    else:
        raise KeyError("Unrecognized service name: {}".format(service_name))
    logging.debug("Deleting Supplier data from %s DB for: %s", service_name,
                  email_address)
    data = (email_address, )
    cursor.execute(sql, data)
    if cursor.description:
        logging.debug("Deletion query results:\n%s", cursor.fetchone())
    else:
        logging.debug("Deletion query did not return any results")
    connection.commit()
    cursor.close()
    connection.close()
    logging.debug("Deleted Supplier data from %s DB for: %s", service_name,
                  email_address)


def delete_expired_django_sessions():
    connection, cursor = get_sso_db_connection()
    cursor.execute(SSO_EXPIRED_SESSION_CLEAN_UP)
    connection.commit()
    cursor.close()
    connection.close()
    logging.debug("Deleted all Django sessions that expired before today")
