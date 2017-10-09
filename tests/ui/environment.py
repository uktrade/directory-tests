# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def before_scenario(context, scenario):
    logging.debug('Starting scenario: %s', scenario.name)
    # re-initialize the scenario data


def before_all(context):
    context.driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME)
