# -*- coding: utf-8 -*-
"""Export Opportunities Load tests"""
import random
import uuid

from directory_constants.constants.exred_sector_names import CODES_SECTORS_DICT
from locust import HttpLocust, TaskSet, task
from requests import Response
from scrapy.selector import Selector
from tests import get_absolute_url, settings


def select_random_sector() -> tuple:
    return random.choice(list(CODES_SECTORS_DICT.items()))


def extract_csrf_middleware_token(response: Response) -> str:
    """Extract CSRF middleware token from the response content.

    Comes in handy when dealing with e.g. Django forms.

    :param response: requests response
    :return: CSRF middleware token or empty string if not found
    """
    content = response.content.decode("utf-8")
    selector = '#content input[type="hidden"]::attr(value)'
    extracted = Selector(text=content).css(selector).extract()
    token = extracted[0] if len(extracted) > 0 else ""
    return token


def response_url_should_match(response: Response, expected_url: str):
    error_message = (
        "Expected the response URL to be '{}', but got '{}' instead."
        .format(expected_url, response.url)
    )
    assert response.url == expected_url, error_message


def should_be_on_what_do_you_want_to_export(response):
    url = get_absolute_url("ui-exred:triage-sector")
    response_url_should_match(response, url)


def should_be_on_have_you_exported_before(response: Response):
    url = get_absolute_url("ui-exred:triage-exported-before")
    response_url_should_match(response, url)


def should_be_on_do_you_export_regularly(response: Response):
    url = get_absolute_url("ui-exred:triage-regular-exporter")
    response_url_should_match(response, url)


def should_be_on_do_you_use_online_marketplaces(response: Response):
    url = get_absolute_url("ui-exred:triage-online-marketplace")
    response_url_should_match(response, url)


def should_be_on_is_your_company_incorporated(response: Response):
    url = get_absolute_url("ui-exred:triage-companies-house")
    response_url_should_match(response, url)


def should_be_on_what_is_your_company_name(response: Response):
    url = get_absolute_url("ui-exred:triage-company")
    response_url_should_match(response, url)


def should_be_on_triage_summary(response: Response):
    url = get_absolute_url("ui-exred:triage-summary")
    response_url_should_match(response, url)


def should_be_on_custom_page(response: Response):
    url = get_absolute_url("ui-exred:custom")
    response_url_should_match(response, url)


class TriagePagesUI(TaskSet):

    def go_to_what_do_you_want_to_export(self) -> Response:
        url = get_absolute_url("ui-exred:triage-sector")
        return self.client.get(url=url)

    def answer_what_do_you_want_to_export(
            self, csrf_middleware_token: str, *, code: str = None) -> Response:
        if not code:
            code, _ = select_random_sector()
        url = get_absolute_url("ui-exred:triage-sector")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "sector-sector": (None, code),
            "triage_wizard_form_view-current_step": (None, "sector")
        }
        return self.client.post(url=url, files=data)

    def answer_have_you_exported_before(
            self, csrf_middleware_token: str, *, answer: bool = None) -> Response:
        if answer is None:
            answer = random.choice([True, False])
        exported_before = str(answer)
        url = get_absolute_url("ui-exred:triage-exported-before")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "exported-before-exported_before": (None, exported_before),
            "triage_wizard_form_view-current_step": (None, "exported-before")
        }
        return self.client.post(url=url, files=data)

    def answer_do_you_export_regularly(
            self, csrf_middleware_token: str, *, answer: bool = None) -> Response:
        if answer is None:
            answer = random.choice([True, False])
        regular = str(answer)
        url = get_absolute_url("ui-exred:triage-regular-exporter")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "regular-exporter-regular_exporter": (None, regular),
            "triage_wizard_form_view-current_step": (None, "regular-exporter")
        }
        return self.client.post(url=url, files=data)

    def answer_do_you_use_online_marketplaces(
            self, csrf_middleware_token: str, *, answer: bool = None) -> Response:
        if answer is None:
            answer = random.choice([True, False])
        use = str(answer)
        url = get_absolute_url("ui-exred:triage-online-marketplace")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "online-marketplace-used_online_marketplace": (None, use),
            "triage_wizard_form_view-current_step": (None, "online-marketplace")
        }
        return self.client.post(url=url, files=data)

    def answer_is_your_company_incorporated(
            self, csrf_middleware_token: str, *, answer: bool = None) -> Response:
        if answer is None:
            answer = random.choice([True, False])
        incorporated = str(answer)
        url = get_absolute_url("ui-exred:triage-companies-house")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "companies-house-is_in_companies_house": (None, incorporated),
            "triage_wizard_form_view-current_step": (None, "companies-house")
        }
        return self.client.post(url=url, files=data)

    def answer_what_is_your_company_name(
            self, csrf_middleware_token: str, *, company_name: str = None,
            company_number: str = None) -> Response:
        company_name = company_name or "RANDOM COMPANY %d" % uuid.uuid4()
        company_number = company_number or ""
        url = get_absolute_url("ui-exred:triage-companies-house")
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "company-company_number": (None, company_number),
            "ompany-company_name": (None, company_name),
            "triage_wizard_form_view-current_step": (None, "company")
        }
        return self.client.post(url=url, files=data)

    def create_my_export_journey(self, csrf_middleware_token: str) -> Response:
        data = {
            "csrfmiddlewaretoken": (None, csrf_middleware_token),
            "triage_wizard_form_view-current_step": (None, "summary")
        }
        url = get_absolute_url("ui-exred:triage-summary")
        return self.client.post(url=url, files=data)

    @task
    def new_and_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=False)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=True)
        should_be_on_what_is_your_company_name(response)
        token = extract_csrf_middleware_token(response)

        # answer Q4: "What is your company name?"
        response = self.answer_what_is_your_company_name(token)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)

    @task
    def new_and_not_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=False)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=False)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)

    @task
    def occasional_and_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=True)
        should_be_on_do_you_export_regularly(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is exporting a regular part of your business activities?"
        response = self.answer_do_you_export_regularly(token, answer=False)
        should_be_on_do_you_use_online_marketplaces(response)
        token = extract_csrf_middleware_token(response)

        # answer Q4: "Do you use online marketplaces to sell your products?"
        response = self.answer_do_you_use_online_marketplaces(token)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q5: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=True)
        should_be_on_what_is_your_company_name(response)
        token = extract_csrf_middleware_token(response)

        # answer Q6: "What is your company name?"
        response = self.answer_what_is_your_company_name(token)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)

    @task
    def occasional_and_not_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=True)
        should_be_on_do_you_export_regularly(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is exporting a regular part of your business activities?"
        response = self.answer_do_you_export_regularly(token, answer=False)
        should_be_on_do_you_use_online_marketplaces(response)
        token = extract_csrf_middleware_token(response)

        # answer Q4: "Do you use online marketplaces to sell your products?"
        response = self.answer_do_you_use_online_marketplaces(token)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q5: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=False)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)

    @task
    def regular_and_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=True)
        should_be_on_do_you_export_regularly(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is exporting a regular part of your business activities?"
        response = self.answer_do_you_export_regularly(token, answer=True)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q4: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=True)
        should_be_on_what_is_your_company_name(response)
        token = extract_csrf_middleware_token(response)

        # answer Q6: "What is your company name?"
        response = self.answer_what_is_your_company_name(token)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)

    @task
    def regular_and_not_incorporated_exporter(self):
        # go to Q1: "What do you want to export?"
        response = self.go_to_what_do_you_want_to_export()
        should_be_on_what_do_you_want_to_export(response)
        token = extract_csrf_middleware_token(response)

        # answer Q1: "What do you want to export?"
        response = self.answer_what_do_you_want_to_export(token)
        should_be_on_have_you_exported_before(response)
        token = extract_csrf_middleware_token(response)

        # answer Q2: "Have you exported before?"
        response = self.answer_have_you_exported_before(token, answer=True)
        should_be_on_do_you_export_regularly(response)
        token = extract_csrf_middleware_token(response)

        # answer Q3: "Is exporting a regular part of your business activities?"
        response = self.answer_do_you_export_regularly(token, answer=True)
        should_be_on_is_your_company_incorporated(response)
        token = extract_csrf_middleware_token(response)

        # answer Q4: "Is your company incorporated in the UK?"
        response = self.answer_is_your_company_incorporated(token, answer=False)
        should_be_on_triage_summary(response)
        token = extract_csrf_middleware_token(response)

        # Create my export journey
        response = self.create_my_export_journey(token)
        should_be_on_custom_page(response)


class ExRedTriageUI(HttpLocust):
    host = settings.EXRED_UI_URL
    task_set = TriagePagesUI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
