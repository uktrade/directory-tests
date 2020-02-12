#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from envparse import env

# Allure results from Smoke tests are kept in results/
RESULTS_DIR = "results"
# Allure results from Functional tests are kept in results_${FEATURE_DIR}/
FEATURE_DIR = env.str("FEATURE_DIR", default=None)
# Allure results from Browser tests are kept in results_${BROWSER}_${CIRCLE_NODE_INDEX}/
BROWSER = env.str("BROWSER", default=None)
CIRCLE_NODE_INDEX = env.str("CIRCLE_NODE_INDEX", default=None)

if FEATURE_DIR:
    RESULTS_DIR = f"results_{FEATURE_DIR}"
if BROWSER and CIRCLE_NODE_INDEX:
    RESULTS_DIR = f"results_{BROWSER}_{CIRCLE_NODE_INDEX}"

ENV_VARS = {
    "Environment": env.str("TEST_ENV", default=None),
    "Automatically_retry_on_failures": env.str("AUTO_RETRY", default=None),
    "Take_screenshots": env.str("TAKE_SCREENSHOTS", default=None),
    "Tags": env.str("TAGS", default=None),
    "Run_tests_in_headless_mode": env.str("BROWSER_HEADLESS", default=None),
    "PyTest_args": env.str("PYTEST_ARGS", default=None),
}

properties_filepath = f"./{RESULTS_DIR}/environment.properties"
with open(properties_filepath, "w") as properties:
    for key, value in ENV_VARS.items():
        if value:
            line = f"{key} = {value}\n"
            properties.write(line)
            print(f"{key} = {value}")
    print(f"All found env vars were saved in {properties_filepath}")
