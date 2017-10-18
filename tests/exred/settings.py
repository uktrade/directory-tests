import os

from selenium.webdriver import Chrome, Firefox, PhantomJS, Remote

EXRED_UI_URL = os.environ["EXRED_UI_URL"]
HUB_URL = os.environ.get("HUB_URL", "http://localhost:4444/wd/hub")
BROWSER = os.environ.get("BROWSER", "chrome")
WIDTH = os.environ.get("WIDTH", 1600)
HEIGHT = os.environ.get("HEIGHT", 1200)

SCREENSHOTS_DIR = os.path.abspath(os.path.join(".", "screenshots"))
DRIVERS = (Remote, Chrome, Firefox, PhantomJS)

print("Will use Selenium Hub @ {} and ExRed @ {}".format(HUB_URL, EXRED_UI_URL))
