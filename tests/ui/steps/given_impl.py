# -*- coding: utf-8 -*-
"""Given steps implementation."""
import logging
from datetime import datetime

from behave.runner import Context

PAGES = {
    "new to exporting": "https://www.export.great.gov.uk/new/"
}


def go_to_page(context: Context, actor_alias: str, page_name: str):
    url = PAGES[page_name.lower()]
    context.driver.get(url)
    filename = 'screenshot-{}-{}.png'.format(
        datetime.isoformat(datetime.utcnow()),
        page_name.lower().replace(" ", "-"))

    context.driver.save_screenshot(filename)
    logging.debug("%s went to: %s", actor_alias, page_name)
