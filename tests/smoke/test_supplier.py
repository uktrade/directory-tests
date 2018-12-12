import http.client

import requests

from tests import join_ui_supplier, get_absolute_url


def test_landing_page_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:landing'), cookies=fas_hawk_cookie
    )

    assert response.status_code == http.client.OK


def test_supplier_list_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:suppliers'), cookies=fas_hawk_cookie
    )

    assert response.status_code == http.client.OK


def test_industries_list_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:industries'), cookies=fas_hawk_cookie
    )

    assert response.status_code == http.client.OK


def test_health_industry_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:industries-health'), 
        cookies=fas_hawk_cookie
    )

    assert response.status_code == http.client.OK


def test_tech_industry_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:industries-tech'), 
        cookies=fas_hawk_cookie
    )

    error_msg = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.OK, error_msg


def test_creative_industry_200(fas_hawk_cookie):
    url = get_absolute_url('ui-supplier:industries-creative')
    response = requests.get(url, cookies=fas_hawk_cookie)

    assert response.status_code == http.client.OK


def test_food_industry_200(fas_hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-supplier:industries-food'),
        cookies=fas_hawk_cookie
    )

    error_msg = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.OK, error_msg


def test_supplier_profile_200(fas_hawk_cookie):
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier('suppliers/09400376/the-coconut-company-uk-ltd/')
    response = requests.get(url, cookies=fas_hawk_cookie)

    assert response.status_code == http.client.OK


def test_supplier_contact_200(fas_hawk_cookie):
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier('suppliers/09400376/contact')
    response = requests.get(url, cookies=fas_hawk_cookie)

    assert response.status_code == http.client.OK


def test_case_study_200(fas_hawk_cookie):
    # case study 6 must exist on the environment the tests are ran against.
    url = join_ui_supplier('case-study/6/')

    response = requests.get(url, cookies=fas_hawk_cookie)

    assert response.status_code == http.client.OK
