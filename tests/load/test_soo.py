import random

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load import USER_AGENT, basic_auth
from tests.load.utils import random_product_categories, random_operating_countries


class SOOTasks(TaskSet):
    @task
    def home_page(self):
        url = get_relative_url("ui-soo:landing")
        self.client.get(
            url,
            headers=USER_AGENT,
            auth=basic_auth()
        )

    @task
    def search(self):
        url = get_relative_url("ui-soo:search-results")

        params = {
            "product_categories": random_product_categories(),
            "operating_countries": random_operating_countries()
        }

        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="/?product_categories=[...]&operating_countries=[...]",
            auth=basic_auth()
       )

    @task
    def marketplace(self):
        urls = [
            "markets/details/etsy/",
            "markets/details/ebay/",
            "markets/details/fruugo/",
            "markets/details/westwing/",
            "markets/details/linio/",
            "markets/details/otto/",
            "markets/details/allegro/",
            "markets/details/la-redoute/",
            "markets/details/kaola/",
            "markets/details/ctrip/"
        ]

        self.client.get(
            random.choice(urls),
            headers=USER_AGENT,
            name="/markets/details/[marketplace]",
            auth=basic_auth()
        )


class SOO(HttpLocust):
    host = settings.SOO_UI_URL
    task_set = SOOTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT

