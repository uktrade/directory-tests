# -*- coding: utf-8 -*-
"""Then steps definitions."""
from behave import then

from steps.then_impl import (
    articles_read_counter_same_as_before_registration,
    articles_should_be_thanked_for_feedback,
    articles_should_not_see_feedback_widget,
    articles_should_not_see_link_to_next_article,
    articles_should_not_see_personas_end_page,
    articles_should_see_article_as_read,
    articles_should_see_in_correct_order,
    articles_should_see_link_to_first_article_from_next_category,
    articles_should_see_read_counter_increase,
    articles_should_see_read_counter_set_to,
    articles_should_see_time_to_complete_decrease,
    articles_total_number_of_articles_should_not_change,
    case_studies_should_see_case_study,
    expected_page_elements_should_not_be_visible_on_get_finance,
    export_readiness_expected_page_elements_should_be_visible,
    export_readiness_should_see_articles,
    guidance_check_if_link_to_next_category_is_displayed,
    guidance_expected_page_elements_should_be_visible,
    guidance_ribbon_should_be_visible,
    guidance_should_see_article_read_counter,
    guidance_should_see_articles,
    guidance_should_see_total_number_of_articles,
    guidance_tile_should_be_highlighted,
    personalised_journey_should_not_see_banner_and_top_10_table,
    personalised_journey_should_see_banner_and_top_10_table,
    personalised_journey_should_see_read_counter,
    personalised_should_see_layout_for,
    should_be_on_page,
    should_see_links_to_services,
    should_see_sections,
    should_see_sections_on_home_page,
    should_see_share_widget,
    triage_should_be_classified_as
)
from steps.when_impl import (
    triage_answer_questions_again,
    triage_should_see_answers_to_questions
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


@then('"{actor_alias}" should see an ordered list of all Guidance Articles selected for "{category}" category')
def then_should_see_guidance_articles(context, actor_alias, category):
    guidance_should_see_articles(context, actor_alias, category)


@then('"{actor_alias}" should see a link to the "{next_category}" Guidance category')
def then_check_if_link_to_next_category_is_displayed(
        context, actor_alias, next_category):
    guidance_check_if_link_to_next_category_is_displayed(
        context, actor_alias, next_category)


@then('"{actor_alias}" should see on the Guidance Articles page "{elements}"')
def then_expected_guidance_page_elements_should_be_visible(
        context, actor_alias, elements):
    guidance_expected_page_elements_should_be_visible(
        context, actor_alias, elements.split(", "))


@then('"{actor_alias}" should see a Guidance Articles read counter for the "{exporter_status}" exporter')
def then_actor_should_see_guidance_articles_read_counter(
        context, actor_alias, exporter_status):
    personalised_journey_should_see_read_counter(
        context, actor_alias, exporter_status)


@then('"{actor_alias}" should be classified as "{classification}" exporter')
def step_impl(context, actor_alias, classification):
    triage_should_be_classified_as(context, actor_alias, classification)


@then('"{actor_alias}" should see the summary page with answers to the questions she was asked')
def then_actor_should_see_answers_to_questions(context, actor_alias):
    triage_should_see_answers_to_questions(context, actor_alias)


@then('"{actor_alias}" should be on the Personalised Journey page for "{classification}" exporters')
def then_classified_exporter_should_be_on_personalised_journey_page(
        context, actor_alias, classification):
    personalised_should_see_layout_for(context, actor_alias, classification)


@then('"{actor_alias}" should be able to answer the triage questions again with his previous answers pre-populated')
def then_actor_should_be_able_to_answer_again(context, actor_alias):
    triage_answer_questions_again(context, actor_alias)


@then('"{actor_alias}" should see an ordered list of all Export Readiness Articles selected for "{category}" Exporters')
def then_should_see_exred_articles(context, actor_alias, category):
    export_readiness_should_see_articles(context, actor_alias, category)


@then('"{actor_alias}" should see on the Export Readiness Articles page "{elements}"')
def then_expected_export_readiness_page_elements_should_be_visible(
        context, actor_alias, elements):
    export_readiness_expected_page_elements_should_be_visible(
        context, actor_alias, elements.split(", "))


@then('"{actor_alias}" should see "{sections}" section on "{page_name}" page')
@then('"{actor_alias}" should see "{sections}" sections on "{page_name}" page')
def then_should_see_sections(context, actor_alias, sections, page_name):
    should_see_sections(context, actor_alias, sections.split(", "), page_name)


@then('"{actor_alias}" should be able to navigate to the next article from the List following the Article Order')
def then_actor_should_see_articles_in_correct_order(context, actor_alias):
    articles_should_see_in_correct_order(context, actor_alias)


@then('"{actor_alias}" should not see the link to the next Article')
def then_there_should_no_link_to_the_next_article(context, actor_alias):
    articles_should_not_see_link_to_next_article(context, actor_alias)


@then('"{actor_alias}" should not see the Personas End Page')
def then_actor_should_not_see_pesonas_end_page(context, actor_alias):
    articles_should_not_see_personas_end_page(context, actor_alias)


@then('"{actor_alias}" should see a link to the fist article from the "{next_category}" category')
def then_actor_should_see_link_to_next_category(
        context, actor_alias, next_category):
    articles_should_see_link_to_first_article_from_next_category(
        context, actor_alias, next_category)


@then('"{actor_alias}" should see this article as read')
def then_actor_should_see_article_as_read(context, actor_alias):
    articles_should_see_article_as_read(context, actor_alias)


@then('"{actor_alias}" should see that Article Read Counter increased by "{increase:d}"')
def then_actor_should_see_read_counter_increase(
        context, actor_alias, increase: int):
    articles_should_see_read_counter_increase(context, actor_alias, increase)


@then('"{actor_alias}" should see that Time to Complete remaining chapters decreased or remained unchanged for short articles')
def then_actor_should_see_time_to_complete_decrease(context, actor_alias):
    articles_should_see_time_to_complete_decrease(context, actor_alias)


@then('feedback widget should disappear')
def then_feedback_widget_should_disappear(context):
    articles_should_not_see_feedback_widget(context)


@then('"{actor_alias}" should be thanked for his feedback')
def then_actor_should_be_thanked_for_the_feedback(context, actor_alias):
    articles_should_be_thanked_for_feedback(context, actor_alias)


@then('"{actor_alias}" should see that Total Number of Articles did not change')
def then_total_number_of_articles_should_not_change(context, actor_alias):
    articles_total_number_of_articles_should_not_change(context, actor_alias)


@then('"{actor_alias}" should see "{case_study_number}" case study')
def then_actor_should_see_case_study(context, actor_alias, case_study_number):
    case_studies_should_see_case_study(context, actor_alias, case_study_number)


@then('"{actor_alias}" should see the Share Widget')
def then_actor_should_see_share_widget(context, actor_alias):
    should_see_share_widget(context, actor_alias)


@then('"{actor_alias}" should see links to following Services "{services}" in "{location}"')
def then_should_see_links_to_services(
        context, actor_alias, services, location):
    should_see_links_to_services(
        context, actor_alias, services.split(", "), location)


@then('"{actor_alias}" should not see "{elements}"')
def step_impl(context, actor_alias, elements):
    expected_page_elements_should_not_be_visible_on_get_finance(
        context, actor_alias, elements.split(", "))


@then('"{actor_alias}" should not see the Top Importer banner and Top 10 Importers table for their sector')
def then_actor_should_not_see_banner_and_top_10_table(context, actor_alias):
    personalised_journey_should_not_see_banner_and_top_10_table(
        context, actor_alias)


@then('"{actor_alias}" should see a Banner and Top importers table for their sector on personalised journey page')
def then_actor_should_see_banner_and_top_10_table(context, actor_alias):
    personalised_journey_should_see_banner_and_top_10_table(
        context, actor_alias)


@then('"{actor_alias}" should see that his reading progress is gone')
def then_reading_progress_should_be_gone(context, actor_alias):
    articles_should_see_read_counter_set_to(context, actor_alias, 0)


@then('"{actor_alias}" should see his reading progress same as before signing in')
@then('"{actor_alias}" should see his reading progress same as before registration')
def then_actor_should_see_previous_reading_progress(context, actor_alias):
    articles_read_counter_same_as_before_registration(context, actor_alias)
