# -*- coding: utf-8 -*-
from random import choice

from rest_framework.status import HTTP_200_OK

import allure
from directory_tests_shared import URLs
from directory_tests_shared.constants import SECTORS
from directory_tests_shared.utils import rare_word
from tests.smoke.cms_api_helpers import get_and_assert

pytestmark = [allure.suite("FAS"), allure.feature("FAS")]


def test_landing_page_200(basic_auth):
    url = URLs.FAS_LANDING.absolute
    get_and_assert(url=url, status_code=HTTP_200_OK, auth=basic_auth)


def test_supplier_list_200(basic_auth):
    url = URLs.FAS_SUPPLIERS.absolute
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


def test_search_supplier_200(basic_auth):
    sector = choice(SECTORS)
    url = URLs.FAS_SEARCH.absolute_template.format(query=rare_word(), industries=sector)
    get_and_assert(
        url=url, status_code=HTTP_200_OK, auth=basic_auth, allow_redirects=True
    )


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
