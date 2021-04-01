#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tests.periodic_tasks.geckoboard_updater.datasets import GeckoboardDatasets
from tests.periodic_tasks.geckoboard_updater.geckoboard_utils import (
    push_circleci_test_results,
    push_directory_service_build_results,
    push_directory_tests_results,
    push_jira_links,
    push_jira_stats,
    push_links_to_content_diff_reports,
    push_links_to_useful_content_test_jobs,
    push_pa11y_test_results,
    push_periodic_tests_results,
)

if __name__ == "__main__":
    print("Finding or creating Geckoboard datasets...")
    datasets = GeckoboardDatasets()

    print("Pushing datasets to Geckoboard...")
    push_jira_stats(datasets)
    push_circleci_test_results(datasets)
    #push_pa11y_test_results(datasets)

    print(f"Pushing text widget data to GeckoBoard...")
    push_jira_links()
    push_directory_service_build_results()
    push_directory_tests_results()
    push_links_to_useful_content_test_jobs()
    push_periodic_tests_results()
    push_links_to_content_diff_reports()
