from __future__ import absolute_import

from tests import get_relative_url, settings

from locust import HttpLocust, TaskSet, task


class PublicPagesSSO(TaskSet):

    @task
    def login(self):
        self.client.get(get_relative_url('sso:login'))

    @task
    def signup(self):
        self.client.get(get_relative_url('sso:signup'))

    @task
    def health(self):
        self.client.get(get_relative_url('sso:health'))

    @task
    def email_confirm(self):
        self.client.get(get_relative_url('sso:email_confirm'))


class AuthenticatedPagesSSO(TaskSet):
    # This checks only the case that redirection occurs

    @task
    def logout(self):
        self.client.get(get_relative_url('sso:logout'))

    @task
    def password_change(self):
        self.client.get(get_relative_url('sso:password_change'))

    @task
    def password_set(self):
        self.client.get(get_relative_url('sso:password_set'))

    @task
    def password_reset(self):
        self.client.get(get_relative_url('sso:password_reset'))

    @task
    def email(self):
        self.client.get(get_relative_url('sso:email'))


class RegularUserSSO(HttpLocust):
    host = settings.DIRECTORY_SSO_URL
    task_set = PublicPagesSSO
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1


class AuthenticatedUserSSO(HttpLocust):
    host = settings.DIRECTORY_SSO_URL
    task_set = AuthenticatedPagesSSO
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1
