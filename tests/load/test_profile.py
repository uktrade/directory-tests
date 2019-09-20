# -*- coding: utf-8 -*-
import random

from directory_tests_shared import URLs, settings
from directory_tests_shared.utils import basic_auth
from locust import HttpLocust, TaskSet, task
from tests.load.utils import USER_AGENT, random_company_number, rare_word


class ProfileTasks(TaskSet):
    @task
    def companies_house_search_by_term(self):
        url = URLs.PROFILE_API_COMPANIES_HOUSE_SEARCH.relative
        params = {
            "term": random.choice([random_company_number(), rare_word()])
        }
        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name=URLs.PROFILE_API_COMPANIES_HOUSE_SEARCH.template,
            auth=basic_auth(),
        )


class Profile(HttpLocust):
    host = settings.PROFILE_URL
    task_set = ProfileTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
