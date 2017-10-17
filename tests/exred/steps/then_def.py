# -*- coding: utf-8 -*-
"""Then step definitions."""
from behave import then

from tests.exred.steps.then_impl import should_see_sections


@then('"{actor_name}" should see the "{sections}" sections')
def then_actor_should_see_sections(context, actor_name, sections):
    should_see_sections(context, actor_name, sections)
