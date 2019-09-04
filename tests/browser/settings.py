# -*- coding: utf-8 -*-
"""Project Settings."""
import os
from datetime import datetime
from urllib.parse import urljoin

import config
from django.conf import settings

# variables set in Paver configuration file
CONFIG_NAME = os.environ.get("CONFIG", "local")
TASK_ID = int(os.environ.get("TASK_ID", 0))

# optional variables set by user
RESTART_BROWSER = os.environ.get("RESTART_BROWSER", "feature")
BROWSERS = os.environ.get("BROWSERS", "").split()
BROWSERS_VERSIONS = os.environ.get("VERSIONS", "").split()
BARRED_USERS = list(filter(None, os.environ.get("BARRED_USERS", "").split(",")))
HUB_URL = os.environ.get("HUB_URL", None)
CAPABILITIES = os.environ.get("CAPABILITIES", None)
BUILD_ID = os.environ.get("CIRCLE_SHA1", str(datetime.date(datetime.now())))
EXRED_UI_URL = os.environ["EXRED_UI_URL"]
INTERNATIONAL_UI_URL = urljoin(EXRED_UI_URL, "international/")
INVEST_UI_URL = os.environ["INVEST_UI_URL"]
INVEST_CONTACT_CONFIRMATION_SUBJECT = os.getenv(
    "INVEST_CONTACT_CONFIRMATION_SUBJECT", "Contact form user email subject")
BASICAUTH_USER = os.getenv("BASICAUTH_USER", None)
BASICAUTH_PASS = os.getenv("BASICAUTH_PASS", None)
HPO_ENQUIRY_CONFIRMATION_SUBJECT = os.getenv(
    "HPO_ENQUIRY_CONFIRMATION_SUBJECT",
    "Your High Potential Opportunity Enquiry – UK Department for International Trade"
)
HPO_AGENT_EMAIL_ADDRESS = os.getenv(
    "HPO_AGENT_EMAIL_ADDRESS", "test@example.com")
HPO_AGENT_EMAIL_SUBJECT = os.getenv(
    "HPO_AGENT_EMAIL_SUBJECT", "HPO Enquiry (Invest in GREAT Britain)")
HPO_PDF_URLS = [
    "https://directory-cms-public.s3.amazonaws.com/documents/documents/A_High_Potential_Opportunity_in_High_Productivity_Food_Production.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Investment_Opportunity_in_Lightweight_Structures.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Investment_Opportunity_in_UK_Rail.pdf",
]
FORMS_API_MAILBOXES = {
    "DIT Enquiry unit": os.getenv("FORMS_API_EMAIL_DIT_ENQUIRIES"),
    "Events mailbox": os.getenv("FORMS_API_EMAIL_EVENTS"),
    "DSO mailbox": os.getenv("FORMS_API_EMAIL_DSO"),
    "Invest mailbox": os.getenv("FORMS_API_EMAIL_INVEST"),
}

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
EIG_LOGO_MD5_CHECKSUM = os.environ.get(
    "EIG_LOGO_MD5_CHECKSUM", "8bc6134cffb3cdb134ad910e6a698fb8"
)
GREAT_LOGO_MD5_CHECKSUM = os.environ.get(
    "GREAT_LOGO_MD5_CHECKSUM", "6af76ffaffc1009edc9f92871ce73274"
)
EVENTS_BIG_HEADER_LOGO_MD5_CHECKSUM = os.environ.get(
    "EVENTS_BIG_LOGO_MD5_CHECKSUM", "cf06c747729c8515086b39a47f149fad"
)
EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM = os.environ.get(
    "EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM", "7efc18df0076a860835196f7ca39e437"
)
UK_GOV_MD5_CHECKSUM = os.environ.get(
    "UK_GOV_MD5_CHECKSUM", "b1cca6e547c89896f0b13632bc298168"
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
MAX_SESSION_RECOVERY_RETRIES = 2


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
DIRECTORY_FORMS_API_URL = os.environ["DIRECTORY_FORMS_API_URL"]
DIRECTORY_FORMS_API_KEY = os.environ["DIRECTORY_FORMS_API_KEY"]
DIRECTORY_FORMS_API_SENDER_ID = os.environ["DIRECTORY_FORMS_API_SENDER_ID"]

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
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME="EXPORT_READINESS",
    
    DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS=DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS,

    DIRECTORY_SSO_API_CLIENT_BASE_URL=DIRECTORY_SSO_API_CLIENT_BASE_URL,
    DIRECTORY_SSO_API_CLIENT_API_KEY=DIRECTORY_SSO_API_CLIENT_API_KEY,
    DIRECTORY_SSO_API_CLIENT_SENDER_ID=DIRECTORY_CMS_API_CLIENT_SENDER_ID,
    DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT,

    CACHES={
        "cms_fallback": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }
)
