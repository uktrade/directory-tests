# -*- coding: utf-8 -*-
"""SSO Common operations."""
import logging

import psycopg2
from psycopg2.extras import RealDictCursor

from settings import (
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

SSO_FLAG_AS_VERIFIED = """
UPDATE account_emailaddress
SET verified = TRUE
WHERE email = %s;
"""


def get_sso_db_connection(*, dict_cursor: bool = False):
    try:
        connection = psycopg2.connect(
            dbname=SSO_DB_NAME, user=SSO_DB_USER, password=SSO_DB_PASSWORD,
            host=SSO_DB_HOST, port=SSO_DB_PORT)
    except psycopg2.OperationalError as e:
        logging.error('Unable to connect to SSO DB!\n%s', e)
        raise
    if dict_cursor:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = connection.cursor()
    return connection, cursor


def verify_account(email: str):
    connection, cursor = get_sso_db_connection()
    data = (email, )
    cursor.execute(SSO_FLAG_AS_VERIFIED, data)
    connection.commit()
    cursor.close()
    connection.close()
    logging.debug("Flagged '%s' account as verified", email)


def delete_supplier_data(service_name, email_address):
    sql = SSO_CLEAN_UP
    connection, cursor = get_sso_db_connection()
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
    logging.debug(
        "Deleted Supplier data from %s DB for: %s", service_name,
        email_address)


def delete_expired_django_sessions():
    connection, cursor = get_sso_db_connection()
    cursor.execute(SSO_EXPIRED_SESSION_CLEAN_UP)
    connection.commit()
    cursor.close()
    connection.close()
    logging.debug("Deleted all Django sessions that expired before today")
