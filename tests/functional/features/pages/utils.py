# -*- coding: utf-8 -*-
"""Common page helpers"""
from random import choice

from faker import Factory

from tests.functional.features.context_utils import CaseStudy
from tests.functional.features.utils import extract_csrf_middleware_token
from tests.settings import SECTORS, JPEGs, JPGs, PNGs

FAKE = Factory.create()


def extract_and_set_csrf_middleware_token(context, response, supplier_alias):
    """Extract CSRF Token from response & set it in Supplier's scenario data.

    :param context: behave `context` object
    :type  context: behave.runner.Context
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :type  supplier_alias: str
    :param response: request with HTML content containing CSRF middleware token
    :type  response: requests.models.Response
    """
    token = extract_csrf_middleware_token(response)
    context.set_actor_csrfmiddlewaretoken(supplier_alias, token)


def random_case_study_data(alias) -> CaseStudy:
    """Return a CaseStudy populated with randomly generated details.

    :param alias: alias of the Case Study
    :return: a CaseStudy namedtuple
    """
    images = PNGs + JPGs + JPEGs
    (title, summary, description, caption_1, caption_2, caption_3, testimonial,
     testimonial_name, testimonial_job, testimonial_company) = (
        FAKE.sentence() for _ in range(10))
    sector = choice(SECTORS)
    website = "http://{}/fake-case-study-url".format(FAKE.domain_name())
    keywords = ", ".join(FAKE.sentence().replace(".", "").split())
    image_1, image_2, image_3 = (choice(images) for _ in range(3))

    case_study = CaseStudy(
        alias=alias, title=title, summary=summary, description=description,
        sector=sector, website=website, keywords=keywords, image_1=image_1,
        image_2=image_2, image_3=image_3, caption_1=caption_1,
        caption_2=caption_2, caption_3=caption_3, testimonial=testimonial,
        testimonial_name=testimonial_name, testimonial_job=testimonial_job,
        testimonial_company=testimonial_company)

    return case_study
