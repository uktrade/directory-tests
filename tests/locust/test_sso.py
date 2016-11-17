from __future__ import absolute_import

import json
from tests import (
    get_random_email_address,
    get_relative_url,
    settings
)
from locust import HttpLocust, TaskSet, task


class PublicPagesSSO(TaskSet):

    @task
    def login_GET(self):
        self.client.get(get_relative_url('sso:login'))

    @task
    def login_POST_unsuccessful(self):
        data = {
            'login': get_random_email_address(),
            'password': 'password',
        }
        self.client.post(
            url=get_relative_url('sso:login'),
            data=json.dumps(data),
            headers={'content-type': 'application/x-www-form-urlencoded'},
        )

    @task
    def signup_GET(self):
        self.client.get(get_relative_url('sso:signup'))

    @task
    def signup_POST_unsuccessful(self):
        data = {
            'email': get_random_email_address(),
            'password1': 'password',
            'password2': 'passwor',
        }
        self.client.post(
            url=get_relative_url('sso:signup'),
            data=json.dumps(data),
            headers={'content-type': 'application/x-www-form-urlencoded'},
        )

    @task
    def signup_POST_successful(self):
        data = {
            'email': get_random_email_address(),
            'password1': 'password',
            'password2': 'password',
        }
        self.client.post(
            url=get_relative_url('sso:signup'),
            data=json.dumps(data),
            headers={'content-type': 'application/x-www-form-urlencoded'},
        )

    @task
    def health(self):
        self.client.get(get_relative_url('sso:health'))

    @task
    def email_confirm_GET(self):
        self.client.get(get_relative_url('sso:email_confirm'))


class AuthenticatedPagesSSO(TaskSet):
    # This checks only the case that redirection occurs

    @task
    def inactive(self):
        self.client.get(get_relative_url('sso:inactive'))

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


class RegularUserSSO(HttpLocust):
    host = settings.DIRECTORY_SSO_URL
    task_set = PublicPagesSSO
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1


class AuthenticatedUserSSO(HttpLocust):
    host = settings.DIRECTORY_SSO_URL
    task_set = AuthenticatedPagesSSO
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1
