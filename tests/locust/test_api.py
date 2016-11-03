from __future__ import absolute_import

from tests import get_relative_url, settings
from tests.locust.helpers import AuthedClientMixin

from locust import HttpLocust, TaskSet, task


class PublicPagesAPI(TaskSet):

    @task
    def health(self):
        self.client.get(get_relative_url('api:health'))


class AuthenticatedPagesAPI(TaskSet):

    @task
    def docs(self):
        self.client.get(get_relative_url('api:docs'))

    @task
    def validate_company_number(self):
        url = get_relative_url('api:validate-company-number')
        self.client.get('{url}?number=09466013'.format(url=url))

    @task
    def companies_house_profile(self):
        url = get_relative_url('api:companies-house-profile')
        self.client.get('{url}?number=09466011'.format(url=url))


class RegularUserAPI(HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = PublicPagesAPI
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1


class AuthenticatedUserAPI(AuthedClientMixin, HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = AuthenticatedPagesAPI
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 1
