import random

from locust import HttpLocust, TaskSet, task
from tests import settings, URLs
from tests.load import USER_AGENT, basic_auth
from tests.load.utils import rare_word, random_sector


class FASTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.FAS_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            auth=basic_auth(),
        )

    @task
    def search(self):
        url = URLs.FAS_SEARCH.relative
        params = {
            "term": rare_word(),
            "sectors": random_sector(),
        }
        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="/search/?term=[term]&sectors=[sectors]",
            auth=basic_auth(),
        )

    @task
    def industry_pages(self):
        urls = [
            "industries/",
            "industries/aerospace/",
            "industries/agritech/",
            "industries/consumer-retail/",
            "industries/creative-services/",
            "industries/cyber-security/",
            "industries/food-and-drink/",
            "industries/healthcare/",
            "industries/legal-services/",
            "industries/life-sciences/",
            "industries/sports-economy/",
            "industries/technology/",
        ]
        self.client.get(
            random.choice(urls),
            headers=USER_AGENT,
            name="/industries/[industry]/",
            auth=basic_auth(),
        )


class FAS(HttpLocust):
    host = settings.DIRECTORY_UI_SUPPLIER_URL
    task_set = FASTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
