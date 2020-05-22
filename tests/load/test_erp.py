# -*- coding: utf-8 -*-
import random

from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth


class ERPTasks(TaskSet):

    erp_generic_get_urls = [
        URLs.ERP_LANDING.relative,
        URLs.ERP_SAVE_FOR_LATER.relative,
        URLs.ERP_TRIAGE_IMPORT_FROM_OVERSEAS.relative,
    ]

    erp_generic_post_urls = [URLs.ERP_TRIAGE_USER_TYPE.absolute]

    erp_business_urls = [
        URLs.ERP_BUSINESS_PRODUCT_SEARCH.absolute,
        URLs.ERP_BUSINESS_PRODUCT_DETAIL.absolute,
        URLs.ERP_BUSINESS_SALES_VOLUME_BEFORE_BREXIT.absolute,
        URLs.ERP_BUSINESS_SALES_REVENUE_BEFORE_BREXIT.absolute,
        URLs.ERP_BUSINESS_SALES_AFTER_BREXIT.absolute,
        URLs.ERP_BUSINESS_MARKET_SIZE_AFTER_BREXIT.absolute,
        URLs.ERP_BUSINESS_OTHER_CHANGES_AFTER_BREXIT.absolute,
        URLs.ERP_BUSINESS_MARKET_SIZE.absolute,
        URLs.ERP_BUSINESS_OTHER_INFORMATION.absolute,
        URLs.ERP_BUSINESS_OUTCOME.absolute,
        URLs.ERP_BUSINESS_BUSINESS_DETAILS.absolute,
        URLs.ERP_BUSINESS_PERSONAL_DETAILS.absolute,
        URLs.ERP_BUSINESS_SUMMARY.absolute,
        URLs.ERP_BUSINESS_FINISHED.absolute,
    ]

    erp_consumer_urls = [
        URLs.ERP_CONSUMER_PRODUCT_SEARCH.absolute,
        URLs.ERP_CONSUMER_PRODUCT_DETAIL.absolute,
        URLs.ERP_CONSUMER_CHANGE.absolute,
        URLs.ERP_CONSUMER_OTHER_CHANGES_AFTER_BREXIT.absolute,
        URLs.ERP_CONSUMER_OUTCOME.absolute,
        URLs.ERP_CONSUMER_TYPE.absolute,
        URLs.ERP_CONSUMER_GROUP_DETAILS.absolute,
        URLs.ERP_CONSUMER_PERSONAL.absolute,
        URLs.ERP_CONSUMER_SUMMARY.absolute,
        URLs.ERP_CONSUMER_FINISHED.absolute,
    ]

    erp_developing_country_urls = [
        URLs.ERP_DEVELOPING_COUNTRY.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_PRODUCT_SEARCH.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_PRODUCT_DETAIL.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_SALES_VOLUME_BEFORE_BREXIT.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_SALES_REVENUE_BEFORE_BREXIT.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_SALES_AFTER_BREXIT.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_MARKET_SIZE_AFTER_BREXIT.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_OTHER_CHANGES_AFTER_BREXIT.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_OUTCOME.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_BUSINESS_DETAILS.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_PERSONAL_DETAILS.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_SUMMARY.absolute,
        URLs.ERP_DEVELOPING_COUNTRY_FINISHED.absolute,
    ]

    erp_importer_urls = [
        URLs.ERP_IMPORTER_IMPORTED_PRODUCT_USAGE.absolute,
        URLs.ERP_IMPORTER_PRODUCT_SEARCH.absolute,
        URLs.ERP_IMPORTER_PRODUCT_DETAIL.absolute,
        URLs.ERP_IMPORTER_SALES_VOLUME_BEFORE_BREXIT.absolute,
        URLs.ERP_IMPORTER_SALES_REVENUE_BEFORE_BREXIT.absolute,
        URLs.ERP_IMPORTER_SALES_AFTER_BREXIT.absolute,
        URLs.ERP_IMPORTER_MARKET_SIZE_AFTER_BREXIT.absolute,
        URLs.ERP_IMPORTER_OTHER_CHANGES_AFTER_BREXIT.absolute,
        URLs.ERP_IMPORTER_PRODUCTION_PERCENTAGE.absolute,
        URLs.ERP_IMPORTER_WHICH_COUNTRIES.absolute,
        URLs.ERP_IMPORTER_EQUIVALENT_UK_GOODS.absolute,
        URLs.ERP_IMPORTER_MARKET_SIZE.absolute,
        URLs.ERP_IMPORTER_OTHER_INFORMATION.absolute,
        URLs.ERP_IMPORTER_OUTCOME.absolute,
        URLs.ERP_IMPORTER_BUSINESS_DETAILS.absolute,
        URLs.ERP_IMPORTER_PERSONAL_DETAILS.absolute,
        URLs.ERP_IMPORTER_SUMMARY.absolute,
        URLs.ERP_IMPORTER_FINISHED.absolute,
    ]

    @task
    def generic_get_pages(self):
        url = random.choice(self.erp_generic_get_urls)
        headers = {"erp_session_id": "invalid_cookie"}
        headers.update(LOAD_TESTS_USER_AGENT)
        self.client.get(url, headers=headers, name=f"generic", auth=basic_auth())

    @task
    def generic_post_pages(self):
        url = random.choice(self.erp_generic_post_urls)
        user_types = ["UK_BUSINESS", "UK_CONSUMER", "DEVELOPING_COUNTRY_COMPANY"]
        form_data = {
            "routing_wizard_view-current_step": "user-type",
            "user-type-choice": random.choice(user_types),
        }
        data = {key: (None, value) for key, value in form_data.items()}
        self.client.post(
            url,
            headers=LOAD_TESTS_USER_AGENT,
            files=data,
            name="generic",
            auth=basic_auth(),
        )

    @task
    def business_forms(self):
        url = random.choice(self.erp_business_urls)
        self.client.get(
            url, headers=LOAD_TESTS_USER_AGENT, name="/business", auth=basic_auth()
        )

    @task
    def consumer_forms(self):
        url = random.choice(self.erp_consumer_urls)
        self.client.get(
            url, headers=LOAD_TESTS_USER_AGENT, name="/consumer", auth=basic_auth()
        )

    @task
    def developing_country_forms(self):
        url = random.choice(self.erp_developing_country_urls)
        self.client.get(
            url,
            headers=LOAD_TESTS_USER_AGENT,
            files={},
            name="GET /developing-country-business",
            auth=basic_auth(),
        )

    @task
    def importer_forms(self):
        url = random.choice(self.erp_importer_urls)
        self.client.get(
            url, headers=LOAD_TESTS_USER_AGENT, name="/importer", auth=basic_auth()
        )


class ERP(HttpUser):
    host = settings.ERP_URL
    tasks = [ERPTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
