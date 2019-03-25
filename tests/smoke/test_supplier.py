from rest_framework.status import HTTP_200_OK

from tests import get_absolute_url, join_ui_supplier
from tests.smoke.cms_api_helpers import get_and_assert


def test_landing_page_200(basic_auth):
    url = get_absolute_url("ui-supplier:landing")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_list_200(basic_auth):
    url = get_absolute_url("ui-supplier:suppliers")
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


def test_industries_list_200(basic_auth):
    url = get_absolute_url("ui-supplier:industries")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_health_industry_200(basic_auth):
    url = get_absolute_url("ui-supplier:industries-health")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_tech_industry_200(basic_auth):
    url = get_absolute_url("ui-supplier:industries-tech")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_creative_industry_200(basic_auth):
    url = get_absolute_url("ui-supplier:industries-creative")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_food_industry_200(basic_auth):
    url = get_absolute_url("ui-supplier:industries-food")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_profile_200(basic_auth):
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier("suppliers/09400376/the-coconut-company-uk-ltd/")
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_contact_200(basic_auth):
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier("suppliers/09400376/contact/")
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


def test_case_study_200(basic_auth):
    # case study 6 must exist on the environment the tests are ran against.
    url = join_ui_supplier("case-study/6/")
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )
