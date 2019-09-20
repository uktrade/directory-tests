# -*- coding: utf-8 -*-
"""Profile - Add Case Study - Images page"""
import logging
from mimetypes import MimeTypes
from os.path import basename

from requests import Response, Session
from retrying import retry

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.context_utils import CaseStudy
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Add case study (images)"
TYPE = PageType.FORM
URL = URLs.PROFILE_CASE_STUDY_IMAGES.absolute
EXPECTED_STRINGS = [
    "Add a caption that tells visitors what the main image represents",
    "Upload a second image",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on 'Create case study or project' - images page")


def prepare_form_data(token: str, case_study: CaseStudy) -> (dict, dict):
    """Prepare form data based on the flags and custom values provided."""
    data = {
        "csrfmiddlewaretoken": token,
        "case_study_wizard_create_view-current_step": "images",
        "images-image_one_caption": case_study.caption_1,
        "images-image_two_caption": case_study.caption_2,
        "images-image_three_caption": case_study.caption_3,
        "images-testimonial": case_study.testimonial,
        "images-testimonial_name": case_study.source_name,
        "images-testimonial_job_title": case_study.source_job,
        "images-testimonial_company": case_study.source_company,
    }

    paths = [case_study.image_1, case_study.image_2, case_study.image_3]

    def get_basename(path):
        return basename(path) if path is not None else ""

    def get_mimetype(path):
        return MimeTypes().guess_type(path)[0] if path is not None else ""

    def read_image(path: str):
        res = ""
        if path is not None:
            with open(path, "rb") as f:
                res = f.read()
        return res

    name_1, name_2, name_3 = (get_basename(path) for path in paths)
    mime_1, mime_2, mime_3 = (get_mimetype(path) for path in paths)
    file_1, file_2, file_3 = (read_image(path) for path in paths)
    files = {
        "images-image_one": (name_1, file_1, mime_1),
        "images-image_two": (name_2, file_2, mime_2),
        "images-image_three": (name_3, file_3, mime_3),
    }

    return data, files


@retry(wait_fixed=10000, stop_max_attempt_number=2)
def submit(session: Session, token: str, case_study: CaseStudy) -> Response:
    """Submit the form with case study images and extra data."""
    data, files = prepare_form_data(token, case_study)
    headers = {"Referer": URL}

    logging.debug(f"DATA: {data}")
    file_names = {k: v[0] for k, v in files.items()}
    logging.debug(f"FILES: {file_names}")
    response = make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        data=data,
        files=files,
        trim=True,
    )
    logging.debug("Supplier successfully submitted case study images: %s", data)

    return response
