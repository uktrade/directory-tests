# -*- coding: utf-8 -*-
from locust import HttpLocust, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth, rare_word


class SearchTasks(TaskSet):
    @task
    def search(self):
        url = URLs.DOMESTIC_SEARCH.relative
        params = {"q": rare_word()}

        self.client.get(
            url,
            params=params,
            headers=LOAD_TESTS_USER_AGENT,
            name="search/?q=[...]",
            auth=basic_auth(),
        )


class Search(HttpLocust):
    host = settings.DOMESTIC_URL
    task_set = SearchTasks
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
