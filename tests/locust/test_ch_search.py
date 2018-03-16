import os
import random

from locust import HttpLocust, TaskSet, task

from tests import get_relative_url, settings


TEST_FILES_DIR = os.path.abspath(os.path.join("tests", "functional", "files"))
with open(os.path.join(TEST_FILES_DIR, "rare.txt"), "r") as f:
    RARE_WORDS = f.read().split()


class RegularUserBuyerUI(TaskSet):

    @task(1)
    def ch_search(self):
        params = {'term': random.choice(RARE_WORDS)}
        self.client.get(
                get_relative_url('api:companies-house-search'), params=params,
                name='/api/internal/companies-house-search/'
        )


class RegularUserCHSearch(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = RegularUserBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
