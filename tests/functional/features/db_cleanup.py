# -*- coding: utf-8 -*-
"""Remove User & Accounts from FAB & SSO after test."""
import logging

import psycopg2

from tests.functional.features.settings import FAB_DB_HOST
from tests.functional.features.settings import FAB_DB_NAME
from tests.functional.features.settings import FAB_DB_PASSWORD
from tests.functional.features.settings import FAB_DB_PORT
from tests.functional.features.settings import FAB_DB_USER
from tests.functional.features.settings import SSO_DB_HOST
from tests.functional.features.settings import SSO_DB_NAME
from tests.functional.features.settings import SSO_DB_PASSWORD
from tests.functional.features.settings import SSO_DB_PORT
from tests.functional.features.settings import SSO_DB_USER


SSO_CLEAN_UP = """
DO $$
DECLARE
userid INTEGER;
BEGIN
    -- STEP 0 - get user ID (need to explicitly cast it to Integer)
    userid := (SELECT id::INTEGER FROM user_user WHERE email = %s);
    -- STEP 1 - delete account email address
    DELETE FROM account_emailaddress WHERE user_id = userid;
    -- STEP 2 - delete user account
    DELETE FROM user_user WHERE id = userid;
    -- STEP 3 - DELETE expired Django sessions
    DELETE FROM django_session WHERE age(expire_date, NOW()) < '1 day';
END $$;
"""

FAB_CLEAN_UP = """
DO $$
DECLARE
companyID INTEGER;
BEGIN
    -- STEP 0 - get company ID (need to explicitly cast it to Integer)
    companyID := (SELECT company_id::INTEGER FROM user_user WHERE company_email = %s);
    -- STEP 1 - delete all possible notifications
    DELETE FROM notifications_supplieremailnotification WHERE supplier_id = companyID;
    DELETE FROM notifications_anonymousunsubscribe WHERE email = '{email}';
    DELETE FROM notifications_anonymousemailnotification WHERE email = '{email}';
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


def get_fab_db_connection():
    connection = psycopg2.connect(dbname=FAB_DB_NAME, user=FAB_DB_USER,
                                  password=FAB_DB_PASSWORD, host=FAB_DB_HOST,
                                  port=FAB_DB_PORT)
    cursor = connection.cursor()
    return connection, cursor


def get_sso_db_connection():
    connection = psycopg2.connect(dbname=SSO_DB_NAME, user=SSO_DB_USER,
                                  password=SSO_DB_PASSWORD, host=SSO_DB_HOST,
                                  port=SSO_DB_PORT)
    cursor = connection.cursor()
    return connection, cursor


def delete_supplier_data(service_name, email_address):
    if service_name == "FAB":
        sql = FAB_CLEAN_UP
        connection, cursor = get_fab_db_connection()
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

