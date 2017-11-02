# -*- coding: utf-8 -*-
"""Then steps definitions."""
from behave import then

from steps.then_impl import (
    guidance_ribbon_should_be_visible,
    guidance_should_see_article_read_counter,
    guidance_should_see_total_number_of_articles,
    guidance_tile_should_be_highlighted,
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


@then('"{actor_alias}" should see that the banner tile for "{tile}" category is highlighted')
def then_guidance_tile_should_be_highlighted(context, actor_alias, tile):
    guidance_tile_should_be_highlighted(context, actor_alias, tile)


@then('"{actor_alias}" should see an article read counter for the "{category}" Guidance category set to "{expected:d}"')
def then_should_see_article_read_counter(
        context, actor_alias, category, expected: int):
    guidance_should_see_article_read_counter(
        context, actor_alias, category, expected)


@then('"{actor_alias}" should see total number of articles for the "{category}" Guidance category')
def then_total_number_of_articles_should_be_visible(context, actor_alias, category):
    guidance_should_see_total_number_of_articles(context, actor_alias, category)
