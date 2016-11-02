from __future__ import absolute_import

from tests import get_relative_url, settings

from locust import HttpLocust, TaskSet, task


class PublicPagesAPI(TaskSet):

    @task
    def health(self):
        self.client.get(get_relative_url('api:health'))

    @task
    def docs(self):
        self.client.get(get_relative_url('api:docs'))


class AuthenticatedPagesAPI(TaskSet):
    @task
    def enrolment(self):
        self.client.get(get_relative_url('api:enrolment'))

    @task
    def sms_verify(self):
        self.client.get(get_relative_url('api:sms-verify'))

    @task
    def confirm_company_email(self):
        self.client.post(get_relative_url('api:confirm-company-email'))

    @task
    def validate_company_number(self):
        self.client.get(get_relative_url('api:validate-company-number'))

    @task
    def companies_house_profile(self):
        self.client.get(get_relative_url('api:companies-house-profile'))


class RegularUserAPI(HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = PublicPagesAPI
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1


class AuthenticatedUserAPI(HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = AuthenticatedPagesAPI
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1
