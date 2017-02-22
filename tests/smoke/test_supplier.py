import httplib

import requests

from tests import join_ui_supplier, get_absolute_url


def test_landing_page_200():
    response = requests.get(get_absolute_url('ui-supplier:landing'))

    assert response.status_code == httplib.OK


def test_supplier_list_200():
    response = requests.get(get_absolute_url('ui-supplier:suppliers'))

    assert response.status_code == httplib.OK


def test_industries_list_200():
    response = requests.get(get_absolute_url('ui-supplier:industries'))

    assert response.status_code == httplib.OK


def test_health_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-health'))

    assert response.status_code == httplib.OK


def test_tech_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-tech'))

    assert response.status_code == httplib.OK


def test_creative_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-creative'))

    assert response.status_code == httplib.OK


def test_food_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-food'))

    assert response.status_code == httplib.OK


def test_terms_200():
    response = requests.get(get_absolute_url('ui-supplier:terms'))

    assert response.status_code == httplib.OK


def test_privacy_200():
    response = requests.get(get_absolute_url('ui-supplier:privacy'))

    assert response.status_code == httplib.OK


def test_supplier_profile_200():
    url = join_ui_supplier('suppliers/09466005/michboly-ltd')
    response = requests.get(url)

    assert response.status_code == httplib.OK


def test_supplier_contact_200():
    url = join_ui_supplier('suppliers/09466005/contact')
    response = requests.get(url)

    assert response.status_code == httplib.OK


def test_case_study_200():
    # 
    url = join_ui_supplier('case-study/6/fred')

    response = requests.get(url)

    assert response.status_code == httplib.OK
