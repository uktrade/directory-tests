# -*- coding: utf-8 -*-
import glob
import json
import os
from collections import namedtuple
from typing import List

from behave.runner import Context

REPORT_FILE = os.getenv("REPORT_FILE", "index.html")
REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", "./reports")

Summary = namedtuple(
    "Summary",
    [
        "file_name",
        "result",
        "color",
        "site_a",
        "site_b",
        "response_time_a",
        "response_time_b",
        "similarity",
    ],
)


def find_html_report_files() -> List[str]:
    path = os.path.join(REPORT_DIRECTORY, "*.html")
    file_paths = glob.glob(path)
    try:
        file_paths.remove(os.path.join(REPORT_DIRECTORY, REPORT_FILE))
    except ValueError:
        pass
    return file_paths


def extract_summary_from_report_file(file_path: str) -> Summary:
    with open(file_path, "r") as f:
        html = f.read().replace("&nbsp;", " ")

    contents_json = file_path.replace(".html", ".json")
    with open(contents_json, "r") as f:
        contents = json.loads(f.read())
        os.remove(contents_json)

    result = "Found differences"
    no_differences_found = "No Differences Found"
    not_found = "This page cannot be found"
    not_found_on_both_sites = "Page is not present on both sites"
    color = "#ff0040"
    site_a = contents["site_a"]["site"]
    site_b = contents["site_b"]["site"]
    response_time_a = contents["site_a"]["response_time"]
    response_time_b = contents["site_b"]["response_time"]
    similarity = contents["similarity"]

    if no_differences_found in html:
        result = no_differences_found
        color = "#00ff80"
    if not_found in html:
        result = not_found
        color = "#00bfff"
    if not_found_on_both_sites in html:
        result = not_found_on_both_sites
        color = "#cc00ff"

    file_name = file_path.replace("./reports/", "")
    return Summary(
        file_name,
        result,
        color,
        site_a,
        site_b,
        response_time_a,
        response_time_b,
        similarity,
    )


def get_report_summaries(html_report_file_paths: List[str]) -> List[Summary]:
    summaries = []
    for report_file_path in html_report_file_paths:
        summaries.append(extract_summary_from_report_file(report_file_path))

    return sorted(
        summaries,
        key=lambda summary: (summary.similarity, summary.result, summary.file_name),
    )


def generate_report_index(summaries: List[Summary]) -> str:
    totals = {}

    for summary in summaries:
        default_value = {"total": 0, "color": summary.color}
        totals.setdefault(summary.result, default_value)
        totals[summary.result]["total"] += 1

    doc_template = """<html>
    <body>
        <table style="border: 1px solid black;width:33%;margin-left:33%;margin-right:33%;">
        <tr>
            <th style="padding:5px;">Result</th>
            <th style="padding:5px;">Total</th>
        </tr>
        {totals_rows}
        </table>
        <br>
        <br>
        <table style="border: 1px solid black;width:80%;margin-left:10%;margin-right:10%;">
        <tr>
            <th style="padding:5px;">Result</th>
            <th style="padding:5px;">Report</th>
            <th style="padding:5px;">Similarity (%)</th>
            <th style="padding:5px;">{site_a}</th>
            <th style="padding:5px;">{site_b}</th>
        </tr>
        {rows}
        </table>
    </body>
    </html>
    """
    totals_rows = []
    for key, values in totals.items():
        result = key
        color = values["color"]
        total = values["total"]
        row = f"""
        <tr style="border: 1px solid black;">
            <td style="padding:5px;background-color:{color};text-align:center">{result}</td>
            <td>{total}</td>
        </tr>
        """
        totals_rows.append(row)

    rows = []
    for summary in summaries:
        file_name = summary.file_name
        result = summary.result
        color = summary.color
        site_a = summary.site_a
        site_b = summary.site_b
        time_a = summary.response_time_a
        time_b = summary.response_time_b
        similarity = summary.similarity
        time_a_color = "#00ff80" if time_a < time_b else "#ff0040"
        time_b_color = "#00ff80" if time_b < time_a else "#ff0040"
        row = f"""
        <tr style="border: 1px solid black;">
            <td style="padding:5px;background-color:{color};text-align:center">{result}</td>
            <td><a href="{file_name}">{file_name}</a></td>
            <td>{similarity}</td>
            <td style="background-color:{time_a_color};text-align:center">{time_a}ms</td>
            <td style="background-color:{time_b_color};text-align:center">{time_b}ms</td>
        </tr>
        """
        rows.append(row)
    return doc_template.format(
        totals_rows="\n\t".join(totals_rows),
        rows="\n\t".join(rows),
        site_a=site_a,
        site_b=site_b,
        similarity=similarity,
        time_a=time_a,
        time_b=time_b,
    )


def save_report_index(html: str):
    path = os.path.join(REPORT_DIRECTORY, REPORT_FILE)
    with open(path, "w") as report:
        report.write(html)


def after_all(context: Context):
    html_report_file_paths = find_html_report_files()
    summaries = get_report_summaries(html_report_file_paths)
    html = generate_report_index(summaries)
    save_report_index(html)
