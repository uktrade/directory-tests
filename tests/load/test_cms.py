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

INTERNATIONAL_PAGE_PATHS = [
    "",
    "eu-exit-form-success",
    "midlands-engine",
    "news",
    "topic/articles",
    "trade",
    "invest/uk-regions",
    "invest/how-we-help-you-expand",
    "invest/how-to-setup-in-the-uk",
    "invest/how-to-setup-in-the-uk/uk-income-tax",
    "invest/how-to-setup-in-the-uk/open-a-uk-business-bank-account",
    "invest/how-to-setup-in-the-uk/uk-visas-and-migration",
    "invest/how-to-setup-in-the-uk/uk-tax-and-incentives",
    "invest/how-to-setup-in-the-uk/establish-a-base-for-business-in-the-uk",
    "invest/how-to-setup-in-the-uk/hire-skilled-workers-for-your-uk-operations",
    "invest/how-to-setup-in-the-uk/register-a-company-in-the-uk",
    "invest/how-to-setup-in-the-uk/access-finance-in-the-uk",
    "invest/how-to-setup-in-the-uk/uk-infrastructure",
    "invest/how-to-setup-in-the-uk/uk-corporation-tax",
    "invest/how-to-setup-in-the-uk/uk-capital-gains-tax",
    "invest/how-to-setup-in-the-uk/uk-income-tax",
    "invest/how-to-setup-in-the-uk/uk-venture-capital-schemes",
    "invest/how-to-setup-in-the-uk/uk-labour-market",
    "invest/how-to-setup-in-the-uk/flexible-uk-labour-terms",
    "invest/how-to-setup-in-the-uk/uk-labour-costs",
]

PAGE_TYPES = get_page_types()


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
    @task
    def get_by_random_query_filter(self):
        query_filter = get_random_query_filter()
        endpoint = URLs.CMS_API_PAGES.relative + query_filter
        self.client.get(
            endpoint,
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/[filter]",
            expected_codes=[200, 400, 404],
        )

    @task
    def get_by_id(self):
        known_broken_pks = [27, 94, 235, 237, 300, 301, 359, 343, 434, 529, 575, 734]
        pk = randint(1, 800)
        while pk in known_broken_pks:
            pk = randint(1, 800)
        self.client.get(
            URLs.CMS_API_PAGE_BY_ID.template.format(page_id=pk),
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/[pk]/",
            expected_codes=[200, 404],
        )

    @task
    def get_international_page_by_path(self):
        self.client.get(
            URLs.CMS_API_PAGE_BY_PATH.template.format(
                site_id=2, path=choice(INTERNATIONAL_PAGE_PATHS)
            ),
            authenticator=LOAD_TESTS_USER_AGENT,
            name="/api/pages/lookup-by-path/[site_id]/[path]",
            expected_codes=[200, 404],
        )


class CMS(CMSAPIAuthClientMixin):
    host = settings.CMS_API_URL
    task_set = CMSTasks
    wait_time = between(settings.LOCUST_MIN_WAIT, settings.LOCUST_MAX_WAIT)
