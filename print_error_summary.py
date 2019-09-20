#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JUnit XML Report Error Summary
Prints out a summary of errors found in a XML report file.

Usage:
  env_writer.py (-h | --help)
  env_writer.py [--report=merged.xml]
  env_writer.py --version

Options:
  -h --help             Show this screen.
  --report=REPORT_FILE  Specify JUnit XML report file [default: ./merged.xml]
  --version             Show version.
"""
from collections import defaultdict, OrderedDict

import xmltodict
from docopt import docopt
from termcolor import cprint


def red(x: str):
    cprint(x, "red", attrs=["bold"])


def green(x: str):
    cprint(x, "green", attrs=["bold"])


def blue(x: str):
    cprint(x, "blue", attrs=["bold"])


def parse_xml_report(*, report: str = "merged.xml") -> OrderedDict:
    with open(report, "r") as xml:
        return xmltodict.parse(xml.read())


def count_errors(doc: OrderedDict) -> dict:
    """
    Non-Assertion errors are stored in "error" nodes.
    Assertions errors are stored in "failure" nodes.
    """
    def get_error_type_and_msg(test_case: OrderedDict) -> tuple:
        if "error" in test_case:
            error_type = test_case["error"]["@type"]
            error_msg = test_case["error"]["@message"]
        elif "failure" in test_case:
            error_type = test_case["failure"]["@type"]
            error_msg = test_case["failure"]["@message"]
        return error_type, error_msg

    failure_types = defaultdict(list)
    # Handle report with only TestSuite and no TestSuites
    if "testuites" not in doc and "testsuite" in doc:
        if isinstance(doc["testsuite"], OrderedDict):
            for tc in doc["testsuite"]["testcase"]:
                if tc["@status"] == "failed":
                    error_type, error_msg = get_error_type_and_msg(tc)
                    failure_types[error_type].append(error_msg)
    # Handle TestSuite with only 1 TestCase
    elif isinstance(doc["testsuites"]["testsuite"], OrderedDict):
        tc = doc["testsuites"]["testsuite"]["testcase"]
        if tc["@status"] == "failed":
            error_type, error_msg = get_error_type_and_msg(tc)
            failure_types[error_type].append(error_msg)
    # Handle TestSuite with multiple TestCases
    elif isinstance(doc["testsuites"]["testsuite"], list):
        for ts in doc["testsuites"]["testsuite"]:
            for tc in ts["testcase"]:
                if isinstance(tc, OrderedDict):
                    if tc["@status"] == "failed":
                        error_type, error_msg = get_error_type_and_msg(tc)
                        failure_types[error_type].append(error_msg)
    return dict(failure_types)


def print_error_summary(summary: dict):
    """
    Format of error summary:
    {
     'WebDriverException': [
        'Message: Session not started or terminated',
        'Message: Session not started or terminated'
     ],
     'NoSuchElementException': [
        'Message: no such element:...',
        'Message: no such element:...',
     ],
     'AttributeError': [
        "module 'pages.exred.ukef_...' has no attribute 'URLs'",
        "module 'pages.exred.ukef_...' has no attribute 'URLs'",
     ],
     'AssertionError': [
        'window.dataLayer on ... is empty!',
        "Expected to see breadcrumb for 'Technology' ...",
        "Couldn't find 'Home' breadcrumb on https://..."
     ],
     'KeyError': [
        'Could not find Page Object for ....'
     ]
    }
    """
    if summary:
        red(f"Report contains:")
        for error_type, errors in summary.items():
            print(f"{len(errors):3} {error_type}")
        blue("Unique error messages for:")
        for error_type, errors in summary.items():
            red(error_type)
            for error in sorted(set(errors)):
                print(f"\t☢ {error}")
    else:
        green("⭐Success! Report contains no errors!⭐")


if __name__ == "__main__":
    arguments = docopt(__doc__, version="error_summary 1.0")
    path_to_report_file = arguments["--report"]

    parsed = parse_xml_report(report=path_to_report_file)
    error_summary = count_errors(parsed)
    print_error_summary(error_summary)
