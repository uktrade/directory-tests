from __future__ import absolute_import

from tests import get_relative_url, get_absolute_url, settings

from locust import HttpLocust, TaskSet, task


class PublicPagesBuyerUI(TaskSet):
    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-buyer:landing'))

    @task
    def start_registration(self):
        self.client.get(get_relative_url('ui-buyer:register'))


class AuthenticatedPagesBuyerUI(TaskSet):
    def on_start(self):
        data = {
            "login": 'load_tests@example.com',
            "password": 'passwordpassword'
        }
        login_url = get_absolute_url('sso:login')
        response = self.client.post(login_url, data=data)
        self.cookie = response.history[0].headers['Set-Cookie']

    @task
    def company_profile(self):
        response = self.client.get(
            get_relative_url('ui-buyer:company-profile'),
            headers={'Cookie': self.cookie}
        )


class RegularUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = PublicPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


class AuthenticatedUserBuyerUI(HttpLocust):
    host = settings.DIRECTORY_UI_BUYER_URL
    task_set = AuthenticatedPagesBuyerUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT


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
    host = settings.DIRECTORY_UI_SUPPLIER_URL
    task_set = PublicPagesSupplierUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
