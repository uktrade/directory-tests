import random

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load import USER_AGENT, basic_auth


class SearchTasks(TaskSet):
    @task
    def search(self):
        url = get_relative_url("ui-domestic:search")
        params = {"q": "food"}

        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="search/?q=[...]",
            auth=basic_auth()
        )


class Search(HttpLocust):
    host = settings.EXRED_UI_URL
    task_set = SearchTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT