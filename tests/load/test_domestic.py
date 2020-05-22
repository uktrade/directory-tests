# -*- coding: utf-8 -*-
from random import choice

from locust import HttpUser, TaskSet, between, task

from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from directory_tests_shared.utils import basic_auth, rare_word

ADVICE_AND_MARKETS = [
    "advice/",
    "advice/create-an-export-plan/",
    "advice/create-an-export-plan/deliver-services-overseas/",
    "advice/create-an-export-plan/how-to-create-an-export-plan/",
    "advice/create-an-export-plan/marketing-services-overseas/",
    "advice/create-an-export-plan/prepare-to-sell-and-deliver-services-overseas/",
    "advice/create-an-export-plan/prepare-to-sell-and-deliver-services-overseas/link",
    "advice/define-route-to-market/",
    "advice/define-route-to-market/create-a-franchise-agreement/",
    "advice/define-route-to-market/create-a-joint-venture-agreement/",
    "advice/define-route-to-market/create-a-licensing-agreement/",
    "advice/define-route-to-market/export-agents/",
    "advice/define-route-to-market/export-distributors/",
    "advice/define-route-to-market/routes-to-market/",
    "advice/define-route-to-market/sell-overseas-directly/",
    "advice/define-route-to-market/set-up-a-business-abroad/",
    "advice/find-an-export-market/",
    "advice/find-an-export-market/research-in-market/",
    "advice/find-an-export-market/trade-shows/",
    "advice/find-an-export-market/understand-export-market-research/",
    "advice/get-export-finance-and-funding/",
    "advice/get-export-finance-and-funding/get-export-finance/",
    "advice/get-export-finance-and-funding/understand-export-finance/",
    "advice/manage-legal-and-ethical-compliance/",
    "advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training/",
    "advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting/",
    "advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations/",
    "advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets/",
    "advice/manage-payment-for-export-orders/",
    "advice/manage-payment-for-export-orders/decide-when-to-get-paid-for-export-orders/",
    "advice/manage-payment-for-export-orders/how-to-create-an-export-invoice/",
    "advice/manage-payment-for-export-orders/insure-against-non-payment/",
    "advice/manage-payment-for-export-orders/managing-non-payment/",
    "advice/manage-payment-for-export-orders/payment-methods-for-exporters/",
    "advice/prepare-for-export-procedures-and-logistics/",
    "advice/prepare-for-export-procedures-and-logistics/documentation-international-trade/",
    "advice/prepare-for-export-procedures-and-logistics/international-trade-contracts-and-incoterms/",
    "advice/prepare-for-export-procedures-and-logistics/moving-goods-and-using-freight-forwarders/",
    "advice/prepare-to-do-business-in-a-foreign-country/",
    "advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website/",
    "advice/prepare-to-do-business-in-a-foreign-country/prepare-your-website-for-international-trade/",
    "advice/prepare-to-do-business-in-a-foreign-country/trade-missions-trade-shows-and-conferences/",
    "advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market/",
    "advice/sell-services-overseas/",
    "advice/sell-services-overseas/market-your-services-overseas/",
    "markets/",
    "markets/?sector=Automotive",
    "markets/?sector=Healthcare",
    "markets/?sector=Security",
    "markets/?sector=Technology",
    "markets/brazil/",
    "markets/germany/",
    "markets/italy/",
    "markets/japan/",
    "markets/netherlands/",
    "markets/south-korea/",
    "markets/turkey/",
    "markets/united-arab-emirates/",
    "markets/usa/",
]


MISC_ENDPOINTS = [
    "",
    "?lang=en-gb",
    "accessibility-statement/",
    "community/",
    "contact/domestic/",
    "contact/feedback/",
    "contact/international/",
    "contact/office-finder/",
    "contact/triage/location/",
    "cookies/",
    "country-cover/",
    "export-opportunities/",
    "export-opportunities/opportunities/occupational-clothing-283",
    "export-opportunities/opportunities?s=shoes&amp;areas[]=&amp;commit=Find+opportunities",
    "get-finance/",
    "get-finance/your-details/",
    "how-we-assess-your-project/",
    "performance-dashboard/",
    "performance-dashboard/export-opportunities/",
    "performance-dashboard/guidance-notes/",
    "performance-dashboard/invest/",
    "performance-dashboard/selling-online-overseas/",
    "performance-dashboard/trade-profiles/",
    "privacy-and-cookies/",
    "privacy-and-cookies/fair-processing-notice-invest-in-great-britain/",
    "project-finance/",
    "report-trade-barrier/",
    "report-trade-barrier/report/about/",
    "services/",
    "success-stories/",
    "success-stories/bubblebum-increase-export-sales/",
    "success-stories/chiswick-retailer-strikes-deal-amazon-australia/",
    "success-stories/derby-rail-business/",
    "success-stories/hello-babys-rapid-online-growth/",
    "success-stories/red-herring-games/",
    "success-stories/york-bag-retailer-goes-global/",
    "terms-and-conditions/",
    "trade-finance/",
    "uk-export-contact-form/",
    "what-we-offer-you/",
]


class DomesticTasks(TaskSet):
    @task
    def advice_and_markets(self):
        self.client.get(
            choice(ADVICE_AND_MARKETS),
            headers=LOAD_TESTS_USER_AGENT,
            name="advice & markets",
            auth=basic_auth(),
        )

    @task
    def misc_pages(self):
        self.client.get(
            choice(MISC_ENDPOINTS),
            headers=LOAD_TESTS_USER_AGENT,
            name="misc pages",
            auth=basic_auth(),
        )

    @task
    def search(self):
        url = URLs.DOMESTIC_SEARCH.relative
        params = {"q": rare_word()}

        self.client.get(
            url,
            params=params,
            headers=LOAD_TESTS_USER_AGENT,
            name="search/?q=[...]",
            auth=basic_auth(),
        )


class Domestic(HttpUser):
    host = settings.DOMESTIC_URL
    tasks = [DomesticTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
