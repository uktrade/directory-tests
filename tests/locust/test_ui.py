from __future__ import absolute_import

from tests import get_relative_url, settings

from locust import HttpLocust, TaskSet, task


class PublicPagesUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui:landing'))

    @task
    def start_registration(self):
        self.client.get(get_relative_url('ui:register'))

    @task
    def sorry_page(self):
        self.client.get(get_relative_url('ui:sorry'))

    @task
    def confirm_company_email(self):
        # This checks only the case when an invalid code is given
        self.client.get(get_relative_url('ui:confirm_email'))


class RegularUserUI(HttpLocust):
    host = settings.DIRECTORY_UI_URL
    task_set = PublicPagesUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 2
