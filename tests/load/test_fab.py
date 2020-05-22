# -*- coding: utf-8 -*-
from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth


class FABTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.FAB_LANDING.relative
        self.client.get(url, headers=LOAD_TESTS_USER_AGENT, auth=basic_auth())


class FAB(HttpUser):
    host = settings.FIND_A_BUYER_URL
    tasks = [FABTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
