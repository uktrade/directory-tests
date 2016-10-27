from locust import HttpLocust, TaskSet, task

import settings


class PublicPages(TaskSet):
    @task
    def landing_page(self):
        self.client.get("")

    @task
    def start_registration(self):
        self.client.get("register")

    @task
    def sorry_page(self):
        self.client.get("sorry")

    @task
    def terms_conditions(self):
        self.client.get("terms_and_conditions")

    @task
    def confirm_email(self):
        # This checks only the case when an invalid code is given
        self.client.get("confirm-email?confirmation_code=code")


class RegularUser(HttpLocust):
    task_set = PublicPages
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
