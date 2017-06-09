# -*- coding: utf-8 -*-
"""FAB Given step implementations."""
import logging

import requests

from tests.functional.features.settings import DIRECTORY_API_URL
from tests import get_absolute_url


def do_something(context, supplier_alias):
    actor = context.get_actor(alias=supplier_alias)
    logging.debug("Got the details of actor called: {}".format(actor.alias))
    client = context.get_actor_client(alias=supplier_alias)
    logging.debug("Got the {}'s HTTP client: {}".format(actor.alias, client))


def select_random_company(context):
    url = get_absolute_url('internal-api:companies-house-search')
    params = {"term": "fuzz"}
    logging.debug(url)
    response = requests.get(url=url, params=params)
    logging.debug("Response: {}".format(response.json()))

