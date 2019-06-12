from random import choice

from locust import HttpLocust, TaskSet, task
from tests import settings, URLs
from tests.load import USER_AGENT, basic_auth


class InvestTasks(TaskSet):

    @task
    def home_page(self):
        url = URLs.INVEST_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            auth=basic_auth(),
        )

    @task
    def industry_pages(self):
        urls = [
            URLs.INVEST_INDUSTRIES.relative,
            URLs.INVEST_INDUSTRIES_ADVANCED_MANUFACTURING.relative,
            URLs.INVEST_INDUSTRIES_AEROSPACE.relative,
            URLs.INVEST_INDUSTRIES_AGRI_TECH.relative,
            URLs.INVEST_INDUSTRIES_ASSET_MANAGEMENT.relative,
            URLs.INVEST_INDUSTRIES_AUTOMOTIVE.relative,
            URLs.INVEST_INDUSTRIES_AUTOMOTIVE_RESEARCH_AND_DEVELOPMENT.relative,
            URLs.INVEST_INDUSTRIES_AUTOMOTIVE_SUPPLY_CHAIN.relative,
            URLs.INVEST_INDUSTRIES_CAPITAL_INVESTMENT.relative,
            URLs.INVEST_INDUSTRIES_CHEMICALS.relative,
            URLs.INVEST_INDUSTRIES_CREATIVE_CONTENT_AND_PRODUCTION.relative,
            URLs.INVEST_INDUSTRIES_CREATIVE_INDUSTRIES.relative,
            URLs.INVEST_INDUSTRIES_DATA_ANALYTICS.relative,
            URLs.INVEST_INDUSTRIES_DIGITAL_MEDIA.relative,
            URLs.INVEST_INDUSTRIES_ELECTRICAL_NETWORKS.relative,
            URLs.INVEST_INDUSTRIES_ENERGY.relative,
            URLs.INVEST_INDUSTRIES_ENERGY_WASTE.relative,
            URLs.INVEST_INDUSTRIES_FINANCIAL_SERVICES.relative,
            URLs.INVEST_INDUSTRIES_FINANCIAL_TECHNOLOGY.relative,
            URLs.INVEST_INDUSTRIES_FOOD_AND_DRINK.relative,
            URLs.INVEST_INDUSTRIES_FOOD_SERVICE_AND_CATERING.relative,
            URLs.INVEST_INDUSTRIES_FREE_FOODS.relative,
            URLs.INVEST_INDUSTRIES_HEALTH_AND_LIFE_SCIENCES.relative,
            URLs.INVEST_INDUSTRIES_MEAT_POULTRY_AND_DAIRY.relative,
            URLs.INVEST_INDUSTRIES_MEDICAL_TECHNOLOGY.relative,
            URLs.INVEST_INDUSTRIES_MOTORSPORT.relative,
            URLs.INVEST_INDUSTRIES_NUCLEAR_ENERGY.relative,
            URLs.INVEST_INDUSTRIES_OFFSHORE_WIND_ENERGY.relative,
            URLs.INVEST_INDUSTRIES_OIL_AND_GAS.relative,
            URLs.INVEST_INDUSTRIES_PHARMACEUTICAL_MANUFACTURING.relative,
            URLs.INVEST_INDUSTRIES_RETAIL.relative,
            URLs.INVEST_INDUSTRIES_TECHNOLOGY.relative,
        ]
        self.client.get(
            choice(urls),
            headers=USER_AGENT,
            name="/industries/[industry]/",
            auth=basic_auth(),
        )


class Invest(HttpLocust):
    host = settings.INVEST_UI_URL
    task_set = InvestTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
