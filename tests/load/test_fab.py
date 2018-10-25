import random

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load.utils import random_company_number, rare_word


class FABTasks(TaskSet):
    @task
    def home_page(self):
        url = get_relative_url("ui-buyer:landing")
        self.client.get(url)

    @task
    def get_promoted(self):
        url = get_relative_url("ui-buyer:landing")
        params = {
            "company_name": rare_word(),
            "company_number": random_company_number(),
        }
        self.client.post(
            url,
            params=params,
            name="/?company_name=[name]&company_number=[number]",
        )

    @task
    def companies_house_search_by_term(self):
        url = get_relative_url("internal-api:companies-house-search")
        params = {
            "term": random.choice([random_company_number(), rare_word()])
        }
        self.client.get(
            url,
            params=params,
            name="api/internal/companies-house-search/?term=[term]",
        )


class FAB(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = FABTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
