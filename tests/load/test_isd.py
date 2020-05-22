# -*- coding: utf-8 -*-
import random

from locust import HttpUser, TaskSet, between, task

from directory_constants.expertise import (
    BUSINESS_SUPPORT,
    FINANCIAL,
    HUMAN_RESOURCES,
    LEGAL,
    MANAGEMENT_CONSULTING,
    PUBLICITY,
)
from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth, rare_word


class ISDTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.ISD_LANDING.relative
        self.client.get(url, headers=LOAD_TESTS_USER_AGENT, auth=basic_auth())

    @task
    def search_by_term(self):
        url = URLs.ISD_SEARCH.relative
        params = {"q": rare_word()}
        self.client.get(
            url,
            params=params,
            headers=LOAD_TESTS_USER_AGENT,
            name="/search/?q={term}",
            auth=basic_auth(),
        )

    @task
    def filtered_search(self):
        filters = {
            "expertise_products_services_financial": FINANCIAL,
            "expertise_products_services_management": MANAGEMENT_CONSULTING,
            "expertise_products_services_human_resources": [
                item.replace(" ", "-") for item in HUMAN_RESOURCES
            ],
            "expertise_products_services_legal": LEGAL,
            "expertise_products_services_publicity": PUBLICITY,
            "expertise_products_services_business_support": BUSINESS_SUPPORT,
        }
        keys = random.choices(
            list(filters.keys()), k=random.randint(1, len(list(filters.keys())))
        )
        random_filters = {
            key: set(
                random.choices(filters[key], k=random.randint(1, len(filters[key])))
            )
            for key in keys
        }
        query = "&".join(
            f"{key}={value}" for key in random_filters for value in random_filters[key]
        )
        url = f"{URLs.ISD_SEARCH.absolute}?{query}"
        self.client.get(
            url=url,
            headers=LOAD_TESTS_USER_AGENT,
            name="/search/{filters}/",
            auth=basic_auth(),
        )


class ISD(HttpUser):
    host = settings.ISD_URL
    tasks = [ISDTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
