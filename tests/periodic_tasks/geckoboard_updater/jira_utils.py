# -*- coding: utf-8 -*-
from collections import Counter
from datetime import date
from enum import Enum
from typing import List
from urllib.parse import quote

from tests.periodic_tasks.geckoboard_updater.jira_queries import JQL


def find_tickets(
    jql: JQL,
    *,
    max_results: int = 100,
    fields: str = "key,labels,summary",
    start_at: int = 0,
) -> dict:
    """Run Jira JQL and return result as JSON."""
    from tests.periodic_tasks.geckoboard_updater.clients import JIRA_CLIENT

    return JIRA_CLIENT.search_issues(
        jql_str=jql.query,
        maxResults=max_results,
        json_result=True,
        fields=fields,
        startAt=start_at,
    )


def count_labels(issues: list) -> Counter:
    counter = Counter()
    for issue in issues:
        if issue["fields"]["labels"]:
            for label in issue["fields"]["labels"]:
                counter[label] += 1
        else:
            counter["unlabelled"] += 1
    return counter


def filter_labels_by_prefix(
    labels: Counter, prefix: str, *, remove_prefix: bool = True
) -> Counter:
    if prefix:
        labels = dict(filter(lambda x: x[0].startswith(prefix), labels.items()))
        if remove_prefix:
            labels = {k.replace(prefix, ""): v for k, v in labels.items()}
    return Counter(labels)


def filter_out_ignored_labels(counter: Counter, ignored_labels: List[str]) -> Counter:
    if not ignored_labels:
        return counter
    filtered = filter(lambda x: x[0] not in ignored_labels, counter.items())
    return Counter(dict(filtered))


def filter_by_sought_labels(counter: Counter, sought_labels: List[str]) -> Counter:
    if not sought_labels:
        return counter
    filtered = filter(lambda x: x[0] in sought_labels, counter.items())
    return Counter(dict(filtered))


def quantity_per_label(
    jql_query_result: dict,
    *,
    label_prefix: str = "",
    remove_label_prefix: bool = False,
    ignored_labels: List[str] = None,
    look_for: List[str] = None,
) -> dict:
    issues = jql_query_result["issues"]
    all_labels = count_labels(issues)
    by_prefix = filter_labels_by_prefix(
        all_labels, label_prefix, remove_prefix=remove_label_prefix
    )
    without_ignored = filter_out_ignored_labels(by_prefix, ignored_labels)
    sought = filter_by_sought_labels(without_ignored, look_for)
    return dict(sought)


def tickets_by_labels(
    jql: Enum, ignored_labels: List[str], team: str, metric: str
) -> List[dict]:
    tickets = find_tickets(jql.value)
    counters = quantity_per_label(tickets, ignored_labels=ignored_labels)
    result = []
    for key in counters:
        item = {
            "date": date.today().isoformat(),
            "team": team,
            "metric": metric,
            "label": key,
            "quantity": counters[key],
        }
        result.append(item)
    return result


def total_tickets(jql: Enum, team: str) -> List[dict]:
    tickets = find_tickets(jql.value)
    return [
        {
            "date": date.today().isoformat(),
            "team": team,
            "metric": jql.value.description,
            "quantity": tickets["total"],
        }
    ]


def jira_links(jql_enum) -> List[str]:
    from tests.periodic_tasks.geckoboard_updater.settings import JIRA_HOST

    url = f"{JIRA_HOST}issues/?jql={{query}}"

    def clean_query(query: str) -> str:
        return query.replace("\n", " ").replace("  ", " ").strip()

    def link(jql):
        query = quote(clean_query(jql.value.query))
        return f'<a href="{url.format(query=query)}" target=_blank>{jql.value.description}</a>'

    return [link(jql) for jql in jql_enum.__members__.values()]
