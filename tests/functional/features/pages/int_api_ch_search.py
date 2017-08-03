import logging

from jsonschema import validate

from tests import get_absolute_url
from tests.functional.features.utils import Method, assertion_msg, make_request
from tests.functional.schemas.Companies import COMPANIES

URL = get_absolute_url('internal-api:companies-house-search')


def search(term: str) -> dict:
    """Will search for companies using provided term.

    NOTE:
    This will validate the response data against appropriate JSON Schema.

    :param term: search term, can be: company name or number, keywords etc.
    :type term: str
    :return: a JSON response from Companies House Search endpoint
    """
    params = {"term": term}
    response = make_request(Method.GET, URL, params=params,
                            allow_redirects=False)
    with assertion_msg(
            "Expected 200 OK from GET %s but instead got {}. In case you're "
            "getting 301 Redirect then check if you're using correct protocol "
            "https or http", response.url, response.status_code):
        assert response.status_code == 200
    logging.debug("Company House Search result: %s", response.json())
    validate(response.json(), COMPANIES)

    return response.json()
