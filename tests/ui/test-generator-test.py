# -*- coding: utf-8 -*-
"""VisualDiff Tests"""
import os

from needle.cases import NeedleTestCase

from tests.ui.drivers import get_needle_web_driver


URL_MAP = {
    "production": {
        "new_to_exporting": "https://www.export.great.gov.uk/new/",
        "occasional_exporter": "https://www.export.great.gov.uk/occasional/",
        "regular_exporer": "https://www.export.great.gov.uk/regular/",
        "export_opportunities": "https://opportunities.export.great.gov.uk/",
        "find_a_buyer": "https://find-a-buyer.export.great.gov.uk/",
        "selling_online_overseas": "https://selling-online-overseas.export.great.gov.uk/",
        "get_finance": "https://www.export.great.gov.uk/get-finance/",
        #"events": "https://www.events.trade.gov.uk/"
    }
}

URLS = URL_MAP[os.environ.get("ENVIRONMENT", "production").lower()]


def open_page(self, page_name):
    print("Opening " + URLS[page_name])
    self.driver.get(URLS[page_name])
    self.driver.implicitly_wait(10)
    #self.driver.delete_all_cookies()
    #self.driver.close()
    return self


def assert_header_did_not_change(self, page_name):
    print("Checking if header on " + page_name + " did not change")
    self.driver.set_page_load_timeout(20)
    result = open_page(self, page_name)
    result.assertScreenshot(
        ".navigation",
        "header-{}-{}".format(self.browser_name, page_name))


def assert_footer_did_not_change(self, page_name):
    print("Checking if footer on " + page_name + " did not change")
    self.driver.set_page_load_timeout(20)
    result = open_page(self, page_name)
    result.assertScreenshot(
        ".footer",
        "footer-{}-{}".format(self.browser_name, page_name))


def make_method(func, input):

    def test_input(self):
        func(self, input)

    test_input.__name__ = 'test_{func}_{input}'.format(func=func.__name__, input=input)
    return test_input


def generate(func, *inputs):
    """
    Take a TestCase and add a test method for each input
    """
    def decorator(klass):
        for input in inputs:
            test_input = make_method(func, input)
            setattr(klass, test_input.__name__, test_input)
        return klass

    return decorator


@generate(assert_header_did_not_change, *URLS)
class DidHeaderChangeTestCase(NeedleTestCase):
    browser_name = os.environ.get("BROWSER", "chrome")
    engine_class = "needle.engines.imagemagick_engine.Engine"
    viewport_width = os.environ.get("WIDTH", 1600)
    viewport_height = os.environ.get("HEIGHT", 4000)

    @classmethod
    def get_web_driver(cls):
        return get_needle_web_driver(cls.browser_name)

    @classmethod
    def teardown_class(cls):
        print("post test class teardown")


@generate(assert_footer_did_not_change, *URLS)
class DidFooterChangeTestCase(NeedleTestCase):
    browser_name = os.environ.get("BROWSER", "chrome")
    engine_class = "needle.engines.imagemagick_engine.Engine"
    viewport_width = os.environ.get("WIDTH", 1600)
    viewport_height = os.environ.get("HEIGHT", 4000)

    @classmethod
    def get_web_driver(cls):
        return get_needle_web_driver(cls.browser_name)

    @classmethod
    def teardown_class(cls):
        print("post test class teardown")
