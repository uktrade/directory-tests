#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

import requests
from termcolor import cprint

from directory_tests_shared.clients import CMS_API_CLIENT


def red(x: str):
    """Print out a message in red to console."""
    cprint(x, "red", attrs=["bold"])


def camel_case_to_separate_words(camel_case_string: str) -> str:
    """Convert CamelCase string into a string with words separated by spaces"""
    words = [[camel_case_string[0]]]

    for character in camel_case_string[1:]:
        if words[-1][-1].islower() and character.isupper():
            words.append(list(character))
        else:
            words[-1].append(character)

    return " ".join("".join(word) for word in words)


def get_pks_by_page_type(page_type: str) -> List[int]:
    result = []
    try:
        response = CMS_API_CLIENT.get(f"api/pages/?type={page_type}")
    except requests.exceptions.HTTPError as ex:
        red(f"GET api/pages/?type={page_type} -> Failed because of: {ex}")
    else:
        if response.status_code != 200:
            red(
                f"GET api/pages/?type={page_type} -> {response.status_code} {response.reason}"
            )
        else:
            result = response.json()
    print(f"GET api/pages/?type={page_type} -> {result}")
    return result


def get_page_by_pk(pk: int) -> dict:
    result = {}
    try:
        response = CMS_API_CLIENT.get(f"api/pages/{pk}/")
    except requests.exceptions.HTTPError as ex:
        red(f"GET api/pages/{pk}/ -> Failed because of: {ex}")
    else:
        if response.status_code != 200:
            red(f"GET api/pages/{pk}/ -> {response.status_code} {response.reason}")
        else:
            result = response.json()
    return result


def pages_status_report() -> dict:
    types = set(CMS_API_CLIENT.get("api/pages/types/").json()["types"])
    skipped_types = {
        "wagtailcore.page",
        "components.bannercomponent",
    }

    page_status = {}
    for page_type in sorted(types - skipped_types):
        page_type_summary = []
        pks_by_page_type = get_pks_by_page_type(page_type)
        for pk in pks_by_page_type:
            page = get_page_by_pk(pk)
            if not page:
                continue
            page_type_summary.append(
                {
                    "id": page["id"],
                    "title": page["title"],
                    "languages": [l[0] for l in page["meta"]["languages"]],
                    "url": page["meta"]["url"],
                    "last_published_at": page["last_published_at"],
                    "draft_token": page["meta"]["draft_token"],
                    "camel_case_page_type": page["page_type"],
                }
            )
        page_status[page_type] = page_type_summary

    return page_status


def generate_html_report(report: dict):
    table_template = """<table style="border: 1px solid black;width:75%;margin-left:12%;margin-right:13%;">
<thead>
<tr style="font-size:16pt">
<th style="padding:5px;text-align:left">ID</th>
<th style="padding:5px;text-align:left">Title</th>
<th style="padding:5px;text-align:left">Published</th>
<th style="padding:5px;text-align:left">Draft</th>
<th style="padding:5px;text-align:left">Languages</th>
</tr>
</thead>
{tbodies}
</table>"""
    tbody_template = """<tbody>
    <tr>
        <th colspan="5" style="font-size:16pt;color:black;background-color:lightgray;text-align:left">{page_type}</th>
    </tr>
{rows}
</tbody>"""
    page_row_template = """<tr style="font-size:14pt">
<td><a href="{admin_url}admin/pages/{id}/edit/" target="_blank">{id}</a></td>
<td><a href="{url}" target="_blank">{title}</a></td>
<td>{last_published_at}</td>
<td>{draft}</td>
<td>{languages}</td>
</tr>"""
    tbodies = ""
    for long_page_type in sorted(report.keys()):
        app_name = long_page_type.split(".")[0].replace("_", " ").title()
        summaries = sorted(report[long_page_type], key=lambda x: x["id"])
        rows = ""
        formatted_page_type = ""
        for summary in summaries:
            short_page_type = camel_case_to_separate_words(
                summary["camel_case_page_type"]
            )
            formatted_page_type = f"{app_name} - {short_page_type}"
            if summary["last_published_at"]:
                last_published_at = datetime.strftime(
                    datetime.strptime(
                        summary["last_published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "%Y-%m-%d %H:%M:%S",
                )
            else:
                last_published_at = ""
            rows += page_row_template.format(
                admin_url=CMS_API_CLIENT.base_url,
                id=summary["id"],
                url=summary["url"],
                title=summary["title"],
                last_published_at=last_published_at,
                draft=f"<a href='{summary['url']}?draft_token={summary['draft_token']}' target='_blank'>draft</a>"
                if summary["draft_token"]
                else "",
                languages=", ".join(
                    [
                        f"<a href='{summary['url']}?lang={l}' target='_blank'>{l}</a>"
                        for l in summary["languages"]
                    ]
                ),
            )
        if rows:
            tbodies += tbody_template.format(page_type=formatted_page_type, rows=rows)
    return table_template.format(tbodies=tbodies)


def save_report(content: str):
    with open("./reports/index.html", "w") as report_file:
        report_file.write(content)


if __name__ == "__main__":
    pages_status = pages_status_report()
    total_pages = sum(len(pages) for pages in pages_status.values())
    print(f"Generating report for {total_pages} found pages")
    html = generate_html_report(pages_status)
    save_report(html)
