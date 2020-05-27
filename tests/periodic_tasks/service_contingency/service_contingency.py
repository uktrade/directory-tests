#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from collections import Counter, defaultdict
from typing import Tuple

GREAT = os.environ["DOMESTIC_URL"]
REPORT_FILE = os.getenv(
    "REPORT_FILE", default="../../../reports/dead_links_report.json"
)

SERVICES = {
    "CMS": os.environ["CMS_API_URL"],
    "Contact": os.environ["CONTACT_US_URL"],
    "ExOpps": os.environ["EXPORT_OPPORTUNITIES_URL"],
    "FAB": os.environ["FIND_A_BUYER_URL"],
    "FAS": os.environ["FIND_A_SUPPLIER_URL"],
    "Invest": os.environ["INVEST_URL"],
    "Old Contact-us": os.environ["LEGACY_CONTACT_US_URL"],
    "SOO": os.environ["SOO_URL"],
    "SSO": os.environ["SSO_URL"],
    "SUD": os.environ["PROFILE_URL"],
}

SKIP_STRINGS = [
    "/static/",
    "?source=",
    "?lang=",
    # "?next=",  # all links to SSO pages contain this param
    "/ar/",
    "/de/",
    "/es/",
    "/fr/",
    "/ja/",
    "/pt/",
    "/zh-hans/",
]


def filter_out_by_services(origins: set, services: tuple) -> list:
    return list(filter(lambda x: not x.startswith(services), origins))


def match_service(link: str) -> tuple:
    matching_services = [
        (service, url) for service, url in SERVICES.items() if link.startswith(url)
    ]

    if matching_services:
        assert len(matching_services) == 1
        return matching_services[0]
    else:
        if link.startswith(GREAT):
            return "Great", GREAT
        else:
            return "Other", None


def count_links_per_service(report: dict) -> Tuple[Counter, Counter, int]:
    pages_per_service = Counter()
    ignored_pages_per_service = Counter()
    ignored_scans = 0

    for page_report in report["pages"]:
        link = page_report["link"]
        # if "?next=" in link:
        #     link = link[0:link.index("?next=")]
        # if any(string in link for string in SKIP_STRINGS):
        # ignored_scans += 1
        # continue
        matching_services = {
            service: url for service, url in SERVICES.items() if link.startswith(url)
        }

        if matching_services:
            error = (
                f"Expected 1 matching service but got "
                f"{len(matching_services)} for {link}: "
                f"{matching_services} -> {SERVICES}"
            )
            assert len(matching_services) == 1, error
            service = list(matching_services.keys())[0]
            # print(f'{service} -> {link}')
            if any(string in link for string in SKIP_STRINGS):
                ignored_pages_per_service[service] += 1
                ignored_scans += 1
                continue
            else:
                pages_per_service[service] += 1
        else:
            if link.startswith(GREAT):
                pages_per_service["Great"] += 1
                # print(f'Great -> {link}')
            else:
                pages_per_service["Other"] += 1

    return pages_per_service, ignored_pages_per_service, ignored_scans


def service_contingency(report: dict) -> dict:
    # 1 - categorize link (to which service it belongs)
    # 2 - remove duplicated origin links
    # 3 - remove origin links that belong to the same service as current link
    # 4 - count origin links by service
    # 5 - add link origin counters to global service contingency counter
    other_service = 0
    same_site_origin = 0
    contingency_per_service = defaultdict(lambda: defaultdict(int))
    for page in report["pages"]:
        link = page["link"]
        # 1
        service_name, service_url = match_service(link)
        if not service_url:
            other_service += 1
            continue
        # 2
        without_query_part = [
            origin[0 : origin.index("?") if "?" in origin else None]  # noqa
            for origin in page["origins"]
        ]
        unique_origin_page = set(without_query_part)
        # 3
        distinct_origins = filter_out_by_services(unique_origin_page, (service_url,))

        if not distinct_origins:
            same_site_origin += 1
            continue

        # 4
        origin_contingency = Counter()
        for origin in distinct_origins:
            origin_service, _ = match_service(origin)
            origin_contingency[origin_service] += 1
            if not origin_contingency:
                print(origin)
        if origin_contingency:
            for origin_service, counter in origin_contingency.items():
                contingency_per_service[service_name][origin_service] += counter
    return contingency_per_service


if __name__ == "__main__":
    with open(REPORT_FILE, "r") as f:
        REPORT = json.load(f)

    print(
        f"Number of unique links (without links to static files, translations and "
        f"queries), per service, scanned by Dead Links Checker:"
    )
    print(
        f"If a link contains any of following strings: {', '.join(SKIP_STRINGS)} then "
        f"it won't be included in the contingency report"
    )

    (
        scans_per_service,
        ignored_links_per_service,
        ignored_scans,
    ) = count_links_per_service(REPORT)
    for name, count in scans_per_service.items():
        print(
            f"{name:15}: {count:5} - (excluding {ignored_links_per_service[name]:4} ignored links)"
        )
    print(f"Ignored links  : {ignored_scans}")
    total_per_service = sum(count for count in scans_per_service.values())
    print(
        f"Total          : {total_per_service+ignored_scans} ({total_per_service}+{ignored_scans})"
    )

    print(f"\nService contingency report:")
    for service, contingency in service_contingency(REPORT).items():
        url = SERVICES[service] if service in SERVICES else GREAT
        print(f"If {service} ({url}) was down then if would affect:")
        for origin, count in contingency.items():
            print(f"{count:10} pages on {origin}")
