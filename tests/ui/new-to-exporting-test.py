from needle.cases import NeedleTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NewToExportingTest(NeedleTestCase):

    engine_class = 'needle.engines.perceptualdiff_engine.Engine'
    # viewport_width = 1024
    # viewport_height = 768
    save_baseline = True

    @classmethod
    def get_web_driver(cls):
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME)
        return driver

    def test_check_navigation_header(self):
        self.driver.set_page_load_timeout(20)
        self.driver.implicitly_wait(20)
        # self.driver.maximize_window()
        self.driver.get('https://www.export.great.gov.uk/new/')
        self.assertScreenshot('.navigation', 'navigation-header-capture')
