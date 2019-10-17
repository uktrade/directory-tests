# -*- coding: utf-8 -*-
"""Generic - 404 page"""
import logging

from directory_tests_shared import PageType, Service
from tests.functional.utils.request import check_response

SERVICE = Service.GENERIC
NAME = "This page cannot be found"
TYPE = PageType.ERROR
URL = None
EXPECTED_STRINGS = [
    "This page cannot be found",
    "If you entered a web address please check it’s correct.",
    "Go to the homepage",
]


def should_be_here(response):
    check_response(response, 404, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on generic 404 page")
