import random

from locust import HttpLocust, TaskSet, task

from directory_constants.expertise import (
    FINANCIAL,
    MANAGEMENT_CONSULTING,
    HUMAN_RESOURCES,
    LEGAL,
    PUBLICITY,
    BUSINESS_SUPPORT,
)

from tests import settings, URLs
from tests.load import USER_AGENT, basic_auth
from tests.load.utils import rare_word


class ISDTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.ISD_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            auth=basic_auth(),
        )

    @task
    def search_by_term(self):
        url = URLs.ISD_SEARCH.relative
        params = {
            "q": rare_word(),
        }
        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="/search/?q={term}",
            auth=basic_auth(),
        )

    @task
    def filtered_search(self):
        filters = {
            "expertise_products_services_financial": FINANCIAL,
            "expertise_products_services_management": MANAGEMENT_CONSULTING,
            "expertise_products_services_human_resources": [
                item.replace(" ", "-")
                for item in HUMAN_RESOURCES
            ],
            "expertise_products_services_legal": LEGAL,
            "expertise_products_services_publicity": PUBLICITY,
            "expertise_products_services_business_support": BUSINESS_SUPPORT,
        }
        keys = random.choices(
            list(filters.keys()),
            k=random.randint(1, len(list(filters.keys())))
        )
        random_filters = {
            key: set(
                random.choices(
                    filters[key],
                    k=random.randint(1, len(filters[key]))
                )
            )
            for key in keys
        }
        query = "&".join(
            f"{key}={value}"
            for key in random_filters
            for value in random_filters[key]
        )
        url = f"{URLs.ISD_SEARCH.absolute}?{query}"
        self.client.get(
            url=url,
            headers=USER_AGENT,
            name="/search/{filters}/",
            auth=basic_auth(),
        )


class ISD(HttpLocust):
    host = settings.ISD_UI_URL
    task_set = ISDTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
