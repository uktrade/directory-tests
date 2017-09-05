# -*- coding: utf-8 -*-
"""FAB Given step definitions."""
from behave import when

from tests.functional.features.steps.fab_when_impl import (
    bp_provide_company_details,
    bp_provide_full_name,
    bp_select_random_sector_and_export_to_country,
    fab_provide_company_details,
    fab_update_case_study,
    fas_search_using_company_details,
    fas_search_with_empty_query,
    fas_search_with_product_service_keyword,
    fas_send_feedback_request,
    fas_send_message_to_supplier,
    fas_view_page,
    fas_view_pages_in_selected_language,
    prof_add_case_study,
    prof_add_invalid_online_profiles,
    prof_add_online_profiles,
    prof_attempt_to_sign_in_to_fab,
    prof_remove_links_to_online_profiles,
    prof_sign_in_to_fab,
    prof_supplier_uploads_logo,
    prof_to_upload_unsupported_logos,
    prof_update_company_details,
    prof_verify_company,
    prof_view_published_profile,
    reg_confirm_company_selection,
    reg_confirm_export_status,
    reg_create_sso_account,
    reg_create_standalone_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    select_random_company,
    sso_go_to_create_trade_profile,
    sso_supplier_confirms_email_address
)


@when('"{supplier_alias}" randomly selects an active company without a '
      'Directory Profile identified by an alias "{alias}"')
def when_supplier_selects_random_company(context, supplier_alias, alias):
    select_random_company(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that "{alias}" is the correct one')
def when_company_selection_is_confirmed(context, supplier_alias, alias):
    reg_confirm_company_selection(context, supplier_alias, alias)


@when('"{supplier_alias}" confirms that the company has exported in the past')
def when_supplier_confirm_export_status(context, supplier_alias):
    reg_confirm_export_status(context, supplier_alias, exported=True)


@when('"{supplier_alias}" confirms that the company has not exported in the '
      'past')
def when_supplier_confirm_that_company_has_not_exported(
        context, supplier_alias):
    reg_confirm_export_status(context, supplier_alias, exported=False)


@when('"{supplier_alias}" creates a SSO/great.gov.uk account for "{alias}" '
      'using valid credentials')
def when_supplier_creates_sso_account_for_selected_company(context,
                                                           supplier_alias,
                                                           alias):
    reg_create_sso_account(context, supplier_alias, alias)


@when('"{supplier_alias}" decides to confirm her email address by using the '
      'email confirmation link')
def when_supplier_confirms_the_email_address(context, supplier_alias):
    reg_open_email_confirmation_link(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address')
def when_supplier_confirms_email_address(context, supplier_alias):
    reg_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address for SSO/great.gov.uk '
      'account')
def when_supplier_confirms_email_address_for_sso(context, supplier_alias):
    sso_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" provides valid details of selected company')
def when_supplier_provides_company_details(context, supplier_alias):
    bp_provide_company_details(context, supplier_alias)


@when('"{supplier_alias}" selects sector the company is in and preferred '
      'country of export')
def when_supplier_selects_random_sector(context, supplier_alias):
    bp_select_random_sector_and_export_to_country(context, supplier_alias)


@when('"{supplier_alias}" provides her full name which will be used to sent '
      'the verification letter')
@when('"{supplier_alias}" provides his full name which will be used to sent '
      'the verification letter')
def when_supplier_provides_full_name(context, supplier_alias):
    bp_provide_full_name(context, supplier_alias)


@when('"{supplier_alias}" verifies the company with the verification code '
      'from the letter sent after Directory Profile was created')
def when_supplier_verifies_company(context, supplier_alias):
    prof_verify_company(context, supplier_alias)


@when('"{supplier_alias}" decides to view published Directory Profile')
def when_supplier_views_published_profile(context, supplier_alias):
    prof_view_published_profile(context, supplier_alias)


@when('"{supplier_alias}" attempts to sign in to Find a Buyer profile')
def when_supplier_attempts_to_sign_in_to_fab(context, supplier_alias):
    prof_attempt_to_sign_in_to_fab(context, supplier_alias)


@when('"{supplier_alias}" signs in to Find a Buyer profile')
def when_supplier_signs_in_to_fab(context, supplier_alias):
    prof_sign_in_to_fab(context, supplier_alias)


@when('"{supplier_alias}" creates a SSO/great.gov.uk account')
def when_supplier_creates_standalone_sso_account(context, supplier_alias):
    reg_create_standalone_sso_account(context, supplier_alias)


@when('"{supplier_alias}" decides to create a trade profile')
def when_supplier_decide_to_create_trade_profile(context, supplier_alias):
    sso_go_to_create_trade_profile(context, supplier_alias)


@when('"{supplier_alias}" updates company\'s details')
def when_supplier_updates_company_details(context, supplier_alias):
    prof_update_company_details(context, supplier_alias, context.table)


@when('"{supplier_alias}" adds links to online profiles')
def when_supplier_adds_online_profiles(context, supplier_alias):
    prof_add_online_profiles(context, supplier_alias, context.table)


@when('"{supplier_alias}" attempts to use invalid links to online profiles')
def when_supplier_attempts_to_add_invalid_links(context, supplier_alias):
    prof_add_invalid_online_profiles(context, supplier_alias, context.table)


@when('"{supplier_alias}" removes links to all online profiles')
def when_supplier_removes_links_to_all_online_profiles(context, supplier_alias):
    prof_remove_links_to_online_profiles(context, supplier_alias)


@when('"{supplier_alias}" adds a complete case study called "{case_alias}"')
def when_supplier_adds_case_study(context, supplier_alias, case_alias):
    prof_add_case_study(context, supplier_alias, case_alias)


@when('"{supplier_alias}" uploads "{picture}" as company\'s logo')
def when_supplier_uploads_logo(context, supplier_alias, picture):
    prof_supplier_uploads_logo(context, supplier_alias, picture)


@when('"{supplier_alias}" attempts to upload a file of unsupported type as '
      'company\'s logo')
def when_supplier_attempts_to_upload_unsupported_file(context, supplier_alias):
    prof_to_upload_unsupported_logos(context, supplier_alias, context.table)


@when('"{supplier_alias}" updates all the details of case study called '
      '"{case_alias}"')
def when_supplier_updates_case_study(context, supplier_alias, case_alias):
    fab_update_case_study(context, supplier_alias, case_alias)


@when('"{buyer_alias}" searches for company "{company_alias}" on FAS using '
      'selected company\'s details')
def when_buyer_searches_on_fas_using_company_details(
        context, buyer_alias, company_alias):
    fas_search_using_company_details(
        context, buyer_alias, company_alias, table_of_details=context.table)


@when('"{buyer_alias}" chooses to view specific FAS page in "{language}" '
      'language')
def when_buyer_views_page_in_selected_language(context, buyer_alias, language):
    fas_view_pages_in_selected_language(
        context, buyer_alias, pages_table=context.table, language=language)


@when('"{buyer_alias}" searches for companies on FAS with empty search query')
def when_buyer_searches_with_emtpy_search_query(context, buyer_alias):
    fas_search_with_empty_query(context, buyer_alias)


@when('"{buyer_alias}" sends a Trade Profiles feedback request from '
      '"{page_name}" FAS page')
def when_buyer_sends_feedback_request(context, buyer_alias, page_name):
    fas_send_feedback_request(context, buyer_alias, page_name)


@when('"{buyer_alias}" searches for Suppliers using product name, service name'
      ' and a keyword')
def when_buyer_search_using_product_servive_keyword(context, buyer_alias):
    fas_search_with_product_service_keyword(context, buyer_alias, context.table)


@when('"{buyer_alias}" sends a message to company "{company_alias}"')
def when_buyer_sends_message_to_supplier(context, buyer_alias, company_alias):
    fas_send_message_to_supplier(context, buyer_alias, company_alias)


@when('"{supplier_alias}" provides company details using following values')
def when_supplier_provide_company_details(context, supplier_alias):
    fab_provide_company_details(context, supplier_alias, context.table)


@when('"{actor_alias}" visits "{page_name}" page on FAS')
def when_actor_visits_page_on_fas(context, actor_alias, page_name):
    fas_view_page(context, actor_alias, page_name)
