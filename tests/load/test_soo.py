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
            "category_id": random_product_categories(),
            "country_id": random_operating_countries(),
            "commit": "Find+a+marketplace",
        }

        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="/?category_id=[...]&country_id=[...]",
            auth=basic_auth()
       )

    @task
    def marketplace(self):
        urls = [
            "markets/details/allegro/",
            "markets/details/amazon-china/",
            "markets/details/amazon-france/",
            "markets/details/amazon-germany/",
            "markets/details/amazon-india/",
            "markets/details/amazon-italy/",
            "markets/details/amazon-japan/",
            "markets/details/amazon-mexico/",
            "markets/details/amazon-spain/",
            "markets/details/amazon-usa/",
            "markets/details/cdiscount/",
            "markets/details/ctrip/",
            "markets/details/dafiti/",
            "markets/details/ebay/",
            "markets/details/etsy/",
            "markets/details/flipkart/",
            "markets/details/fruugo/",
            "markets/details/goxip/",
            "markets/details/jd-worldwide/",
            "markets/details/kaola/",
            "markets/details/la-redoute/",
            "markets/details/lamoda/",
            "markets/details/linio/",
            "markets/details/mercado-libre/",
            "markets/details/newegg-business/",
            "markets/details/newegg-canada/",
            "markets/details/newegg-inc/",
            "markets/details/otto/",
            "markets/details/privalia/",
            "markets/details/rakuten/",
            "markets/details/royal-mail-t-mall/",
            "markets/details/sfbest/",
            "markets/details/shangpin/",
            "markets/details/spartoo/",
            "markets/details/the-iconic/",
            "markets/details/tmall-global/",
            "markets/details/trademe/",
            "markets/details/tthigo/",
            "markets/details/westwing/",
            "markets/details/xiu/",
            "markets/details/zalora/",
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
