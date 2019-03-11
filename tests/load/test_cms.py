from collections import namedtuple
from random import choice

from directory_constants.constants import cms
from locust import TaskSet, task
from tests import settings
from tests.load import USER_AGENT
from tests.load.cms_helpers import CMSAPIAuthClientMixin


UA = namedtuple("UA", "headers")
user_agent = UA(headers=USER_AGENT)


class CMSTasks(TaskSet):

    @task
    def lookup_by_slug(self):
        services = [
            cms.INVEST,
            cms.FIND_A_SUPPLIER,
            cms.EXPORT_READINESS,
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
            authenticator=user_agent,
            name="/api/pages/lookup-by-slug/[slug]/",
            service_name=choice(services),
            expected_codes=[200, 404],
        )


class CMS(CMSAPIAuthClientMixin):
    host = settings.DIRECTORY_CMS_API_CLIENT_BASE_URL
    task_set = CMSTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
