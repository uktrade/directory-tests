# -*- coding: utf-8 -*-
"""SSO-Profile static assets."""
from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service

NAME = "Static assets"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_LANDING.absolute + "static/"
PAGE_TITLE = "Static assets"

SELECTORS = {}
