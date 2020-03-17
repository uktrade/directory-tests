# -*- coding: utf-8 -*-
from behave import then, when
from behave.runner import Context

from tests.periodic_tasks.content_diff.steps.steps_impl import (
    extract_page_content,
    look_for_differences,
)


@when(
    'you look at the "{section}" section of the "{endpoint}" page on "{service}" "{site_a}" and "{site_b}"'
)
def look_at_pages(
    context: Context,
    section: str,
    endpoint: str,
    service: str,
    site_a: str,
    site_b: str,
):
    extract_page_content(context, section, endpoint, service, site_a, site_b)


@then("there should be no differences")
def there_should_be_no_differences(context: Context):
    look_for_differences(context)
