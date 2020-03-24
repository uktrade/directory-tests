# -*- coding: utf-8 -*-
import difflib
import json
import os
from typing import List
from urllib.parse import urljoin

import requests
from behave.runner import Context
from bs4 import BeautifulSoup
from envparse import env
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from retrying import retry

SITES_INVEST = {
    "dev": env.str("DEV_INVEST_URL"),
    "stage": env.str("STAGE_INVEST_URL"),
    "uat": env.str("UAT_INVEST_URL"),
    "prod": env.str("PROD_INVEST_URL"),
}
SITES_DOMESTIC = {
    "dev": env.str("DEV_DOMESTIC_URL"),
    "stage": env.str("STAGE_DOMESTIC_URL"),
    "uat": env.str("UAT_DOMESTIC_URL"),
    "prod": env.str("PROD_DOMESTIC_URL"),
}
SITES_FAS = {
    "dev": env.str("DEV_FIND_A_SUPPLIER_URL"),
    "stage": env.str("STAGE_FIND_A_SUPPLIER_URL"),
    "uat": env.str("UAT_FIND_A_SUPPLIER_URL"),
    "prod": env.str("PROD_FIND_A_SUPPLIER_URL"),
}
SITES_INTERNATIONAL = {
    "dev": env.str("DEV_INTERNATIONAL_URL"),
    "stage": env.str("STAGE_INTERNATIONAL_URL"),
    "uat": env.str("UAT_INTERNATIONAL_URL"),
    "prod": env.str("PROD_INTERNATIONAL_URL"),
}

BASICAUTH_USER = os.environ["DEV_BASICAUTH_USER"]
BASICAUTH_PASS = os.environ["DEV_BASICAUTH_PASS"]


def get_basic_auth():
    return BASICAUTH_USER, BASICAUTH_PASS


def retry_if_network_error(exception: Exception) -> bool:
    return isinstance(exception, (Timeout, ConnectionError, TooManyRedirects))


def merge_data_section_lines(lines, data_section_lines):
    """Merge data section lines into one line.

    This is because:
    on current invest:
    <p><span>168 Milliarden GBP</span> Beitrag zur britischen Wirtschaftsleistung</p>

    and on new invest (dev):
    <div class="data">
    <span class="data-item font-xlarge">168 Milliarden GBP</span>
    <span>Beitrag zur britischen Wirtschaftsleistung</span>
    </div>
    """
    if data_section_lines:
        index = lines.index(data_section_lines[0])
        lines[index] = " ".join(data_section_lines)
        lines.pop(index + 1)


def get_text(content: str, section_name: str) -> List[str]:
    soup = BeautifulSoup(content, "lxml")
    section = soup.find(section_name)
    if not section:
        section = soup.find("body")

    for element in section.findAll(["script", "css", "img", "style", "select"]):
        element.extract()
    for element in section.select("#beta-bar"):
        element.extract()
    for element in section.select("#error-reporting-section-contact-us"):
        element.extract()
    # list of companies on FAS Industry pages
    for element in section.select("#companies-section ul"):
        element.extract()
    data_section_lines = [
        line
        for span in section.findAll("div", class_="data")
        for line in span.get_text().splitlines()
        if line
    ]

    lines = [line.strip() for line in section.get_text().splitlines() if line.strip()]

    merge_data_section_lines(lines, data_section_lines)

    return lines


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_network_error,
    wrap_exception=False,
)
def extract_page_content(
    context: Context,
    section: str,
    endpoint: str,
    service: str,
    site_a: str,
    site_b: str,
):
    if service.lower() == "fas":
        sites = SITES_FAS
    elif service.lower() == "domestic":
        sites = SITES_DOMESTIC
    elif service.lower() == "invest":
        sites = SITES_INVEST
    elif service.lower() == "international":
        sites = SITES_INTERNATIONAL

    site_a = sites[site_a.lower()]
    site_b = sites[site_b.lower()]
    url_a = urljoin(site_a, endpoint) if endpoint != "/" else site_a
    url_b = urljoin(site_b, endpoint) if endpoint != "/" else site_b
    auth_a = get_basic_auth() if site_a.lower() != "prod" else None
    auth_b = get_basic_auth() if site_b.lower() != "prod" else None

    response_a = requests.get(url_a, auth=auth_a)
    response_b = requests.get(url_b, auth=auth_b)

    content_a = response_a.content
    content_b = response_b.content

    text_a = get_text(content_a, section)
    text_b = get_text(content_b, section)

    response_time_a = int(response_a.elapsed.total_seconds() * 1000)
    response_time_b = int(response_b.elapsed.total_seconds() * 1000)

    contents = {
        "endpoint": endpoint,
        "site_a": {
            "site": site_a,
            "url": url_a,
            "text": text_a,
            "response_time": response_time_a,
        },
        "site_b": {
            "site": site_b,
            "url": url_b,
            "text": text_b,
            "response_time": response_time_b,
        },
    }

    context.contents = contents


def look_for_differences(context: Context):
    contents = context.contents
    endpoint = contents["endpoint"]
    url_a = contents["site_a"]["url"]
    url_b = contents["site_b"]["url"]
    text_a = contents["site_a"]["text"]
    text_b = contents["site_b"]["text"]
    missing_page = "This page cannot be found"
    found_on_both_sites = True
    if (missing_page in text_a) and (missing_page in text_b):
        text_a.append(f"Page is not present on both sites. Check {url_a}")
        text_b.append(f"Page is not present on both sites. Check {url_b}")
        found_on_both_sites = False
    from_desc_url_a = f"<a href='{url_a}' target=_blank>{url_a}</a>"
    from_desc_url_b = f"<a href='{url_b}' target=_blank>{url_b}</a>"
    html = difflib.HtmlDiff(tabsize=4, wrapcolumn=120).make_file(
        text_a,
        text_b,
        fromdesc=from_desc_url_a,
        todesc=from_desc_url_b,
        context=True,
        numlines=1,
    )
    sm = difflib.SequenceMatcher(None, text_a, text_b)
    contents["similarity"] = int(sm.ratio() * 100)

    clean_endpoint = endpoint
    if clean_endpoint.startswith("/"):
        clean_endpoint = clean_endpoint[1:]
    if clean_endpoint.endswith("/"):
        clean_endpoint = clean_endpoint[:-1]
    # https://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
    clean_endpoint = clean_endpoint.replace("/", "_")
    clean_endpoint = clean_endpoint.replace("?", "_")
    clean_endpoint = clean_endpoint.replace("=", "_")
    clean_endpoint = clean_endpoint.replace("__", "_")
    clean_endpoint = clean_endpoint or "home"
    report_name = "./reports/{}.html".format(clean_endpoint)
    with open(report_name, "w") as file:
        file.write(html)

    contents_file_name = "./reports/{}.json".format(clean_endpoint)
    with open(contents_file_name, "w") as file:
        file.write(json.dumps(contents))

    assert found_on_both_sites, f"{endpoint} doesn't exist on both sites"
    no_differences = "No Differences Found" in html
    not_found = "This page cannot be found" in html.replace("&nbsp;", " ")
    assert not not_found, f"{endpoint} was not found see {report_name}"
    assert no_differences, f"Found differences on {endpoint} see {report_name}"
