# -*- coding: utf-8 -*-
"""Geckoboard Dataset Schemas"""
from collections import namedtuple
from enum import Enum, EnumMeta

from geckoboard import Client as GeckoClient
from geckoboard.dataset import Dataset

Schema = namedtuple("Schema", ["dataset_id", "fields", "unique_by"])

DATE_TEAM_METRIC_LABEL_QUANTITY = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATE_TEAM_METRIC_QUANTITY = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "team": {"type": "string", "name": "Team", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATE_METRIC_ENVIRONMENT_ERRORS_FAILURES_TESTS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "metric": {"type": "string", "name": "Metric", "optional": False},
    "environment": {"type": "string", "name": "Environment", "optional": False},
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "tests": {"type": "number", "name": "Tests", "optional": False},
}
DATE_SERVICE_ERRORS_WARNINGS_PAGES = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "service": {"type": "string", "name": "Service", "optional": False},
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "warnings": {"type": "number", "name": "Warnings", "optional": False},
    "pages": {"type": "number", "name": "Pages", "optional": False},
}

# values can be optional
# it allows for sending results for endpoints that returned failures
LOCUST_RESPONSE_TIME_DISTRIBUTION = {
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
LOCUST_RESPONSE_TIME_METRICS = {
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
DATE_METRIC_ENVIRONMENT = ["date", "metric", "environment"]
DATE_NAME_ENDPOINT = ["date", "name", "endpoint"]
DATE_TEAM_METRIC = ["date", "team", "metric"]
DATE_TEAM_METRIC_LABEL = ["date", "team", "metric", "label"]
DATE_SERVICE = ["date", "service"]


def jira_bugs_by_labels() -> Schema:
    return Schema(
        dataset_id=f"jira.bugs_by_labels",
        fields=DATE_TEAM_METRIC_LABEL_QUANTITY,
        unique_by=DATE_TEAM_METRIC_LABEL,
    )


def jira_bug_and_ticket_counters() -> Schema:
    return Schema(
        dataset_id=f"jira.bug_and_ticket_counters",
        fields=DATE_TEAM_METRIC_QUANTITY,
        unique_by=DATE_TEAM_METRIC,
    )


def periodic_tests_results() -> Schema:
    return Schema(
        dataset_id=f"periodic_tests.results",
        fields=DATE_METRIC_ENVIRONMENT_ERRORS_FAILURES_TESTS,
        unique_by=DATE_METRIC_ENVIRONMENT,
    )


def load_tests_response_time_distributions() -> Schema:
    """Returns a schema schema for load test (locust.io) response time (percentile) distributions.
    One dataset for all results (endpoints).
    """
    return Schema(
        dataset_id=f"load_tests.result_distribution",
        fields=LOCUST_RESPONSE_TIME_DISTRIBUTION,
        unique_by=DATE_NAME_ENDPOINT,
    )


def load_tests_response_time_metrics() -> Schema:
    """Returns a dataset schema for Load test (locust.io) response time metrics.
    One dataset for all results.
    """
    return Schema(
        dataset_id=f"load_tests.result_requests",
        fields=LOCUST_RESPONSE_TIME_METRICS,
        unique_by=DATE_NAME_ENDPOINT,
    )


def pa11y_tests_results() -> Schema:
    """Pa11y accessibility test results.
    One dataset for all results"""
    return Schema(
        dataset_id=f"pa11y.results_per_service",
        fields=DATE_SERVICE_ERRORS_WARNINGS_PAGES,
        unique_by=DATE_SERVICE,
    )


class Datasets(Enum):
    """Simple Geckoboard Dataset enum with two extra properties."""

    @property
    def dataset(self) -> Dataset:
        return self.value.dataset

    @property
    def schema(self) -> Schema:
        return self.value.schema


def find_or_create_datasets(
    dataset_enum: EnumMeta, gecko_client: GeckoClient
) -> Datasets:
    """Before you can push a dataset to Geckoboard you have to ensure that it exists and create one if it doesn't.
    More on it in the official documentation:
    https://developer.geckoboard.com/hc/en-us/articles/360019475652
    """
    DatasetAndSchema = namedtuple("DatasetAndSchema", ["dataset", "schema"])
    datasets = {
        key: DatasetAndSchema(
            dataset=gecko_client.datasets.find_or_create(*schema.value),
            schema=schema.value,
        )
        for key, schema in dataset_enum.__members__.items()
    }
    return Datasets(value="Datasets", names=datasets)


class DatasetSchemas(Enum):
    JIRA_BUG_AND_TICKET_COUNTERS = jira_bug_and_ticket_counters()
    JIRA_BUGS_BY_LABELS = jira_bugs_by_labels()
    LOAD_TESTS_RESPONSE_TIME_DISTRIBUTION = load_tests_response_time_distributions()
    LOAD_TESTS_RESPONSE_TIME_METRICS = load_tests_response_time_metrics()
    PA11Y_TESTS_RESULTS = pa11y_tests_results()
    PERIODIC_TESTS_RESULTS = periodic_tests_results()
