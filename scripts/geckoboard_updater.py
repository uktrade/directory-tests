# -*- coding: utf-8 -*-
import os
from collections import namedtuple, Counter
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
JQL_BUGS_CLOSED_TODAY = """
PROJECT in (ED) 
AND issuetype = Bug 
AND Status CHANGED FROM (Backlog, Planning, "Blocked!", "Design To Do", 
"Design - ready", "Design - in Progress", "Sign-off", "User research", 
"Dev - Planning", "Dev - selected", "Dev To Do", "Dev - ready", 
"Dev - in progress", "Dev - code review", Testing) 
TO (Closed, Done, "Release Candidate", Release) 
DURING (-0d, now()) 
ORDER BY key ASC, updated DESC
"""
JQL_TICKETS_CLOSED_TODAY = """
PROJECT in (ED) 
AND issuetype != Bug 
AND Status CHANGED FROM (Backlog, Planning, "Blocked!", "Design To Do", 
"Design - ready", "Design - in Progress", "Sign-off", "User research", 
"Dev - Planning", "Dev - selected", "Dev To Do", "Dev - ready", 
"Dev - in progress", "Dev - code review", Testing) 
TO (Closed, Done, "Release Candidate", Release) 
DURING (-0d, now()) 
ORDER BY key ASC, updated DESC
"""

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

# Number of bugs closed today (moved to Close, Release or Release Candidate)
DATASET_BUGS_CLOSED_TODAY_NAME = 'export.bugs_closed_today'
DATASET_BUGS_CLOSED_TODAY_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'closed': {'type': 'number', 'name': 'Bugs closed today', 'optional': False}
}
DATASET_BUGS_CLOSED_TODAY_UNIQUE_BY = ['date']

# Number of tickets (without bugs) closed today (moved to Close, Release 
# or Release Candidate)
DATASET_TICKETS_CLOSED_TODAY_NAME = 'export.tickets_closed_today'
DATASET_TICKETS_CLOSED_TODAY_FIELDS = {
    'date': {'type': 'date', 'name': 'Date', 'optional': False},
    'closed': {'type': 'number', 'name': 'Tickets closed today', 'optional': False}
}
DATASET_TICKETS_CLOSED_TODAY_UNIQUE_BY = ['date']


DataSets = namedtuple('DataSets',
                      [
                          'ON_KANBAN_BY_LABELS', 'IN_BACKLOG',
                          'AUTO_VS_MANUAL', 'TO_AUTOMATE',
                          'UNLABELLED_ON_KANBAN', 'UNLABELLED_IN_BACKLOG',
                          'IN_BACKLOG_BY_LABELS', 'BUGS_CLOSED_TODAY',
                          'TICKETS_CLOSED_TODAY'
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

    bugs_closed_today = gecko_client.datasets.find_or_create(
        DATASET_BUGS_CLOSED_TODAY_NAME,
        DATASET_BUGS_CLOSED_TODAY_FIELDS,
        DATASET_BUGS_CLOSED_TODAY_UNIQUE_BY)

    tickets_closed_today = gecko_client.datasets.find_or_create(
        DATASET_TICKETS_CLOSED_TODAY_NAME,
        DATASET_TICKETS_CLOSED_TODAY_FIELDS,
        DATASET_TICKETS_CLOSED_TODAY_UNIQUE_BY)

    return DataSets(
        on_kanban_by_labels, in_backlog, auto_vs_manual, to_automate,
        unlabelled_on_kanban, unlabelled_in_backlog, in_backlog_by_labels,
        bugs_closed_today, tickets_closed_today)


def find_issues(
        jql: str, *, max_results: int = 100,
        fields: str = 'key,labels,summary') -> dict:
    """Run Jira JQL and return result as JSON."""
    return JIRA_CLIENT.search_issues(
        jql_str=jql, maxResults=max_results, json_result=True, fields=fields)


def count_labels(issues: list) -> Counter:
    counter = Counter()
    for issue in issues:
        for label in issue['fields']['labels']:
            counter[label] += 1
    return counter


def filter_labels_by_prefix(
        labels: Counter, prefix: str, *, remove_prefix: bool = True) -> Counter:
    filtered = dict(filter(lambda x: x[0].startswith(prefix), labels.items()))
    if remove_prefix:
        filtered = {k.replace(prefix, ''): v for k, v in filtered.items()}
    return Counter(filtered)


def filter_out_ignored_labels(
        counter: Counter, ignored_labels: List[str]) -> Counter:
    if not ignored_labels:
        return counter
    filtered = filter(lambda x: x[0] not in ignored_labels, counter.items())
    return Counter(dict(filtered))


def filter_by_sought_labels(
        counter: Counter, sought_labels: List[str]) -> Counter:
    if not sought_labels:
        return counter
    filtered = filter(lambda x: x[0] in sought_labels, counter.items())
    return Counter(dict(filtered))


def get_quantity_per_label(
        jql_query_result: dict, *, label_prefix: str = 'qa_',
        remove_label_prefix: bool = True, ignored_labels: List[str] = None,
        look_for: List[str] = None) -> dict:
    issues = jql_query_result['issues']
    all_labels = count_labels(issues)
    by_prefix = filter_labels_by_prefix(
        all_labels, label_prefix, remove_prefix=remove_label_prefix)
    without_ignored = filter_out_ignored_labels(by_prefix, ignored_labels)
    sought = filter_by_sought_labels(without_ignored, look_for)
    return dict(sought)


def get_number_of_bugs_on_kanban_board_by_labels() -> List[dict]:
    kanban_bugs = find_issues(JQL_KANBAN_BUGS)
    types = get_quantity_per_label(
            kanban_bugs, ignored_labels=['auto', 'manual'])
    result = []
    for bug_type in types:
        item = {'date': TODAY, 'label': bug_type, 'quantity': types[bug_type]}
        result.append(item)
    return result


def get_number_of_bugs_in_backlog_by_labels() -> List[dict]:
    backlog_bugs = find_issues(JQL_BACKLOG_BUGS)
    types = get_quantity_per_label(
            backlog_bugs, ignored_labels=['auto', 'manual'])
    result = []
    for bug_type in types:
        item = {'date': TODAY, 'label': bug_type, 'quantity': types[bug_type]}
        result.append(item)
    return result


def get_number_of_unlabelled_bugs_on_kanban_board() -> List[dict]:
    unlabelled = find_issues(JQL_KANBAN_BUGS)
    number = len([issue for issue in unlabelled['issues']
                  if not issue['fields']['labels']])
    return [{'date': TODAY, 'quantity': number}]


def get_number_of_unlabelled_bugs_in_backlog() -> List[dict]:
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


def get_number_of_bugs_closed_today() -> List[dict]:
    closed = find_issues(JQL_BUGS_CLOSED_TODAY)
    return [{'date': TODAY, 'closed': closed['total']}]


def get_number_of_tickets_closed_today() -> List[dict]:
    closed = find_issues(JQL_TICKETS_CLOSED_TODAY)
    return [{'date': TODAY, 'closed': closed['total']}]


def circle_ci_get_recent_builds(
        project: str, *, username: str = 'uktrade', limit: int = 20,
        branch: str = 'master') -> List[dict]:
    return CIRCLE_CI_CLIENT.build.recent(
        username=username, project=project, limit=limit, branch=branch)


def circle_ci_get_last_workflow_id(recent_builds: List[dict]) -> str:
    result = ''
    for build in recent_builds:
        if build['status'] == 'not_run':
            print(
                'Ignoring skipped {} build: {}'
                .format(build['reponame'], build['build_num']))
            continue
        if 'workflows' in build:
            result = build['workflows']['workflow_id']
            break
    return result


def circle_ci_get_builds_for_workflow(recent_circle_ci_builds: List[dict],
                                      last_workflow_id: str) -> List[dict]:
    return [build for build in recent_circle_ci_builds
            if build['workflows']['workflow_id'] == last_workflow_id]


def circle_ci_get_last_workflow_test_results(
        last_workflow_builds: List[dict], *,
        job_name_mappings: dict = CIRCLE_CI_WORKFLOW_JOB_NAME_MAPPINGS
) -> dict:
    most_recent_build = last_workflow_builds[0]
    frmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    last_build_date = ""
    if most_recent_build['start_time']:
        datetime_object = datetime.strptime(
            most_recent_build['start_time'], frmt)
        last_build_date = datetime_object.strftime('%d %b %H:%M')
    skipped = True if last_workflow_builds[0]['status'] == 'not_run' else False
    test_results = {
        'user_avatar': most_recent_build['user']['avatar_url'],
        'user_name': most_recent_build['user']['name'],
        'user_login': most_recent_build['user']['login'],
        'workflow_id': most_recent_build['workflows']['workflow_id'],
        'last_build_date': last_build_date,
        'skipped': skipped
    }
    for build in last_workflow_builds:
        job_name = build['workflows']['job_name']
        if job_name in job_name_mappings.keys():
            friendly_name = job_name_mappings[job_name]
            build_time = 0
            if build['build_time_millis']:
                build_time = round(build['build_time_millis'] / 1000)
            test_results[friendly_name] = {
                'start_time': build['start_time'],
                'stop_time': build['stop_time'],
                'build_time': build_time,
                'build_num': build['build_num'],
                'build_url': build['build_url'],
                'status': build['status']
            }
    return test_results


def circle_ci_get_last_build_results(build: dict) -> dict:
    frmt = '%Y-%m-%dT%H:%M:%S.%fZ'
    last_build_date = ""
    if build['start_time']:
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


def circle_ci_get_last_test_results(
        project_name: str, *, ignored_workflows: List[str] = None,
        limit: int = None) -> dict:
    recent_builds = circle_ci_get_recent_builds(project_name, limit=limit)
    if ignored_workflows:
        recent_builds = [build for build in recent_builds
                         if build['workflows']['workflow_name']
                         not in ignored_workflows]
    last_workflow_id = circle_ci_get_last_workflow_id(recent_builds)
    if last_workflow_id:
        last_workflow_builds = circle_ci_get_builds_for_workflow(
            recent_builds, last_workflow_id)
        result = circle_ci_get_last_workflow_test_results(last_workflow_builds)
    else:
        most_recent_build = recent_builds[0]
        result = circle_ci_get_last_build_results(most_recent_build)
    return result


def circle_ci_get_last_test_results_per_project() -> dict:
    ignored_workflows = ['refresh_geckoboard_periodically']
    return {
        'Tests': circle_ci_get_last_test_results(
            'directory-tests', ignored_workflows=ignored_workflows, limit=100),
        'API': circle_ci_get_last_test_results('directory-api'),
        'FAS': circle_ci_get_last_test_results('directory-ui-supplier'),
        'FAB': circle_ci_get_last_test_results('directory-ui-buyer'),
        'ExRed': circle_ci_get_last_test_results('directory-ui-export-readiness'),
        'SSO': circle_ci_get_last_test_results('directory-sso'),
        'SUD': circle_ci_get_last_test_results('directory-sso-profile'),
        'SSO Proxy': circle_ci_get_last_test_results('directory-sso-proxy'),
        'CH Search': circle_ci_get_last_test_results('directory-companies-house-search'),
    }


def geckoboard_get_job_color(status: str) -> str:
    status_colors = {
        'failed': 'red',
        'fixed': 'green',
        'not_run': 'grey',
        'queued': 'purple',
        'running': 'blue',
        'success': 'green',
    }
    return status_colors[status]


def geckoboard_get_build_summary(test_results: dict) -> str:
    details = {
        'start': test_results['start_time'],
        'stop': test_results['stop_time'],
        'seconds': test_results['build_time'],
        'number': test_results['build_num']
    }
    return ("Build #{number} took {seconds} seconds to run. It started at "
            "{start} and finished at {stop}".format(**details))


def geckoboard_generate_table_rows_for_test_results(
        services_test_results: dict) -> str:
    workflow_row_template = """
        <tr style="font-size:20pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td></td>
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
    build_row_template = """
        <tr style="font-size:20pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td><a target="_blank" href="{build_url}" style="color:{status_color}" title="{summary}">{status}</a></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    """
    result = ''
    for service_name, test_results in services_test_results.items():
        if ('workflow_id' not in test_results) or (test_results['skipped']):
            result += build_row_template.format(
                service_name=service_name,
                user_avatar_url=test_results['user_avatar'],
                user_name=test_results['user_name'],

                last_build_date=test_results['last_build_date'],
                build_url=test_results['build_url'],
                status_color=geckoboard_get_job_color(test_results['status']),
                summary=geckoboard_get_build_summary(test_results),
                status=test_results['status'].capitalize(),
            )
            continue
        smoke = test_results['Smoke']
        urls = test_results['URLs']
        fab = test_results['FAB']
        fas = test_results['FAS']
        sso = test_results['SSO']
        sud = test_results['SUD']
        chrome = test_results['ER Chrome']
        firefox = test_results['ER Firefox']
        result += workflow_row_template.format(
            service_name=service_name,
            user_avatar_url=test_results['user_avatar'],
            user_name=test_results['user_name'],

            last_build_date=test_results['last_build_date'],

            smoke_build_url=smoke['build_url'],
            smoke_status_color=geckoboard_get_job_color(smoke['status']),
            smoke_build_summary=geckoboard_get_build_summary(smoke),
            smoke_status=smoke['status'].capitalize(),

            urls_build_url=urls['build_url'],
            urls_status_color=geckoboard_get_job_color(urls['status']),
            urls_build_summary=geckoboard_get_build_summary(urls),
            urls_status=urls['status'].capitalize(),

            fab_build_url=fab['build_url'],
            fab_status_color=geckoboard_get_job_color(fab['status']),
            fab_build_summary=geckoboard_get_build_summary(fab),
            fab_status=fab['status'].capitalize(),

            fas_build_url=fas['build_url'],
            fas_status_color=geckoboard_get_job_color(fas['status']),
            fas_build_summary=geckoboard_get_build_summary(fas),
            fas_status=fas['status'].capitalize(),

            sso_build_url=sso['build_url'],
            sso_status_color=geckoboard_get_job_color(sso['status']),
            sso_build_summary=geckoboard_get_build_summary(sso),
            sso_status=sso['status'].capitalize(),

            sud_build_url=sud['build_url'],
            sud_status_color=geckoboard_get_job_color(sud['status']),
            sud_build_summary=geckoboard_get_build_summary(sud),
            sud_status=sud['status'].capitalize(),

            exred_chrome_build_url=chrome['build_url'],
            exred_chrome_status_color=geckoboard_get_job_color(chrome['status']),
            exred_chrome_build_summary=geckoboard_get_build_summary(chrome),
            exred_chrome_status=chrome['status'].capitalize(),

            exred_firefox_build_url=firefox['build_url'],
            exred_firefox_status_color=geckoboard_get_job_color(firefox['status']),
            exred_firefox_build_summary=geckoboard_get_build_summary(firefox),
            exred_firefox_status=firefox['status'].capitalize(),
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
        <th>Build</th>
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
    bugs_closed_today = get_number_of_bugs_closed_today()
    tickets_closed_today = get_number_of_tickets_closed_today()

    print('Bugs by labels on the Kanban board: ', kanban_bugs_by_labels)
    print('Unlabelled bugs on the Kanban board: ', unlabelled_on_kanban)
    print('Number of bugs in Backlog', in_backlog)
    print('Bugs by labels in the Backlog: ', backlog_bugs_by_labels)
    print('Unlabelled bugs in Backlog: ', unlabelled_in_backlog)
    print('Automated vs Manual: ', auto_vs_manual)
    print('Number of scenarios to automate: ', to_automate)
    print('Number of bugs closed today: ', bugs_closed_today)
    print('Number of tickets closed today: ', tickets_closed_today)

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
    datasets.BUGS_CLOSED_TODAY.post(bugs_closed_today)
    datasets.TICKETS_CLOSED_TODAY.post(tickets_closed_today)
    print('All datasets pushed')

    print('Pushing tests results to Geckoboard widget')
    geckoboard_push_test_results()
    print('Tests results successfully pushed to Geckoboard widget')
