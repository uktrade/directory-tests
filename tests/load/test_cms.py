from random import choice

from directory_constants.constants import cms as SERVICE_NAMES
from locust import TaskSet, task
from tests import settings
from tests.load.cms_helpers import CMSAPIAuthClientMixin


class CMSTasks(TaskSet):
    @task
    def lookup_by_full_path(self):
        """ATM This works only for ExRed prototype pages."""
        services = [
            # SERVICE_NAMES.INVEST,
            # SERVICE_NAMES.FIND_A_SUPPLIER,
            SERVICE_NAMES.EXPORT_READINESS
        ]
        paths = [
            "/advice-and-guidance/logistics/",
            "/advice-and-guidance/legal-and-compliance/",
            "/advice-and-guidance/understand-your-market/",
            "/advice-and-guidance/finance/",
            "/advice-and-guidance/tax-and-customs/",
            "/advice-and-guidance/strategy/",
            "/advice-and-guidance/preparing-for-exiting-the-eu/",
            "/advice-and-guidance/how-to-start-exporting/",
        ]
        path = choice(paths)
        self.client.default_service_name = choice(services)
        self.client.lookup_by_full_path(
            path,
            fields=None,
            name="/api/pages/lookup-by-full-path/",
            expected_codes=[200, 404],
        )

    @task
    def lookup_by_slug(self):
        services = [
            SERVICE_NAMES.INVEST,
            SERVICE_NAMES.FIND_A_SUPPLIER,
            SERVICE_NAMES.EXPORT_READINESS,
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
        self.client.default_service_name = choice(services)
        self.client.lookup_by_slug(
            slug,
            fields=None,
            name="/api/pages/lookup-by-slug/[slug]/",
            expected_codes=[200, 404],
        )


class CMS(CMSAPIAuthClientMixin):
    host = settings.DIRECTORY_CMS_API_CLIENT_BASE_URL
    task_set = CMSTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
