from locust import HttpLocust, TaskSet, task
from directory_tests_shared import settings, URLs
from tests.load import USER_AGENT, basic_auth


class FABTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.FAB_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            auth=basic_auth(),
        )


class FAB(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = FABTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
