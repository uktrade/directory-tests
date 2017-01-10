from __future__ import absolute_import

import json
from datetime import datetime

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
    def get_company(self):
        url = get_relative_url('api:company').format(
            sso_id=settings.SSO_USER_ID)
        self.client.get(url)

    @task
    def put_company(self):
        url = get_relative_url('api:company').format(
            sso_id=settings.SSO_USER_ID)
        data = {
            'export_status': 'YES',
            'name': 'Test Company',
            'number': '04296006',
        }  # just required fields here
        headers = {'content-type': 'application/json'}
        self.client.put(url, data=json.dumps(data), headers=headers)

    @task
    def patch_company(self):
        url = get_relative_url('api:company').format(
            sso_id=settings.SSO_USER_ID)
        data = {
            'export_status': 'YES',
            'name': 'Test Company',
            'number': '04296006',
        }  # just required fields here
        headers = {'content-type': 'application/json'}
        self.client.patch(url, data=json.dumps(data), headers=headers)

    @task
    def get_user(self):
        url = get_relative_url('api:user').format(sso_id=settings.SSO_USER_ID)
        self.client.get(url)

    @task
    def put_user(self):
        url = get_relative_url('api:user').format(sso_id=settings.SSO_USER_ID)
        data = {
            'sso_id': settings.SSO_USER_ID,
            'company_email': get_random_email_address(),
            'mobile_number': '0800888777',
            'referrer': 'google',
            'terms_agreed': True,
            'date_joined': str(datetime.now()),
        }
        headers = {'content-type': 'application/json'}
        self.client.put(url, data=json.dumps(data), headers=headers)

    @task
    def patch_user(self):
        url = get_relative_url('api:user').format(sso_id=settings.SSO_USER_ID)
        data = {
            'sso_id': settings.SSO_USER_ID,
            'company_email': get_random_email_address(),
            'mobile_number': '0800888777',
            'referrer': 'google',
            'terms_agreed': True,
            'date_joined': str(datetime.now()),
        }
        headers = {'content-type': 'application/json'}
        self.client.patch(url, data=json.dumps(data), headers=headers)

    @task
    def enrolment(self):
        data = {
            'export_status': 'ONE_TWO_YEARS_AGO',
            'name': 'Example corp',
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

    @task
    def test_sms_verify_invalid_data(self):
        url = get_relative_url('api:sms-verify')
        headers = {'content-type': 'application/json'}
        data = json.dumps({'phone_number': 'a' * 50})  # invalid phone number
        with self.client.post(url, data=data, headers=headers,
                              catch_response=True) as response:
            if response.status_code == 400:
                response.success()
            else:
                response.failure("Expected 400 status for invalid data")

    @task
    def test_confirm_company_email_invalid_data(self):
        url = get_relative_url('api:confirm-company-email')
        headers = {'content-type': 'application/json'}
        data = json.dumps({'confirmation_code': 'invalid'})
        with self.client.post(url, data=data, headers=headers,
                              catch_response=True) as response:
            if response.status_code == 400:
                response.success()
            else:
                response.failure("Expected 400 status for invalid data")


class RegularUserAPI(HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = PublicPagesAPI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


class AuthenticatedUserAPI(AuthedClientMixin, HttpLocust):
    host = settings.DIRECTORY_API_URL
    task_set = AuthenticatedPagesAPI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
