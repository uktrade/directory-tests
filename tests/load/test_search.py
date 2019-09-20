# -*- coding: utf-8 -*-
from directory_tests_shared import URLs, settings
from directory_tests_shared.utils import basic_auth
from locust import HttpLocust, TaskSet, task
from tests.load.utils import USER_AGENT, rare_word


class SearchTasks(TaskSet):
    @task
    def search(self):
        url = URLs.DOMESTIC_SEARCH.relative
        params = {"q": rare_word()}

        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="search/?q=[...]",
            auth=basic_auth(),
        )


class Search(HttpLocust):
    host = settings.EXRED_UI_URL
    task_set = SearchTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
