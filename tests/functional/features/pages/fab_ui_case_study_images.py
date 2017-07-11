# -*- coding: utf-8 -*-
"""FAB - Add Case Study - Images page"""
import logging
from random import choice

from faker import Factory

from tests import get_absolute_url
from tests.functional.features.context_utils import CaseStudy
from tests.functional.features.pages import fab_ui_profile
from tests.functional.features.pages.utils import (
    extract_and_set_csrf_middleware_token
)
from tests.functional.features.utils import Method, check_response, make_request
from tests.settings import JPEGs, JPGs, PNGs

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


def prepare_form_data(
        context, supplier_alias, *, current_case_no=None,
        new_img_1=True, new_img_2=True, new_img_3=True,
        new_caption_1=True, new_caption_2=True, new_caption_3=True,
        new_testimonial=True, new_name=True, new_job=True, new_company=True,
        custom_img_1=None, custom_img_2=None, custom_img_3=None,
        custom_caption_1=None, custom_caption_2=None, custom_caption_3=None,
        custom_testimonial=None, custom_name=None, custom_job=None,
        custom_company=None):
    """Prepare form data based on the flags and custom values provided.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    :param current_case_no: number of current study case stored in scenario data
                            Will use empty one if not provided.
    :param new_img_1: use new Image 1 if True | use current one if False
    :param new_img_2: use new Image 2 if True | use current one if False
    :param new_img_3: use new Image 3 if True | use current one if False
    :param new_caption_1: use new Caption for Image 1 if True | current if False
    :param new_caption_2: use new Caption for Image 2 if True | current if False
    :param new_caption_3: use new Caption for Image 3 if True | current if False
    :param new_testimonial: use new Testimonial if True | current one if False
    :param new_name: use new Source Name if True | current one if False
    :param new_job: use new Source Job Title if True | current one if False
    :param new_company: use new Source Company if True | current one if False
    :param custom_img_1: use custom image 1
    :param custom_img_2: use custom image 2
    :param custom_img_3: use custom image 3
    :param custom_caption_1: use custom caption for image 1
    :param custom_caption_2: use custom caption for image 2
    :param custom_caption_3: use custom caption for image 3
    :param custom_testimonial: use custom testimonial text
    :param custom_name: use custom testimonial source name
    :param custom_job: use custom testimonial source job title
    :param custom_company: use custom testimonial source company name
    :return: a tuple consisting of form data and files to upload
    """
    actor = context.get_actor(supplier_alias)
    company = context.get_company(actor.company_alias)
    token = actor.csrfmiddlewaretoken
    c = company.case_studies.get(current_case_no, CaseStudy())

    # gather a list of all supported images
    images = PNGs + JPGs + JPEGs
    random_img_1, random_img_2, random_img_3 = (choice(images) for _ in range(3))
    (f_caption_1, f_caption_2, f_caption_3, f_testimonial, f_name, f_job,
     f_company) = (FAKE.sentence() for _ in range(7))

    def choose(use_new: bool, fake, custom, current):
        if use_new:
            # explicitly compare to None, as we can send empty string as value
            if custom is not None:
                result = custom
            else:
                result = fake
        else:
            result = current
        return result

    image_1 = choose(new_img_1, random_img_1, custom_img_1, c.image_1)
    image_2 = choose(new_img_2, random_img_2, custom_img_2, c.image_2)
    image_3 = choose(new_img_3, random_img_3, custom_img_3, c.image_3)
    caption_1 = choose(new_caption_1, f_caption_1, custom_caption_1, c.caption_1)
    caption_2 = choose(new_caption_2, f_caption_2, custom_caption_2, c.caption_2)
    caption_3 = choose(new_caption_3, f_caption_3, custom_caption_3, c.caption_3)
    testimonial = choose(new_testimonial, f_testimonial, custom_testimonial, c.testimonial)
    name = choose(new_name, f_name, custom_name, c.source_name)
    job = choose(new_job, f_job, custom_job, c.source_job)
    company = choose(new_company, f_company, custom_company, c.source_company)

    data = {
        "csrfmiddlewaretoken": token,
        "supplier_case_study_wizard_view-current_step": "rich-media",
        "rich-media-image_one_caption": caption_1,
        "rich-media-image_two_caption": caption_2,
        "rich-media-image_three_caption": caption_3,
        "rich-media-testimonial": testimonial,
        "rich-media-testimonial_name": name,
        "rich-media-testimonial_job_title": job,
        "rich-media-testimonial_company": company
    }
    files = {
        "rich-media-image_one": open(image_1, "rb") if image_1 else "",
        "rich-media-image_two": open(image_2, "rb") if image_2 else "",
        "rich-media-image_three": open(image_3, "rb") if image_3 else ""
    }

    return data, files


def submit_form(context, supplier_alias):
    """Submit the form with case study images and extra data.

    :param context: behave `context` object
    :param supplier_alias: alias of the Actor used in the scope of the scenario
    """
    actor = context.get_actor(supplier_alias)
    session = actor.session

    data, files = prepare_form_data(context, supplier_alias)
    headers = {"Referer": URL}
    response = make_request(Method.POST, URL, session=session, headers=headers,
                            data=data, files=files, allow_redirects=False,
                            context=context)

    fab_ui_profile.should_be_here(response)
    extract_and_set_csrf_middleware_token(context, response, supplier_alias)
    logging.debug("%s successfully submitted case study images: %s",
                  supplier_alias, data)
