# -*- coding: utf-8 -*-
from collections import Counter, defaultdict
from datetime import datetime
from typing import List
from urllib.parse import urljoin

import requests
from retrying import retry

from tests.periodic_tasks.geckoboard_updater.settings import (
    PA11Y_PASSWORD,
    PA11Y_URL,
    PA11Y_USERNAME,
)


@retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_tasks_with_last_results() -> dict:
    url = urljoin(PA11Y_URL, "/ws/tasks?lastres=true")
    response = requests.get(url, auth=(PA11Y_USERNAME, PA11Y_PASSWORD))
    assert response.status_code == 200, f"Pa11y responded with {response.status_code}"
    return response.json()


def parse_task_results(raw_pa11y_results: dict) -> List[dict]:
    """Parse raw Pa11y task data with last test results.

    Example Pa11y task data:
    [
      ...,
      {
       'id': '5d00f3db06e38314002017b5',
       'name': 'SERVICE NAME - PAGE NAME',
       'url': 'https://example.domain/some/endpoint/',
       'timeout': 30000,
       'wait': 0,
       'standard': 'WCAG2AA',
       'ignore': [],
       'actions': [],
       'annotations': [],
       'last_result': {
         'id': '5ec1d70c75e6e50017924065',
         'task': '5d00f3db06e38314002017b5',
         'date': '2020-05-18T00:30:04.190Z',
         'count': {'total': 60, 'error': 3, 'warning': 5, 'notice': 52},
         'ignore': []
        }
       }
     ]

    Expected task name format:
        Domestic - Feedback
        Domestic - Home
        Domestic - Market

    It will skip tasks:
     * without a `-` which separates service name from page name
     * last_result field
     * with last_result other than from today

    Returns a list of task test results.
    Each items represents results for one task (page) tested by Pa11y.
    Items don't contain page name as it's not relevant because we're after aggregate values.

    Example result:
    [
     ...
     {'service': 'Profile', 'errors': 3, 'warnings': 5},
     {'service': 'Profile', 'errors': 3, 'warnings': 4},
     {'service': 'SOO', 'errors': 11, 'warnings': 13},
     {'service': 'SOO', 'errors': 4, 'warnings': 5},
     {'service': 'SSO', 'errors': 3, 'warnings': 4},
     {'service': 'SSO', 'errors': 3, 'warnings': 4}
    ]
    """
    results = []
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    for task in raw_pa11y_results:
        if "-" not in task["name"]:
            continue
        if "last_result" not in task:
            continue
        datetime_object = datetime.strptime(task["last_result"]["date"], date_format)
        if datetime_object.date() != datetime.today().date():
            continue
        service = task["name"].split("-")[0].strip()
        errors = task["last_result"]["count"]["error"]
        warnings = task["last_result"]["count"]["warning"]
        results.append({"service": service, "errors": errors, "warnings": warnings})
    return results


def generate_dataset_counters(results: List[dict]) -> List[dict]:
    """Generate Geckoboard dataset from Pa11y test result counters.

    It is assumed that input results are from today.

    Every item in the result dataset contains aggregate number of:
    * errors
    * warnings
    * tested pages per service
    and today's date.

    Example result:
     [
     ...
     {'date': '2020-05-18',
      'service': 'SOO',
      'errors': 33,
      'warnings': 40,
      'pages': 4},
     {'date': '2020-05-18',
      'service': 'SSO',
      'errors': 6,
      'warnings': 8,
      'pages': 2}
     ]
    """
    dict_counter = defaultdict(Counter)
    for item in results:
        service_name = item["service"]
        counter_values = {k: item[k] for k in ["errors", "warnings"]}
        dict_counter[service_name].update(counter_values)
        dict_counter[service_name].update({"pages": 1})
    date = datetime.today().strftime("%Y-%m-%d")
    return [
        {"date": date, "service": service_name, **dict(counters)}
        for service_name, counters in dict_counter.items()
    ]
