# -*- coding: utf-8 -*-
"""Project Settings."""
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from envparse import env

from utils.browser import get_driver_capabilities

#####################################################################
# Behave specific settings
#####################################################################
AUTO_RETRY = env.bool("AUTO_RETRY", default=True)
TAKE_SCREENSHOTS = env.bool("TAKE_SCREENSHOTS", default=False)


#####################################################################
# Browser & BrowserStack related settings
#####################################################################
BROWSER = env.str("BROWSER", default="chrome")
BROWSER_CUSTOM_CAPABILITIES = env.dict("CAPABILITIES", default=None)
BROWSER_ENVIRONMENT = env.str("BROWSER_ENVIRONMENT", default="local")
BROWSER_HEADLESS = env.bool("HEADLESS", default=False)
BROWSER_RESTART_POLICY = env.str("RESTART_POLICY", default="feature")
BROWSER_TYPE = env.str("BROWSER_TYPE", default="desktop")
BROWSER_VERSION = env.str("VERSION", default=None)
BROWSERSTACK_PASS = env.str("BROWSERSTACK_PASS", default="")
BROWSERSTACK_SERVER = env.str("BROWSERSTACK_SERVER", default="hub.browserstack.com")
BROWSERSTACK_SESSIONS_URL = "https://www.browserstack.com/automate/sessions/{}.json"
BROWSERSTACK_USER = env.str("BROWSERSTACK_USER", default="")
BROWSERSTACK_EXECUTOR_URL = (
    f"http://{BROWSERSTACK_USER}:{BROWSERSTACK_PASS}@{BROWSERSTACK_SERVER}/wd/hub"
)
BUILD_ID = env.str("CIRCLE_SHA1", default=datetime.isoformat(datetime.now()))
HUB_URL = env.str("HUB_URL", default=None)

if BROWSER_ENVIRONMENT.lower() == "remote" and (
    BROWSERSTACK_USER and BROWSERSTACK_PASS
):
    HUB_URL = BROWSERSTACK_EXECUTOR_URL

DRIVER_CAPABILITIES = get_driver_capabilities(
    environment=BROWSER_ENVIRONMENT, browser_type=BROWSER_TYPE, browser=BROWSER,
    version=BROWSER_VERSION, custom_capabilities=BROWSER_CUSTOM_CAPABILITIES,
    build=BUILD_ID
)


#####################################################################
# Service URLs & Credentials
#####################################################################
BARRED_USERS = list(filter(None, env.str("BARRED_USERS", default="").split(",")))
BASICAUTH_PASS = env.str("BASICAUTH_PASS", default=None)
BASICAUTH_USER = env.str("BASICAUTH_USER", default=None)
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str("DIRECTORY_CMS_API_CLIENT_API_KEY")
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str("DIRECTORY_CMS_API_CLIENT_BASE_URL")
DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS = env.int(
    "DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS", default=60 * 60 * 24 * 30
)  # 30 days
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = env.int(
    "DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT", default=30
)
DIRECTORY_CMS_API_CLIENT_SENDER_ID = env.str(
    "DIRECTORY_CMS_API_CLIENT_SENDER_ID", default="directory"
)
DIRECTORY_CONTACT_US_UI_URL = env.str("DIRECTORY_CONTACT_US_UI_URL")
DIRECTORY_FORMS_API_KEY = env.str("DIRECTORY_FORMS_API_KEY")
DIRECTORY_FORMS_API_SENDER_ID = env.str("DIRECTORY_FORMS_API_SENDER_ID")
DIRECTORY_FORMS_API_URL = env.str("DIRECTORY_FORMS_API_URL")
DIRECTORY_SSO_API_CLIENT_API_KEY = env.str("DIRECTORY_SSO_API_CLIENT_API_KEY")
DIRECTORY_SSO_API_CLIENT_BASE_URL = env.str("DIRECTORY_SSO_API_CLIENT_BASE_URL")
DIRECTORY_UI_BUYER_URL = env.str("DIRECTORY_UI_BUYER_URL")
DIRECTORY_UI_PROFILE_URL = env.str("DIRECTORY_UI_PROFILE_URL")
DIRECTORY_UI_SSO_URL = env.str("DIRECTORY_UI_SSO_URL")
DIRECTORY_UI_SUPPLIER_URL = env.str("DIRECTORY_UI_SUPPLIER_URL")
EVENTS_UI_URL = env.str("EVENTS_UI_URL")
EXPORT_OPPORTUNITIES_UI_URL = env.str("EXPORT_OPPORTUNITIES_UI_URL")
EXRED_UI_URL = env.str("EXRED_UI_URL")
GOV_NOTIFY_API_KEY = env.str("GOV_NOTIFY_API_KEY")
INTERNATIONAL_UI_URL = urljoin(env.str("EXRED_UI_URL"), "international/")
INVEST_UI_URL = env.str("INVEST_UI_URL")
SELLING_ONLINE_OVERSEAS_UI_URL = env.str("SELLING_ONLINE_OVERSEAS_UI_URL")


#####################################################################
# Content specific settings
#####################################################################
FORMS_API_MAILBOXES = {
    "DIT Enquiry unit": env.str("FORMS_API_SENDER_EMAIL_DIT_ENQUIRIES"),
    "Events mailbox": env.str("FORMS_API_SENDER_EMAIL_EVENTS"),
    "DSO mailbox": env.str("FORMS_API_SENDER_EMAIL_DSO"),
    "Invest mailbox": env.str("FORMS_API_SENDER_EMAIL_INVEST"),
    "Trade mailbox": env.str("FORMS_API_SENDER_EMAIL_TRADE"),
}
INVEST_CONTACT_CONFIRMATION_SUBJECT = env.str(
    "INVEST_CONTACT_CONFIRMATION_SUBJECT", default="Contact form user email subject"
)
HPO_ENQUIRY_CONFIRMATION_SUBJECT = env.str(
    "HPO_ENQUIRY_CONFIRMATION_SUBJECT",
    default="Your High Potential Opportunity Enquiry – UK Department for International Trade",
)
HPO_AGENT_EMAIL_ADDRESS = env.str("HPO_AGENT_EMAIL_ADDRESS", default="test@example.com")
HPO_AGENT_EMAIL_SUBJECT = env.str(
    "HPO_AGENT_EMAIL_SUBJECT", default="HPO Enquiry (Invest in GREAT Britain)"
)
HPO_PDF_URLS = [
    "https://directory-cms-public.s3.amazonaws.com/documents/documents/A_High_Potential_Opportunity_in_High_Productivity_Food_Production.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Investment_Opportunity_in_Lightweight_Structures.pdf",
    "https://directory-cms-public.s3.amazonaws.com/documents/A_High_Potential_Investment_Opportunity_in_UK_Rail.pdf",
]
MD5_CHECKSUM_EIG_LOGO = env.str(
    "EIG_LOGO_MD5_CHECKSUM", default="8bc6134cffb3cdb134ad910e6a698fb8"
)
MD5_CHECKSUM_GREAT_LOGO = env.str(
    "GREAT_LOGO_MD5_CHECKSUM", default="6af76ffaffc1009edc9f92871ce73274"
)
MD5_CHECKSUM_EVENTS_BIG_HEADER_LOGO = env.str(
    "EVENTS_BIG_LOGO_MD5_CHECKSUM", default="cf06c747729c8515086b39a47f149fad"
)
MD5_CHECKSUM_EVENTS_BIG_FOOTER_LOGO = env.str(
    "EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM", default="7efc18df0076a860835196f7ca39e437"
)
MD5_CHECKSUM_INVEST_IN_GREAT = env.str(
    "MD5_CHECKSUM_INVEST_IN_GREAT", default="b1cca6e547c89896f0b13632bc298168"
)
MD5_CHECKSUM_DIT_FAVICON = env.str(
    "DIT_FAVICON_MD5_CHECKSUM", default="93bd34ac9de2cb059c65c5e7931667a2"
)


#####################################################################
# API clients settings
#####################################################################
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
    },
)
