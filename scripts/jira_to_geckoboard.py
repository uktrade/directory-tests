# -*- coding: utf-8 -*-
import os
from datetime import date
from typing import List

from collections import namedtuple
from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient

# Get credentials from env variables
GECKOBOARD_API_KEY = os.environ['GECKOBOARD_API_KEY']
JIRA_HOST = os.environ['JIRA_HOST']
JIRA_USERNAME = os.environ['JIRA_USERNAME']
JIRA_PASSWORD = os.environ['JIRA_PASSWORD']

# Instantiate clients
JIRA_CLIENT = JiraClient(JIRA_HOST, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)

# other variables
TODAY = date.today().isoformat()

# Jira JQL queries
JQL_KANBAN_BUGS = "project = ED AND issuetype = Bug AND status != Backlog AND status != Done ORDER BY created DESC"
JQL_BACKLOG_BUGS = "project = ED AND issuetype = Bug AND status = Backlog ORDER BY created DESC"
JQL_MANUAL_VS_AUTOMATED = "project = ED AND resolution = Unresolved AND labels in (qa_auto, qa_manual) ORDER BY priority DESC, updated DESC"
JQL_SCENARIOS_TO_AUTOMATE = "project = ED AND issuetype in (Task, Sub-task) AND resolution = Unresolved AND labels = qa_automated_scenario ORDER BY created DESC"

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
