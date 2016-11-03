from __future__ import absolute_import

import json

from locust import HttpLocust, TaskSet, task

from tests import get_random_email_address, get_relative_url, settings
from tests.locust.helpers import AuthedClientMixin


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

    @task
    def enrolment(self):
        data = {
            'export_status': 'ONE_TWO_YEARS_AGO',
            'name': 'Examlple corp',
            'number': '09466013',
            'sso_id': 2,
            'company_email': get_random_email_address(),
            'mobile_number': '07700900418',
            'referrer': 'email'
        }
        headers = {'content-type': 'application/json'}
        self.client.post(
            get_relative_url('api:enrolment'),
            data=json.dumps(data),
            headers=headers
        )


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
