# -*- coding: utf-8 -*-
"""Project Settings."""
import os
from datetime import datetime

from directory_constants.constants.exred_sector_names import CODES_SECTORS_DICT

import config
from django.conf import settings

EXRED_SECTORS = CODES_SECTORS_DICT

# variables set in Paver configuration file
CONFIG_NAME = os.environ.get("CONFIG", "local")
TASK_ID = int(os.environ.get("TASK_ID", 0))

# optional variables set by user
RESTART_BROWSER = os.environ.get("RESTART_BROWSER", "feature")
BROWSERS = os.environ.get("BROWSERS", "").split()
BROWSERS_VERSIONS = os.environ.get("VERSIONS", "").split()
HUB_URL = os.environ.get("HUB_URL", None)
CAPABILITIES = os.environ.get("CAPABILITIES", None)
BUILD_ID = os.environ.get("CIRCLE_SHA1", str(datetime.date(datetime.now())))
EXRED_UI_URL = os.environ["EXRED_UI_URL"]
INVEST_UI_URL = os.environ["INVEST_UI_URL"]
INVEST_MAILBOX_ADMIN_EMAIL = os.environ["INVEST_MAILBOX_ADMIN_EMAIL"]
INVEST_CONTACT_CONFIRMATION_SUBJECT = os.getenv(
    "INVEST_CONTACT_CONFIRMATION_SUBJECT", "Contact form user email subject")
INVEST_AGENT_CONTACT_CONFIRMATION_SUBJECT = os.getenv(
    "INVEST_AGENT_CONTACT_CONFIRMATION_SUBJECT",
    "Contact form agent email subject"
)
IP_RESTRICTOR_SKIP_CHECK_SENDER_ID = os.environ["IP_RESTRICTOR_SKIP_CHECK_SENDER_ID"]
IP_RESTRICTOR_SKIP_CHECK_SECRET = os.environ["IP_RESTRICTOR_SKIP_CHECK_SECRET"]
HPO_ENQUIRY_CONFIRMATION_SUBJECT = os.getenv(
    "HPO_ENQUIRY_CONFIRMATION_SUBJECT",
    "Your High Potential Opportunity Enquiry – UK Department for International Trade"
)
HPO_AGENT_EMAIL_ADDRESS = os.getenv(
    "HPO_AGENT_EMAIL_ADDRESS", "test@example.com")
HPO_AGENT_EMAIL_SUBJECT = os.getenv(
    "HPO_AGENT_EMAIL_SUBJECT", "HPO Enquiry (Invest in GREAT Britain)")
HPO_PDF_URLS = [
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Opportunity_in_High_Productivity_Food_Production.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_HPO_in_Lightweight_Structures.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_HPO_in_Rail_Infrastructure.pdf",
]
MAILGUN_API_USER = os.getenv("MAILGUN_API_USER", "api")
MAILGUN_INVEST_DOMAIN = os.getenv("MAILGUN_INVEST_DOMAIN")
MAILGUN_INVEST_EVENTS_URL = "https://api.mailgun.net/v3/%s/events" % MAILGUN_INVEST_DOMAIN
MAILGUN_INVEST_SECRET_API_KEY = os.getenv("MAILGUN_INVEST_SECRET_API_KEY")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_TOKEN = os.getenv("ZENDESK_TOKEN")
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
DIRECTORY_SSO_API_CLIENT_API_KEY = os.environ["DIRECTORY_SSO_API_CLIENT_API_KEY"]
DIRECTORY_SSO_API_CLIENT_BASE_URL = os.environ["DIRECTORY_SSO_API_CLIENT_BASE_URL"]
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_UI_SSO_URL = os.environ["DIRECTORY_UI_SSO_URL"]
DIRECTORY_UI_PROFILE_URL = os.environ["DIRECTORY_UI_PROFILE_URL"]
DIRECTORY_CONTACT_US_UI_URL = os.environ["DIRECTORY_CONTACT_US_UI_URL"]
GOV_NOTIFY_API_KEY = os.environ["GOV_NOTIFY_API_KEY"]
SELLING_ONLINE_OVERSEAS_UI_URL = os.environ["SELLING_ONLINE_OVERSEAS_UI_URL"]
EXPORT_OPPORTUNITIES_UI_URL = os.environ["EXPORT_OPPORTUNITIES_UI_URL"]
EVENTS_UI_URL = os.environ["EVENTS_UI_URL"]
DIT_LOGO_MD5_CHECKSUM = os.environ.get(
    "DIT_LOGO_MD5_CHECKSUM", "c4873f79300c7726f227e7934aff8e70"
)
UK_GOV_MD5_CHECKSUM = os.environ.get(
    "UK_GOV_MD5_CHECKSUM", "c547abd199ebb51619381f8755128741"
)
DIT_FAVICON_MD5_CHECKSUM = os.environ.get(
    "DIT_FAVICON_MD5_CHECKSUM", "93bd34ac9de2cb059c65c5e7931667a2"
)

__take_screenshots = os.environ.get("TAKE_SCREENSHOTS", "false")
TAKE_SCREENSHOTS = (
    True
    if __take_screenshots
    and __take_screenshots.lower() in ["true", "1", "yes"]
    else False
)
__auto_retry = os.environ.get("AUTO_RETRY", "true")
AUTO_RETRY = (
    True
    if __auto_retry and __auto_retry.lower() in ["true", "1", "yes"]
    else False
)
__set_hawk_cookie = os.environ.get("SET_HAWK_COOKIE", "true")
SET_HAWK_COOKIE = (
    True
    if __set_hawk_cookie and __set_hawk_cookie.lower() in ["true", "1", "yes"]
    else False
)

# BrowserStack variables
BROWSERSTACK_SERVER = os.environ.get(
    "BROWSERSTACK_SERVER", "hub.browserstack.com"
)
BROWSERSTACK_USER = os.environ.get("BROWSERSTACK_USER", "")
BROWSERSTACK_PASS = os.environ.get("BROWSERSTACK_PASS", "")
BROWSERSTACK_EXECUTOR_URL = "http://{}:{}@{}/wd/hub".format(
    BROWSERSTACK_USER, BROWSERSTACK_PASS, BROWSERSTACK_SERVER
)
BROWSERSTACK_SESSIONS_URL = (
    "https://www.browserstack.com/automate/sessions/{}.json"
)


if CONFIG_NAME.startswith("browserstack") and (
    BROWSERSTACK_SERVER and BROWSERSTACK_USER and BROWSERSTACK_PASS
):
    HUB_URL = BROWSERSTACK_EXECUTOR_URL

if CAPABILITIES:
    import json

    CAPABILITIES = json.loads(CAPABILITIES)

CONFIG = config.get(
    config_file=CONFIG_NAME,
    hub_url=HUB_URL,
    capabilities=CAPABILITIES,
    browsers=BROWSERS,
    versions=BROWSERS_VERSIONS,
    build_id=BUILD_ID,
)

DIRECTORY_CMS_API_CLIENT_BASE_URL = os.environ["DIRECTORY_CMS_API_CLIENT_BASE_URL"]
DIRECTORY_CMS_API_CLIENT_API_KEY = os.environ["DIRECTORY_CMS_API_CLIENT_API_KEY"]
DIRECTORY_CMS_API_CLIENT_SENDER_ID = os.getenv("DIRECTORY_CMS_API_CLIENT_SENDER_ID", "directory")
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = int(os.getenv("DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT", 30))
DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS = int(os.getenv("DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS", 60 * 60 * 24 * 30))  # 30 days
settings.configure(
    DIRECTORY_CMS_API_CLIENT_BASE_URL=DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_CLIENT_API_KEY=DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_SENDER_ID=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS,
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME='EXPORT_READINESS',
    CACHES={
        'cms_fallback': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
)
