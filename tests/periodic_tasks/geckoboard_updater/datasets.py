# -*- coding: utf-8 -*-
"""Geckoboard Dataset Schemas"""
from dataclasses import dataclass
from typing import List

from geckoboard.dataset import Dataset
from tests.periodic_tasks.geckoboard_updater.clients import GECKOBOARD_CLIENT


@dataclass
class Schema:
    dataset_id: str
    fields: dict
    unique_by: List[str]


date_team_metric_label_quantity = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
date_team_metric_quantity = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
date_metric_environment_errors_failures_tests = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "environment": {"type": "string", "name": "Environment", "optional": False},
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "tests": {"type": "number", "name": "Tests", "optional": False},
}
date_service_errors_warnings_pages = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "service": {"type": "string", "name": "Service", "optional": False},
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "warnings": {"type": "number", "name": "Warnings", "optional": False},
    "pages": {"type": "number", "name": "Pages", "optional": False},
}

# values can be optional
# it allows for sending results for endpoints that returned failures
locust_response_time_distribution = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "name": {"type": "string", "name": "Name", "optional": False},
    "endpoint": {"type": "string", "endpoint": "Name", "optional": False},
    "requests": {"type": "number", "name": "# requests", "optional": True},
    "50": {"type": "number", "name": "50%", "optional": True},
    "75": {"type": "number", "name": "75%", "optional": True},
    "90": {"type": "number", "name": "90%", "optional": True},
    "95": {"type": "number", "name": "95%", "optional": True},
    "99": {"type": "number", "name": "99%", "optional": True},
    "100": {"type": "number", "name": "100%", "optional": True},
}
locust_response_time_metrics = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "name": {"type": "string", "name": "Name", "optional": False},
    "endpoint": {"type": "string", "endpoint": "Name", "optional": False},
    "requests": {"type": "number", "name": "# requests", "optional": True},
    "failures": {"type": "number", "name": "Failures", "optional": True},
    "median_response_time": {
        "type": "number",
        "name": "Med resp time",
        "optional": True,
    },
    "average_response_time": {
        "type": "number",
        "name": "Avg resp time",
        "optional": True,
    },
    "min_response_time": {"type": "number", "name": "Min resp time", "optional": True},
    "max_response_time": {"type": "number", "name": "Max resp time", "optional": True},
    "requests_per_s": {"type": "number", "name": "RPS", "optional": True},
}

# Define arrays of one or more field names whose values will be unique across all your records.
# Geckoboard will ignore incoming dataset entries for which matching records already exist.
date_metric_environment = ["date", "metric", "environment"]
date_name_endpoint = ["date", "name", "endpoint"]
date_team_metric = ["date", "team", "metric"]
date_team_metric_label = ["date", "team", "metric", "label"]
date_service = ["date", "service"]

jira_bug_and_ticket_counters = Schema(
    dataset_id=f"jira.bug_and_ticket_counters",
    fields=date_team_metric_quantity,
    unique_by=date_team_metric,
)
jira_bugs_by_labels = Schema(
    dataset_id=f"jira.bugs_by_labels",
    fields=date_team_metric_label_quantity,
    unique_by=date_team_metric_label,
)
load_tests_response_time_distributions = Schema(
    dataset_id=f"load_tests.result_distribution",
    fields=locust_response_time_distribution,
    unique_by=date_name_endpoint,
)
load_tests_response_time_metrics = Schema(
    dataset_id=f"load_tests.result_requests",
    fields=locust_response_time_metrics,
    unique_by=date_name_endpoint,
)
pa11y_results_per_service = Schema(
    dataset_id=f"pa11y.results_per_service",
    fields=date_service_errors_warnings_pages,
    unique_by=date_service,
)
periodic_tests_results = Schema(
    dataset_id=f"periodic_tests.results",
    fields=date_metric_environment_errors_failures_tests,
    unique_by=date_metric_environment,
)


class GeckoboardDatasets:
    def find_or_create(self, schema: Schema) -> Dataset:
        """Before you can push a dataset to Geckoboard you have to ensure that it exists and create one if it doesn't.
        More on it in the official documentation:
        https://developer.geckoboard.com/hc/en-us/articles/360019475652
        """
        return self.client.datasets.find_or_create(
            schema.dataset_id, schema.fields, unique_by=schema.unique_by
        )

    def __init__(self):
        self.client = GECKOBOARD_CLIENT
        self.jira_bug_and_ticket_counters = self.find_or_create(
            jira_bug_and_ticket_counters
        )
        self.jira_bugs_by_labels = self.find_or_create(jira_bugs_by_labels)
        self.load_tests_response_time_distribution = self.find_or_create(
            load_tests_response_time_distributions
        )
        self.load_tests_response_time_metrics = self.find_or_create(
            load_tests_response_time_metrics
        )
        self.pa11y_tests_results = self.find_or_create(pa11y_results_per_service)
        self.periodic_tests_results = self.find_or_create(periodic_tests_results)
