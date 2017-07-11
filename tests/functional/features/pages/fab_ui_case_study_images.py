# -*- coding: utf-8 -*-
"""FAB - Add Case Study - Images page"""
import logging

from faker import Factory
from requests import Response

from tests import get_absolute_url
from tests.functional.features.utils import Method, check_response, make_request

URL = get_absolute_url("ui-buyer:case-study-add")
EXPECTED_STRINGS = [
    "Add images and testimonial", "Basic", "Images",
    "Upload main image for this case study:",
    ("This image will be shown at full width on your case study page and must "
     "be at least 700 pixels wide and in landscape format. For best results, "
     "upload an image at 1820 x 682 pixels."),
    "Add a caption that tells visitors what the main image represents:",
    "Maximum 120 characters", "Upload a second image (optional):",
    "Add a caption that tells visitors what this second image represents:",
    "Upload a third image (optional):",
    "Add a caption that tells visitors what this third image represents:",
    "Testimonial or block quote (optional):",
    ("Add testimonial from a satisfied client or use this space to highlight an"
     " important part of your case study."),
    "Full name of the source of the testimonial (optional):",
    ("Add the source to make the quote more credible and to help buyers "
     "understand the importance of the testimonial."),
    "Job title of the source (optional):", "< Back to previous step", "Save",
    "Company name of the source (optional):"
]
FAKE = Factory.create()


def should_be_here(response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - images page")


def prepare_form_data(token, case_study):
    """Prepare form data based on the flags and custom values provided.

    :param token: CSRF middleware token required to submit the form
    :param case_study: a CaseStudy namedtuple with random data
    :return: a tuple consisting of form data and files to upload
    """
    data = {
        "csrfmiddlewaretoken": token,
        "supplier_case_study_wizard_view-current_step": "rich-media",
        "rich-media-image_one_caption": case_study.caption_1,
        "rich-media-image_two_caption": case_study.caption_2,
        "rich-media-image_three_caption": case_study.caption_3,
        "rich-media-testimonial": case_study.testimonial,
        "rich-media-testimonial_name": case_study.source_name,
        "rich-media-testimonial_job_title": case_study.source_job,
        "rich-media-testimonial_company": case_study.source_company
    }
    files = {
        "rich-media-image_one": open(case_study.image_1, "rb"),
        "rich-media-image_two": open(case_study.image_2, "rb"),
        "rich-media-image_three": open(case_study.image_3, "rb")
    }

    return data, files


def submit_form(context, supplier_alias, case_study) -> Response:
    """Submit the form with case study images and extra data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param case_study: a CaseStudy namedtuple with random data
    :return: response object
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session
    token = actor.csrfmiddlewaretoken
    data, files = prepare_form_data(token, case_study)
    headers = {"Referer": URL}

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data,
        files=files, allow_redirects=False, context=context)
    logging.debug("%s successfully submitted case study images: %s",
                  supplier_alias, data)

    return response
