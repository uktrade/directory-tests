# -*- coding: utf-8 -*-
"""Then steps definitions."""
from behave import then

from steps.then_impl import (
    guidance_ribbon_should_be_visible,
    should_be_on_page,
    should_see_sections_on_home_page
)


@then('"{actor_name}" should see the "{sections}" sections on home page')
def then_actor_should_see_sections(context, actor_name, sections):
    should_see_sections_on_home_page(context, actor_name, sections)


@then('"{actor_alias}" should be on the "{page_name}" page')
def then_actor_should_be_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@then('"{actor_alias}" should see the Guidance Navigation Ribbon')
def then_guidance_ribbon_should_be_visible(context, actor_alias):
    guidance_ribbon_should_be_visible(context, actor_alias)
