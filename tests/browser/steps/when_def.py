# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""When step definitions."""
from behave import register_type, when
from behave.runner import Context

import parse
from steps.then_impl import (
    domestic_search_finder_should_see_page_number,
    should_be_on_page,
)
from steps.when_impl import (
    articles_open_any,
    articles_share_on_social_media,
    clear_the_cookies,
    click_on_header_menu_button,
    click_on_page_element,
    contact_us_navigate_through_options,
    domestic_find_more_about_search_result_type,
    domestic_submit_soo_contact_us_form,
    erp_drill_down_hierarchy_tree,
    erp_open_restore_session_link,
    erp_save_for_later,
    erp_select_random_search_result,
    fas_search_for_companies,
    fas_view_article,
    fas_view_selected_company_profile,
    generic_accept_all_cookies,
    generic_click_on_random_element,
    generic_click_on_random_industry,
    generic_click_on_random_marketplace,
    generic_download_all_pdfs,
    generic_fill_out_and_submit_form,
    generic_open_any_tag,
    generic_open_guide_link,
    generic_open_industry_page,
    generic_open_news_article,
    generic_pick_radio_option,
    generic_pick_radio_option_and_submit,
    generic_pick_random_radio_option_and_submit,
    generic_remove_previous_field_selections,
    generic_report_problem_with_page,
    generic_search_for_phrase,
    generic_select_dropdown_option,
    generic_submit_form,
    generic_trigger_all_gtm_events,
    generic_unfold_elements_in_section,
    generic_visit_current_page_with_lang_parameter,
    language_selector_change_to,
    language_selector_close,
    language_selector_navigate_through_links_with_keyboard,
    language_selector_open,
    office_finder_find_trade_office,
    promo_video_close,
    promo_video_watch,
    registration_submit_form_and_verify_account,
    sign_in,
    sign_out,
    soo_look_for_marketplace,
    visit_page,
)


@when('"{actor_alias}" opens any article on the list')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)


@when('"{actor_alias}" goes to the "{page_name}" page')
def when_actor_goes_to_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@when('"{actor_alias}" decides to share the article via "{social_media}"')
def when_actor_shares_article(context, actor_alias, social_media):
    articles_share_on_social_media(context, actor_alias, social_media)


@when('"{actor_alias}" decides to watch "{play_time:d}" seconds of the promotional video')
def when_actor_decides_to_watch_promo_video(
        context, actor_alias, *, play_time: int = None):
    promo_video_watch(context, actor_alias, play_time=play_time)


@when('"{actor_alias}" closes the window with promotional video')
def when_actor_decides_to_close_the_promotional_video(context, actor_alias):
    promo_video_close(context, actor_alias)


@when('"{actor_alias}" opens up the language selector')
def when_actor_opens_up_language_selector(context, actor_alias):
    language_selector_open(context, actor_alias)


@when('"{actor_alias}" closes the language selector using his keyboard')
@when('"{actor_alias}" closes the language selector')
def when_actor_closes_language_selector(context, actor_alias):
    language_selector_close(context, actor_alias)


@when('"{actor_alias}" uses her keyboard to navigate through all links visible on language selector')
@when('"{actor_alias}" uses his keyboard to navigate through all links visible on language selector')
def when_actor_navigates_through_language_selector_links_with_keyboard(
        context, actor_alias):
    language_selector_navigate_through_links_with_keyboard(context, actor_alias)


@when('"{actor_alias}" decides to view the page in "{preferred_language}"')
def when_actor_views_page_in_selected_language(
        context, actor_alias, preferred_language):
    language_selector_change_to(context, actor_alias, preferred_language)


@when('"{actor_alias}" decides to find out more about "{element_name}"')
@when('"{actor_alias}" decides to use "{element_name}" button')
@when('"{actor_alias}" decides to use "{element_name}" link')
@when('"{actor_alias}" decides to open "{element_name}"')
@when('"{actor_alias}" decides to click on "{element_name}"')
@when('"{actor_alias}" decides to see "{element_name}"')
@when('"{actor_alias}" decides to "{element_name}"')
def when_actor_decides_to_click_on_page_element(
        context, actor_alias, element_name):
    click_on_page_element(context, actor_alias, element_name)


@when('"{actor_alias}" decides to use one of the "{elements_name}"')
def when_actor_clicks_on_random_element(
        context: Context, actor_alias: str, elements_name: str
):
    generic_click_on_random_element(context, actor_alias, elements_name)


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


@when('"{actor_alias}" says that affected goods are "{option}" from overseas')
@when('"{actor_alias}" says that his business is in "{option}"')
@when('"{actor_alias}" says that his business is "{option}"')
@when('"{actor_alias}" says that he represents an "{option}"')
@when('"{actor_alias}" says that he represents a "{option}"')
@when('"{actor_alias}" chooses "{option}" option')
def when_actor_chooses_form_option_and_submits_form(
        context: Context, actor_alias: str, option: str):
    generic_pick_radio_option_and_submit(context, actor_alias, option)


@when('"{actor_alias}" picks "{option}" option')
def when_actor_chooses_form_option(
        context: Context, actor_alias: str, option: str):
    generic_pick_radio_option(context, actor_alias, option)


@when('"{actor_alias}" decides to view "{profile_number}" company profile')
def fas_when_actor_views_selected_company_profile(
        context: Context, actor_alias: str, profile_number: str):
    fas_view_selected_company_profile(context, actor_alias, profile_number)


@when('"{actor_alias}" decides to read "{article_number}" marketing article')
def fas_when_actor_views_article(
        context: Context, actor_alias: str, article_number: str):
    fas_view_article(context, actor_alias, article_number)


@when('"{actor_alias}" decides to read "{guide_name}" guide')
def when_actor_goes_to_guide(
        context: Context, actor_alias: str, guide_name: str):
    generic_open_guide_link(context, actor_alias, guide_name)


@when('"{actor_alias}" fills out and submits the form (and go 1 page back on error)')
def when_actor_fills_out_and_submits_the_form(context: Context, actor_alias: str):
    generic_fill_out_and_submit_form(context, actor_alias, custom_details_table=context.table, retry_on_errors=True, go_back=True)


@when('"{actor_alias}" removed previous "{selector_name}" selections')
def when_actor_removes_previous_form_selections(
        context: Context, actor_alias: str, selector_name: str
):
    generic_remove_previous_field_selections(
        context, actor_alias, selector_name
    )


# -- TYPE CONVERTER: For a simple, on/off values
@parse.with_pattern(r".*")
def parse_on_off(text: str) -> bool:
    result = True if text.lower() == "on" else False
    return result


# -- REGISTER TYPE-CONVERTER: With behave
register_type(OnOff=parse_on_off)


@when('"{actor_alias}" decides to find new markets for her business')
@when('"{actor_alias}" decides to find new markets for his business')
@when('"{actor_alias}" fills out and submits the form with captcha dev check turned "{check_captcha_dev_mode:OnOff}"')
@when('"{actor_alias}" fills out and submits "{form_name}" with "captcha in dev mode" check turned "{check_captcha_dev_mode:OnOff}"')
@when('"{actor_alias}" fills out and submits "{form_name}" form')
@when('"{actor_alias}" fills out and submits the form')
def when_actor_fills_out_and_submits_the_form(
        context: Context, actor_alias: str, *, form_name: str = None, check_captcha_dev_mode: bool = True
):
    generic_fill_out_and_submit_form(
        context, actor_alias, custom_details_table=context.table, form_name=form_name,
        check_captcha_dev_mode=check_captcha_dev_mode,
    )


@when('"{actor_alias}" downloads all visible PDFs')
def when_actor_downloads_all_visible_pdfs(context: Context, actor_alias: str):
    generic_download_all_pdfs(context, actor_alias)


@when('"{actor_alias}" submits the form')
def when_actor_submits_the_form(context: Context, actor_alias: str):
    generic_submit_form(context, actor_alias)


@when('"{actor_alias}" manually change the page language to "{preferred_language}"')
def when_actor_sets_lang_url_query_param(
        context: Context, actor_alias: str,  preferred_language: str):
    generic_visit_current_page_with_lang_parameter(
        context, actor_alias,  preferred_language)


@when('"{actor_alias}" opens "{ordinal_number}" news article')
def when_actor_opens_news_article(
        context: Context, actor_alias: str, ordinal_number: str):
    generic_open_news_article(context, actor_alias, ordinal_number)


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
def when_actor_is_on_page(context: Context, actor_alias: str, page_name: str):
    should_be_on_page(context, actor_alias, page_name)


@when('"{actor_alias}" decides to report a problem with the page')
def when_actor_reports_problem_with_page(context: Context, actor_alias: str):
    generic_report_problem_with_page(context, actor_alias)


@when('"{actor_alias}" searches for marketplaces in "{country}" to sell "{category}"')
def when_actor_looks_for_marketplace_using_countries_and_products(
        context: Context, actor_alias: str, country: str, category: str):
    soo_look_for_marketplace(context, actor_alias, country, category)


@when('"{actor_alias}" randomly selects a marketplace')
@when('"{actor_alias}" selects a random market')
def when_actor_selects_marketplace(context: Context, actor_alias: str):
    generic_click_on_random_marketplace(context, actor_alias)


@when('"{actor_alias}" submits the SOO contact-us form')
def when_actor_submits_soo_contact_us_form(
        context: Context, actor_alias: str):
    domestic_submit_soo_contact_us_form(
        context, actor_alias, custom_details_table=context.table
    )


@when('"{actor_alias}" searches using "{phrase}"')
def when_actor_search_for_phrase(
        context: Context, actor_alias: str, phrase: str):
    generic_search_for_phrase(context, actor_alias, phrase)


@when('"{actor_alias}" decides to find out more about random "{type_of}" result')
def when_actor_decides_to_find_out_more_about_result_type(
        context: Context, actor_alias: str, type_of: str):
    domestic_find_more_about_search_result_type(context, actor_alias, type_of)


@when('"{actor_alias}" should see search results page number "{page_num:d}" for "{phrase}"')
def then_actor_should_see_page_number(
        context: Context, actor_alias: str, page_num: int, phrase: str):
    domestic_search_finder_should_see_page_number(context, actor_alias, page_num)


@when('"{actor_alias}" triggers all GTM events defined for "{tagging_package}"')
def when_actor_triggers_all_gtm_events(
        context: Context, actor_alias: str, tagging_package: str
):
    generic_trigger_all_gtm_events(context, actor_alias, tagging_package)


@when('"{actor_alias}" triggers all GTM "{event_group}" events defined for "{tagging_package}"')
def when_actor_triggers_all_gtm_events(
        context: Context, actor_alias: str, event_group: str, tagging_package: str
):
    generic_trigger_all_gtm_events(
        context, actor_alias, tagging_package, event_group=event_group
    )


@when('"{actor_alias}" selects a random product code from an expanded hierarchy of product codes')
def when_actor_selects_random_product_code(context: Context, actor_alias: str):
    erp_drill_down_hierarchy_tree(context, actor_alias, use_expanded_category=True)


@when('"{actor_alias}" selects a random product code from the hierarchy of product codes')
def when_actor_selects_random_product_code(context: Context, actor_alias: str):
    erp_drill_down_hierarchy_tree(context, actor_alias)


@when('"{actor_alias}" saves progress for later')
def when_actor_saves_progress_for_later(context: Context, actor_alias: str):
    erp_save_for_later(context, actor_alias)


@when('"{actor_alias}" decides to restore saved ERP progress using the link she received')
@when('"{actor_alias}" decides to restore saved ERP progress using the link he received')
def when_actor_restores_erp_progress(context, actor_alias):
    erp_open_restore_session_link(context, actor_alias)


@when('"{actor_alias}" selects a random product "{result_type}" from search results')
def when_actor_selects_one_of_search_results(
        context: Context, actor_alias: str, result_type: str
):
    erp_select_random_search_result(context, actor_alias, result_type)


@when('"{actor_alias}" unfolds all elements in "{section_name}" section')
def when_actor_unfolds_elements_in_section(context: Context, actor_alias: str, section_name: str):
    generic_unfold_elements_in_section(context, actor_alias, section_name)


@when('"{actor_alias}" accepts all cookies')
def when_user_accepts_all_cookies(context: Context, actor_alias: str):
    generic_accept_all_cookies(context, actor_alias)


###############################################################################
# Currently unused but useful steps
###############################################################################


@when('"{actor_alias}" completes the registration and fake email verification process')
def when_actor_registers_fake_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=True)


@when('"{actor_alias}" signs out')
def when_actor_signs_out(context, actor_alias):
    sign_out(context, actor_alias)


@when('"{actor_alias}" completes the registration and real email verification process')
def when_actor_registers_real_email_verification(context, actor_alias):
    registration_submit_form_and_verify_account(
        context, actor_alias, fake_verification=False)


@when('"{actor_alias}" clears the cookies')
def when_actor_clears_the_cookies(context, actor_alias):
    clear_the_cookies(context, actor_alias)


@when('"{actor_alias}" signs in')
def when_actor_signs_in(context, actor_alias):
    sign_in(context, actor_alias)


@when('"{actor_alias}" searches for local trade office near "{post_code}"')
def when_actor_looks_for_trade_office(context: Context, actor_alias: str, post_code: str):
    office_finder_find_trade_office(context, actor_alias, post_code)


@when('"{actor_alias}" clicks the Menu button')
def when_actor_clicks_header_menu_button(context: Context, actor_alias: str):
    click_on_header_menu_button(context)


@when('"{actor_alias}" selects "{option}" from "{dropdown_name}" dropdown')
def when_actor_selects_form_option(
        context: Context, actor_alias: str, option: str, dropdown_name: str):
    generic_select_dropdown_option(context, actor_alias, dropdown_name, option)


@when('"{actor_alias}" opens up the language selector using her keyboard')
@when('"{actor_alias}" opens up the language selector using his keyboard')
def when_actor_opens_up_language_selector_with_keyboard(context, actor_alias):
    language_selector_open(context, actor_alias, with_keyboard=True)


@when('"{actor_alias}" decides to see related news articles by using one of the tags')
def when_actor_open_tag(context: Context, actor_alias: str):
    generic_open_any_tag(context, actor_alias)
