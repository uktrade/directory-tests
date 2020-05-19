#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict, namedtuple
from enum import Enum, EnumMeta
from typing import List

import requests

from circleclient.circleclient import CircleClient
from geckoboard.client import Client as GeckoClient
from geckoboard.dataset import Dataset
from tests.periodic_tasks.geckoboard_updater.circleci_helpers import (
    last_directory_service_build_results,
    last_directory_tests_results,
    last_periodic_tests_results,
    last_useful_content_diff_report_links,
    last_useful_content_tests_results,
)
from tests.periodic_tasks.geckoboard_updater.gecko_dataset_schemas import Schema

DatasetAndSchema = namedtuple("DatasetAndSchema", ["dataset", "schema"])


class Datasets(Enum):
    """Geckoboard Dataset enumeration."""

    @property
    def dataset(self) -> Dataset:
        return self.value.dataset

    @property
    def schema(self) -> Schema:
        return self.value.schema


def create_datasets(dataset_enum: EnumMeta, gecko_client: GeckoClient) -> Datasets:
    """
    More on datasets.find_or_create()
    https://developer.geckoboard.com/api-reference/python/#findorcreate
    """
    dasets = {
        key: DatasetAndSchema(
            dataset=gecko_client.datasets.find_or_create(*schema.value),
            schema=schema.value,
        )
        for key, schema in dataset_enum.__members__.items()
    }
    return Datasets(value="Datasets", names=dasets)


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
    table_template = """<table style="width:100%">
<thead>
<tr style="font-size:14pt">
<th>Name</th><th>When</th><th>Time</th><th>Status</th>
</tr>
</thead>
<tbody>
{rows}
</tbody></table>"""
    row_template = """<tr style="font-size:14pt">
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
    table_template = """<table style="width:100%">
<thead>
<tr style="font-size:14pt">
<th>Name</th><th>When</th><th>Time</th><th>Unit</th><th>flake8</th>
</tr>
</thead><tbody>
{rows}
</tbody></table>"""
    row_template = """<tr style="font-size:14pt">
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
    table_template = """<table style="width:100%">
<tbody>{rows}
</tbody></table>"""
    row_template = """\n<tr style="font-size:14pt">
<td>{link}</td>
</tr>"""
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


def push_directory_tests_results(
    circle_ci_client: CircleClient,
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):
    last_test_results = last_directory_tests_results(circle_ci_client)
    text = widget_text_for_directory_tests(last_test_results)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_periodic_tests_results(
    circle_ci_client: CircleClient,
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):
    last_periodic_test_results = last_periodic_tests_results(circle_ci_client)
    text = widget_text_for_directory_tests(last_periodic_test_results)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_links_to_useful_content_test_jobs(
    circle_ci_client: CircleClient,
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):
    last_content_obs = last_useful_content_tests_results(circle_ci_client)
    sorted_results = OrderedDict(sorted(last_content_obs.items()))
    links = [
        f'<a href="{details["build_url"]}" target=_blank>{job}</a>'
        for job, details in sorted_results.items()
    ]
    text = widget_links(links)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_links_to_content_diff_reports(
    circle_ci_client: CircleClient,
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):

    last_content_diff_report_links = last_useful_content_diff_report_links(
        circle_ci_client
    )
    sorted_results = OrderedDict(sorted(last_content_diff_report_links.items()))
    links = [
        f'<a href="{url}" target=_blank>{job}</a>'
        for job, url in sorted_results.items()
    ]
    text = widget_links(links)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_directory_service_build_results(
    circle_ci_client: CircleClient,
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):
    last_service_build_results = last_directory_service_build_results(circle_ci_client)
    text = widget_text_for_service_build(last_service_build_results)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_jira_query_links(
    links: List[str],
    geckoboard_push_url: str,
    geckoboard_api_key: str,
    widget_key: str,
):
    text = widget_links(links)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)
