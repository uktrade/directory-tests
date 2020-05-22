# -*- coding: utf-8 -*-
from random import choice

from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth


class InvestTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.INVEST_LANDING.relative
        self.client.get(url, headers=LOAD_TESTS_USER_AGENT, name="/", auth=basic_auth())

    @task
    def contact(self):
        self.client.get(
            URLs.INVEST_CONTACT.absolute,
            headers=LOAD_TESTS_USER_AGENT,
            name="/contact/",
            auth=basic_auth(),
        )

    @task
    def hpo(self):
        hpo_urls = [
            URLs.INVEST_HPO_FOOD.absolute,
            URLs.INVEST_HPO_LIGHTWEIGHT.absolute,
            URLs.INVEST_HPO_RAIL.absolute,
            URLs.INVEST_HPO_CONTACT.absolute,
        ]
        self.client.get(
            choice(hpo_urls),
            headers=LOAD_TESTS_USER_AGENT,
            name="/high-potential-opportunities/[hpo]/",
            auth=basic_auth(),
        )


class Invest(HttpUser):
    host = settings.INVEST_URL
    tasks = [InvestTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
