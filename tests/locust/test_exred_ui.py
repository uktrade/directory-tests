# -*- coding: utf-8 -*-
"""Export Opportunities Load tests"""

from locust import HttpLocust, TaskSet, task

from tests import get_relative_url, get_absolute_url, settings


class PublicPagesSupplierUI(TaskSet):

    @task
    def landing_page(self):
        self.client.get(get_relative_url('ui-exred:landing'))

    @task
    def landing_uk_page(self):
        self.client.get(get_relative_url('ui-exred:landing-uk'))

    @task
    def international_page(self):
        self.client.get(get_relative_url('ui-exred:international'))

    @task
    def international_uk_page(self):
        self.client.get(get_relative_url('ui-exred:international-uk'))

    @task
    def international_zh_page(self):
        self.client.get(get_relative_url('ui-exred:international-zh'))

    @task
    def international_de_page(self):
        self.client.get(get_relative_url('ui-exred:international-de'))

    @task
    def international_ja_page(self):
        self.client.get(get_relative_url('ui-exred:international-ja'))

    @task
    def international_es_page(self):
        self.client.get(get_relative_url('ui-exred:international-es'))

    @task
    def international_pt_page(self):
        self.client.get(get_relative_url('ui-exred:international-pt'))

    @task
    def international_ar_page(self):
        self.client.get(get_relative_url('ui-exred:international-ar'))

    @task
    def triage_sector_page(self):
        self.client.get(get_relative_url('ui-exred:triage-sector'))

    @task
    def triage_exported_before_page(self):
        self.client.get(get_relative_url('ui-exred:triage-exported-before'))

    @task
    def triage_regular_exporter_page(self):
        self.client.get(get_relative_url('ui-exred:triage-regular-exporter'))

    @task
    def triage_online_marketplace_page(self):
        self.client.get(get_relative_url('ui-exred:triage-online-marketplace'))

    @task
    def triage_companies_house_page(self):
        self.client.get(get_relative_url('ui-exred:triage-companies-house'))

    @task
    def triage_company_page(self):
        self.client.get(get_relative_url('ui-exred:triage-company'))

    @task
    def triage_summary_page(self):
        self.client.get(get_relative_url('ui-exred:triage-summary'))

    @task
    def custom_page(self):
        self.client.get(get_relative_url('ui-exred:custom'))

    @task
    def new_page(self):
        self.client.get(get_relative_url('ui-exred:new'))

    @task
    def occasional_page(self):
        self.client.get(get_relative_url('ui-exred:occasional'))

    @task
    def regular_page(self):
        self.client.get(get_relative_url('ui-exred:regular'))

    @task
    def market_research_page(self):
        self.client.get(get_relative_url('ui-exred:market-research'))

    @task
    def customer_insight_page(self):
        self.client.get(get_relative_url('ui-exred:customer-insight'))

    @task
    def finance_page(self):
        self.client.get(get_relative_url('ui-exred:finance'))

    @task
    def business_planning_page(self):
        self.client.get(get_relative_url('ui-exred:business-planning'))

    @task
    def getting_paid_page(self):
        self.client.get(get_relative_url('ui-exred:getting-paid'))

    @task
    def operations_and_compliance_page(self):
        self.client.get(get_relative_url('ui-exred:operations-and-compliance'))

    @task
    def get_finance_page(self):
        self.client.get(get_relative_url('ui-exred:get-finance'))

    @task
    def export_opportunities_page(self):
        self.client.get(get_relative_url('ui-exred:export-opportunities'))

    @task
    def story_first_page(self):
        self.client.get(get_relative_url('ui-exred:story-first'))

    @task
    def story_second_page(self):
        self.client.get(get_relative_url('ui-exred:story-second'))

    @task
    def story_third_page(self):
        self.client.get(get_relative_url('ui-exred:story-thrid'))


class RegularUserSupplierUI(HttpLocust):
    host = settings.EXRED_UI_URL
    task_set = PublicPagesSupplierUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
