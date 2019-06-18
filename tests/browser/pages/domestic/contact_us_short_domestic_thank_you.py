# -*- coding: utf-8 -*-
"""Export Readiness - Short Domestic Contact us - Thank you for your enquiry."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, check_url, take_screenshot
from settings import EXRED_UI_URL

NAME = "Thank you for your enquiry"
NAMES = [
    "Thank you for your enquiry",
    "Thank you for your enquiry (Events)",
    "Thank you for your enquiry (Defence and Security Organisation (DSO))",
    "Thank you for your enquiry (Other)",
    "Thank you for your enquiry (I haven't had a response from the opportunity I applied for)",
    "Thank you for your enquiry (My daily alerts are not relevant to me)",
    "Thank you for your enquiry (I have not received an email confirmation)",
    "Thank you for your enquiry (I need to reset my password)",
    "Thank you for your enquiry (My Companies House login is not working)",
    "Thank you for your enquiry (I do not know where to enter my verification code)",
    "Thank you for your enquiry (I have not received my letter containing the verification code)",
    "Thank you for your enquiry (I have not received a verification code)",
]
SERVICE = "Export Readiness"
TYPE = "Short Domestic Contact us"
URL = urljoin(EXRED_UI_URL, "contact/domestic/success/")
PAGE_TITLE = "Welcome to great.gov.uk"

PDF_LINKS = Selector(By.CSS_SELECTOR, "#documents-section a.link")
SELECTORS = {
    "confirmation": {
        "itself": Selector(By.ID, "confirmation-section"),
        "heading": Selector(
            By.CSS_SELECTOR, "#confirmation-section div.heading-container"
        ),
    },
    "what happens next": {
        "itself": Selector(By.ID, "next-container"),
        "heading": Selector(By.CSS_SELECTOR, "#next-container h2"),
        "text": Selector(By.CSS_SELECTOR, "#next-container p"),
        "continue to great.gov.uk": Selector(By.CSS_SELECTOR, "#next-container a"),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
}

URLs = {
    "thank you for your enquiry": URL,
    "thank you for your enquiry (events)": urljoin(URL, "/contact/events/success/"),
    "thank you for your enquiry (defence and security organisation (dso))": urljoin(
        URL, "/contact/defence-and-security-organisation/success/"
    ),
    "thank you for your enquiry (other)": URL,
    "thank you for your enquiry (i haven't had a response from the opportunity i applied for)": URL,
    "thank you for your enquiry (my daily alerts are not relevant to me)": URL,
    "thank you for your enquiry (i have not received an email confirmation)": URL,
    "thank you for your enquiry (i need to reset my password)": URL,
    "thank you for your enquiry (my companies house login is not working)": URL,
    "thank you for your enquiry (i do not know where to enter my verification code)": URL,
    "thank you for your enquiry (i have not received my letter containing the verification code)": URL,
    "thank you for your enquiry (i have not received a verification code)": URL,
}


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=True)
