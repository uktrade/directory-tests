import json

from locust import HttpLocust, TaskSet, task

from tests import (
    get_random_email_address,
    get_relative_url,
    settings
)
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


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
    def healthcheck_database(self):
        params = {'token': TOKEN}
        self.client.get(
            get_relative_url('sso-api:healthcheck-database'), 
            params=params,
            name="/healthcheck/database/?token=[token]"
        )

    @task
    def email_confirm_GET(self):
        self.client.get(get_relative_url('sso:email_confirm'))

    @task
    def inactive(self):
        # This checks only that redirection occurs
        self.client.get(get_relative_url('sso:inactive'))

    @task
    def logout(self):
        # This checks only that redirection occurs
        self.client.get(get_relative_url('sso:logout'))

    @task
    def password_change(self):
        # This checks only that redirection occurs
        self.client.get(get_relative_url('sso:password_change'))

    @task
    def password_set(self):
        # This checks only that redirection occurs
        self.client.get(get_relative_url('sso:password_set'))

    @task
    def password_reset(self):
        # This checks only that redirection occurs
        self.client.get(get_relative_url('sso:password_reset'))


class RegularUserSSO(HttpLocust):
    host = settings.DIRECTORY_SSO_URL
    task_set = PublicPagesSSO
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
