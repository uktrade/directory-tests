import http.client

import pytest
import requests
from retrying import retry

from tests import get_absolute_url, is_500


def test_about_200(basic_auth, hawk_cookie):
    response = requests.get(
        get_absolute_url('profile:about'), allow_redirects=False,
        auth=basic_auth,
        cookies=hawk_cookie
    )

    assert response.status_code == http.client.OK


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:landing'),
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_301_redirects_for_anon_user(absolute_url, basic_auth, hawk_cookie):
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth, cookies=hawk_cookie
    )
    error_msg = f"Expected 301 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.FOUND, error_msg


@pytest.mark.skip(reason="see bug ED-3050")
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_302_redirects_after_removing_trailing_slash_for_anon_user(
        absolute_url, basic_auth, hawk_cookie):
    # get rid of trailing slash
    if absolute_url[-1] == "/":
        absolute_url = absolute_url[:-1]
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth, cookies=hawk_cookie
    )
    error_msg = f"Expected 302 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.MOVED_PERMANENTLY, error_msg


@pytest.mark.session_auth
@retry(wait_fixed=3000, stop_max_attempt_number=2, retry_on_exception=is_500)
@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('profile:landing'),
    get_absolute_url('profile:soo'),
    get_absolute_url('profile:fab'),
    get_absolute_url('profile:exops-alerts'),
    get_absolute_url('profile:exops-applications'),
])
def test_access_to_non_health_check_endpoints_as_logged_in_user(
        logged_in_session, absolute_url, basic_auth, hawk_cookie):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, auth=basic_auth, cookies=hawk_cookie
    )
    error_msg = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == http.client.OK, error_msg
