import pytest
from rest_framework.status import HTTP_302_FOUND

from tests import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.skip(reason="See CMS-1834")
@pytest.mark.parametrize(
    "old_url,to_new_endpoint",
    [
        (
            URLs.FAS_INDUSTRIES_HEALTH.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(endpoint="industries/health")
        ),
        (
            URLs.FAS_INDUSTRIES_TECH.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(endpoint="industries/tech")
        ),
        (
            URLs.FAS_INDUSTRIES_CREATIVE.absolute,
            URLs.FAS_INCOMING_REDIRECT.absolute_template.format(endpoint="industries/creative")
        ),
    ],
)
def test_ed_4152_redirect_on_stage_from_old_industry_page(
    old_url, to_new_endpoint, basic_auth
):
    response = get_and_assert(
        url=old_url,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
        allow_redirects=False,
    )

    error_msg = (
        f"Expected request to '{old_url}' to be redirected to "
        f"'{to_new_endpoint}' but instead it was redirected to "
        f"'{response.headers['Location']}'"
    )
    assert response.headers["Location"] == to_new_endpoint, error_msg
