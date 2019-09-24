# -*- coding: utf-8 -*-
"""Find a Buyer - Upload Logo page"""
import logging
import mimetypes
import os

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Service.PROFILE
NAME = "Upload logo"
TYPE = PageType.FORM
URL = URLs.PROFILE_UPLOAD_LOGO.absolute
EXPECTED_STRINGS = [
    "Company logo",
    "Logo:",
    (
        "For best results this should be a transparent PNG file of 600 x 600 "
        "pixels and no more than 2MB"
    ),
]

EXPECTED_STRINGS_INVALID = [
    "Invalid image format, allowed formats: PNG, JPG, JPEG",
    (
        "Upload a valid image. The file you uploaded was either not an image or a"
        " corrupted image."
    ),
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the FAB Upload Logo page")


def upload(session: Session, file_path: str) -> Response:
    headers = {"Referer": URLs.PROFILE_UPLOAD_LOGO.absolute}
    data = {"company_profile_logo_edit_view-current_step": "logo"}
    with open(file_path, "rb") as f:
        picture = f.read()
    mime = mimetypes.MimeTypes().guess_type(file_path)[0]
    files = {"logo": (os.path.basename(file_path), picture, mime)}
    response = make_request(
        Method.POST,
        URL,
        session=session,
        headers=headers,
        data=data,
        files=files,
        trim=True,
    )
    return response


def was_upload_rejected(response: Response) -> bool:
    """Check if uploaded file was rejected or not."""
    content = response.content.decode("utf-8")
    has_error = any([phrase in content for phrase in EXPECTED_STRINGS_INVALID])
    is_200 = response.status_code == 200
    return is_200 and has_error
