# -*- coding: utf-8 -*-
"""Common page helpers"""
from tests.functional.features.utils import extract_csrf_middleware_token


def extract_and_set_csrf_middleware_token(context, response, supplier_alias):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param response: request with HTML content containing CSRF middleware token
    :type  response: requests.models.Response
    """
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)
