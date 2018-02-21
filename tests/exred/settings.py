# -*- coding: utf-8 -*-
"""Project Settings."""
import os
from datetime import datetime
from urllib import parse as urlparse

from directory_constants.constants.exred_sector_names import CODES_SECTORS_DICT

import config

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
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_UI_SSO_URL = os.environ["DIRECTORY_UI_SSO_URL"]
DIRECTORY_UI_PROFILE_URL = os.environ["DIRECTORY_UI_PROFILE_URL"]
SSO_PROXY_API_CLIENT_BASE_URL = os.environ["SSO_PROXY_API_CLIENT_BASE_URL"]
SSO_PROXY_SIGNATURE_SECRET = os.environ["SSO_PROXY_SIGNATURE_SECRET"]
SELLING_ONLINE_OVERSEAS_UI_URL = os.environ["SELLING_ONLINE_OVERSEAS_UI_URL"]
EXPORT_OPPORTUNITIES_UI_URL = os.environ["EXPORT_OPPORTUNITIES_UI_URL"]
EVENTS_UI_URL = os.environ["EVENTS_UI_URL"]
DIT_LOGO_MD5_CHECKSUM = os.environ.get(
    "DIT_LOGO_MD5_CHECKSUM", "c4873f79300c7726f227e7934aff8e70")
DIT_FAVICON_MD5_CHECKSUM = os.environ.get(
    "DIT_FAVICON_MD5_CHECKSUM", "93bd34ac9de2cb059c65c5e7931667a2")

__take_screenshots = os.environ.get("TAKE_SCREENSHOTS", "false")
TAKE_SCREENSHOTS = (True
                    if __take_screenshots
                    and __take_screenshots.lower() in ["true", "1", "yes"]
                    else False)
__auto_retry = os.environ.get("AUTO_RETRY", "true")
AUTO_RETRY = (True
              if __auto_retry
              and __auto_retry.lower() in ["true", "1", "yes"]
              else False)

# Mailgun details required to get verification emails
MAILGUN_SSO_DOMAIN = os.environ["MAILGUN_SSO_DOMAIN"]
MAILGUN_SSO_EVENTS_URL = (
        "https://api.mailgun.net/v3/%s/events" % MAILGUN_SSO_DOMAIN)
MAILGUN_SSO_API_USER = "api"
MAILGUN_SSO_SECRET_API_KEY = os.environ["MAILGUN_SSO_SECRET_API_KEY"]

# BrowserStack variables
BROWSERSTACK_SERVER = os.environ.get(
    "BROWSERSTACK_SERVER", "hub.browserstack.com")
BROWSERSTACK_USER = os.environ.get("BROWSERSTACK_USER", "")
BROWSERSTACK_PASS = os.environ.get("BROWSERSTACK_PASS", "")
BROWSERSTACK_EXECUTOR_URL = ("http://{}:{}@{}/wd/hub".format(
    BROWSERSTACK_USER, BROWSERSTACK_PASS, BROWSERSTACK_SERVER))
BROWSERSTACK_SESSIONS_URL = (
    "https://www.browserstack.com/automate/sessions/{}.json")


# These DB details are required to do post-test clean-up in SSO DB
SSO_DB_URL = urlparse.urlparse(os.getenv('SSO_DATABASE_URL'))
SSO_DB_NAME = SSO_DB_URL.path[1:] if SSO_DB_URL else None
SSO_DB_USER = SSO_DB_URL.username if SSO_DB_URL else None
SSO_DB_PASSWORD = SSO_DB_URL.password if SSO_DB_URL else None
SSO_DB_HOST = SSO_DB_URL.hostname if SSO_DB_URL else None
SSO_DB_PORT = SSO_DB_URL.port if SSO_DB_URL else None


if (CONFIG_NAME.startswith("browserstack") and
        (BROWSERSTACK_SERVER and BROWSERSTACK_USER and BROWSERSTACK_PASS)):
    HUB_URL = BROWSERSTACK_EXECUTOR_URL

if CAPABILITIES:
    import json
    CAPABILITIES = json.loads(CAPABILITIES)

CONFIG = config.get(
    config_file=CONFIG_NAME, hub_url=HUB_URL, capabilities=CAPABILITIES,
    browsers=BROWSERS, versions=BROWSERS_VERSIONS, build_id=BUILD_ID)
