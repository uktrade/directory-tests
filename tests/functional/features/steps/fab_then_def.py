# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import then

from tests.functional.features.steps.fab_then_impl import (
    bp_should_be_prompted_to_build_your_profile,
    fab_no_links_to_online_profiles_are_visible,
    fab_profile_is_verified,
    fab_should_see_all_case_studies,
    fab_should_see_company_details,
    fab_should_see_online_profiles,
    fas_check_profiles,
    fas_find_supplier_using_case_study_details,
    fas_no_links_to_online_profiles_are_visible,
    fas_pages_should_be_in_selected_language,
    fas_should_be_on_profile_page,
    fas_should_be_told_that_message_has_been_sent,
    fas_should_find_all_sought_companies,
    fas_should_find_with_company_details,
    fas_should_see_all_case_studies,
    fas_should_see_company_details,
    fas_should_see_different_logo_picture,
    fas_should_see_logo_picture,
    fas_supplier_cannot_be_found_using_case_study_details,
    fas_supplier_should_receive_message_from_buyer,
    prof_all_unsupported_files_should_be_rejected,
    prof_should_be_on_profile_page,
    prof_should_be_told_about_invalid_links,
    prof_should_be_told_about_missing_description,
    prof_should_see_logo_picture,
    profile_supplier_should_be_on_landing_page,
    reg_should_get_verification_email,
    reg_sso_account_should_be_created,
    reg_supplier_has_to_verify_email_first,
    reg_supplier_is_not_appropriate_for_fab,
    sso_should_be_signed_in_to_sso_account
)
from tests.functional.features.steps.fab_when_impl import (
    fas_feedback_request_should_be_submitted,
    fas_should_be_told_about_empty_search_results
)


@then('"{alias}" should be told about the verification email')
def then_sso_account_was_created(context, alias):
    reg_sso_account_should_be_created(context.response, alias)


@then('"{alias}" should receive an email verification msg entitled "{subject}"')
def then_supplier_should_receive_verification_email(context, alias, subject):
    reg_should_get_verification_email(context, alias)


@then('"{supplier_alias}" should be prompted to Build and improve your '
      'Directory Profile')
def then_supplier_should_be_prompted_to_build_your_profile(
        context, supplier_alias):
    bp_should_be_prompted_to_build_your_profile(context, supplier_alias)


@then('"{supplier_alias}" should be on edit Company\'s Directory Profile page')
def then_supplier_should_be_on_profile_page(context, supplier_alias):
    prof_should_be_on_profile_page(context.response, supplier_alias)


@then('"{supplier_alias}" should be told that her company has no description')
def then_supplier_should_be_told_about_missing_description(
        context, supplier_alias):
    response = context.response
    prof_should_be_told_about_missing_description(response, supplier_alias)


@then('"{supplier_alias}" should be told that her company is published')
def then_supplier_should_be_told_that_profile_is_published(
        context, supplier_alias):
    fab_profile_is_verified(context, supplier_alias)


@then('"{supplier_alias}" should be on FAS Directory Profile page of company '
      '"{company_alias}"')
def then_supplier_should_be_on_company_fas_page(context, supplier_alias,
                                                company_alias):
    fas_should_be_on_profile_page(context, supplier_alias, company_alias)


@then('"{supplier_alias}" should be told that his company is currently not '
      'appropriate to feature in the FAB service')
def then_supplier_is_not_appropriate_for_fab(context, supplier_alias):
    reg_supplier_is_not_appropriate_for_fab(context, supplier_alias)


@then('"{supplier_alias}" should be told that she needs to verify her email '
      'address first')
def then_supplier_has_to_verify_email_first(context, supplier_alias):
    reg_supplier_has_to_verify_email_first(context, supplier_alias)


@then('"{supplier_alias}" should be on Welcome to your great.gov.uk profile '
      'page')
def then_supplier_should_be_on_profile_landing_page(context, supplier_alias):
    profile_supplier_should_be_on_landing_page(context, supplier_alias)


@then('"{supplier_alias}" should be signed in to SSO/great.gov.uk account')
def then_supplier_should_be_signed_in_to_sso_account(context, supplier_alias):
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


@then('"{supplier_alias}" should see new details on FAB Company\'s Directory '
      'Profile page')
def then_supplier_should_see_new_details(context, supplier_alias):
    fab_should_see_company_details(context, supplier_alias)


@then('"{supplier_alias}" should see links to all online profiles on FAB '
      'Company\'s Directory Profile page')
def then_supplier_should_see_online_profiles_on_fab(context, supplier_alias):
    fab_should_see_online_profiles(context, supplier_alias)


@then('"{supplier_alias}" should see links to all online profiles on FAS '
      'Company\'s Directory Profile page')
def then_supplier_should_see_online_profiles_on_fas(context, supplier_alias):
    fas_check_profiles(context, supplier_alias)


@then('"{supplier_alias}" should be told to provide valid links to all online '
      'profiles')
def then_supplier_should_be_told_to_use_valid_links(context, supplier_alias):
    prof_should_be_told_about_invalid_links(context, supplier_alias)


@then('"{supplier_alias}" should not see any links to online profiles on FAB '
      'Company\'s Directory Profile page')
def then_no_online_profiles_are_visible_on_fab(context, supplier_alias):
    fab_no_links_to_online_profiles_are_visible(context, supplier_alias)


@then('"{supplier_alias}" should not see any links to online profiles on FAS '
      'Company\'s Directory Profile page')
def then_no_online_profiles_are_visible_on_fas(context, supplier_alias):
    fas_no_links_to_online_profiles_are_visible(context, supplier_alias)


@then('"{supplier_alias}" should see all case studies on the FAB Company\'s '
      'Directory Profile page')
def then_supplier_should_see_all_case_studies_fab(context, supplier_alias):
    fab_should_see_all_case_studies(context, supplier_alias)


@then('"{supplier_alias}" should see all case studies on the FAS Company\'s '
      'Directory Profile page')
def then_supplier_should_see_all_case_studies_fas(context, supplier_alias):
    fas_should_see_all_case_studies(context, supplier_alias)


@then('"{supplier_alias}" should see that logo on FAB Company\'s '
      'Directory Profile page')
def then_supplier_should_see_logo_picture_on_fab(context, supplier_alias):
    prof_should_see_logo_picture(context, supplier_alias)


@then('"{supplier_alias}" should see that logo on FAS Company\'s '
      'Directory Profile page')
def then_supplier_should_see_logo_picture_on_fas(context, supplier_alias):
    fas_should_see_logo_picture(context, supplier_alias)


@then('for every uploaded unsupported file "{supplier_alias}" should be told '
      'that only certain image types can be used as company\'s logo')
def then_every_invalid_logo_should_be_rejected(context, supplier_alias):
    prof_all_unsupported_files_should_be_rejected(context, supplier_alias)


@then('"{supplier_alias}" should see new details on FAS Company\'s Directory '
      'Profile page')
def then_supplier_should_see_new_details_on_fas(context, supplier_alias):
    fas_should_see_company_details(context, supplier_alias)


@then('"{buyer_alias}" should be able to find company "{company_alias}" on FAS '
      'using words from case study "{case_alias}"')
def then_buyer_should_find_supplier_using_part_of_case_study(
        context, buyer_alias, company_alias, case_alias):
    fas_find_supplier_using_case_study_details(
        context, buyer_alias, company_alias, case_alias,
        properties=context.table)


@then('"{buyer_alias}" should NOT be able to find company "{company_alias}" on '
      'FAS by using any part of case study "{case_alias}"')
def step_impl(context, buyer_alias, company_alias, case_alias):
    fas_supplier_cannot_be_found_using_case_study_details(
        context, buyer_alias, company_alias, case_alias)


@then('"{buyer_alias}" should be able to find company "{company_alias}" on FAS '
      'using any part of case study "{case_alias}"')
def then_buyer_should_find_supplier_using_any_part_of_case_study(
        context, buyer_alias, company_alias, case_alias):
    fas_find_supplier_using_case_study_details(
        context, buyer_alias, company_alias, case_alias)


@then('"{buyer_alias}" should be able to find company "{company_alias}" on FAS '
      'using selected company\'s details')
def then_buyer_should_find_supplier_using_company_details(
        context, buyer_alias, company_alias):
    fas_should_find_with_company_details(context, buyer_alias, company_alias)


@then('the "{page_part}" part of the viewed FAS page should be presented '
      'in "{language}" language with probability greater than "{probability}"')
def then_page_should_be_in(context, page_part, language, probability):
    fas_pages_should_be_in_selected_language(
        context, pages_table=context.table, language=language,
        page_part=page_part, probability=float(probability))


@then('"{buyer_alias}" should be told that the search did not match any UK '
      'trade profiles')
def then_should_be_told_about_empty_search_results(context, buyer_alias):
    fas_should_be_told_about_empty_search_results(context, buyer_alias)


@then('"{buyer_alias}" should be told that the feedback request has been '
      'submitted')
def then_buyer_should_be_told_about_feedback_request_confirmation(
        context, buyer_alias):
    fas_feedback_request_should_be_submitted(context, buyer_alias)


@then('"{buyer_alias}" should be able to find all sought companies')
def then_buyer_should_find_all_sought_companies(context, buyer_alias):
    fas_should_find_all_sought_companies(context, buyer_alias)


@then('"{buyer_alias}" should be told that the message has been sent to company'
      ' "{company_alias}"')
def then_buyer_should_be_told_that_message_has_been_sent(
        context, buyer_alias, company_alias):
    fas_should_be_told_that_message_has_been_sent(
        context, buyer_alias, company_alias)


@then('"{supplier_alias}" should receive an email message from "{buyer_alias}"')
def then_supplier_should_receive_message_from_buyer(
        context, supplier_alias, buyer_alias):
    fas_supplier_should_receive_message_from_buyer(context, supplier_alias, buyer_alias)


@then('"{actor_alias}" should see a logo thumbnail on FAS Company\'s Directory'
      ' Profile page')
def then_buyer_should_see_logo_on_fas_profile_page(context, actor_alias):
    fas_should_see_logo_picture(context, actor_alias)


@then('"{actor_alias}" should see different updated thumbnail of the logo on '
      'FAS Company\'s Directory Profile page')
def then_actor_should_see_different_logo_on_fas(context, actor_alias):
    fas_should_see_different_logo_picture(context, actor_alias)
