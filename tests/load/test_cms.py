# -*- coding: utf-8 -*-
from collections import namedtuple
from random import choice, randint

from locust import TaskSet, between, task

from directory_constants.cms import EXPORT_READINESS, FIND_A_SUPPLIER, INVEST
from directory_tests_shared import URLs, settings
from directory_tests_shared.constants import LOAD_TESTS_USER_AGENT
from tests.load.cms_helpers import CMSAPIAuthClientMixin, get_page_types

UA = namedtuple("UA", "headers")
LOAD_TESTS_USER_AGENT = UA(headers=LOAD_TESTS_USER_AGENT)

SERVICES = [INVEST, FIND_A_SUPPLIER, EXPORT_READINESS]
PAGE_TYPES = get_page_types()

PAGE_PATHS = {
    "2": [
        "",
        "get-finance/",
        "performance-dashboard/",
        "markets",
        "markets/brazil/",
        "markets/germany/",
        "markets/italy/",
        "markets/japan/",
        "markets/netherlands/",
        "markets/south-korea/",
        "markets/china/",
        "markets/turkey/",
        "markets/usa/",
        "markets/united-arab-emirates/",
        "advice/",
        "advice/create-an-export-plan/",
        "advice/find-an-export-market/",
        "advice/define-route-to-market/",
        "advice/manage-payment-for-export-orders/",
        "advice/prepare-to-do-business-in-a-foreign-country/",
        "advice/manage-legal-and-ethical-compliance/",
        "advice/prepare-for-export-procedures-and-logistics/",
        "advice/get-export-finance-and-funding/",
        "advice/sell-services-overseas/",
        "advice/create-an-export-plan/how-to-create-an-export-plan/",
        "advice/create-an-export-plan/deliver-services-overseas/",
        "advice/create-an-export-plan/prepare-to-sell-and-deliver-services-overseas/",
        "advice/create-an-export-plan/marketing-services-overseas/",
        "advice/find-an-export-market/understand-export-market-research/",
        "advice/find-an-export-market/research-in-market/",
        "advice/find-an-export-market/trade-shows/",
        "advice/find-an-export-market/plan-export-market-research/",
        "advice/define-route-to-market/routes-to-market/",
        "advice/define-route-to-market/sell-overseas-directly/",
        "advice/define-route-to-market/export-agents/",
        "advice/define-route-to-market/export-distributors/",
        "advice/define-route-to-market/create-a-licensing-agreement/",
        "advice/define-route-to-market/create-a-franchise-agreement/",
        "advice/define-route-to-market/create-a-joint-venture-agreement/",
        "advice/define-route-to-market/set-up-a-business-abroad/",
        "advice/manage-payment-for-export-orders/how-to-create-an-export-invoice/",
        "advice/manage-payment-for-export-orders/decide-when-to-get-paid-for-export-orders/",
        "advice/manage-payment-for-export-orders/payment-methods-for-exporters/",
        "advice/manage-payment-for-export-orders/insure-against-non-payment/",
        "advice/manage-payment-for-export-orders/managing-non-payment/",
        "advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market/",
        "advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website/",
        "advice/prepare-to-do-business-in-a-foreign-country/trade-missions-trade-shows-and-conferences/",
        "advice/prepare-to-do-business-in-a-foreign-country/prepare-your-website-for-international-trade/",
        "advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets/",
        "advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations/",
        "advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training/",
        "advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting/",
        "advice/prepare-for-export-procedures-and-logistics/plan-logistics-for-exporting/",
        "advice/prepare-for-export-procedures-and-logistics/get-your-export-documents-right/",
        "advice/prepare-for-export-procedures-and-logistics/use-a-freight-forwarder-to-export/",
        "advice/prepare-for-export-procedures-and-logistics/use-incoterms-in-contracts/",
        "advice/get-export-finance-and-funding/understand-export-finance/",
        "advice/get-export-finance-and-funding/get-export-finance/",
        "advice/sell-services-overseas/market-your-services-overseas/",
    ],
    "3": [
        "",
        "eu-exit-form-success",
        "trade",
        "invest/uk-regions",
        "invest/how-we-help-you-expand",
        "invest/how-to-setup-in-the-uk",
        "invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account",
        "invest/how-to-setup-in-the-uk/uk-tax-and-incentives",
        "invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations",
        "invest/how-to-setup-in-the-uk/access-finance-in-the-uk",
        "about-uk/",
        "about-uk/industries/",
        "about-uk/industries/creative-industries/",
        "about-uk/industries/energy/",
        "about-uk/industries/engineering-and-manufacturing/",
        "about-uk/industries/financial-services/",
        "about-uk/industries/health-and-life-sciences/",
        "about-uk/industries/legal-services/",
        "about-uk/industries/real-estate/",
        "about-uk/industries/technology/",
        "about-uk/regions/",
        "about-uk/regions/midlands/",
        "about-uk/regions/north-england/",
        "about-uk/regions/northern-ireland/",
        "about-uk/regions/south-england/",
        "about-uk/regions/wales/",
        "about-uk/why-choose-uk/",
        "about-uk/why-choose-uk/uk-infrastructure/",
        "about-uk/why-choose-uk/uk-talent-and-labour/",
        "about-us/",
        "capital-invest/",
        "capital-invest/contact/",
        "capital-invest/how-we-help-you-invest-capital/",
        "invest/",
        "invest/high-potential-opportunities/contact/",
        "invest/high-potential-opportunities/lightweight-structures/",
        "invest/high-potential-opportunities/rail-infrastructure/",
        "invest/how-to-setup-in-the-uk/",
        "invest/how-to-setup-in-the-uk/access-finance-in-the-uk/",
        "invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations/",
        "invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account/",
        "invest/how-to-setup-in-the-uk/uk-tax-and-incentives/",
        "invest/how-we-help-you-expand/",
        "invest/uk-regions/scotland/",
        "opportunities/",
        "opportunities/birmingham-curzon/",
        "opportunities/real-estate-aero-centre-yorkshire/",
        "opportunities/real-estate-axiom-regional-shopping-centre/",
        "opportunities/real-estate-bargate-quarter/",
        "opportunities/real-estate-bexhill-enterprise-park/",
        "opportunities/real-estate-bicester-motion/",
        "opportunities/real-estate-camro/",
        "opportunities/real-estate-corporation-street-and-tomb-street-belfast/",
        "opportunities/real-estate-dundee-waterfront/",
        "opportunities/real-estate-edinburgh-bioquarter/",
        "opportunities/real-estate-edinburgh-international-business-gateway/",
        "opportunities/real-estate-fawley-waterside/",
        "opportunities/real-estate-festival-park/",
        "opportunities/real-estate-follingsby-max/",
        "opportunities/real-estate-forrest-park/",
        "opportunities/real-estate-future-carrington/",
        "opportunities/real-estate-gateshead-quays/",
        "opportunities/real-estate-george-street-complex/",
        "opportunities/real-estate-island-site/",
        "opportunities/real-estate-kimmerfields/",
        "opportunities/real-estate-kirkstall-forge/",
        "opportunities/real-estate-liverpool-waters/",
        "opportunities/real-estate-magenta/",
        "opportunities/real-estate-mediacityuk/",
        "opportunities/real-estate-mku/",
        "opportunities/real-estate-north-essex-garden-communities/",
        "opportunities/real-estate-otterpool-park/",
        "opportunities/real-estate-paddington-village/",
        "opportunities/real-estate-pall-mall-exchange/",
        "opportunities/real-estate-perth-west/",
        "opportunities/real-estate-protos/",
        "opportunities/real-estate-sixth-building-royal-avenue-belfast/",
        "opportunities/real-estate-stafford-gateway-north/",
        "opportunities/real-estate-stockport-exchange/",
        "opportunities/real-estate-titanic-quarter-belfast/",
        "opportunities/real-estate-trafford-waters/",
        "opportunities/real-estate-uk-central-hub-and-hs2-interchange/",
        "opportunities/real-estate-unity/",
        "opportunities/real-estate-waterside/",
        "opportunities/real-estate-weavers-cross/",
        "opportunities/real-estate-winter-gardens/",
        "opportunities/real-estate-wirral-waters/",
        "opportunities/real-estate-wisbech-garden-town/",
        "opportunities/real-estate-york-central/",
        "trade/how-we-help-you-buy/",
        "invest/",
        "trade/",
        "trade/contact/",
    ],
}


def get_random_query_filter():
    filters = [
        "",
        "?type={}",
        "?title={}".format(
            choice(["Components", "Great Domestic pages", "great.gov.uk international"])
        ),
        "?child_of={}".format(randint(1, 500)),
    ]
    query_filter = choice(filters)
    if query_filter == "?type={}":
        query_filter = "?type={}".format(choice(PAGE_TYPES))
    return query_filter


class CMSTasks(TaskSet):
    @task(1)
    def get_by_random_query_filter(self):
        query_filter = get_random_query_filter()
        endpoint = URLs.CMS_API_PAGES.relative + query_filter
        self.client.get(
            endpoint,
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/[filter]",
            expected_codes=[200, 204, 400, 404],
        )

    @task(4)
    def get_by_id(self):
        self.client.get(
            URLs.CMS_API_PAGE_BY_ID.template.format(page_id=randint(1, 1000)),
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/[pk]/",
            expected_codes=[200, 204, 404],
        )

    @task(2)
    def get_international_page_by_path(self):
        site_id = choice(list(PAGE_PATHS.keys()))
        path = choice(PAGE_PATHS[site_id])
        self.client.get(
            URLs.CMS_API_PAGE_BY_PATH.template.format(site_id=site_id, path=path),
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/lookup-by-path/[site_id]/[path]",
        )


class CMS(CMSAPIAuthClientMixin):
    host = settings.CMS_API_URL
    tasks = [CMSTasks]
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
