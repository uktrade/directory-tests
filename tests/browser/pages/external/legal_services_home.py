# -*- coding: utf-8 -*-
"""External site - Legal Services Page Object."""
import logging

from selenium import webdriver
from utils import take_screenshot

from pages.common_actions import check_url

NAME = "Home"
SERVICE = "Legal Services"
TYPE = "home"
URL = "https://medium.com/legal-services-are-great"
SELECTORS = {}


def should_be_here(driver: webdriver):
    take_screenshot(driver, SERVICE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
