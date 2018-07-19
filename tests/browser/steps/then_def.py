# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""Then steps definitions."""
from behave import then
from behave.runner import Context

from steps.then_impl import (
    articles_read_counter_same_as_before_registration,
    articles_read_counter_should_be_merged,
    articles_should_be_on_share_page,
    articles_should_be_thanked_for_feedback,
    articles_should_not_see_feedback_widget,
    articles_should_not_see_link_to_next_article,
    articles_should_not_see_link_to_register,
    articles_should_not_see_link_to_sign_in,
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
    fas_search_results_filtered_by_industries,
    guidance_check_if_link_to_next_category_is_displayed,
    guidance_expected_page_elements_should_be_visible,
    guidance_ribbon_should_be_visible,
    guidance_should_see_article_read_counter,
    guidance_should_see_articles,
    guidance_should_see_total_number_of_articles,
    guidance_tile_should_be_highlighted,
    header_check_dit_logo,
    header_check_favicon,
    invest_should_see_topic_contents,
    invest_should_see_uk_gov_logo,
    language_selector_keyboard_should_be_trapped,
    language_selector_should_not_see_it,
    language_selector_should_see_it,
    personalised_journey_should_not_see_banner_and_top_10_table,
    personalised_journey_should_see_banner_and_top_10_table,
    personalised_journey_should_see_read_counter,
    personalised_should_see_layout_for,
    promo_video_check_watch_time,
    promo_video_should_not_see_modal_window,
    share_page_should_be_prepopulated,
    share_page_via_email_should_have_article_details,
    should_be_on_page,
    should_be_on_page_or_international_page,
    should_not_see_sections,
    should_see_links_to_services,
    should_see_page_in_preferred_language,
    should_see_sections,
    should_see_share_widget,
    triage_should_be_classified_as,
    triage_should_see_change_your_answers_link,
    generic_should_see_expected_page_content,
    stats_and_tracking_elements_should_be_present,
    stats_and_tracking_elements_should_not_be_present,
)
from steps.when_impl import (
    triage_answer_questions_again,
    triage_should_see_answers_to_questions
)


@then('"{actor_alias}" should be on the "{page_name}" page')
def then_actor_should_be_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@then('"{actor_alias}" should be on the "{page_name}" page or on the International page')
def then_actor_should_be_on_page_on_international_page(
        context, actor_alias, page_name):
    should_be_on_page_or_international_page(context, actor_alias, page_name)


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
def then_actor_should_be_classified_as(context, actor_alias, classification):
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


@then('"{actor_alias}" should see following sections')
def then_should_see_sections(context, actor_alias):
    should_see_sections(context, actor_alias, sections_table=context.table)


@then('"{actor_alias}" should not see "{sections}" section on "{page_name}" page')
@then('"{actor_alias}" should not see "{sections}" sections on "{page_name}" page')
def then_should_not_see_sections(context, actor_alias, sections, page_name):
    should_not_see_sections(context, actor_alias, sections.split(", "), page_name)


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


@then('"{actor_alias}" should not see the link to sign in on the "{page_name}" page')
def then_actor_should_not_see_sign_in_link(context, actor_alias, page_name):
    articles_should_not_see_link_to_sign_in(context, actor_alias, page_name)


@then('"{actor_alias}" should not see the link to register on the "{page_name}" page')
def then_actor_should_not_see_register_link(context, actor_alias, page_name):
    articles_should_not_see_link_to_register(context, actor_alias, page_name)


@then('"{actor_alias}"\'s current reading progress should be merged with the one from before signing out without any overwriting')
def then_actror_should_see_reading_progress_merged(context, actor_alias):
    articles_read_counter_should_be_merged(context, actor_alias)


@then('"{actor_alias}" should be taken to a new tab with the "{social_media}" share page opened')
def then_actor_should_be_on_share_page(context, actor_alias, social_media):
    articles_should_be_on_share_page(context, actor_alias, social_media)


@then('"{actor_alias}" should that "{social_media}" share page has been pre-populated with message and the link to the article')
def then_share_page_should_be_prepopulated(context, actor_alias, social_media):
    share_page_should_be_prepopulated(context, actor_alias, social_media)


@then('"{actor_alias}" should see that the share via email link will pre-populate the message subject and body with Article title and URL')
def then_check_share_via_email_link(context, actor_alias):
    share_page_via_email_should_have_article_details(context, actor_alias)


@then('"{actor_alias}" should see an option to change his triage answers')
def then_actor_should_see_option_to_change_triage_answers(context, actor_alias):
    triage_should_see_change_your_answers_link(context, actor_alias)


@then('"{actor_alias}" should be able to watch at least first "{expected_watch_time:d}" seconds of the promotional video')
def then_actor_should_watch_the_promo_video(
        context, actor_alias, expected_watch_time: int):
    promo_video_check_watch_time(context, actor_alias, expected_watch_time)


@then('"{actor_alias}" should not see the window with promotional video')
def then_actor_should_not_see_video_modal_window(context, actor_alias):
    promo_video_should_not_see_modal_window(context, actor_alias)


@then('"{actor_alias}" should see correct DIT logo in page header')
def then_actor_should_see_correct_dit_logo(context, actor_alias):
    header_check_dit_logo(context, actor_alias)


@then('"{actor_alias}" should see the language selector')
def then_actor_should_see_language_selector(context, actor_alias):
    language_selector_should_see_it(context, actor_alias)


@then('"{actor_alias}" should not see the language selector')
def then_actor_should_not_see_language_selector(context, actor_alias):
    language_selector_should_not_see_it(context, actor_alias)


@then('"{actor_alias}"\'s keyboard should be trapped to the language selector')
def then_keyboard_should_be_trapped_to_language_selector(context, actor_alias):
    language_selector_keyboard_should_be_trapped(context, actor_alias)


@then('"{actor_alias}" should see the page in "{preferred_language}"')
def then_page_language_should_be(context, actor_alias, preferred_language):
    should_see_page_in_preferred_language(
        context, actor_alias, preferred_language)


@then('"{actor_alias}" should see the correct favicon')
def then_actor_should_see_correct_favicon(context, actor_alias):
    header_check_favicon(context, actor_alias)


@then('"{actor_alias}" should see content specific to "{industry_name}" page')
def fas_then_actor_should_see_expected_content(
        context: Context, actor_alias: str, industry_name: str):
    generic_should_see_expected_page_content(context, actor_alias, industry_name)


@then('"{actor_alias}" should see search results filtered by "{industry_names}" industries')
@then('"{actor_alias}" should see search results filtered by "{industry_names}" industry')
def fas_should_see_filtered_search_results(
        context: Context, actor_alias: str, industry_names: str):
    fas_search_results_filtered_by_industries(
        context, actor_alias, industry_names.split(", "))


@then('"{actor_alias}" should see brief explanation why the UK is the best place for his business')
def then_actor_should_see_topic_content(context: Context, actor_alias: str):
    invest_should_see_topic_contents(context, actor_alias)


@then('following web statistics analysis or tracking elements should NOT be present')
def then_stats_and_tracking_elements_should_be_present(context: Context):
    stats_and_tracking_elements_should_not_be_present(context, context.table)


@then('following web statistics analysis or tracking elements should be present')
def then_stats_and_tracking_elements_should_be_present(context: Context):
    stats_and_tracking_elements_should_be_present(context, context.table)


@then('"{actor_alias}" should see correct UK Government logo in page "{section}"')
def then_user_should_see_uk_gov_logo(
        context: Context, actor_alias: str, section: str):
    invest_should_see_uk_gov_logo(context, actor_alias, section)