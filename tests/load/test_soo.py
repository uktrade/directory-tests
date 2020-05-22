# -*- coding: utf-8 -*-
import random

from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import (
    basic_auth,
    random_operating_countries,
    random_product_categories,
)


class SOOTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.SOO_LANDING.relative
        self.client.get(url, headers=LOAD_TESTS_USER_AGENT, auth=basic_auth())

    @task
    def search(self):
        url = URLs.SOO_SEARCH_RESULTS.relative

        params = {
            "category_id": random_product_categories(),
            "country_id": random_operating_countries(),
            "commit": "Find+a+marketplace",
        }

        self.client.get(
            url,
            params=params,
            headers=LOAD_TESTS_USER_AGENT,
            name="/?category_id=[...]&country_id=[...]",
            auth=basic_auth(),
        )

    @task
    def marketplace(self):
        urls = [
            # URLs.SOO_MARKET_DETAILS.template.format(market="allegro"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="amazon-china"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="amazon-india"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="ctrip"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="dafiti"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="etsy"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="lamoda"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="mercado-libre"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="otto"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="sfbest"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="shangpin"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="the-iconic"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="tmall-global"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="westwing"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="xiu"),
            # URLs.SOO_MARKET_DETAILS.template.format(market="zalora"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-france"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-germany"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-italy"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-japan"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-mexico"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-spain"),
            URLs.SOO_MARKET_DETAILS.template.format(market="amazon-usa"),
            URLs.SOO_MARKET_DETAILS.template.format(market="cdiscount"),
            URLs.SOO_MARKET_DETAILS.template.format(market="ebay"),
            URLs.SOO_MARKET_DETAILS.template.format(market="flipkart"),
            URLs.SOO_MARKET_DETAILS.template.format(market="fruugo"),
            URLs.SOO_MARKET_DETAILS.template.format(market="goxip"),
            URLs.SOO_MARKET_DETAILS.template.format(market="jd-worldwide"),
            URLs.SOO_MARKET_DETAILS.template.format(market="kaola"),
            URLs.SOO_MARKET_DETAILS.template.format(market="la-redoute"),
            URLs.SOO_MARKET_DETAILS.template.format(market="linio"),
            URLs.SOO_MARKET_DETAILS.template.format(market="newegg-business"),
            URLs.SOO_MARKET_DETAILS.template.format(market="newegg-canada"),
            URLs.SOO_MARKET_DETAILS.template.format(market="newegg-inc"),
            URLs.SOO_MARKET_DETAILS.template.format(market="privalia"),
            URLs.SOO_MARKET_DETAILS.template.format(market="rakuten"),
            URLs.SOO_MARKET_DETAILS.template.format(market="royal-mail-t-mall"),
            URLs.SOO_MARKET_DETAILS.template.format(market="spartoo"),
            URLs.SOO_MARKET_DETAILS.template.format(market="trademe"),
            URLs.SOO_MARKET_DETAILS.template.format(market="tthigo"),
        ]

        self.client.get(
            random.choice(urls),
            headers=LOAD_TESTS_USER_AGENT,
            name="/markets/details/[marketplace]",
            auth=basic_auth(),
        )


class SOO(HttpUser):
    host = settings.SOO_URL
    tasks = [SOOTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
