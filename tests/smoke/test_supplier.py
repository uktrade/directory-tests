import pytest
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from tests import URLs
from tests.smoke.cms_api_helpers import get_and_assert


def test_landing_page_200(basic_auth):
    url = URLs.FAS_LANDING.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_list_200(basic_auth):
    url = URLs.FAS_SUPPLIERS.absolute
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


def test_industries_list_200(basic_auth):
    url = URLs.FAS_INDUSTRIES.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_health_industry_200(basic_auth):
    url = URLs.FAS_INDUSTRY_HEALTHCARE.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


@pytest.mark.dev
def test_tech_industry_200(basic_auth):
    url = URLs.FAS_INDUSTRY_TECHNOLOGY.absolute
    get_and_assert(url=url, status_code=HTTP_302_FOUND, auth=basic_auth)


@pytest.mark.stage
def test_tech_industry_200(basic_auth):
    url = URLs.FAS_INDUSTRY_TECHNOLOGY.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_creative_industry_200(basic_auth):
    url = URLs.FAS_INDUSTRY_CREATIVE_SERVICES.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_food_industry_200(basic_auth):
    url = URLs.FAS_INDUSTRY_FOOD_AND_DRINK.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_profile_200(basic_auth):
    # company 09466005 must exist on the environment the tests are ran against.
    url = URLs.FAS_SUPPLIERS.absolute_template.format(
        ch_number="09400376", slug="the-coconut-company-uk-ltd"
    )
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_contact_200(basic_auth):
    # company 09466005 must exist on the environment the tests are ran against.
    url = URLs.FAS_CONTACT_SUPPLIER.absolute_template.format(ch_number="09400376")
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


def test_case_study_200(basic_auth):
    # case study 6 must exist on the environment the tests are ran against.
    url = URLs.FAS_CASE_STUDY.absolute_template.format(number="6")
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )
