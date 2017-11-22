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
BROWSERS = os.environ.get("BROWSERS", "").split()
BROWSERS_VERSIONS = os.environ.get("VERSIONS", "").split()
HUB_URL = os.environ.get("HUB_URL", None)
CAPABILITIES = os.environ.get("CAPABILITIES", None)
BUILD_ID = os.environ.get("CIRCLE_SHA1", str(datetime.date(datetime.now())))
EXRED_UI_URL = os.environ["EXRED_UI_URL"]
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SSO_URL = os.environ["DIRECTORY_UI_SSO_URL"]
SELLING_ONLINE_OVERSEAS_UI_URL = os.environ["SELLING_ONLINE_OVERSEAS_UI_URL"]
EXPORT_OPPORTUNITIES_UI_URL = os.environ["EXPORT_OPPORTUNITIES_UI_URL"]
EVENTS_UI_URL = os.environ["EVENTS_UI_URL"]

__take_screenshots = os.environ.get("TAKE_SCREENSHOTS")
TAKE_SCREENSHOTS = (True
                    if __take_screenshots
                    and __take_screenshots.lower() in ["true", "1", "yes"]
                    else False)

# BrowserStack variables
BROWSERSTACK_SERVER = os.environ.get(
    "BROWSERSTACK_SERVER", "hub.browserstack.com")
BROWSERSTACK_USER = os.environ.get("BROWSERSTACK_USER", "")
BROWSERSTACK_PASS = os.environ.get("BROWSERSTACK_PASS", "")
BROWSERSTACK_EXECUTOR_URL = ("http://{}:{}@{}/wd/hub".format(
    BROWSERSTACK_USER, BROWSERSTACK_PASS, BROWSERSTACK_SERVER))
BROWSERSTACK_SESSIONS_URL = "https://www.browserstack.com/automate/sessions/{}.json"


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

CONFIG = config.get(
    config_file=CONFIG_NAME, hub_url=HUB_URL, capabilities=CAPABILITIES,
    browsers=BROWSERS, versions=BROWSERS_VERSIONS, build_id=BUILD_ID)
