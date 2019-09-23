# -*- coding: utf-8 -*-
from collections import namedtuple
from random import choice

from directory_constants.cms import EXPORT_READINESS, FIND_A_SUPPLIER, INVEST
from locust import TaskSet, task

from directory_tests_shared import settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from tests.load.cms_helpers import CMSAPIAuthClientMixin

UA = namedtuple("UA", "headers")
LOAD_TESTS_USER_AGENT = UA(headers=LOAD_TESTS_USER_AGENT)


class CMSTasks(TaskSet):

    @task
    def lookup_by_slug(self):
        services = [
            INVEST,
            FIND_A_SUPPLIER,
            EXPORT_READINESS,
        ]
        slugs = [
            "advanced-manufacturing",
            "aerospace",
            "agri-tech",
            "apply-for-a-uk-visa",
            "asset-management",
            "automotive",
            "automotive-research-and-development",
            "automotive-supply-chain",
            "capital-investment",
            "chemicals",
            "creative-content-and-production",
            "creative-industries",
            "data-analytics",
            "digital-media",
            "electrical-networks",
            "energy",
            "energy-waste",
            "establish-a-base-for-business-in-the-uk",
            "financial-services",
            "financial-technology",
            "food-and-drink",
            "food-service-and-catering",
            "hire-skilled-workers-for-your-uk-operations",
            "home-page",
            "invest-sector-landing-page",
            "open-a-uk-business-bank-account",
            "sector-landing-page",
            "sector-landing-page",
            "setup-guide-landing-page",
        ]
        slug = choice(slugs)
        self.client.lookup_by_slug(
            slug,
            fields=None,
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/lookup-by-slug/[slug]/",
            service_name=choice(services),
            expected_codes=[200, 404],
        )


class CMS(CMSAPIAuthClientMixin):
    host = settings.CMS_API_URL
    task_set = CMSTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
