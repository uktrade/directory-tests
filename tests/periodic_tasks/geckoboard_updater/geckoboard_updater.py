#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import date

from envparse import env

from circleclient import circleclient
from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient
from tests.periodic_tasks.geckoboard_updater.geckoboard_datasets import Datasets
from tests.periodic_tasks.geckoboard_updater.geckoboard_helpers import (
    push_directory_service_build_results,
    push_directory_tests_results,
    push_jira_query_links,
    push_links_to_content_diff_reports,
    push_links_to_useful_content_test_jobs,
    push_periodic_tests_results,
)

# Env Vars
CIRCLE_TOKEN = env.str("CIRCLE_TOKEN")
GECKOBOARD_API_KEY = env.str("GECKOBOARD_API_KEY")
GECKOBOARD_PUSH_URL = os.getenv(
    "GECKOBOARD_PUSH_URL", "https://push.geckoboard.com/v1/send/"
)
GECKOBOARD_CONTENT_DIFF_REPORTS_WIDGET_KEY = env.str(
    "GECKOBOARD_CONTENT_DIFF_REPORTS_WIDGET_KEY"
)
GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY = env.str(
    "GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY"
)
GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY = env.str(
    "GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY"
)
GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY = env.str(
    "GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY"
)
GECKOBOARD_TEST_RESULTS_WIDGET_KEY = env.str("GECKOBOARD_TEST_RESULTS_WIDGET_KEY")
GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY = env.str(
    "GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY"
)
JIRA_HOST = env.str("JIRA_HOST")
JIRA_TOKEN = env.str("JIRA_TOKEN")
JIRA_USERNAME = env.str("JIRA_USERNAME")
PA11Y_PASSWORD = env.str("PA11Y_PASSWORD")
PA11Y_URL = env.str("PA11Y_URL")
PA11Y_USERNAME = env.str("PA11Y_USERNAME")

# other variables
TODAY = date.today().isoformat()

# Clients
JIRA_CLIENT = JiraClient(JIRA_HOST, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
CIRCLE_CI_CLIENT = circleclient.CircleClient(CIRCLE_TOKEN)


if __name__ == "__main__":
    print("Find or create Geckoboard datasets")
    DATASETS = Datasets(GECKO_CLIENT)

    print("Fetching stats from Jira")
    from tests.periodic_tasks.geckoboard_updater.jira_results import (
        jira_bug_and_ticket_counters,
        jira_bugs_by_labels,
        tools_jira_links,
    )

    print("Pushing Jira stats to Geckoboard")
    DATASETS.jira_bugs_by_labels.post(jira_bugs_by_labels)
    DATASETS.jira_bug_and_ticket_counters.post(jira_bug_and_ticket_counters)

    print("Fetching test results from CircleCi")
    from tests.periodic_tasks.geckoboard_updater.circleci_results import (
        circle_ci_periodic_tests_results,
        load_tests_response_times_distributions,
        load_tests_response_times_metrics,
    )

    print("Pushing periodic tests results to Geckoboard")
    DATASETS.periodic_tests_results.post(circle_ci_periodic_tests_results)
    print("Pushing load tests result distribution results to Geckoboard")
    DATASETS.load_tests_response_time_distribution.post(
        load_tests_response_times_distributions
    )
    print("Pushing load test response times metrics to Geckoboard")
    DATASETS.load_tests_response_time_metrics.post(load_tests_response_times_metrics)

    from tests.periodic_tasks.geckoboard_updater.pa11y_results import (
        aggregated_accessibility_issues_per_service,
    )

    print("Pushing aggregated Pa11y accessibility test results to Geckoboard")
    DATASETS.pa11y_tests_results.post(aggregated_accessibility_issues_per_service)

    print(f"Pushing text widget data to GeckoBoard")
    push_directory_service_build_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_TEST_RESULTS_WIDGET_KEY,
    )
    push_directory_tests_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY,
    )
    push_links_to_useful_content_test_jobs(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY,
    )
    push_jira_query_links(
        tools_jira_links,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY,
    )
    push_periodic_tests_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY,
    )
    push_links_to_content_diff_reports(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_CONTENT_DIFF_REPORTS_WIDGET_KEY,
    )
