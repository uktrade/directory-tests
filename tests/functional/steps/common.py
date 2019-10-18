# -*- coding: utf-8 -*-
import logging

from requests import Response, Session

from directory_tests_shared.utils import check_for_errors
from tests.functional.pages import fas
from tests.functional.utils.generic import get_number_of_search_result_pages


def can_find_supplier_by_term(
    session: Session, company_title: str, term: str, term_type: str, max_pages: int = 5
) -> (str, Response):
    """

    :param session: Buyer's session object
    :param company_title: sought Supplier name
    :param term: a text used to find the Supplier
    :param term_type: type of the term, e.g.: product, service, keyword etc.
    :param max_pages: maximum number of search results pages to go through
    :return: a tuple with search result (True/False), last search Response and
             an endpoint to company's profile
    """
    response = fas.search.go_to(session, term=term)
    check_for_errors(response.content.decode("UTF-8"), response.url)
    profile_link = fas.search.find_profile_link(response, company_title)
    if profile_link:
        logging.debug(
            f"SEARCH: Found Supplier '{company_title}' on the first FAS search result page. "
            f"Search was done using '{term_type}': '{term}'"
        )
        return profile_link, response

    number_of_pages = get_number_of_search_result_pages(response)

    if number_of_pages < 2:
        logging.debug(f"SEARCH: Search results returned {number_of_pages} pages")
        return profile_link, response

    page_number = 2
    while page_number <= max_pages:
        logging.debug(
            f"SEARCH: page {page_number} out of {number_of_pages} profile_link={profile_link}"
        )
        logging.debug(f"SEARCH: Checking search result page number: {page_number}")
        response = fas.search.go_to(session, term=term, page=page_number)
        check_for_errors(response.content.decode("UTF-8"), response.url)
        profile_link = fas.search.find_profile_link(response, company_title)
        if profile_link:
            logging.debug(
                f"SEARCH: Breaking out of vicious search loop as company "
                f"'{company_title}' was found using '{term_type}': '{term}' on"
                f" {response.url}"
            )
            break
        page_number += 1

    return profile_link, response
