# -*- coding: utf-8 -*-
"""Then step definitions."""
from behave import then

from tests.exred.steps.then_impl import should_be_on_page, should_see_sections


@then('"{actor_name}" should see the "{sections}" sections')
def then_actor_should_see_sections(context, actor_name, sections):
    should_see_sections(context, actor_name, sections)


@then('"{actor_alias}" should be on the "{page_name}" page')
def then_actor_should_be_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)
