# -*- coding: utf-8 -*-
"""ExRed utils."""
import logging
from datetime import datetime
from os.path import abspath, join

from tests.exred.drivers import DRIVERS
from tests.settings import EXRED_SCREENSHOTS_DIR


def take_screenshot(driver: DRIVERS, page_name: str):
    """Will take a screenshot of current page.

    :param driver: Any of the WebDrivers
    :param page_name: page name which will be used in the screenshot filename
    """
    stamp = datetime.isoformat(datetime.utcnow())
    file_name = "{}-{}.png".format(stamp, page_name)
    file_path = abspath(join(EXRED_SCREENSHOTS_DIR, file_name))
    driver.get_screenshot_as_file(file_path)
    logging.debug("User took a screenshot of %s page. You can find it here:"
                  " %s", page_name, file_path)
