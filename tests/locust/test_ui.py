from __future__ import absolute_import

from tests import get_relative_url, settings

from locust import HttpLocust, TaskSet, task


class PublicPagesBuyerUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-buyer:landing'))

    @task
    def start_registration(self):
        self.client.get(get_relative_url('ui-buyer:register'))


class AuthPagesBuyerUI(TaskSet):
    def on_start(self):
        data = {
            "login": 'load_tests@example.com',
            "password": 'passwordpassword'
        }
        login_url = settings.DIRECTORY_SSO_URL + get_relative_url('sso:login')
        response = self.client.post(login_url, data=data)
        self.cookie = response.history[0].headers['Set-Cookie']

    @task
    def company_profile(self):
        response = self.client.get(
            get_relative_url('ui-buyer:company-profile'),
            headers={'Cookie': self.cookie}
        )


class RegularUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_BUYER_UI_URL
    task_set = PublicPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 2


class AuthUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_BUYER_UI_URL
    task_set = AuthPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 2


class PublicPagesSupplierUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-supplier:landing'))

    @task
    def suppliers(self):
        self.client.get(get_relative_url('ui-supplier:suppliers'))

    @task
    def suppliers_detail(self):
        self.client.get(get_relative_url('ui-supplier:suppliers-detail'))

    @task
    def sectors(self):
        self.client.get(get_relative_url('ui-supplier:sectors'))

    @task
    def sectors_health(self):
        self.client.get(get_relative_url('ui-supplier:sectors-health'))

    @task
    def sectors_tech(self):
        self.client.get(get_relative_url('ui-supplier:sectors-tech'))

    @task
    def sectors_creative(self):
        self.client.get(get_relative_url('ui-supplier:sectors-creative'))

    @task
    def sectors_food(self):
        self.client.get(get_relative_url('ui-supplier:sectors-food'))

    @task
    def case_study(self):
        self.client.get(get_relative_url('ui-supplier:case-study'))


class RegularUserSupplierUI(HttpLocust):
    host = settings.DIRECTORY_SUPPLIER_UI_URL
    task_set = PublicPagesSupplierUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
    weight = 2
