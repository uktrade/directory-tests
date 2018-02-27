# -*- coding: utf-8 -*-
"""
Count number of ticket labels.

Example input CSV file with ticket labels:
    qa_functional,qa_manual,,,
    qa_manual,qa_ui,,,
    qa_functional,qa_manual,,,
    qa_functional,qa_manual,,,
    qa_functional,qa_manual,,,
    qa_manual,qa_ui,,,
    qa_manual,qa_ui,,,
    ...

Example result:
    {'qa_accessibility': 13,
    'qa_auto': 28,
    'qa_backend': 48,
    'qa_browser': 6,
    'qa_content': 35,
    'qa_functional': 21,
    'qa_manual': 156,
    'qa_mobile': 6,
    'qa_ui': 68}
"""
import argparse
import csv
import getopt
import sys
from pprint import pprint


def load_labels_from_csv(csv_path: str) -> list:
    all_labels = []
    with open(csv_path, "r") as csvfile:
        tagsreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in tagsreader:
            values = [item for item in row[0].split(",") if item]
            all_labels.append(values)
    return all_labels


def count_labels(all_labels: list) -> dict:
    result = {}
    for label_list in all_labels:
        for label in label_list:
            if label in result:
                result[label] += 1
            else:
                result[label] = 1
    return result


def parse_arguments(argv) -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="Path to CSV with labels", type=str)
    args = parser.parse_args()
    return args.inputfile


if __name__ == "__main__":
    input_path = parse_arguments(sys.argv[1:])
    all_labels = load_labels_from_csv(input_path)
    result = count_labels(all_labels)
    pprint(result)
