#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from envparse import env

variables = {
    "Environment": env.str("TEST_ENV", default=None).upper(),
    "Automatically_retry_on_failures": env.str("AUTO_RETRY", default=None),
    "Take_screenshots": env.str("TAKE_SCREENSHOTS", default=None),
    "Tags": env.str("TAGS", default=None),
    "Run_tests_in_headless_mode": env.str("BROWSER_HEADLESS", default=None),
}

with open("./environment.properties", "w") as properties:
    for key, var in variables.items():
        if var:
            line = f"{key} = {var}\n"
            properties.write(line)
