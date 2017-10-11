# -*- coding: utf-8 -*-
"""VisualDiff Tests"""
import os

from needle.cases import NeedleTestCase

from tests.ui.drivers import get_needle_web_driver

URL_MAP = {
    "production": {
        "export_opportunities": "https://opportunities.export.great.gov.uk/",
        "find_a_buyer": "https://find-a-buyer.export.great.gov.uk/",
        "get_finance": "https://www.export.great.gov.uk/get-finance/",
        "new_to_exporting": "https://www.export.great.gov.uk/new/",
        "occasional_exporter": "https://www.export.great.gov.uk/occasional/",
        "regular_exporter": "https://www.export.great.gov.uk/regular/",
        "selling_online_overseas": "https://selling-online-overseas.export.great.gov.uk/markets/",
        "events": "https://www.events.trade.gov.uk/"
    }
}

URLS = URL_MAP[os.environ.get("ENVIRONMENT", "production").lower()]


class DirectoryFooterHeaderTest(NeedleTestCase):

    browser_name = os.environ.get("BROWSER", "chrome")
    urls = URL_MAP[os.environ.get("ENVIRONMENT", "production").lower()]
    engine_class = "needle.engines.imagemagick_engine.Engine"
    viewport_width = os.environ.get("WIDTH", 1600)
    viewport_height = os.environ.get("HEIGHT", 4000)

    @classmethod
    def get_web_driver(cls):
        driver = get_needle_web_driver(cls.browser_name)
        driver.set_page_load_timeout(20)
        return driver

    def check_page_footer(self, page_name):
        self.driver.get(self.urls[page_name])
        self.driver.implicitly_wait(10)
        self.assertScreenshot(
            ".footer",
            "footer-{}-{}".format(self.browser_name, page_name))

    def check_page_header(self, page_name):
        self.driver.get(self.urls[page_name])
        self.driver.implicitly_wait(10)
        self.assertScreenshot(
            ".navigation",
            "header-{}-{}".format(self.browser_name, page_name))

    def footer_export_opportunities_test(self):
        self.check_page_footer("export_opportunities")

    def footer_find_a_buyer_test(self):
        self.check_page_footer("find_a_buyer")

    def footer_get_finance_test(self):
        self.check_page_footer("get_finance")

    def footer_new_to_exporting_test(self):
        self.check_page_footer("new_to_exporting")

    def footer_occasional_exporter_test(self):
        self.check_page_footer("occasional_exporter")

    def footer_regular_exporter_test(self):
        self.check_page_footer("regular_exporter")

    def footer_selling_online_overseas_test(self):
        self.check_page_footer("selling_online_overseas")

    def header_export_opportunities_test(self):
        self.check_page_header("export_opportunities")

    def header_find_a_buyer_test(self):
        self.check_page_header("find_a_buyer")

    def header_get_finance_test(self):
        self.check_page_header("get_finance")

    def header_new_to_exporting_test(self):
        self.check_page_header("new_to_exporting")

    def header_occasional_exporter_test(self):
        self.check_page_header("occasional_exporter")

    def header_regular_exporter_test(self):
        self.check_page_header("regular_exporter")

    def header_selling_online_overseas_test(self):
        self.check_page_header("selling_online_overseas")
