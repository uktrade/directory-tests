# -*- coding: utf-8 -*-
"""FAB - Add Case Study - Images page"""
import logging
from mimetypes import MimeTypes
from os.path import basename

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.features.context_utils import CaseStudy
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


def should_be_here(response: Response):
    """Check if User is on the correct page.

    :param response: response object
    """
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - images page")


def prepare_form_data(token: str, case_study: CaseStudy) -> (dict, dict):
    """Prepare form data based on the flags and custom values provided.

    :param token: CSRF middleware token required to submit the form
    :param case_study: a CaseStudy namedtuple with random data
    :return: a tuple consisting of form data and files to upload
    """
    def read_image(file_path: str):
        with open(file_path, "rb") as f:
            return f.read()

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

    paths = [case_study.image_1, case_study.image_2, case_study.image_3]
    name_1, name_2, name_3 = (basename(path) for path in paths)
    mime_1, mime_2, mime_3 = (MimeTypes().guess_type(path)[0] for path in paths)
    file_1, file_2, file_3 = (read_image(path) for path in paths)
    files = {
        "rich-media-image_one": (name_1, file_1, mime_1),
        "rich-media-image_two": (name_2, file_2, mime_2),
        "rich-media-image_three": (name_3, file_3, mime_3),
    }

    return data, files


def submit_form(session: Session, token: str, case_study: CaseStudy) -> Response:
    """Submit the form with case study images and extra data.

    :param session: Supplier session object
    :param token: CSRF token required to submit the form
    :param case_study: a CaseStudy namedtuple with random data
    :return: response object
    """
    data, files = prepare_form_data(token, case_study)
    headers = {"Referer": URL}

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data,
        files=files)
    logging.debug("Supplier successfully submitted case study images: %s", data)

    return response
