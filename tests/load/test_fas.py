import random

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load.utils import rare_word, random_sector


class FASTasks(TaskSet):
    @task
    def home_page(self):
        url = get_relative_url("ui-supplier:landing")
        self.client.get(url)

    @task
    def search(self):
        url = get_relative_url("ui-supplier:search")
        params = {
            "term": rare_word(),
            "sectors": random_sector(),
        }
        self.client.get(
            url,
            params=params,
            name="/search/?term=[term]&sectors=[sectors]",
        )

    @task
    def blank_search(self):
        url = get_relative_url("ui-supplier:search")
        params = {
            "term": "",
            "sectors": "",
        }
        self.client.get(
            url,
            params=params,
        )

    @task
    def industries(self):
        url = get_relative_url("ui-supplier:industries")
        self.client.get(url)

    @task
    def industry_pages(self):
        urls = [
            "/industries/aerospace/",
            "/industries/agritech/",
            "/industries/consumer-retail/",
            "/industries/creative-services/",
            "/industries/cyber-security/",
            "/industries/food-and-drink/",
            "/industries/healthcare/",
            "/industries/legal-services/",
            "/industries/life-sciences/",
            "/industries/sports-economy/",
            "/industries/technology/",
        ]
        self.client.get(random.choice(urls), name="/industries/[industry]/")


class FAS(HttpLocust):
    host = settings.DIRECTORY_UI_SUPPLIER_URL
    task_set = FASTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
