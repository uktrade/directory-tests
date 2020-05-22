# -*- coding: utf-8 -*-
from collections import OrderedDict
from typing import List

import requests

from tests.periodic_tasks.geckoboard_updater.circleci_utils import (
    DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS,
    DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS,
    get_load_test_response_time_distribution,
    get_load_test_response_time_metrics,
    last_directory_service_build_results,
    last_directory_tests_results,
    last_load_test_artifacts,
    last_periodic_tests_results,
    last_tests_results_from_junit_artifacts,
    last_useful_content_diff_report_links,
    last_useful_content_tests_results,
    last_useful_production_cms_page_status_report_link,
)
from tests.periodic_tasks.geckoboard_updater.clients import CIRCLE_CI_CLIENT
from tests.periodic_tasks.geckoboard_updater.datasets import GeckoboardDatasets
from tests.periodic_tasks.geckoboard_updater.jira_queries import ToolsJQLs
from tests.periodic_tasks.geckoboard_updater.jira_utils import (
    jira_links,
    tickets_by_labels,
    total_tickets,
)
from tests.periodic_tasks.geckoboard_updater.pa11y import (
    generate_dataset_counters,
    get_tasks_with_last_results,
    parse_task_results,
)
from tests.periodic_tasks.geckoboard_updater.settings import (
    GECKOBOARD_API_KEY,
    GECKOBOARD_CONTENT_DIFF_REPORTS_WIDGET_KEY,
    GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY,
    GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY,
    GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY,
    GECKOBOARD_PUSH_URL,
    GECKOBOARD_TEST_RESULTS_WIDGET_KEY,
    GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY,
)


def job_status_color(status: str) -> str:
    status_colors = {
        "failed": "red",
        "fixed": "green",
        "not_run": "grey",
        "not_running": "grey",
        "queued": "purple",
        "running": "blue",
        "success": "green",
        "timedout": "red",
        "canceled": "grey",
    }
    return status_colors[status]


def widget_text_for_directory_tests(test_results: dict) -> str:
    table_template = """<table style="width:100%;font-size:14pt">
<thead>
<tr>
<th>Name</th><th>When</th><th>Time</th><th>Status</th>
</tr>
</thead>
<tbody>
{rows}
</tbody></table>"""
    row_template = """<tr>
<td>{name}</td>
<td><img src="{user_avatar}" title="{user_name}" width="25" height="25"/>{start_time}</td>
<td>{build_time}</td>
<td><a target="_blank" href="{build_url}" style="color:{status_color}">{status}</a></td>
</tr>"""
    rows = ""
    for friendly_name, result in test_results.items():
        rows += row_template.format(
            name=friendly_name,
            status_color=job_status_color(result["status"]),
            **result,
        )
    return table_template.format(rows=rows).replace("\n", "").replace('"', "'")


def widget_text_for_service_build(build_results: dict) -> str:
    table_template = """<table style="width:100%;font-size:14pt">
<thead>
<tr style="font-size:14pt">
<th>Name</th><th>When</th><th>Time</th><th>Unit</th><th>flake8</th>
</tr>
</thead><tbody>
{rows}
</tbody></table>"""
    row_template = """<tr>
<td>{name}</td>
<td><img src="{user_avatar}" title="{user_name}" width="25" height="25"/>{start_time}</td>
<td>{build_time}</td>
{unit}
{flake8}
</tr>"""
    job_status_template = """<td><a target="_blank" href="{build_url}" style="color:{status_color}">{status}</a></td>"""
    empty_row = "<td>N/A</td>"
    rows = ""
    for friendly_name, results in build_results.items():
        flake8 = empty_row
        unit = job_status_template.format(
            status_color=job_status_color(results["Unit Tests"]["status"]),
            **results["Unit Tests"],
        )
        if "flake8" in results:
            flake8 = job_status_template.format(
                status_color=job_status_color(results["flake8"]["status"]),
                **results["flake8"],
            )
        rows += row_template.format(
            name=friendly_name, unit=unit, flake8=flake8, **results["Unit Tests"],
        )
    return table_template.format(rows=rows).replace("\n", "").replace('"', "'")


def widget_links(links: List[str]) -> str:
    table_template = (
        """<table style="width:100%;font-size:14pt"><tbody>{rows}</tbody></table>"""
    )
    row_template = """\n<tr><td>{link}</td></tr>"""
    rows = ""
    for link in links:
        rows += row_template.format(link=link)
    return table_template.format(rows=rows).replace("\n", "").replace('"', "'")


def push_widget_text(push_url: str, api_key: str, widget_key: str, text: str):
    message = {
        "api_key": api_key,
        "data": {"item": [{"text": text, "type": 0}]},
    }
    url = push_url + widget_key
    response = requests.post(url, json=message)
    error = (
        f"Expected 200 but got {response.status_code} → {response.content} -> \n"
        f"{response.request.body}"
    )
    assert response.status_code == 200, error


def push_directory_tests_results():
    last_test_results = last_directory_tests_results(CIRCLE_CI_CLIENT)
    if not last_test_results:
        print(
            f"Couldn't find new results for directory tests jobs. Will keep the old ones in place"
        )
        return
    text = widget_text_for_directory_tests(last_test_results)
    push_widget_text(
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY,
        text,
    )


def push_periodic_tests_results():
    last_periodic_test_results = last_periodic_tests_results(CIRCLE_CI_CLIENT)
    if not last_periodic_test_results:
        print(
            f"Couldn't find new results for periodic tests jobs. Will keep the old ones in place"
        )
        return
    text = widget_text_for_directory_tests(last_periodic_test_results)
    push_widget_text(
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY,
        text,
    )


def push_links_to_useful_content_test_jobs():
    most_recent_content_job_links = last_useful_content_tests_results(CIRCLE_CI_CLIENT)
    if not most_recent_content_job_links:
        print(
            f"Couldn't find new links to content test jobs. Will keep the old ones in place"
        )
        return
    sorted_links_to_content_jobs = OrderedDict(
        sorted(most_recent_content_job_links.items())
    )
    links = [
        f'<a href="{details["build_url"]}" target=_blank>{job}</a>'
        for job, details in sorted_links_to_content_jobs.items()
    ]

    most_recent_cms_page_status_report_link = last_useful_production_cms_page_status_report_link(
        CIRCLE_CI_CLIENT
    )
    if most_recent_cms_page_status_report_link:
        cms_page_status_report_link = [
            f'<a href="{report_link}" target=_blank>{report_name}</a>'
            for report_name, report_link in most_recent_cms_page_status_report_link.items()
        ]
        links.extend(cms_page_status_report_link)

    text = widget_links(links)
    push_widget_text(
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY,
        text,
    )


def push_links_to_content_diff_reports():
    last_content_diff_report_links = last_useful_content_diff_report_links(
        CIRCLE_CI_CLIENT
    )
    if not last_content_diff_report_links:
        print(
            f"Couldn't find new links to content diff reports. Will keep the old ones in place"
        )
        return
    sorted_results = OrderedDict(sorted(last_content_diff_report_links.items()))
    links = [
        f'<a href="{url}" target=_blank>{job}</a>'
        for job, url in sorted_results.items()
    ]
    text = widget_links(links)
    push_widget_text(
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_CONTENT_DIFF_REPORTS_WIDGET_KEY,
        text,
    )


def push_directory_service_build_results():
    last_service_build_results = last_directory_service_build_results(CIRCLE_CI_CLIENT)
    if not last_service_build_results:
        print(
            f"Couldn't find new service build results in CircleCI. Will keep the old ones in place"
        )
        return
    text = widget_text_for_service_build(last_service_build_results)
    push_widget_text(
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_TEST_RESULTS_WIDGET_KEY,
        text,
    )


def push_jira_query_links(links: List[str], widget_key: str):
    text = widget_links(links)
    push_widget_text(GECKOBOARD_PUSH_URL, GECKOBOARD_API_KEY, widget_key, text)


def push_jira_links():
    print("Pushing Jira Query links to Geckoboard")
    tools_jira_links = jira_links(ToolsJQLs)
    push_jira_query_links(
        tools_jira_links, GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY
    )


def push_jira_stats(datasets: GeckoboardDatasets):
    tools_bugs_in_backlog_by_labels = tickets_by_labels(
        jql=ToolsJQLs.BUGS_IN_BACKLOG,
        ignored_labels=["auto", "manual"],
        team="tools",
        metric="Bugs in Backlog by labels",
    )
    tools_bugs_on_board_by_labels = tickets_by_labels(
        jql=ToolsJQLs.BUGS_ON_BOARD,
        ignored_labels=["auto", "manual"],
        team="tools",
        metric="Bugs on Board by labels",
    )
    tools_bugs_closed_today = total_tickets(
        jql=ToolsJQLs.BUGS_CLOSED_TODAY, team="tools"
    )
    tools_bugs_in_backlog = total_tickets(jql=ToolsJQLs.BUGS_IN_BACKLOG, team="tools")
    tools_tickets_closed_today = total_tickets(
        jql=ToolsJQLs.TICKETS_CLOSED_TODAY, team="tools"
    )
    tools_tickets_on_board = total_tickets(jql=ToolsJQLs.TICKETS_ON_BOARD, team="tools")

    jira_bugs_by_labels = (
        tools_bugs_in_backlog_by_labels + tools_bugs_on_board_by_labels
    )

    jira_bug_and_ticket_counters = (
        tools_bugs_closed_today
        + tools_bugs_in_backlog
        + tools_tickets_closed_today
        + tools_tickets_on_board
    )
    print("Pushing Jira stats to Geckoboard...")
    datasets.jira_bugs_by_labels.post(jira_bugs_by_labels)
    datasets.jira_bug_and_ticket_counters.post(jira_bug_and_ticket_counters)


def push_pa11y_test_results(datasets: GeckoboardDatasets):
    raw_results = get_tasks_with_last_results()
    parsed_results = parse_task_results(raw_results)
    aggregated_accessibility_issues_per_service = generate_dataset_counters(
        parsed_results
    )
    print("Pushing aggregated Pa11y accessibility test results to Geckoboard...")
    datasets.pa11y_tests_results.post(aggregated_accessibility_issues_per_service)


def push_circleci_test_results(datasets: GeckoboardDatasets):
    circle_ci_periodic_tests_results = last_tests_results_from_junit_artifacts(
        CIRCLE_CI_CLIENT, "directory-tests", DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS,
    )
    load_tests_artifacts = last_load_test_artifacts(
        CIRCLE_CI_CLIENT,
        "directory-tests",
        job_name_mappings=DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS,
    )
    load_tests_response_times_distributions = get_load_test_response_time_distribution(
        load_tests_artifacts
    )
    load_tests_response_times_metrics = get_load_test_response_time_metrics(
        load_tests_artifacts
    )

    print("Pushing periodic tests results to Geckoboard...")
    datasets.periodic_tests_results.post(circle_ci_periodic_tests_results)

    print("Pushing load tests result distribution results to Geckoboard...")
    datasets.load_tests_response_time_distribution.post(
        load_tests_response_times_distributions
    )

    print("Pushing load test response times metrics to Geckoboard...")
    datasets.load_tests_response_time_metrics.post(load_tests_response_times_metrics)
