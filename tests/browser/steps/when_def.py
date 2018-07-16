# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""When step definitions."""
from behave import when
from behave.runner import Context

from steps.then_impl import triage_should_be_classified_as
from steps.when_impl import (
    articles_found_useful_or_not,
    articles_go_back_to_article_list,
    articles_go_back_to_last_read_article,
    articles_go_back_to_same_group,
    articles_open_any,
    articles_open_any_but_the_last,
    articles_open_group,
    articles_share_on_social_media,
    articles_show_all,
    case_studies_go_to,
    clear_the_cookies,
    click_on_page_element,
    continue_export_journey,
    export_readiness_open_category,
    fas_fill_out_and_submit_contact_us_form,
    fas_search_for_companies,
    fas_use_breadcrumb,
    fas_view_article,
    fas_view_more_companies,
    fas_view_selected_company_profile,
    generic_click_on_uk_gov_logo,
    generic_open_guide_link,
    generic_open_industry_page,
    generic_see_more_industries,
    generic_unfold_topics,
    guidance_open_category,
    guidance_read_through_all_articles,
    header_footer_click_on_dit_logo,
    header_footer_open_link,
    invest_read_more,
    language_selector_change_to,
    language_selector_close,
    language_selector_navigate_through_links_with_keyboard,
    language_selector_open,
    open_link,
    open_service_link_on_interim_page,
    personalised_choose_sector,
    personalised_journey_create_page,
    personalised_journey_update_preference,
    promo_video_close,
    promo_video_watch,
    registration_go_to,
    registration_submit_form_and_verify_account,
    set_sector_preference,
    sign_in,
    sign_out,
    start_triage,
    triage_are_you_incorporated,
    triage_change_answers,
    triage_create_exporting_journey,
    triage_do_you_export_regularly,
    triage_go_through_again,
    triage_have_you_exported_before,
    triage_question_what_do_you_want_to_export,
    triage_say_whether_you_use_online_marketplaces,
    triage_should_see_answers_to_questions,
    triage_what_is_your_company_name,
    visit_page,
)


@when('"{actor_alias}" decides to get started in Exporting journey section')
def when_actor_starts_triage(context, actor_alias):
    start_triage(context, actor_alias)


@when('"{actor_alias}" decides to continue in Exporting journey section')
def when_actor_continues_export_journey(context, actor_alias):
    continue_export_journey(context, actor_alias)


@when('"{actor_alias}" goes to the "{category}" Guidance articles via "{location}"')
def when_actor_goes_to_guidance_articles(
        context, actor_alias, category, location):
    guidance_open_category(context, actor_alias, category, location)


@when('"{actor_alias}" creates a personalised journey page for herself')
def when_actor_creates_personalised_journey_page(context, actor_alias):
    personalised_journey_create_page(context, actor_alias)


@when('"{actor_alias}" says what does he wants to export')
@when('"{actor_alias}" says what does she wants to export')
def when_actor_says_what_he_wants_to_export(context, actor_alias):
    personalised_choose_sector(context, actor_alias)


@when('"{actor_alias}" says that he "{has_or_has_never}" exported before')
@when('"{actor_alias}" says that she "{has_or_has_never}" exported before')
def when_actor_answers_whether_he_exported_before(
        context, actor_alias, has_or_has_never):
    triage_have_you_exported_before(context, actor_alias, has_or_has_never)


@when('"{actor_alias}" says that exporting is "{regular_or_not}" part of her business')
@when('"{actor_alias}" says that exporting is "{regular_or_not}" part of his business')
def when_actor_tells_whether_he_exports_regularly_or_not(
        context, actor_alias, regular_or_not):
    triage_do_you_export_regularly(context, actor_alias, regular_or_not)


@when('"{actor_alias}" says that her company "{is_or_not}" incorporated')
@when('"{actor_alias}" says that his company "{is_or_not}" incorporated')
def when_actor_says_whether_company_is_incorporated(
        context, actor_alias, is_or_not):
    triage_are_you_incorporated(context, actor_alias, is_or_not)


@when('"{actor_alias}" "{decision}" her company name')
@when('"{actor_alias}" "{decision}" his company name')
def when_actor_decide_to_enter_company_name(context, actor_alias, decision):
    triage_what_is_your_company_name(context, actor_alias, decision)


@when('"{actor_alias}" sees the summary page with answers to the questions he was asked')
@when('"{actor_alias}" sees the summary page with answers to the questions she was asked')
def when_actor_sees_answers_to_the_questions(context, actor_alias):
    triage_should_see_answers_to_questions(context, actor_alias)


@when('"{actor_alias}" decides to create her personalised journey page')
@when('"{actor_alias}" decides to create his personalised journey page')
def when_actor_decides_to_create_personalised_page(context, actor_alias):
    triage_create_exporting_journey(context, actor_alias)


@when('"{actor_alias}" can see that he was classified as a "{classification}" exporter')
@when('"{actor_alias}" can see that she was classified as a "{classification}" exporter')
def when_actor_is_classified_as(context, actor_alias, classification):
    triage_should_be_classified_as(context, actor_alias, classification)


@when('"{actor_alias}" says that she "{decision}" used online marketplaces')
def when_actor_says_whether_he_used_online_marktet_places(
        context, actor_alias, decision):
    triage_say_whether_you_use_online_marketplaces(
        context, actor_alias, decision)


@when('"{actor_alias}" decides to change her answers')
@when('"{actor_alias}" decides to change his answers')
def when_actor_decides_to_change_the_answers(context, actor_alias):
    triage_change_answers(context, actor_alias)


@when('"{actor_alias}" goes to the Export Readiness Articles for "{category}" Exporters via "{location}"')
def when_actor_goes_to_exred_articles(context, actor_alias, category, location):
    export_readiness_open_category(context, actor_alias, category, location)


@when('"{actor_alias}" decides to read through all remaining Articles from selected list')
@when('"{actor_alias}" decides to read through all Articles from selected list')
def when_actor_reads_through_all_guidance_articles(context, actor_alias):
    guidance_read_through_all_articles(context, actor_alias)


@when('"{actor_alias}" opens any Article but the last one')
def when_actor_opens_any_article_but_the_last_one(context, actor_alias):
    articles_open_any_but_the_last(context, actor_alias)


@when('"{actor_alias}" opens any article on the list')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)


@when('"{actor_alias}" goes back to the Article List page')
def when_actor_goes_back_to_article_list(context, actor_alias):
    articles_go_back_to_article_list(context, actor_alias)


@when('"{actor_alias}" decides to tell us that he "{useful_or_not}" this article useful')
@when('"{actor_alias}" decides to tell us that she "{useful_or_not}" this article useful')
def when_actor_tells_us_about_usefulness(context, actor_alias, useful_or_not):
    articles_found_useful_or_not(context, actor_alias, useful_or_not)


@when('"{actor_alias}" goes to the "{case_number}" Case Study via carousel')
def when_actor_goes_to_case_study(context, actor_alias, case_number):
    case_studies_go_to(context, actor_alias, case_number)


@when('"{actor_alias}" goes to "{category}" using "{group}" link on "{location}"')
@when('"{actor_alias}" goes to "{category}" using "{group}" links in "{location}"')
def when_actor_opens_link(context, actor_alias, category, group, location):
    open_link(context, actor_alias, group, category, location)


@when('"{actor_alias}" opens the link to "{service}" from interim page')
def when_open_service_link_on_interim_page(context, actor_alias, service):
    open_service_link_on_interim_page(context, actor_alias, service)


@when('"{actor_alias}" decides to change the sector to "{service}" service')
def when_actor_sets_sector_service_preference(context, actor_alias, service):
    set_sector_preference(context, actor_alias, service=service)


@when('"{actor_alias}" decides to change the sector to "{good}" good')
def when_actor_sets_sector_good_preference(context, actor_alias, good):
    set_sector_preference(context, actor_alias, good=good)


@when('"{actor_alias}" decides to update his triage preferences')
def when_actor_updates_triage_preferences(context, actor_alias):
    personalised_journey_update_preference(context, actor_alias)


@when('"{actor_alias}" goes through triage again')
def when_actor_goes_through_triage_again(context, actor_alias):
    triage_go_through_again(context, actor_alias)


@when('"{actor_alias}" decides to register to save her reading progress using link visible in the "{location}"')
@when('"{actor_alias}" decides to register to save his reading progress using link visible in the "{location}"')
def when_actor_decides_to_register(context, actor_alias, location):
    registration_go_to(context, actor_alias, location)


@when('"{actor_alias}" completes the registration and fake email verification process')
def when_actor_registers_fake_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=True)


@when('"{actor_alias}" completes the registration and real email verification process')
def when_actor_registers_real_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=False)


@when('"{actor_alias}" signs out and forgets the article reading history by clearing the cookies')
def when_actor_clears_the_cookies(context, actor_alias):
    clear_the_cookies(context, actor_alias)


@when('"{actor_alias}" signs in')
@when('"{actor_alias}" signs in using link visible in the "{location}"')
def when_actor_signs_in(context, actor_alias, *, location="top bar"):
    sign_in(context, actor_alias, location)


@when('"{actor_alias}" goes to the "{page_name}" page')
def when_actor_goes_to_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@when('"{actor_alias}" goes back to the same "{group}" Article category via "{location}"')
def when_actor_goes_to_the_same_article_group(
        context, actor_alias, group, location):
    articles_go_back_to_same_group(context, actor_alias, group, location=location)


@when('"{actor_alias}" goes back to the last Article he read')
@when('"{actor_alias}" goes back to the last Article she read')
def when_actor_goes_to_last_read_article(context, actor_alias):
    articles_go_back_to_last_read_article(context, actor_alias)


@when('"{actor_alias}" signs out')
def when_actor_signs_out(context, actor_alias):
    sign_out(context, actor_alias)


@when('"{actor_alias}" goes to randomly selected "{group}" Article category via "{location}"')
def when_actor_is_on_article_list(context, actor_alias, group, location):
    articles_open_group(context, actor_alias, group, location=location)


@when('"{actor_alias}" goes to randomly selected "{group}" Article category')
def when_actor_goes_to_random_article_group(context, actor_alias, group):
    articles_open_group(context, actor_alias, group)


@when('"{actor_alias}" decides to share the article via "{social_media}"')
def when_actor_shares_article(context, actor_alias, social_media):
    articles_share_on_social_media(context, actor_alias, social_media)


@when('"{actor_alias}" decides to watch "{play_time:d}" seconds of the promotional video')
@when('"{actor_alias}" decides to watch the promotional video')
def when_actor_decides_to_watch_promo_video(
        context, actor_alias, *, play_time: int = None):
    promo_video_watch(context, actor_alias, play_time=play_time)


@when('"{actor_alias}" closes the window with promotional video')
def when_actor_decides_to_close_the_promotional_video(context, actor_alias):
    promo_video_close(context, actor_alias)


@when('"{actor_alias}" opens up the language selector')
def when_actor_opens_up_language_selector(context, actor_alias):
    language_selector_open(context, actor_alias)


@when('"{actor_alias}" closes the language selector')
def when_actor_closes_language_selector(context, actor_alias):
    language_selector_close(context, actor_alias)


@when('"{actor_alias}" opens up the language selector using her keyboard')
@when('"{actor_alias}" opens up the language selector using his keyboard')
def when_actor_opens_up_language_selector_with_keyboard(context, actor_alias):
    language_selector_open(context, actor_alias, with_keyboard=True)


@when('"{actor_alias}" closes the language selector using his keyboard')
def when_actor_closes_language_selector_with_keyboard(context, actor_alias):
    language_selector_close(context, actor_alias, with_keyboard=True)


@when('"{actor_alias}" uses her keyboard to navigate through all links visible on language selector')
@when('"{actor_alias}" uses his keyboard to navigate through all links visible on language selector')
def when_actor_navigates_through_language_selector_links_with_keyboard(
        context, actor_alias):
    language_selector_navigate_through_links_with_keyboard(context, actor_alias)


@when('"{actor_alias}" decides to view the page in "{preferred_language}"')
def when_actor_views_page_in_selected_language(
        context, actor_alias, preferred_language):
    language_selector_change_to(context, actor_alias, preferred_language)


@when('"{actor_alias}" shows all of the articles on the page whenever possible')
def given_actor_shows_all_articles(context, actor_alias):
    articles_show_all(context, actor_alias)


@when('"{actor_alias}" goes to the "{page_name}" page via "{group}" links in "{location}"')
def when_actor_opens_link_from_header_menu(context, actor_alias, page_name, group, location):
    header_footer_open_link(context, actor_alias, group, page_name, location)


@when('"{actor_alias}" decides to use "{element_name}" button on "{page_name}" page')
@when('"{actor_alias}" decides to use "{element_name}" link on "{page_name}" page')
@when('"{actor_alias}" decides to use "{element_name}" link from page "{page_name}"')
@when('"{actor_alias}" decides to use "{element_name}" on "{page_name}" page')
@when('"{actor_alias}" decides to use "{element_name}" button in "{page_name}"')
@when('"{actor_alias}" decides to use "{element_name}" link in "{page_name}"')
@when('"{actor_alias}" decides to use "{element_name}" in "{page_name}"')
@when('"{actor_alias}" decides to "{element_name}" via "{page_name}" page')
def when_actor_decides_to_click_on_page_element(
        context, actor_alias, element_name, page_name):
    click_on_page_element(context, actor_alias, element_name, page_name)


@when('"{actor_alias}" says what he wants to export "{goods_or_services}"')
@when('"{actor_alias}" says what she wants to export "{goods_or_services}"')
def when_actor_says_what_is_exported(context, actor_alias, goods_or_services):
    triage_question_what_do_you_want_to_export(context, actor_alias, goods_or_services)


@when('"{actor_alias}" decides to click on the DIT logo in the "{logo_location}"')
def when_actor_clicks_on_the_dit_logo(context, actor_alias, logo_location):
    header_footer_click_on_dit_logo(context, actor_alias, logo_location)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword in "{sector}" sector on "{page_alias}" page')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str, sector: str,
        page_alias: str):
    fas_search_for_companies(
        context, actor_alias, keyword=keyword, sector=sector,
        page_alias=page_alias)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword on "{page_alias}" page')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str, page_alias: str):
    fas_search_for_companies(
        context, actor_alias, keyword=keyword, page_alias=page_alias)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str):
    fas_search_for_companies(
        context, actor_alias, keyword=keyword)


@when('"{actor_alias}" decides to find out out more about "{industry_name}"')
def fas_when_actor_opens_industry_page(
        context: Context, actor_alias: str, industry_name: str):
    generic_open_industry_page(context, actor_alias, industry_name)


@when('"{actor_alias}" fills out and submits the contact us form')
def fas_when_actor_fills_out_and_submits_contanct_us_form(
        context: Context, actor_alias: str):
    fas_fill_out_and_submit_contact_us_form(context, actor_alias)


@when('"{actor_alias}" decides to see more UK industries')
def fas_landing_page_see_more_industries(context: Context, actor_alias: str):
    generic_see_more_industries(context, actor_alias)


@when('"{actor_alias}" decides to use "{breadcrumb_name}" breadcrumb on the "{page_name}" page')
def fas_industries_use_breadcrumb(
        context: Context, actor_alias: str, breadcrumb_name: str,
        page_name: str):
    fas_use_breadcrumb(context, actor_alias, breadcrumb_name, page_name)


@when('"{actor_alias}" decides to view more companies in the current industry')
def fas_when_actors_views_more_companies(context: Context, actor_alias: str):
    fas_view_more_companies(context, actor_alias)


@when('"{actor_alias}" decides to view "{profile_number}" company profile')
def fas_when_actor_views_selected_company_profile(
        context: Context, actor_alias: str, profile_number: str):
    fas_view_selected_company_profile(context, actor_alias, profile_number)


@when('"{actor_alias}" decides to read "{article_number}" marketing article')
def fas_when_actor_views_article(
        context: Context, actor_alias: str, article_number: str):
    fas_view_article(context, actor_alias, article_number)


@when('"{actor_alias}" decides to read more on following topics')
def actor_decides_to_read_more(context: Context, actor_alias: str):
    invest_read_more(context, actor_alias, context.table)


@when('"{actor_alias}" decides to read "{guide_name}" guide')
def when_actor_goes_to_guide(
        context: Context, actor_alias: str, guide_name: str):
    generic_open_guide_link(context, actor_alias, guide_name)


@when('"{actor_alias}" unfolds all topic sections on "{page_name}" page')
def when_actor_unfolds_all_topic_sections(
        context: Context, actor_alias: str, page_name: str):
    generic_unfold_topics(context, actor_alias, page_name)


@when('"{actor_alias}" decides to click on the UK Government logo in the page "{page_name}"')
def when_actor_clicks_on_uk_gov_logo(
        context: Context, actor_alias: str, page_name: str):
    generic_click_on_uk_gov_logo(context, actor_alias, page_name)
