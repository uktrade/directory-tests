# -*- coding: utf-8 -*-
# flake8: noqa
# fmt: off
"""Then steps definitions."""
from behave import then
from behave.runner import Context

from steps.then_impl import (
    articles_should_be_on_share_page,
    case_studies_should_see_case_study,
    exred_search_finder_should_see_page_number,
    fas_search_results_filtered_by_industries,
    form_check_state_of_element,
    form_should_see_error_messages,
    forms_confirmation_email_should_not_be_sent,
    generic_article_counter_should_match_number_of_articles,
    generic_article_counters_should_match,
    generic_contact_us_should_receive_confirmation_email,
    generic_should_be_on_one_of_the_pages,
    generic_should_see_expected_page_content,
    generic_should_see_form_choices,
    header_check_favicon,
    header_check_logo,
    hpo_agent_should_receive_enquiry_email,
    hpo_should_receive_enquiry_confirmation_email,
    invest_mailbox_admin_should_receive_contact_confirmation_email,
    invest_should_receive_contact_confirmation_email,
    invest_should_see_topic_contents,
    invest_should_see_uk_gov_logo,
    language_selector_keyboard_should_be_trapped,
    language_selector_should_not_see_it,
    language_selector_should_see_it,
    marketplace_finder_should_see_marketplaces,
    office_finder_should_see_correct_office_details,
    pdf_check_expected_details,
    pdf_check_for_dead_links,
    promo_video_check_watch_time,
    promo_video_should_not_see_modal_window,
    share_page_should_be_prepopulated,
    share_page_via_email_should_have_article_details,
    should_be_on_page,
    should_be_on_page_or_international_page,
    should_not_see_sections,
    should_see_articles_filtered_by_tag,
    should_see_links_in_specific_location,
    should_see_page_in_preferred_language,
    should_see_sections,
    should_see_share_widget,
    stats_and_tracking_elements_should_be_present,
    stats_and_tracking_elements_should_not_be_present,
    zendesk_should_receive_confirmation_email,
)
from steps.when_impl import generic_get_verification_code


@then('"{actor_alias}" should be on the "{page_name}" page')
def then_actor_should_be_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@then('"{actor_alias}" should be on the "{page_name}" page or on the International page')
def then_actor_should_be_on_page_on_international_page(
        context, actor_alias, page_name):
    should_be_on_page_or_international_page(context, actor_alias, page_name)


@then('"{actor_alias}" should not see following sections')
@then('"{actor_alias}" should not see following section')
def then_should_not_see_sections(context, actor_alias):
    should_not_see_sections(context, actor_alias, sections_table=context.table)


@then('"{actor_alias}" should see following sections')
@then('"{actor_alias}" should see following section')
def then_should_see_sections(context, actor_alias):
    should_see_sections(context, actor_alias, sections_table=context.table)


@then('"{actor_alias}" should see "{case_study_number}" case study')
def then_actor_should_see_case_study(context, actor_alias, case_study_number):
    case_studies_should_see_case_study(context, actor_alias, case_study_number)


@then('"{actor_alias}" should see the Share Widget')
def then_actor_should_see_share_widget(context, actor_alias):
    should_see_share_widget(context, actor_alias)


@then('"{actor_alias}" should see links to following "{section}" categories in "{location}"')
def then_should_see_links_to_services(
        context, actor_alias, section, location):
    should_see_links_in_specific_location(
        context, actor_alias, section, context.table, location)


@then('"{actor_alias}" should be taken to a new tab with the "{social_media}" share page opened')
def then_actor_should_be_on_share_page(context, actor_alias, social_media):
    articles_should_be_on_share_page(context, actor_alias, social_media)


@then('"{actor_alias}" should see that "{social_media}" share link contains link to the article')
@then('"{actor_alias}" should see that "{social_media}" share page has been pre-populated with message and the link to the article')
def then_share_page_should_be_prepopulated(context, actor_alias, social_media):
    share_page_should_be_prepopulated(context, actor_alias, social_media)


@then('"{actor_alias}" should see that the share via email link will pre-populate the message subject and body with Article title and URL')
def then_check_share_via_email_link(context, actor_alias):
    share_page_via_email_should_have_article_details(context, actor_alias)


@then('"{actor_alias}" should be able to watch at least first "{expected_watch_time:d}" seconds of the promotional video')
def then_actor_should_watch_the_promo_video(
        context, actor_alias, expected_watch_time: int):
    promo_video_check_watch_time(context, actor_alias, expected_watch_time)


@then('"{actor_alias}" should not see the window with promotional video')
def then_actor_should_not_see_video_modal_window(context, actor_alias):
    promo_video_should_not_see_modal_window(context, actor_alias)


@then('"{actor_alias}" should see correct "{logo_name}" logo')
def then_actor_should_see_correct_logo(context, actor_alias, logo_name):
    header_check_logo(context, actor_alias, logo_name)


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


@then('"{actor_alias}" should receive a contact confirmation email from "{sender_email}"')
def then_should_receive_contact_confirmation_email(
        context: Context, actor_alias: str, sender_email: str):
    invest_should_receive_contact_confirmation_email(
        context, actor_alias, sender_email)


@then('"{actor_alias}" should receive an "{subject}" confirmation email')
@then('"{actor_alias}" should receive a "{subject}" confirmation email')
@then('"{actor_alias}" should receive "{subject}" confirmation email')
@then('"{actor_alias}" should receive "{subject}" email')
def then_should_receive_confirmation_email_from_govnotify(
        context: Context, actor_alias: str, subject: str):
    generic_contact_us_should_receive_confirmation_email(
        context, actor_alias, subject
    )


@then('Invest mailbox admin should also receive a contact confirmation email from "{sender_email}"')
def then_invest_mailbox_admin_should_also_receive_contact_confirmation_email(
        context: Context, sender_email: str):
    invest_mailbox_admin_should_receive_contact_confirmation_email(
        context, sender_email)


@then('"{actor_alias}" should receive HPO enquiry confirmation email')
def then_should_receive_hpo_enquiry_confirmation_email(
        context: Context, actor_alias: str):
    hpo_should_receive_enquiry_confirmation_email(context, actor_alias)


@then('HPO Agent should receive HPO enquiry email from "{actor_alias}"')
def then_hpo_agent_should_receive_hpo_enquiry_email(
        context: Context, actor_alias: str):
    hpo_agent_should_receive_enquiry_email(context, actor_alias)


@then('"{actor_alias}" should see that "{element}" in the form is "{state}"')
def then_actor_should_see_form_element_in_specific_stage(
        context: Context, actor_alias: str, element: str, state: str):
    form_check_state_of_element(context, actor_alias, element, state)


@then('"{actor_alias}" should see correct details in every downloaded PDF')
def then_pdfs_should_contain_expected_details(
        context: Context, actor_alias: str):
    pdf_check_expected_details(context, actor_alias, context.table)


@then('there should not be any dead links in every downloaded PDF')
def then_should_not_see_dead_links_in_pdf(context: Context):
    pdf_check_for_dead_links(context)


@then('"{actor_alias}" should see error message saying that mandatory fields are required')
def then_should_see_an_error_message(context: Context, actor_alias: str):
    form_should_see_error_messages(context, actor_alias)


@then('"{actor_alias}" should see list of news articles filtered by selected tag')
def then_should_see_articles_filtered_by_tag(context: Context, actor_alias: str):
    should_see_articles_filtered_by_tag(context, actor_alias)


@then('"{actor_alias}" should see following form choices')
def then_should_see_form_choices(context: Context, actor_alias: str):
    generic_should_see_form_choices(context, actor_alias, context.table)


@then('"{actor_alias}" should receive a "{subject}" confirmation email from Zendesk')
@then('"{actor_alias}" should receive a "{subject}" email from Zendesk')
def step_impl(context: Context, actor_alias: str, subject: str):
    zendesk_should_receive_confirmation_email(context, actor_alias, subject)


@then('"{actor_alias}" should see that article counter matches expected number')
def then_article_counter_should_match(context: Context, actor_alias: str):
    generic_article_counters_should_match(context, actor_alias)


@then('"{actor_alias}" should see that article counter matches the number of articles on the page')
def then_article_counter_should_match_number_of_articles(context: Context, actor_alias: str):
    generic_article_counter_should_match_number_of_articles(context, actor_alias)


@then('"{actor_alias}" should see contact details for "{trade_office}" office in "{city}"')
def then_should_see_correct_trade_office_details(
        context: Context, actor_alias: str, trade_office: str, city: str):
    office_finder_should_see_correct_office_details(
        context, actor_alias, trade_office, city)


@then('"{actor_alias}" should not receive a confirmation email')
def then_confirmation_email_should_not_be_sent(context: Context, actor_alias: str):
    forms_confirmation_email_should_not_be_sent(context, actor_alias)


@then('"{actor_alias}" should receive email confirmation code')
def then_actor_should_get_verifaction_code(context: Context, actor_alias: str):
    generic_get_verification_code(context, actor_alias)


@then('"{actor_alias}" should see marketplaces which operate globally or in multiple countries "{countries}"')
def then_actor_should_see_expected_marketplaces(
        context: Context, actor_alias: str, countries: str):
    marketplace_finder_should_see_marketplaces(context, actor_alias, countries)


@then('"{actor_alias}" should see search results page number "{page_num:d}" for "{phrase}"')
def then_actor_should_see_page_number(
        context: Context, actor_alias: str, page_num: int, phrase: str):
    exred_search_finder_should_see_page_number(context, actor_alias, page_num)


@then('"{actor_alias}" should be on one of the "{expected_pages}" pages')
def then_actor_should_be_on_one_of_the_pages(context: Context, actor_alias: str, expected_pages: str):
    generic_should_be_on_one_of_the_pages(context, actor_alias, expected_pages)
