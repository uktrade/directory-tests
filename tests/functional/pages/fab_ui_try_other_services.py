# -*- coding: utf-8 -*-
"""FAB - Try our other services page"""
import logging

from requests import Response
from tests.functional.utils.request import check_response

EXPECTED_STRINGS = [
    "Try our other business services",
    "The Find a Buyer service promotes companies that are currently "
    "exporting or looking to export in the near future. The answers you "
    "gave suggest that your company is currently not appropriate to feature"
    " in the Find a Buyer service.",
    "Exporting is GREAT advice for new exporters"
]


def should_be_here(response: Response):
    """Check if Supplier is on Try our other services page.

    Supplier can get here, when the company has not exporting intent.

    :param response: response with Try our other services page
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on Try our other services page")
