# -*- coding: utf-8 -*-
# flake8: noqa
"""Then step definitions."""
from behave import then
from behave.runner import Context

from tests.functional.steps.then_impl import (
    fab_company_should_be_verified,
    fab_should_be_asked_about_verification_form,
    fab_should_not_see_collaborator,
    fab_should_see_case_study_error_message,
    fas_check_profiles,
    fas_find_supplier_using_case_study_details,
    fas_no_links_to_online_profiles_are_visible,
    fas_should_be_on_profile_page,
    fas_should_be_told_that_message_has_been_sent,
    fas_should_find_all_sought_companies,
    fas_should_find_with_company_details,
    fas_should_not_find_with_company_details,
    fas_should_see_all_case_studies,
    fas_should_see_company_once_in_search_results,
    fas_should_see_different_png_logo_thumbnail,
    fas_should_see_filtered_search_results,
    fas_should_see_highlighted_search_term,
    fas_should_see_png_logo_thumbnail,
    fas_should_see_unfiltered_search_results,
    fas_supplier_cannot_be_found_using_case_study_details,
    fas_supplier_should_receive_message_from_buyer,
    generic_content_of_viewed_pages_should_in_selected_language,
    generic_language_switcher_should_be_set_to,
    generic_page_language_should_be_set_to,
    generic_should_get_email_notifications,
    international_should_see_links_to_industry_pages,
    isd_should_be_told_about_empty_search_results,
    isd_should_see_unfiltered_search_results,
    prof_should_be_told_about_missing_description,
    profile_all_unsupported_files_should_be_rejected,
    profile_business_profile_should_be_ready_for_publishing,
    profile_no_links_to_online_profiles_are_visible,
    profile_profile_is_published,
    profile_should_be_told_about_invalid_links,
    profile_should_get_request_for_becoming_owner,
    profile_should_not_see_options_to_manage_users,
    profile_should_see_all_case_studies,
    profile_should_see_company_details,
    profile_should_see_expected_error_messages,
    profile_should_see_logo_picture,
    profile_should_see_online_profiles,
    profile_supplier_should_be_on_landing_page,
    reg_should_get_verification_email,
    reg_supplier_has_to_verify_email_first,
    should_be_at,
    should_be_taken_to_selected_page,
    should_not_be_able_to_access_page,
    should_not_see_message,
    should_see_message,
    should_see_selected_pages,
    sso_should_be_signed_in_to_sso_account,
    sso_should_be_told_about_password_reset,
    sso_should_get_password_reset_email,
    sso_should_get_request_for_collaboration_email,
    sso_should_see_invalid_password_reset_link_error,
    sud_should_not_see_options_to_manage_users,
    sud_should_see_options_to_manage_users,
)
from tests.functional.steps.when_impl import (
    fas_feedback_request_should_be_submitted,
    fas_should_be_told_about_empty_search_results,
    fas_should_be_told_to_enter_search_term_or_use_filters,
)


@then('"{alias}" should receive an email verification msg entitled "{subject}"')
def then_supplier_should_receive_verification_email(context, alias, subject):
    reg_should_get_verification_email(context, alias, subject=subject)


@then('"{supplier_alias}" should be told that her company has no description')
def then_supplier_should_be_told_about_missing_description(context, supplier_alias):
    response = context.response
    prof_should_be_told_about_missing_description(response, supplier_alias)


@then('"{supplier_alias}" should be told that her company is published')
def then_supplier_should_be_told_that_profile_is_published(context, supplier_alias):
    profile_profile_is_published(context, supplier_alias)


@then('"{supplier_alias}" should be on "{company_alias}"\'s FAS Business Profile page')
def then_supplier_should_be_on_company_fas_page(context, supplier_alias, company_alias):
    fas_should_be_on_profile_page(context, supplier_alias, company_alias)


@then(
    '"{supplier_alias}" should be told that she needs to verify her email address first'
)
def then_supplier_has_to_verify_email_first(context, supplier_alias):
    reg_supplier_has_to_verify_email_first(context, supplier_alias)


@then('"{supplier_alias}" should be on Welcome to your great.gov.uk profile page')
def then_supplier_should_be_on_profile_landing_page(context, supplier_alias):
    profile_supplier_should_be_on_landing_page(context, supplier_alias)


@then('"{supplier_alias}" should be signed in to SSO/great.gov.uk account')
def then_supplier_should_be_signed_in_to_sso_account(context, supplier_alias):
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


@then('"{supplier_alias}" should see new details on "{page_name}" page')
def then_supplier_should_see_new_details(context, supplier_alias, page_name):
    profile_should_see_company_details(context, supplier_alias, page_name)


@then(
    '"{supplier_alias}" should see links to all online profiles on Edit Business Profile page'
)
def then_supplier_should_see_online_profiles_on_fab(context, supplier_alias):
    profile_should_see_online_profiles(context, supplier_alias)


@then(
    '"{supplier_alias}" should see links to all online profiles on FAS Business Profile page'
)
def then_supplier_should_see_online_profiles_on_fas(context, supplier_alias):
    fas_check_profiles(context, supplier_alias)


@then('"{supplier_alias}" should be told to provide valid links to all online profiles')
def then_supplier_should_be_told_to_use_valid_links(context, supplier_alias):
    profile_should_be_told_about_invalid_links(context, supplier_alias)


@then(
    '"{supplier_alias}" should not see any links to online profiles on edit Business Profile page'
)
def then_no_online_profiles_are_visible_on_fab(context, supplier_alias):
    profile_no_links_to_online_profiles_are_visible(context, supplier_alias)


@then(
    '"{supplier_alias}" should not see any links to online profiles on FAS Business Profile page'
)
def then_no_online_profiles_are_visible_on_fas(context, supplier_alias):
    fas_no_links_to_online_profiles_are_visible(context, supplier_alias)


@then(
    '"{supplier_alias}" should see all case studies on the edit Business Profile page'
)
def then_supplier_should_see_all_case_studies_fab(context, supplier_alias):
    profile_should_see_all_case_studies(context, supplier_alias)


@then('"{supplier_alias}" should see all case studies on the FAS Business Profile page')
def then_supplier_should_see_all_case_studies_fas(context, supplier_alias):
    fas_should_see_all_case_studies(context, supplier_alias)


@then(
    '"{supplier_alias}" should see that logo on FAB Company\'s Directory Profile page'
)
def then_supplier_should_see_logo_picture_on_fab(context, supplier_alias):
    profile_should_see_logo_picture(context, supplier_alias)


@then(
    '"{supplier_alias}" should see that logo on FAS Company\'s Directory Profile page'
)
def then_supplier_should_see_logo_picture_on_fas(context, supplier_alias):
    fas_should_see_png_logo_thumbnail(context, supplier_alias)


@then(
    'for every uploaded unsupported file "{supplier_alias}" should be told that only certain image types can be used as company\'s logo'
)
def then_every_invalid_logo_should_be_rejected(context, supplier_alias):
    profile_all_unsupported_files_should_be_rejected(context, supplier_alias)


@then(
    '"{buyer_alias}" should be able to find company "{company_alias}" on FAS using words from case study "{case_alias}"'
)
def then_buyer_should_find_supplier_using_part_of_case_study(
    context, buyer_alias, company_alias, case_alias
):
    fas_find_supplier_using_case_study_details(
        context, buyer_alias, company_alias, case_alias, properties=context.table
    )


@then(
    '"{buyer_alias}" should NOT be able to find company "{company_alias}" on FAS by using any part of case study "{case_alias}"'
)
def then_buyer_should_not_be_able_to_find_company(
    context, buyer_alias, company_alias, case_alias
):
    fas_supplier_cannot_be_found_using_case_study_details(
        context, buyer_alias, company_alias, case_alias
    )


@then(
    '"{buyer_alias}" should be able to find company "{company_alias}" on FAS using any part of case study "{case_alias}"'
)
def then_buyer_should_find_supplier_using_any_part_of_case_study(
    context, buyer_alias, company_alias, case_alias
):
    fas_find_supplier_using_case_study_details(
        context, buyer_alias, company_alias, case_alias
    )


@then(
    '"{buyer_alias}" should NOT be able to find company "{company_alias}" on FAS using selected company\'s details'
)
def then_buyer_should_find_supplier_using_company_details(
    context, buyer_alias, company_alias
):
    fas_should_not_find_with_company_details(context, buyer_alias, company_alias)


@then(
    '"{buyer_alias}" should be able to find company "{company_alias}" on FAS using selected company\'s details'
)
def then_buyer_should_find_supplier_using_company_details(
    context, buyer_alias, company_alias
):
    fas_should_find_with_company_details(context, buyer_alias, company_alias)


@then(
    'the "{page_part}" part of the viewed FAS page should be presented in "{language}" language with probability greater than "{probability}"'
)
@then(
    'the "{page_part}" part of the viewed pages should be presented in "{language}" language with probability greater than "{probability}"'
)
def then_page_should_be_in(context, page_part, language, probability):
    generic_content_of_viewed_pages_should_in_selected_language(
        context, language=language, page_part=page_part, probability=float(probability)
    )


@then(
    '"{buyer_alias}" should be told that the search did not match any UK trade profiles'
)
def then_should_be_told_about_empty_search_results(context, buyer_alias):
    fas_should_be_told_about_empty_search_results(context, buyer_alias)


@then('"{buyer_alias}" should be told to enter a search term or use the filters')
def then_should_be_told_about_empty_search_results(context, buyer_alias):
    fas_should_be_told_to_enter_search_term_or_use_filters(context, buyer_alias)


@then('"{buyer_alias}" should be told that the search did not match any ISD companies')
def then_should_be_told_about_empty_search_results(context, buyer_alias):
    isd_should_be_told_about_empty_search_results(context, buyer_alias)


@then('"{buyer_alias}" should be told that the feedback request has been submitted')
def then_buyer_should_be_told_about_feedback_request_confirmation(context, buyer_alias):
    fas_feedback_request_should_be_submitted(context, buyer_alias)


@then('"{buyer_alias}" should be able to find all sought companies')
def then_buyer_should_find_all_sought_companies(context, buyer_alias):
    fas_should_find_all_sought_companies(context, buyer_alias)


@then(
    '"{buyer_alias}" should be told that the message has been sent to company "{company_alias}"'
)
def then_buyer_should_be_told_that_message_has_been_sent(
    context, buyer_alias, company_alias
):
    fas_should_be_told_that_message_has_been_sent(context, buyer_alias, company_alias)


@then('"{supplier_alias}" should receive an email message from "{buyer_alias}"')
def then_supplier_should_receive_message_from_buyer(
    context, supplier_alias, buyer_alias
):
    fas_supplier_should_receive_message_from_buyer(context, supplier_alias, buyer_alias)


@then(
    '"{actor_alias}" should see a PNG logo thumbnail on FAS Company\'s Directory Profile page'
)
def then_buyer_should_see_logo_on_fas_profile_page(context, actor_alias):
    fas_should_see_png_logo_thumbnail(context, actor_alias)


@then(
    '"{actor_alias}" should see different updated thumbnail of the logo on FAS Company\'s Directory Profile page'
)
def then_actor_should_see_different_logo_on_fas(context, actor_alias):
    fas_should_see_different_png_logo_thumbnail(context, actor_alias)


@then('"{supplier_alias}" should see expected error messages')
def then_supplier_should_see_expected_error_messages(context, supplier_alias):
    profile_should_see_expected_error_messages(context, supplier_alias)


@then(
    '"{actor_alias}" should see links to all industry pages available in "{language}" language'
)
def then_actor_should_see_links_to_industry_pages(
    context: Context, actor_alias: str, language: str
):
    international_should_see_links_to_industry_pages(context, actor_alias, language)


@then('"{actor_alias}" should see search results filtered by appropriate sector')
@then('"{actor_alias}" should see search results filtered by appropriate sectors')
def then_actor_should_see_filtered_search_results(context, actor_alias):
    fas_should_see_filtered_search_results(context, actor_alias)


@then(
    '"{actor_alias}" should see that FAS search results are not filtered by any sector'
)
def then_actor_should_see_unfiltered_search_results(context, actor_alias):
    fas_should_see_unfiltered_search_results(context, actor_alias)


@then(
    '"{actor_alias}" should see that ISD search results are not filtered by any sector'
)
def then_actor_should_see_unfiltered_search_results(context, actor_alias):
    isd_should_see_unfiltered_search_results(context, actor_alias)


@then(
    '"{actor_alias}" should see company "{company_alias}" only once on browsed search result pages'
)
def then_actor_should_see_company_once_in_search_results(
    context, actor_alias, company_alias
):
    fas_should_see_company_once_in_search_results(context, actor_alias, company_alias)


@then(
    '"{actor_alias}" should see that some of the results have the "{search_term}" search terms highlighted'
)
def then_should_see_highlighted_search_term(context, actor_alias, search_term):
    fas_should_see_highlighted_search_term(context, actor_alias, search_term)


@then(
    '"{supplier_alias}" should be told that business profile is ready to be published'
)
def then_company_should_be_verified(context, supplier_alias):
    profile_business_profile_should_be_ready_for_publishing(context, supplier_alias)


@then('"{supplier_alias}" should be told that company has been verified')
def then_company_should_be_verified(context, supplier_alias):
    fab_company_should_be_verified(context, supplier_alias)


@then('"{supplier_alias}" should see expected case study error message')
def then_supplier_should_see_expected_case_study_error_message(context, supplier_alias):
    fab_should_see_case_study_error_message(context, supplier_alias)


@then('"{supplier_alias}" should be told that password was reset')
def then_should_be_told_that_password_was_reset(context, supplier_alias):
    sso_should_be_told_about_password_reset(context, supplier_alias)


@then('"{supplier_alias}" should receive a password reset email')
def then_supplier_should_receive_password_reset_email(context, supplier_alias):
    sso_should_get_password_reset_email(context, supplier_alias)


@then('"{supplier_alias}" should be told that password reset link is invalid')
def then_should_see_invalid_password_reset_link_error(context, supplier_alias):
    sso_should_see_invalid_password_reset_link_error(context, supplier_alias)


@then('"{supplier_alias}" should see "{page_name}" page')
@then('"{supplier_alias}" should be on "{page_name}" page')
def then_supplier_should_see_specific_page(context, supplier_alias, page_name):
    should_be_at(context, supplier_alias, page_name)


@then('"{actor_alias}" should be able to see all selected pages')
def then_actor_should_see_selected_pages(context, actor_alias):
    should_see_selected_pages(context, actor_alias)


@then('"{actor_alias}" should be taken to "{page_name}" for all requests')
def then_actor_should_see_selected_pages(context, actor_alias, page_name):
    should_be_taken_to_selected_page(context, actor_alias, page_name)


@then('"{supplier_alias}" should be asked to decide how to verify her identity')
def then_supplier_should_be_asked_about_verification(context, supplier_alias):
    fab_should_be_asked_about_verification_form(context, supplier_alias)


@then('"{actor_alias}" should see "{message}" on the page')
@then('"{actor_alias}" should see "{message}" message')
def then_actor_should_see_a_message(context, actor_alias, message):
    should_see_message(context, actor_alias, message)


@then('"{actor_alias}" should not see "{message}" on the page')
@then('"{actor_alias}" should not see "{message}" message')
def then_actor_should_not_see_a_message(context, actor_alias, message):
    should_not_see_message(context, actor_alias, message)


@then(
    '"{actor_aliases}" should receive an email with a request to confirm that he\'s been added to company "{company_alias}" Find a Buyer profile'
)
@then(
    '"{actor_aliases}" should receive an email with a request to confirm that she\'s been added to company "{company_alias}" Find a Buyer profile'
)
@then(
    '"{actor_aliases}" should receive an email with a request to confirm that they\'ve been added to company "{company_alias}" Find a Buyer profile'
)
def then_actor_should_receive_email_with_request_for_collaboration(
    context, actor_aliases, company_alias
):
    sso_should_get_request_for_collaboration_email(
        context, actor_aliases, company_alias
    )


@then(
    '"{actor_alias}" should see options to manage Find a Buyer profile users on SSO Profile'
)
def then_actor_should_see_options_to_manage_account_users(
    context: Context, actor_alias: str
):
    sud_should_see_options_to_manage_users(context, actor_alias)


@then(
    '"{actor_alias}" should not see options to manage Find a Buyer profile users on SSO Profile'
)
def then_actor_should_not_see_options_to_manage_account_users(
    context: Context, actor_alias: str
):
    sud_should_not_see_options_to_manage_users(context, actor_alias)


@then(
    '"{new_owner_alias}" should receive an email with a request for becoming the owner of the company "{company_alias}" profile'
)
def then_actor_should_receive_email_with_transfer_account_ownership_request(
    context, new_owner_alias, company_alias
):
    profile_should_get_request_for_becoming_owner(
        context, new_owner_alias, company_alias
    )


@then(
    '"{supplier_alias}" should not see "{collaborators_aliases}" among the users associated with company\'s profile'
)
def then_supplier_should_not_see_collaborator(
    context, supplier_alias, collaborators_aliases
):
    fab_should_not_see_collaborator(context, supplier_alias, collaborators_aliases)


@then('"{collaborator_alias}" should not be able to access "{page_name}" page')
def then_collaborator_should_not_be_able_to_access_page(
    context, collaborator_alias, page_name
):
    should_not_be_able_to_access_page(context, collaborator_alias, page_name)


@then(
    'the HTML document language for viewed pages should be set to "{language}" language'
)
def then_page_language_should_be_set_to(context: Context, language: str):
    generic_page_language_should_be_set_to(context, language)


@then(
    'the language switcher on viewed pages should show "{language}" as selected language'
)
def then_language_switcher_should_be_set_to(context: Context, language: str):
    generic_language_switcher_should_be_set_to(context, language)


@then('"{actor_alias}" should not see options to manage profile')
def then_actor_should_not_see_options_to_manage_account_users(
    context: Context, actor_alias: str
):
    profile_should_not_see_options_to_manage_users(context, actor_alias)


@then('"{actor_alias}" should receive an email notification with subject "{subject}"')
def then_actor_should_get_email(context: Context, actor_alias: str, subject: str):
    generic_should_get_email_notifications(context, actor_alias, subject)
