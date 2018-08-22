from random import randint, choice

from locust import TaskSet, task

from tests import get_relative_url, settings
from directory_constants.constants import cms as SERVICE_NAMES
from tests.locust.helpers import CMSAPIAuthClientMixin


class AuthenticatedPagesAPI(TaskSet):

    @task
    def get_page_by_id(self):
        url = get_relative_url('cms-api:pages')
        endpoint = f"{url}{randint(1, 100)}/"
        self.client.get(endpoint, name="/api/pages/[id]/")

    @task
    def get_child_pages_by_id(self):
        url = get_relative_url('cms-api:pages')
        endpoint = f"{url}?child_of={randint(1, 100)}"
        self.client.get(endpoint, name="/api/pages/?child_of=[id]")

    @task
    def get_pages_by_type(self):
        types = [
            "export_readiness.GetFinancePage",
            "export_readiness.PerformanceDashboardNotesPage",
            "export_readiness.PerformanceDashboardPage",
            "export_readiness.PrivacyAndCookiesPage",
            "export_readiness.TerAndConditionsPage",
            "find_a_supplier.IndustryArticlePage",
            "find_a_supplier.IndustryContactPage",
            "find_a_supplier.IndustryLandingPage",
            "find_a_supplier.IndustryPage",
            "find_a_supplier.LandingPage",
            "invest.InfoPage",
            "invest.InvestHomePage",
            "invest.SectorLandingPage",
            "invest.SectorPage",
            "invest.SetupGuideLandingPage",
        ]
        url = get_relative_url('cms-api:pages')
        endpoint = f"{url}?type={choice(types)}"
        self.client.get(endpoint, name="/api/pages/?type=[type]")

    @task
    def get_page_by_slug(self):
        services = [
            SERVICE_NAMES.INVEST,
            SERVICE_NAMES.FIND_A_SUPPLIER,
            SERVICE_NAMES.EXPORT_READINESS
        ]
        slugs = [
            "advanced-manufacturing", "aerospace", "agri-tech",
            "apply-for-a-uk-visa", "asset-management", "automotive",
            "automotive-research-and-development", "automotive-supply-chain",
            "capital-investment", "chemicals",
            "creative-content-and-production", "creative-industries",
            "data-analytics", "digital-media", "electrical-networks",
            "energy", "energy-from-waste",
            "establish-a-base-for-business-in-the-uk", "financial-services",
            "financial-technology", "food-and-drink",
            "food-service-and-catering",
            "hire-skilled-workers-for-your-uk-operations", "home-page",
            "invest-sector-landing-page", "open-a-uk-business-bank-account",
            "sector-landing-page", "sector-landing-page",
            "setup-guide-landing-page",
        ]
        slug = choice(slugs)
        fields = f"*&service_name={choice(services)}"
        self.client.lookup_by_slug(
            slug, fields=fields, name="/api/pages/lookup-by-slug/[slug]/")


class AuthenticatedUserAPI(CMSAPIAuthClientMixin):
    host = settings.DIRECTORY_CMS_API_CLIENT_BASE_URL
    task_set = AuthenticatedPagesAPI
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
