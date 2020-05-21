# -*- coding: utf-8 -*-
from circleclient.circleclient import CircleClient
from geckoboard.client import Client as GeckoClient
from jira import JIRA
from tests.periodic_tasks.geckoboard_updater.settings import (
    CIRCLE_TOKEN,
    GECKOBOARD_API_KEY,
    JIRA_HOST,
    JIRA_TOKEN,
    JIRA_USERNAME,
)

CIRCLE_CI_CLIENT = CircleClient(CIRCLE_TOKEN)
JIRA_CLIENT = JIRA(JIRA_HOST, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
GECKOBOARD_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
