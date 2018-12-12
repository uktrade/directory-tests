from random import choice

from locust import HttpLocust, TaskSet, task
from tests import get_relative_url, settings
from tests.load import USER_AGENT, invest_hawk_cookie


class InvestTasks(TaskSet):
    @task
    def home_page(self):
        url = get_relative_url("ui-invest:landing")
        self.client.get(
            url,
            headers=USER_AGENT,
            cookies=invest_hawk_cookie(),
        )

    @task
    def uk_setup_guides_pages(self):
        endpoints = [
            "uk-setup-guide/",
            "uk-setup-guide/apply-uk-visa/",
            "uk-setup-guide/establish-base-business-uk/",
            "uk-setup-guide/hire-skilled-workers-your-uk-operations/",
            "uk-setup-guide/open-uk-business-bank-account/",
            "uk-setup-guide/setup-your-business-uk/",
            "uk-setup-guide/understand-uk-tax-and-incentives/",
        ]
        self.client.get(
            choice(endpoints),
            headers=USER_AGENT,
            name="/uk-setup-guide/[guide]/",
            cookies=invest_hawk_cookie(),
        )


    @task
    def industry_pages(self):
        urls = [
            "industries/",
            "industries/advanced-manufacturing/",
            "industries/aerospace/",
            "industries/agri-tech/",
            "industries/asset-management/",
            "industries/automotive/",
            "industries/automotive-research-and-development/",
            "industries/automotive-supply-chain/",
            "industries/capital-investment/",
            "industries/chemicals/",
            "industries/creative-content-and-production/",
            "industries/creative-industries/",
            "industries/data-analytics/",
            "industries/digital-media/",
            "industries/electrical-networks/",
            "industries/energy/",
            "industries/energy-waste/",
            "industries/financial-services/",
            "industries/financial-technology/",
            "industries/food-and-drink/",
            "industries/food-service-and-catering/",
            "industries/free-foods/",
            "industries/health-and-life-sciences/",
            "industries/meat-poultry-and-dairy/",
            "industries/medical-technology/",
            "industries/motorsport/",
            "industries/nuclear-energy/",
            "industries/offshore-wind-energy/",
            "industries/oil-and-gas/",
            "industries/pharmaceutical-manufacturing/",
            "industries/retail/",
            "industries/technology/",
        ]
        self.client.get(
            choice(urls),
            headers=USER_AGENT,
            name="/industries/[industry]/",
            cookies=invest_hawk_cookie(),
        )


class Invest(HttpLocust):
    host = settings.INVEST_UI_URL
    task_set = InvestTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
