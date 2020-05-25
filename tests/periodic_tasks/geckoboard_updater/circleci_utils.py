# -*- coding: utf-8 -*-
import csv
from collections import defaultdict
from datetime import datetime
from io import StringIO
from os.path import basename, splitext
from typing import List
from xml.etree import ElementTree

import requests
from retrying import retry

from circleclient.circleclient import CircleClient

# Mapping of CircleCI job names to human friendly ones
DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS = {
    "Content diffs": {
        "domestic_compare_prod_and_dev_pages": "Domestic Prod Dev",
        "domestic_compare_prod_and_stage_pages": "Domestic Prod Stage",
        "domestic_compare_prod_and_uat_pages": "Domestic Prod UAT",
        "domestic_compare_stage_and_uat_pages": "Domestic Stage UAT",
        "domestic_compare_stage_and_dev_pages": "Domestic Stage Dev",
        "international_compare_prod_and_uat_pages": "International Prod UAT",
        "international_compare_prod_and_stage_pages": "International Prod Stage",
        "international_compare_stage_and_uat_pages": "International Stage UAT",
        "international_compare_stage_and_dev_pages": "International Stage Dev",
    },
    "Availability of CMS pages": {
        "check_cms_pages_on_production_return_200": "Prod. CMS pages return 200 OK",
    },
    "Production CMS page status report": {
        "generate_cms_page_status_report_for_prod": "Prod. CMS page status report",
    },
    "Dead links": {
        "check_for_dead_links_on_prod": "Prod Dead links",
        "check_for_dead_links_on_uat": "UAT Dead links",
        "check_for_dead_links_on_stage": "Stage Dead links",
        "check_for_dead_links_on_dev": "Dev Dead links",
    },
}

USEFUL_CONTENT_TESTS_JOB_NAME_MAPPINGS = {
    "check_cms_pages_on_production_return_200": "Prod. CMS pages return 200 OK",
    "check_for_dead_links_on_prod": "Dead links - Prod",
    "check_for_dead_links_on_uat": "Dead links - UAT",
    "check_for_dead_links_on_stage": "Dead links - Stage",
    "check_for_dead_links_on_dev": "Dead links - Dev",
}

DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS = {
    "load_cms_tests_stage": "Load STAGE CMS",
    "load_domestic_tests_stage": "Load STAGE Domestic",
    "load_erp_tests_stage": "Load STAGE ERP",
    "load_fab_tests_stage": "Load STAGE FAB",
    "load_fas_tests_stage": "Load STAGE FAS",
    "load_international_tests_stage": "Load STAGE International",
    "load_invest_tests_stage": "Load STAGE Invest",
    "load_isd_tests_stage": "Load STAGE ISD",
    "load_profile_tests_stage": "Load STAGE Profile",
    "load_soo_tests_stage": "Load STAGE SOO",
}

DIRECTORY_TESTS_JOB_NAME_MAPPINGS = {
    "dev_parallel_browser_tests_using_circleci": "Browser Dev",
    "func_fas_test_dev": "Dev FAS",
    "func_international_test_dev": "Dev Int",
    "func_sso_test_dev": "Dev SSO",
    "func_profile_test_dev": "Dev SUD",
    "smoke_tests_dev": "Dev Smoke",
    "stage_parallel_browser_tests_using_circleci": "Browser Stage",
    "browser_all_firefox_stage": "Stage Firefox",
    "func_fas_test_stage": "Stage FAS",
    "func_international_test_stage": "Stage Int",
    "func_sso_test_stage": "Stage SSO",
    "func_profile_test_stage": "Stage SUD",
    "smoke_tests_stage": "Stage Smoke",
    "uat_parallel_browser_tests_using_circleci": "Browser UAT",
    "func_fas_test_uat": "UAT FAS",
    "func_international_test_uat": "UAT Int",
    "func_sso_test_uat": "UAT SSO",
    "func_profile_test_uat": "UAT SUD",
    "smoke_tests_uat": "UAT Smoke",
}

DIRECTORY_TESTS_JOB_NAME_MAPPINGS.update(DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS)

DIRECTORY_SERVICE_JOB_NAME_MAPPINGS = {
    "test": "Unit Tests",
    "flake8": "flake8",
}

DIRECTORY_CH_SEARCH_JOB_NAME_MAPPINGS = {"test": "Unit Tests"}


@retry(wait_fixed=10000, stop_max_attempt_number=2)
def recent_builds(
    circle_ci_client: CircleClient,
    project: str,
    *,
    username: str = "uktrade",
    limit: int = 10,
    branch: str = "master",
    offset: int = 0,
) -> List[dict]:
    return circle_ci_client.build.recent(
        username=username, project=project, limit=limit, branch=branch, offset=offset
    )


def last_build_per_job(builds: List[dict], job_mappings: dict) -> dict:
    # flatten nested dict of dicts with job name mappings
    if isinstance(list(job_mappings.values())[0], dict):
        job_mappings = {
            key: item
            for subdict in list(job_mappings.values())
            for key, item in subdict.items()
        }
    last_builds = {}
    for build in builds:
        if "workflows" not in build:
            print(
                f"Ignoring legacy CircleCI 1.0  build #{build['build_num']} "
                f"for {build['reponame']}"
            )
            continue
        if build["workflows"]["job_name"] in job_mappings:
            friendly_name = job_mappings[build["workflows"]["job_name"]]
            if friendly_name not in last_builds:
                last_builds[friendly_name] = build
                continue
    return last_builds


@retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_build_artifact_link(
    circle_ci_client: CircleClient,
    builds: dict,
    name: str,
    *,
    username: str = "uktrade",
) -> dict:
    """Fetch a link to single build artifact than matches specified name.

    Example result:
    {
      'International Prod Stage': 'https://32078-71367747-gh.circle-artifacts.com/0/reports/index.html',
    }
    """

    artifact_urls = {}
    for friendly_name, build in builds.items():
        build_num = build["build_num"]
        project_name = build["reponame"]
        artifacts = circle_ci_client.build.artifacts(username, project_name, build_num)
        if artifacts:
            for artifact in artifacts:
                if artifact["path"].endswith(name):
                    artifact_urls[friendly_name] = artifact["url"]
                    print(
                        f"Found a link to '{name}' among artifacts for '{friendly_name}' job #{build_num}"
                    )

    return artifact_urls


@retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_build_artifacts(
    circle_ci_client: CircleClient,
    builds: dict,
    extentions: List[str],
    *,
    username: str = "uktrade",
    decode_content: bool = True,
) -> dict:
    """Fetch build artifacts that match one of selected file extensions"""

    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    build_artifacts = {}
    for friendly_name, build in builds.items():
        build_num = build["build_num"]
        project_name = build["reponame"]
        if build["start_time"]:
            datetime_object = datetime.strptime(build["start_time"], date_format)
            run_date = datetime_object.strftime("%Y-%m-%d")
        else:
            run_date = "N/A"
        artifacts = circle_ci_client.build.artifacts(username, project_name, build_num)
        if artifacts:
            for artifact in artifacts:
                artifact["date"] = run_date
                artifact["build_num"] = build_num
            build_artifacts[friendly_name] = artifacts

    artifact_urls = defaultdict(list)
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            filename = basename(artifact["path"])
            _, extension = splitext(filename)
            if extension in extentions:
                url = {
                    "filename": filename,
                    "url": artifact["url"],
                    "date": artifact["date"],
                    "build_num": artifact["build_num"],
                }
                artifact_urls[friendly_name].append(url)
                print(
                    f"Found '{friendly_name}' build artifact {filename} in "
                    f"build #{artifact['build_num']}"
                )

    results = defaultdict(list)
    for friendly_name, artifacts in artifact_urls.items():
        for artifact in artifacts:
            filename = artifact["filename"]
            url = artifact["url"]
            build_num = artifact["build_num"]
            print(
                f"Fetching '{friendly_name}' build artifact: '{filename}' "
                f"from build #{build_num}"
            )
            response = requests.get(url)
            error = (
                f"Could not get {url} as CircleCI responded with "
                f"{response.status_code}: {response.content}"
            )
            assert response.status_code == 200, error
            if decode_content:
                content = response.content.decode("utf-8")
            else:
                content = response.content
            artifact.update({"content": content})
            results[friendly_name].append(artifact)

    return dict(results)


def xml_report_summary(xml_report: str) -> dict:
    """Extract root level attributes from XML (Junit) report

    JUnit report should contain following attributes:
        {'disabled': '0',
         'errors': '0',
         'failures': '9',
         'tests': '1421',
         'time': '655.9097394943237'}
    Only a subset of those attributes will be returned.
    """
    root = ElementTree.fromstring(xml_report)
    attributes = root.attrib
    if not attributes:
        # iterate over results from all test suites and aggregate basic stats
        test_suites_results = [child.attrib for child in root.getchildren()]
        attributes = defaultdict(int)
        for kid in test_suites_results:
            for key, value in kid.items():
                if key in ["errors", "failures", "tests"]:
                    attributes[key] += int(value)
        attributes = dict(attributes)

    return {
        "tests": int(attributes["tests"]),
        "errors": int(attributes["errors"]),
        "failures": int(attributes["failures"]),
    }


def last_workflow_test_results(builds: dict) -> dict:
    result = {}
    github_avatar = (
        "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    )
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    for job_name, build in builds.items():

        build_time = 0
        if build["build_time_millis"]:
            build_time = round(build["build_time_millis"] / 1000)

        if build["user"]["is_user"]:
            user_avatar = build["user"]["avatar_url"]
            user_name = build["user"]["name"]
        else:
            user_avatar = github_avatar
            user_name = "github"

        if not build["start_time"]:
            last_build_date = "N/A"
        else:
            datetime_object = datetime.strptime(build["start_time"], date_format)
            last_build_date = datetime_object.strftime("%d %b %H:%M")

        result[job_name] = {
            "start_time": last_build_date,
            "build_time": build_time,
            "build_url": build["build_url"],
            "status": build["status"],
            "user_avatar": user_avatar,
            "user_name": user_name,
        }

    return result


def last_build_test_results(
    circle_ci_client: CircleClient,
    project_name: str,
    job_name_mappings: dict,
    *,
    limit: int = 10,
) -> dict:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    build_per_job = last_build_per_job(recent, job_name_mappings)
    return last_workflow_test_results(build_per_job)


def last_directory_tests_results(circle_ci_client: CircleClient) -> dict:
    return last_build_test_results(
        circle_ci_client,
        "directory-tests",
        job_name_mappings=DIRECTORY_TESTS_JOB_NAME_MAPPINGS,
        limit=100,
    )


def last_periodic_tests_results(circle_ci_client: CircleClient,) -> dict:
    return last_build_test_results(
        circle_ci_client,
        "directory-tests",
        job_name_mappings=DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS,
        limit=100,
    )


def last_useful_content_tests_results(circle_ci_client: CircleClient) -> dict:
    return last_build_test_results(
        circle_ci_client,
        "directory-tests",
        job_name_mappings=USEFUL_CONTENT_TESTS_JOB_NAME_MAPPINGS,
        limit=100,
    )


def last_useful_content_diff_report_links(circle_ci_client: CircleClient) -> dict:
    recent = recent_builds(circle_ci_client, "directory-tests", limit=100)
    build_per_job = last_build_per_job(
        recent, DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS["Content diffs"]
    )
    return get_build_artifact_link(circle_ci_client, build_per_job, "index.html")


def last_useful_production_cms_page_status_report_link(
    circle_ci_client: CircleClient,
) -> dict:
    recent = recent_builds(circle_ci_client, "directory-tests", limit=100)
    build_per_job = last_build_per_job(
        recent,
        DIRECTORY_PERIODIC_TESTS_JOB_NAME_MAPPINGS["Production CMS page status report"],
    )
    return get_build_artifact_link(circle_ci_client, build_per_job, "index.html")


def last_directory_service_build_results(circle_ci_client: CircleClient) -> dict:
    return {
        "API": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-api",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "FAB": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-ui-buyer",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "Domestic": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="great-domestic-ui",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "SSO": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "Profile": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso-profile",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "SSO Proxy": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso-proxy",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "CH Search": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-companies-house-search",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "CMS": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-cms",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "International": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="great-international-ui",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "Forms API": last_build_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-forms-api",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
    }


def parse_locust_stats_csv(csv_content: str) -> List[dict]:
    return [dict(endpoint) for endpoint in csv.DictReader(StringIO(csv_content))]


def extract_response_time_distribution_from_csv(
    csv_content: str,
    test_name: str,
    test_date: str,
    *,
    ignored_results: List[str] = ["aggregated"],
    ignored_columns: List[str] = [
        "failure count",
        "median response time",
        "average response time",
        "min response time",
        "max response time",
        "average content size",
        "requests/s",
        "failures/s",
        "66%",
        "80%",
        "98%",
        "99.9%",
        "99.99%",
        "99.999%",
    ],
) -> List[dict]:

    parsed_csv_results = parse_locust_stats_csv(csv_content)

    clean_results = []
    for result in parsed_csv_results:
        if result["Name"].lower() in ignored_results:
            continue

        # in order to reduce number of fields in the dataset (Geckoboard
        # accepts max 10 fields per dataset) we're replacing existing result
        # name with the "test name" e.g. "Load STAGE FAB" and set the endpoint
        # property to contain both HTTP Method and original result Name
        # https://api-docs.geckoboard.com/#schemas-and-types
        result["endpoint"] = f'{result["Type"]} {result["Name"]}'
        result.pop("Type")
        result.pop("Name")

        clean_result = {}
        for key, value in result.items():
            if key.lower() in ignored_columns:
                continue
            if key == "Request Count":
                clean_key = "requests"
            else:
                clean_key = key.replace("%", "").strip().lower()
            if value == "N/A":
                # Geckoboard requires that values for missing dataset entries
                # be set to None
                # https://api-docs.geckoboard.com/#number-format
                clean_result[clean_key] = None
            else:
                clean_value = int(value) if value.isnumeric() else value
                clean_result[clean_key] = clean_value

        clean_result["name"] = test_name
        clean_result["date"] = test_date
        clean_results.append(clean_result)
    return clean_results


def replace_all(text: str, replacements: dict) -> str:
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def extract_response_time_metrics_from_csv(
    csv_content: str,
    test_name: str,
    test_date: str,
    *,
    ignored_results: List[str] = ["aggregated"],
    ignored_metrics: List[str] = [
        "average content size",
        "failures/s",
        "50%",
        "66%",
        "75%",
        "80%",
        "90%",
        "95%",
        "98%",
        "99%",
        "99.9%",
        "99.99%",
        "99.999%",
        "100%",
    ],
) -> List[dict]:
    """Takes Locust's results_stats.csv & converts it into Geckoboard dataset.

    It takes a string containing Locust's stats CSV file and turns it into
    a list of dicts which are structured to match Geckoboard's load tests
    dataset locust_response_time_metrics

    An example results_stats.csv file generated by Locust v.1.0+ looks like this:
        "Type","Name","Request Count","Failure Count","Median Response Time","Average Response Time","Min Response Time","Max Response Time","Average Content Size","Requests/s","Failures/s","50%","66%","75%","80%","90%","95%","98%","99%","99.9%","99.99%","99.999%","100%"  # noqa
        "GET","/?category_id=[]",2,0,224,338,224,452,33797,2.75,0.00,450,450,450,450,450,450,450,450,450,450,450,450
        "None","Aggregated",2,0,224,338,224,452,33797,2.75,0.00,450,450,450,450,450,450,450,450,450,450,450,450

    This method will:
        * ignore all metrics define in ignored_metrics argument
        * skip "Aggregated" row
        * rename few metrics to match field names defined in locust_response_time_metrics dataset

    An example output will look like this:
    [
         {'requests': 290,
          'name': 'Load STAGE FAB',
          'date': '2018-10-22',
          'failures': 0,
          'median_response_time': 110,
          'average_response_time': 171,
          'min_response_time': 85,
          'max_response_time': 757,
          'requests_per_s': 1.9,
          'endpoint': 'GET /'
         },
         {'requests': 282,
          'name': 'Load STAGE FAB',
          'date': '2018-10-22',
          'failures': 0,
          'median_response_time': 120,
          'average_response_time': 193,
          'min_response_time': 85,
          'max_response_time': 2194,
          'requests_per_s': 1.85,
          'endpoint': 'POST /?company_name=[name]&company_number=[number]'},
         {'requests': 324,
          'name': 'Load STAGE FAB',
          'date': '2018-10-22',
          'failures': 0,
          'median_response_time': 170,
          'average_response_time': 223,
          'min_response_time': 140,
          'max_response_time': 2577,
          'requests_per_s': 2.13,
          'endpoint': 'GET api/internal/companies-house-search/?term=[term]'}
    ]
    """  # flake8: noqa
    parsed_csv_results = parse_locust_stats_csv(csv_content)

    clean_results = []
    for result in parsed_csv_results:
        if result["Name"].lower() in ignored_results:
            continue

        # in order to reduce number of fields in the dataset (Geckoboard
        # accepts max 10 fields per dataset) we're replacing existing result
        # name with the "test name" e.g. "Load STAGE FAB" and set the endpoint
        # property to contain both HTTP Method and original result Name
        result["endpoint"] = f'{result["Type"]} {result["Name"]}'
        result.pop("Type")
        result.pop("Name")

        clean_result = {}
        for metric_name, metric_value in result.items():
            if metric_name.lower() in ignored_metrics:
                continue
            if metric_name.lower() == "failure count":
                clean_key = "failures"
            elif metric_name.lower() == "request count":
                clean_key = "requests"
            else:
                replacements = {"# ": "", "/": "_per_", " ": "_"}
                clean_key = replace_all(metric_name, replacements).strip().lower()
            if metric_value == "N/A":
                # Geckoboard requires that values for missing dataset entries
                # be set to None
                # https://developer.geckoboard.com/?curl#number-format
                clean_result[clean_key] = None
            else:
                if clean_key == "requests_per_s":
                    clean_value = float(metric_value)
                else:
                    clean_value = (
                        int(metric_value) if metric_value.isnumeric() else metric_value
                    )
                clean_result[clean_key] = clean_value
            clean_result["name"] = test_name
            clean_result["date"] = test_date
        clean_results.append(clean_result)
    return clean_results


def get_load_test_response_time_distribution(
    build_artifacts: dict, *, artifact_filename: str = "results_stats.csv",
) -> List[dict]:
    results = []
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"] == artifact_filename:
                csv_content = artifact["content"]
                test_date = artifact["date"]
                parsed = extract_response_time_distribution_from_csv(
                    csv_content=csv_content,
                    test_name=friendly_name,
                    test_date=test_date,
                )
                results += parsed

    return results


def get_load_test_response_time_metrics(
    build_artifacts: dict, *, artifact_filename: str = "results_stats.csv"
) -> List[dict]:
    results = []
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"] == artifact_filename:
                csv_content = artifact["content"]
                test_date = artifact["date"]
                parsed = extract_response_time_metrics_from_csv(
                    csv_content=csv_content,
                    test_name=friendly_name,
                    test_date=test_date,
                )
                results += parsed

    return results


def last_load_test_artifacts(
    circle_ci_client: CircleClient,
    project_name: str,
    job_name_mappings: dict,
    *,
    limit: int = 50,
) -> dict:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    filtered_builds = last_build_per_job(recent, job_name_mappings)
    return get_build_artifacts(circle_ci_client, filtered_builds, extentions=[".csv"])


def parse_junit_results(build_artifacts: dict, metric: str) -> List[dict]:
    results = []
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"].endswith(".xml"):
                parsed = xml_report_summary(artifact["content"])
                parsed["environment"] = friendly_name
                parsed["date"] = artifact["date"]
                parsed["metric"] = metric
                results.append(parsed)

    return results


def last_tests_results_from_junit_artifacts(
    circle_ci_client: CircleClient,
    project_name: str,
    job_name_mappings: dict,
    *,
    limit: int = 100,
) -> List[dict]:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    result = []
    for metric, mapping in job_name_mappings.items():
        filtered_builds = last_build_per_job(recent, mapping)
        artifacts = get_build_artifacts(
            circle_ci_client, filtered_builds, extentions=[".xml"]
        )
        result += parse_junit_results(artifacts, metric)
    return result
