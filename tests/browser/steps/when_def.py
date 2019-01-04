# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""When step definitions."""
from behave import when
from behave.runner import Context

from steps.then_impl import should_be_on_page
from steps.when_impl import (
    articles_found_useful_or_not,
    articles_open_any,
    articles_share_on_social_media,
    articles_show_all,
    case_studies_go_to,
    clear_the_cookies,
    click_on_page_element,
    contact_us_navigate_through_options,
    fas_fill_out_and_submit_contact_us_form,
    fas_search_for_companies,
    fas_use_breadcrumb,
    fas_view_article,
    fas_view_more_companies,
    fas_view_selected_company_profile,
    generic_click_on_random_industry,
    generic_click_on_uk_gov_logo,
    generic_download_all_pdfs,
    generic_fill_out_and_submit_form,
    generic_open_any_tag,
    generic_open_guide_link,
    generic_open_industry_page,
    generic_open_news_article,
    generic_pick_radio_option_and_submit,
    generic_pick_random_radio_option_and_submit,
    generic_report_problem_with_page,
    generic_see_more_industries,
    generic_submit_form,
    generic_unfold_topics,
    generic_visit_current_page_with_lang_param,
    header_footer_click_on_dit_logo,
    header_footer_open_link,
    invest_read_more,
    language_selector_change_to,
    language_selector_close,
    language_selector_navigate_through_links_with_keyboard,
    language_selector_open,
    open_any_element,
    open_link,
    open_service_link_on_interim_page,
    promo_video_close,
    promo_video_watch,
    registration_submit_form_and_verify_account,
    sign_in,
    sign_out,
    visit_page,
)


@when('"{actor_alias}" opens any article on the list')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)


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


@when('"{actor_alias}" signs out')
def when_actor_signs_out(context, actor_alias):
    sign_out(context, actor_alias)


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
    click_on_page_element(context, actor_alias, element_name, page_name=page_name)


@when('"{actor_alias}" decides to use "{element_name}" button')
@when('"{actor_alias}" decides to use "{element_name}" link')
@when('"{actor_alias}" decides to open "{element_name}"')
@when('"{actor_alias}" decides to see "{element_name}"')
@when('"{actor_alias}" decides to "{element_name}"')
def when_actor_decides_to_click_on_page_element(
        context, actor_alias, element_name):
    click_on_page_element(context, actor_alias, element_name)


@when('"{actor_alias}" decides to click on the DIT logo in the "{logo_location}"')
def when_actor_clicks_on_the_dit_logo(context, actor_alias, logo_location):
    header_footer_click_on_dit_logo(context, actor_alias, logo_location)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword in "{sector}" sector')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str, sector: str):
    fas_search_for_companies(
        context, actor_alias, keyword=keyword, sector=sector)


@when('"{actor_alias}" searches for companies using "{keyword}" keyword')
def fas_when_actor_searches_for_companies(
        context: Context, actor_alias: str, keyword: str):
    fas_search_for_companies(
        context, actor_alias, keyword=keyword)


@when('"{actor_alias}" decides to find out out more about "{industry_name}"')
def fas_when_actor_opens_industry_page(
        context: Context, actor_alias: str, industry_name: str):
    generic_open_industry_page(context, actor_alias, industry_name)


@when('"{actor_alias}" fills out and submits the contact us form without passing captcha')
def fas_when_actor_fills_out_and_submits_contact_us_form_wo_captcha(
        context: Context, actor_alias: str):
    fas_fill_out_and_submit_contact_us_form(context, actor_alias, captcha=False)


@when('"{actor_alias}" fills out and submits the contact us form')
def fas_when_actor_fills_out_and_submits_contact_us_form(
        context: Context, actor_alias: str):
    fas_fill_out_and_submit_contact_us_form(context, actor_alias)


@when('"{actor_alias}" says that his business is in "{option}"')
@when('"{actor_alias}" says that his business is "{option}"')
@when('"{actor_alias}" chooses "{option}" option')
def when_actor_chooses_form_option(
        context: Context, actor_alias: str, option: str):
    generic_pick_radio_option_and_submit(context, actor_alias, option)


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


@when('"{actor_alias}" unfolds all topic sections')
def when_actor_unfolds_all_topic_sections(context: Context, actor_alias: str):
    generic_unfold_topics(context, actor_alias)


@when('"{actor_alias}" decides to click on the UK Government logo in the page "{page_name}"')
def when_actor_clicks_on_uk_gov_logo(
        context: Context, actor_alias: str, page_name: str):
    generic_click_on_uk_gov_logo(context, actor_alias, page_name)


@when('"{actor_alias}" fills out and submits the form')
def when_actor_fills_out_and_submits_the_form(context: Context, actor_alias: str):
    generic_fill_out_and_submit_form(context, actor_alias)


@when('"{actor_alias}" downloads all visible PDFs')
def when_actor_downloads_all_visible_pdfs(context: Context, actor_alias: str):
    generic_download_all_pdfs(context, actor_alias)


@when('"{actor_alias}" submits the form')
def when_actor_submits_the_form(context: Context, actor_alias: str):
    generic_submit_form(context, actor_alias)


@when('"{actor_alias}" manually change the page language to "{preferred_language}"')
def when_actor_sets_lang_url_query_param(
        context: Context, actor_alias: str,  preferred_language: str):
    generic_visit_current_page_with_lang_param(
        context, actor_alias,  preferred_language)


@when('"{actor_alias}" opens "{ordinal_number}" news article')
def when_actor_opens_news_article(
        context: Context, actor_alias: str, ordinal_number: str):
    generic_open_news_article(context, actor_alias, ordinal_number)


@when('"{actor_alias}" decides to see related news articles by using one of the tags')
def when_actor_open_tag(context: Context, actor_alias: str):
    generic_open_any_tag(context, actor_alias)


@when('"{actor_alias}" decides to read about one of listed industries')
def when_actor_clicks_on_random_industry(context: Context, actor_alias: str):
    generic_click_on_random_industry(context, actor_alias)


@when('"{actor_alias}" chooses any available option except "{ignored}"')
def when_actor_chooses_random_form_option_except(
        context: Context, actor_alias: str, ignored: str):
    generic_pick_random_radio_option_and_submit(context, actor_alias, ignored)


@when('"{actor_alias}" navigates via "{via}"')
def given_actor_navigates_via_contact_us_options(
        context: Context, actor_alias: str, via: str):
    contact_us_navigate_through_options(context, actor_alias, via)


@when('"{actor_alias}" is on the "{page_name}" page')
def step_impl(context: Context, actor_alias: str, page_name: str):
    should_be_on_page(context, actor_alias, page_name)


@when('"{actor_alias}" opens any "{element_type}" available in the "{section_name}" section')
def when_user_opens_any_element(
        context: Context, actor_alias: str, element_type: str, section_name: str):
    open_any_element(context, actor_alias, element_type, section_name)


@when('"{actor_alias}" decides to report a problem with the page')
def when_actor_reports_problem_with_page(context: Context, actor_alias: str):
    generic_report_problem_with_page(context, actor_alias)


###############################################################################
# Currently unused but useful steps
###############################################################################


@when('"{actor_alias}" completes the registration and fake email verification process')
def when_actor_registers_fake_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=True)


@when('"{actor_alias}" completes the registration and real email verification process')
def when_actor_registers_real_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=False)
