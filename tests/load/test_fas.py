import random

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load import USER_AGENT
from tests.load.utils import rare_word, random_sector


class FASTasks(TaskSet):
    @task
    def home_page(self):
        url = get_relative_url("ui-supplier:landing")
        self.client.get(
            url,
            headers=USER_AGENT,
        )

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
            headers=USER_AGENT,
            name="/search/?term=[term]&sectors=[sectors]",
        )

    @task
    def industry_pages(self):
        urls = [
            "/industries/",
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
        self.client.get(
            random.choice(urls),
            headers=USER_AGENT,
            name="/industries/[industry]/",
        )


class FAS(HttpLocust):
    host = settings.DIRECTORY_UI_SUPPLIER_URL
    task_set = FASTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
