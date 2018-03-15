# -*- coding: utf-8 -*-
import os
from collections import namedtuple
from datetime import date, datetime
from typing import List

import requests
from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient
from circleclient import circleclient

# Get credentials from env variables
GECKOBOARD_API_KEY = os.environ['GECKOBOARD_API_KEY']
GECKOBOARD_TEST_RESULTS_WIDGET_KEY = os.environ['GECKOBOARD_TEST_RESULTS_WIDGET_KEY']
GECKOBOARD_PUSH_URL = os.getenv('GECKOBOARD_PUSH_URL', 'https://push.geckoboard.com/v1/send/')
JIRA_HOST = os.environ['JIRA_HOST']
JIRA_USERNAME = os.environ['JIRA_USERNAME']
JIRA_PASSWORD = os.environ['JIRA_PASSWORD']
CIRCLE_CI_API_TOKEN = os.environ['CIRCLE_CI_API_TOKEN']

# Instantiate clients
JIRA_CLIENT = JiraClient(JIRA_HOST, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
CIRCLE_CI_CLIENT = circleclient.CircleClient(CIRCLE_CI_API_TOKEN)

# other variables
TODAY = date.today().isoformat()

# Jira JQL queries
JQL_KANBAN_BUGS = "project = ED AND issuetype = Bug AND status != Backlog AND status != Done ORDER BY created DESC"
JQL_BACKLOG_BUGS = "project = ED AND issuetype = Bug AND status = Backlog ORDER BY created DESC"
JQL_MANUAL_VS_AUTOMATED = "project = ED AND resolution = Unresolved AND labels in (qa_auto, qa_manual) ORDER BY priority DESC, updated DESC"
JQL_SCENARIOS_TO_AUTOMATE = "project = ED AND issuetype in (Task, Sub-task) AND resolution = Unresolved AND labels = qa_automated_scenario ORDER BY created DESC"

# Mapping of CircleCI job names to more human friendly ones
CIRCLE_CI_WORKFLOW_JOB_NAME_MAPPINGS = {
    'exred_tests_chrome': 'ER Chrome',
    'exred_tests_firefox': 'ER Firefox',
    'fab_functional_tests': 'FAB',
    'fas_functional_tests': 'FAS',
    'smoke_tests': 'Smoke',
    'smoke_tests_links_checker': 'URLs',
    'sso_functional_tests': 'SSO',
    'sud_functional_tests': 'SUD'
}

# Geckoboard datasets

###############################################################################
# KANBAN BOARD
###############################################################################
# Number of bugs on the Kanban board grouped by label (not in Backlog or Done)
DATASET_ON_KANBAN_BY_LABELS_NAME = 'export.bugs_wip_by_labels'
DATASET_ON_KANBAN_BY_LABELS_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'label': {'type': 'string', 'name': 'Label', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
}
DATASET_ON_KANBAN_BY_LABELS_UNIQUE_BY = ['date', 'label']

# Number of bugs on Kanban board without a `qa_*` label
DATASET_UNLABELLED_ON_KANBAN_NAME = 'export.bugs_unlabelled'
DATASET_UNLABELLED_ON_KANBAN_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
}
DATASET_UNLABELLED_ON_KANBAN_UNIQUE_BY = ['date']

###############################################################################
# BACKLOG
###############################################################################

# Number of bugs in the Backlog board grouped by label (not in Backlog or Done)
DATASET_BUGS_IN_BACKLOG_BY_LABELS_NAME = 'export.bugs_in_backlog_by_labels'
DATASET_BUGS_IN_BACKLOG_BY_LABELS_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'label': {'type': 'string', 'name': 'Label', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
}
DATASET_BUGS_IN_BACKLOG_BY_LABELS_UNIQUE_BY = ['date', 'label']

# Number of bugs in Backlog without a `qa_*` label
DATASET_UNLABELLED_IN_BACKLOG_NAME = 'export.bugs_unlabelled_in_backlog'
DATASET_UNLABELLED_IN_BACKLOG_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
}
DATASET_UNLABELLED_IN_BACKLOG_UNIQUE_BY = ['date']

# Number of bugs in the Backlog
DATASET_BUGS_IN_BACKLOG_NAME = 'export.bugs_in_backlog'
DATASET_BUGS_IN_BACKLOG_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
}
DATASET_BUGS_IN_BACKLOG_UNIQUE_BY = ['date']

###############################################################################
# OTHER
###############################################################################

# Number of scenarios to automate (tagged with `qa_automated_scenario`)
DATASET_TO_AUTOMATE_NAME = 'export.scenarios_to_automate'
DATASET_TO_AUTOMATE_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'quantity': {'type': 'number', 'name': 'Quantity', 'optional': False}
    }
DATASET_TO_AUTOMATE_UNIQUE_BY = ['date']

# Number of bugs on the Kanban board discovered manually or by automated tests
DATASET_VS_NAME = 'export.bugs_auto_vs_manual'
DATASET_VS_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'auto': {'type': 'number', 'name': 'automated tests', 'optional': False},
    'manual': {'type': 'number', 'name': 'manually', 'optional': False}
}
DATASET_VS_UNIQUE_BY = ['date']


DataSets = namedtuple('DataSets',
                      [
                          'ON_KANBAN_BY_LABELS', 'IN_BACKLOG',
                          'AUTO_VS_MANUAL', 'TO_AUTOMATE',
                          'UNLABELLED_ON_KANBAN', 'UNLABELLED_IN_BACKLOG',
                          'IN_BACKLOG_BY_LABELS'
                      ])


def create_datasets(gecko_client: GeckoClient) -> DataSets:
    """
    More on datasets.find_or_create()
    https://developer.geckoboard.com/api-reference/python/#findorcreate
    """
    on_kanban_by_labels = gecko_client.datasets.find_or_create(
        DATASET_ON_KANBAN_BY_LABELS_NAME, DATASET_ON_KANBAN_BY_LABELS_FIELDS,
        DATASET_ON_KANBAN_BY_LABELS_UNIQUE_BY)

    in_backlog = gecko_client.datasets.find_or_create(
        DATASET_BUGS_IN_BACKLOG_NAME, DATASET_BUGS_IN_BACKLOG_FIELDS,
        DATASET_BUGS_IN_BACKLOG_UNIQUE_BY)

    in_backlog_by_labels = gecko_client.datasets.find_or_create(
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_NAME,
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_FIELDS,
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_UNIQUE_BY
        )

    auto_vs_manual = gecko_client.datasets.find_or_create(
        DATASET_VS_NAME, DATASET_VS_FIELDS, DATASET_VS_UNIQUE_BY)

    to_automate = gecko_client.datasets.find_or_create(
        DATASET_TO_AUTOMATE_NAME, DATASET_TO_AUTOMATE_FIELDS,
        DATASET_TO_AUTOMATE_UNIQUE_BY)

    unlabelled_on_kanban = gecko_client.datasets.find_or_create(
        DATASET_UNLABELLED_ON_KANBAN_NAME, DATASET_UNLABELLED_ON_KANBAN_FIELDS,
        DATASET_UNLABELLED_ON_KANBAN_UNIQUE_BY)

    unlabelled_in_backlog = gecko_client.datasets.find_or_create(
        DATASET_UNLABELLED_IN_BACKLOG_NAME,
        DATASET_UNLABELLED_IN_BACKLOG_FIELDS,
        DATASET_UNLABELLED_IN_BACKLOG_UNIQUE_BY)

    return DataSets(
        on_kanban_by_labels, in_backlog, auto_vs_manual, to_automate,
        unlabelled_on_kanban, unlabelled_in_backlog, in_backlog_by_labels)


def find_issues(
        jql: str, *, max_results: int = 100,
        fields: str = 'key,labels,summary') -> dict:
    """Run Jira JQL and return result as JSON."""
    return JIRA_CLIENT.search_issues(
        jql_str=jql, maxResults=max_results, json_result=True, fields=fields)


def get_quantity_per_label(
        jql_query_result: dict, *, label_prefix: str = 'qa_',
        remove_label_prefix: bool = True, ignored_labels: List[str] = None,
        look_for: List[str] = None) -> dict:
    result = {}
    issues = jql_query_result['issues']
    for issue in issues:
        labels = [label for label in issue['fields']['labels']
                  if label.startswith(label_prefix)]
        for label in labels:
            if remove_label_prefix:
                label = label.replace(label_prefix, '')
            if ignored_labels:
                if label in ignored_labels:
                    continue
            if look_for:
                if label not in look_for:
                    continue
            if label in result:
                result[label] += 1
            else:
                result[label] = 1
    return result


def get_number_of_bugs_on_kanban_board_by_labels() -> List[dict]:
    kanban_bugs = find_issues(JQL_KANBAN_BUGS)
    types = get_quantity_per_label(
            kanban_bugs, ignored_labels=['auto', 'manual'])
    result = []
    for bug_type in types:
        item = {'date': TODAY, 'label': bug_type, 'quantity': types[bug_type]}
        result.append(item)
    return result


def get_number_of_bugs_in_backlog_by_labels():
    backlog_bugs = find_issues(JQL_BACKLOG_BUGS)
    types = get_quantity_per_label(
            backlog_bugs, ignored_labels=['auto', 'manual'])
    result = []
    for bug_type in types:
        item = {'date': TODAY, 'label': bug_type, 'quantity': types[bug_type]}
        result.append(item)
    return result


def get_number_of_unlabelled_bugs_on_kanban_board():
    unlabelled = find_issues(JQL_KANBAN_BUGS)
    number = len([issue for issue in unlabelled['issues']
                  if not issue['fields']['labels']])
    return [{'date': TODAY, 'quantity': number}]


def get_number_of_unlabelled_bugs_in_backlog():
    unlabelled = find_issues(JQL_BACKLOG_BUGS)
    number = len([issue for issue in unlabelled['issues']
                  if not issue['fields']['labels']])
    return [{'date': TODAY, 'quantity': number}]


def get_number_of_automated_vs_manual() -> List[dict]:
    vs = find_issues(JQL_MANUAL_VS_AUTOMATED)
    labels = get_quantity_per_label(vs, look_for=['auto', 'manual'])
    auto = labels['auto']
    manual = labels['manual']
    return [{'date': TODAY, 'auto': auto, 'manual': manual}]


def get_number_of_bugs_in_backlog() -> List[dict]:
    bugs_in_backlog = find_issues(JQL_BACKLOG_BUGS)
    dataset = [{'date': TODAY, 'quantity': bugs_in_backlog['total']}]
    return dataset


def get_number_of_scenarios_to_automate() -> List[dict]:
    scenarios_to_automate = find_issues(JQL_SCENARIOS_TO_AUTOMATE)
    return [{'date': TODAY, 'quantity': scenarios_to_automate['total']}]


def circle_ci_get_recent_builds(
        project: str, *, username: str = 'uktrade', limit: int = 20,
        branch: str = 'master') -> List[dict]:
    return CIRCLE_CI_CLIENT.build.recent(
        username=username, project=project, limit=limit, branch=branch)


def circle_ci_get_last_workflow_id(recent_builds: List[dict]) -> str:
    return recent_builds[0]['workflows']['workflow_id']


def circle_ci_get_builds_for_workflow(
        recent_circle_ci_builds: List[dict], last_workflow_id: str) -> List[dict]:
    return [build for build in recent_circle_ci_builds
            if build['workflows']['workflow_id'] == last_workflow_id]


def circle_ci_get_last_workflow_test_results(
        last_workflow_builds: List[dict], *,
        job_name_mappings: dict = CIRCLE_CI_WORKFLOW_JOB_NAME_MAPPINGS) -> dict:
    most_recent_build = last_workflow_builds[0]
    frmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    datetime_object = datetime.strptime(most_recent_build['start_time'], frmt)
    last_build_date = datetime_object.strftime('%d %b %H:%M')
    test_results = {
        'user_avatar': most_recent_build['user']['avatar_url'],
        'user_name': most_recent_build['user']['name'],
        'user_login': most_recent_build['user']['login'],
        'workflow_id': most_recent_build['workflows']['workflow_id'],
        'last_build_date': last_build_date
    }
    for build in last_workflow_builds:
        job_name = build['workflows']['job_name']
        if job_name in job_name_mappings.keys():
            friendly_name = job_name_mappings[job_name]
            test_results[friendly_name] = {
                'start_time': build['start_time'],
                'stop_time': build['stop_time'],
                'build_time': round(build['build_time_millis'] / 1000),
                'build_num': build['build_num'],
                'build_url': build['build_url'],
                'status': build['status']
            }
    return test_results


def circle_ci_get_last_build_results(build: dict) -> dict:
    frmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    datetime_object = datetime.strptime(build['start_time'], frmt)
    last_build_date = datetime_object.strftime('%d %b %H:%M')
    build_time = None
    if build['build_time_millis']:
        build_time = round(build['build_time_millis'] / 1000)
    test_results = {
        'user_avatar': build['user']['avatar_url'],
        'user_name': build['user']['name'],
        'user_login': build['user']['login'],
        'last_build_date': last_build_date,
        'start_time': build['start_time'],
        'stop_time': build['stop_time'],
        'build_time': build_time,
        'build_num': build['build_num'],
        'build_url': build['build_url'],
        'status': build['status']
    }
    return test_results


def circle_ci_get_last_test_results(project_name: str):
    recent_builds = circle_ci_get_recent_builds(project_name)
    last_workflow_id = circle_ci_get_last_workflow_id(recent_builds)
    last_workflow_builds = circle_ci_get_builds_for_workflow(
        recent_builds, last_workflow_id)
    return circle_ci_get_last_workflow_test_results(last_workflow_builds)


def circle_ci_get_last_test_results_per_project() -> dict:
    result = {
        'Directory Tests': circle_ci_get_last_test_results('directory-tests')
    }
    return result


def geckoboard_generate_table_rows_for_test_results(services_test_results: dict) -> str:
    row_template = """
        <tr style="font-size:20pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td><a target="_blank" href="{smoke_build_url}" style="color:{smoke_status_color}" title="{smoke_build_summary}">{smoke_status}</a></td>
            <td><a target="_blank" href="{urls_build_url}" style="color:{urls_status_color}" title="{urls_build_summary}">{urls_status}</td>
            <td><a target="_blank" href="{fab_build_url}" style="color:{fab_status_color}" title="{fab_build_summary}">{fab_status}</td>
            <td><a target="_blank" href="{fas_build_url}" style="color:{fas_status_color}" title="{fas_build_summary}">{fas_status}</td>
            <td><a target="_blank" href="{sso_build_url}" style="color:{sso_status_color}" title="{sso_build_summary}">{sso_status}</td>
            <td><a target="_blank" href="{sud_build_url}" style="color:{sud_status_color}" title="{sud_build_summary}">{sud_status}</td>
            <td><a target="_blank" href="{exred_chrome_build_url}" style="color:{exred_chrome_status_color}" title="{exred_chrome_build_summary}">{exred_chrome_status}</td>
            <td><a target="_blank" href="{exred_firefox_build_url}" style="color:{exred_firefox_status_color}" title="{exred_firefox_build_summary}">{exred_firefox_status}</td>
        </tr>
    """
    result = ''
    success_color = 'green'
    failed_color = 'red'
    for service_name, test_results in services_test_results.items():
        result += row_template.format(
            service_name=service_name,
            user_avatar_url=test_results['user_avatar'],
            user_name=test_results['user_name'],

            last_build_date=test_results['last_build_date'],

            smoke_build_url=test_results['Smoke']['build_url'],
            smoke_status_color=success_color if test_results['Smoke']['status'] == 'success' else failed_color,
            smoke_build_summary="",
            smoke_status=test_results['Smoke']['status'].capitalize(),

            urls_build_url=test_results['URLs']['build_url'],
            urls_status_color=success_color if test_results['URLs']['status'] == 'success' else failed_color,
            urls_build_summary="",
            urls_status=test_results['URLs']['status'].capitalize(),

            fab_build_url=test_results['FAB']['build_url'],
            fab_status_color=success_color if test_results['FAB']['status'] == 'success' else failed_color,
            fab_build_summary="",
            fab_status=test_results['FAB']['status'].capitalize(),

            fas_build_url=test_results['FAS']['build_url'],
            fas_status_color=success_color if test_results['FAS']['status'] == 'success' else failed_color,
            fas_build_summary="",
            fas_status=test_results['FAS']['status'].capitalize(),

            sso_build_url=test_results['SSO']['build_url'],
            sso_status_color=success_color if test_results['SSO']['status'] == 'success' else failed_color,
            sso_build_summary="",
            sso_status=test_results['SSO']['status'].capitalize(),

            sud_build_url=test_results['SUD']['build_url'],
            sud_status_color=success_color if test_results['SUD']['status'] == 'success' else failed_color,
            sud_build_summary="",
            sud_status=test_results['SUD']['status'].capitalize(),

            exred_chrome_build_url=test_results['ER Chrome']['build_url'],
            exred_chrome_status_color=success_color if test_results['ER Chrome']['status'] == 'success' else failed_color,
            exred_chrome_build_summary="",
            exred_chrome_status=test_results['ER Chrome']['status'].capitalize(),

            exred_firefox_build_url=test_results['ER Firefox']['build_url'],
            exred_firefox_status_color=success_color if test_results['ER Firefox']['status'] == 'success' else failed_color,
            exred_firefox_build_summary="",
            exred_firefox_status=test_results['ER Firefox']['status'].capitalize(),
        )
    return result


def geckoboard_generate_content_for_test_results_widget_update(
        test_results: dict) -> dict:
    table_template = """
    <table width="100%">
    <thead>
    <tr style="font-size:20pt">
        <th>Project</th>
        <th>When</th>
        <th>Smoke</th>
        <th>URLs</th>
        <th>FAB</th>
        <th>FAS</th>
        <th>SSO</th>
        <th>SUD</th>
        <th>ER Chrome</th>
        <th>ER Firefox</th>
    </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
    </table>
    """
    rows = geckoboard_generate_table_rows_for_test_results(test_results)
    text = table_template.format(rows=rows)
    message = {
        "api_key": GECKOBOARD_API_KEY,
        "data": {
            "item": [{"text": text, "type": 0}]
        }
    }
    return message


def geckoboard_push_test_results():
    last_test_results = circle_ci_get_last_test_results_per_project()
    message = geckoboard_generate_content_for_test_results_widget_update(
        last_test_results)
    url = GECKOBOARD_PUSH_URL + GECKOBOARD_TEST_RESULTS_WIDGET_KEY
    response = requests.post(url, json=message)
    assert response.status_code == 200


if __name__ == '__main__':
    kanban_bugs_by_labels = get_number_of_bugs_on_kanban_board_by_labels()
    backlog_bugs_by_labels = get_number_of_bugs_in_backlog_by_labels()
    unlabelled_on_kanban = get_number_of_unlabelled_bugs_on_kanban_board()
    unlabelled_in_backlog = get_number_of_unlabelled_bugs_in_backlog()
    auto_vs_manual = get_number_of_automated_vs_manual()
    in_backlog = get_number_of_bugs_in_backlog()
    to_automate = get_number_of_scenarios_to_automate()

    print('Bugs by labels on the Kanban board: ', kanban_bugs_by_labels)
    print('Unlabelled bugs on the Kanban board: ', unlabelled_on_kanban)
    print('Number of bugs in Backlog', in_backlog)
    print('Bugs by labels in the Backlog: ', backlog_bugs_by_labels)
    print('Unlabelled bugs in Backlog: ', unlabelled_in_backlog)
    print('Automated vs Manual: ', auto_vs_manual)
    print('Number of scenarios to automate: ', to_automate)

    print('Creating datasets in Geckoboard...')
    datasets = create_datasets(GECKO_CLIENT)
    print("All datasets properly created.")

    print('Pushing all datasets to Geckoboard')
    datasets.ON_KANBAN_BY_LABELS.post(kanban_bugs_by_labels)
    datasets.IN_BACKLOG_BY_LABELS.post(backlog_bugs_by_labels)
    datasets.UNLABELLED_ON_KANBAN.post(unlabelled_on_kanban)
    datasets.UNLABELLED_IN_BACKLOG.post(unlabelled_in_backlog)
    datasets.AUTO_VS_MANUAL.post(auto_vs_manual)
    datasets.IN_BACKLOG.post(in_backlog)
    datasets.TO_AUTOMATE.post(to_automate)
    print('All datasets pushed')

    print('Pushing tests results to Geckoboard widget')
    geckoboard_push_test_results()
    print('Tests results successfully pushed to Geckoboard widget')
