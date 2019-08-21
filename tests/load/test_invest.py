from random import choice

from locust import HttpLocust, TaskSet, task
from tests import settings, URLs
from tests.load import USER_AGENT, basic_auth


class InvestTasks(TaskSet):

    @task
    def home_page(self):
        url = URLs.INVEST_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            name="/",
            auth=basic_auth(),
        )

    @task
    def contact(self):
        self.client.get(
            URLs.INVEST_CONTACT.absolute,
            headers=USER_AGENT,
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
            headers=USER_AGENT,
            name="/high-potential-opportunities/[hpo]/",
            auth=basic_auth(),
        )


class Invest(HttpLocust):
    host = settings.INVEST_UI_URL
    task_set = InvestTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
