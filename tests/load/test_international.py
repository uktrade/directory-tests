# -*- coding: utf-8 -*-
from random import choice

from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth


class InternationalTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.INTERNATIONAL_LANDING.relative
        self.client.get(url, headers=LOAD_TESTS_USER_AGENT, name="/", auth=basic_auth())

    @task
    def misc_pages(self):
        urls = [
            URLs.INTERNATIONAL_CAPITAL_INVEST.relative,
            URLs.INTERNATIONAL_CONTACT_US.relative,
            URLs.CONTACT_US_INTERNATIONAL_BREXIT_CONTACT.relative,
        ]
        self.client.get(
            choice(urls),
            headers=LOAD_TESTS_USER_AGENT,
            name="misc pages",
            auth=basic_auth(),
        )

    @task
    def uk_setup_guides_pages(self):
        endpoints = [
            URLs.INVEST_UK_SETUP_GUIDE.relative,
            URLs.INVEST_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT.relative,
            URLs.INVEST_UK_SETUP_GUIDE_ACCESS_FINANCE.relative,
            URLs.INVEST_UK_SETUP_GUIDE_UK_TAX.relative,
        ]
        self.client.get(
            choice(endpoints).replace("/invest/", "/"),
            headers=LOAD_TESTS_USER_AGENT,
            name=URLs.INVEST_UK_SETUP_GUIDE.template,
            auth=basic_auth(),
        )

    @task
    def industry_pages(self):
        industries = [
            "creative-industries/",
            "engineering-and-manufacturing/",
            "financial-and-professional-services/",
            "financial-services/",
            "legal-services/",
            "technology/",
        ]
        urls = [
            URLs.INTERNATIONAL_INDUSTRIES_STAGING.relative,
            URLs.INTERNATIONAL_INDUSTRIES_STAGING.template.format(
                industry=choice(industries)
            ),
        ]
        self.client.get(
            choice(urls),
            headers=LOAD_TESTS_USER_AGENT,
            name=URLs.INTERNATIONAL_INDUSTRIES_STAGING.template,
            auth=basic_auth(),
        )


class International(HttpUser):
    host = settings.INTERNATIONAL_URL
    tasks = [InternationalTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
