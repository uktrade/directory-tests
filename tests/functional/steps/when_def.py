# -*- coding: utf-8 -*-
# flake8: noqa
"""When step definitions."""
from behave import when
from behave.runner import Context

from tests.functional.steps.when_impl import (
    fab_choose_to_verify_with_code,
    fab_collaborator_create_sso_account_and_confirm_email,
    fab_decide_to_verify_profile_with_letter,
    fab_remove_collaborators,
    fab_submit_verification_code,
    fab_transfer_ownership,
    fas_browse_suppliers_by_company_sectors,
    fas_browse_suppliers_by_invalid_sectors,
    fas_browse_suppliers_by_multiple_sectors,
    fas_browse_suppliers_using_every_sector_filter,
    fas_clear_search_filters,
    fas_follow_case_study_links_to_related_sectors,
    fas_get_case_study_slug,
    fas_search_using_company_details,
    fas_search_with_empty_query,
    fas_search_with_product_service_keyword,
    fas_search_with_term,
    fas_send_feedback_request,
    fas_send_message_to_supplier,
    generic_view_pages_in_selected_language,
    go_to_page,
    go_to_pages,
    isd_search,
    prof_attempt_to_sign_in_to_sso,
    profile_add_case_study,
    profile_add_collaborator,
    profile_add_invalid_online_profiles,
    profile_add_online_profiles,
    profile_attempt_to_add_case_study,
    profile_confirm_collaboration_request,
    profile_enrol_user,
    profile_go_to_letter_verification,
    profile_provide_business_details,
    profile_provide_products_and_services,
    profile_remove_links_to_online_profiles,
    profile_request_to_verify,
    profile_send_transfer_ownership_request,
    profile_supplier_uploads_logo,
    profile_to_upload_unsupported_logos,
    profile_unpublish_profile_from_fas,
    profile_update_case_study,
    profile_update_company_details,
    profile_verify_company_profile,
    profile_view_published_profile,
    profile_view_unpublished_profile,
    reg_create_sso_account,
    reg_open_email_confirmation_link,
    reg_supplier_confirms_email_address,
    sso_change_password_with_password_reset_link,
    sso_open_password_reset_link,
    sso_request_password_reset,
    sso_sign_in,
    sso_supplier_confirms_email_address,
)


@when(
    '"{supplier_alias}" creates a SSO/great.gov.uk account for "{alias}" using valid credentials'
)
def when_supplier_creates_sso_account_for_selected_company(
    context, supplier_alias, alias
):
    reg_create_sso_account(context, supplier_alias, alias)


@when(
    '"{supplier_alias}" decides to confirm her email address by using the email confirmation link'
)
def when_supplier_confirms_the_email_address(context, supplier_alias):
    reg_open_email_confirmation_link(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address')
def when_supplier_confirms_email_address(context, supplier_alias):
    reg_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" confirms the email address for SSO/great.gov.uk account')
def when_supplier_confirms_email_address_for_sso(context, supplier_alias):
    sso_supplier_confirms_email_address(context, supplier_alias)


@when('"{supplier_alias}" decides to verify her identity with a verification letter')
@when('"{supplier_alias}" decides to verify his identity with a verification letter')
def when_supplier_provides_full_name(context, supplier_alias):
    fab_decide_to_verify_profile_with_letter(context, supplier_alias)


@when(
    '"{supplier_alias}" verifies the company with the verification code from the letter sent after Directory Profile was created'
)
def when_supplier_verifies_company(context, supplier_alias):
    profile_verify_company_profile(context, supplier_alias)


@when('"{supplier_alias}" decides to view published FAS Business Profile')
def when_supplier_views_published_profile(context, supplier_alias):
    profile_view_published_profile(context, supplier_alias)


@when(
    '"{supplier_alias}" decides to view unpublished profile on Find a Supplier service'
)
def when_supplier_views_published_profile(context, supplier_alias):
    profile_view_unpublished_profile(context, supplier_alias)


@when('"{supplier_alias}" attempts to sign in to SSO/great.gov.uk account')
def when_supplier_attempts_to_sign_in_to_fab(context, supplier_alias):
    prof_attempt_to_sign_in_to_sso(context, supplier_alias)


@when('"{supplier_alias}" updates company\'s details')
def when_supplier_updates_company_details(context, supplier_alias):
    profile_update_company_details(context, supplier_alias, context.table)


@when('"{supplier_alias}" adds links to online profiles')
def when_supplier_adds_online_profiles(context, supplier_alias):
    profile_add_online_profiles(context, supplier_alias, context.table)


@when('"{supplier_alias}" attempts to use invalid links to online profiles')
def when_supplier_attempts_to_add_invalid_links(context, supplier_alias):
    profile_add_invalid_online_profiles(context, supplier_alias, context.table)


@when('"{supplier_alias}" removes links to all online profiles')
def when_supplier_removes_links_to_all_online_profiles(context, supplier_alias):
    profile_remove_links_to_online_profiles(context, supplier_alias)


@when('"{supplier_alias}" adds a complete case study called "{case_alias}"')
def when_supplier_adds_case_study(context, supplier_alias, case_alias):
    profile_add_case_study(context, supplier_alias, case_alias)


@when('"{supplier_alias}" uploads "{picture}" as company\'s logo')
def when_supplier_uploads_logo(context, supplier_alias, picture):
    profile_supplier_uploads_logo(context, supplier_alias, picture)


@when(
    '"{supplier_alias}" attempts to upload a file of unsupported type as company\'s logo'
)
def when_supplier_attempts_to_upload_unsupported_file(context, supplier_alias):
    profile_to_upload_unsupported_logos(context, supplier_alias, context.table)


@when('"{supplier_alias}" updates all the details of case study called "{case_alias}"')
def when_supplier_updates_case_study(context, supplier_alias, case_alias):
    profile_update_case_study(context, supplier_alias, case_alias)


@when(
    '"{buyer_alias}" searches for company "{company_alias}" on FAS using selected company\'s details'
)
def when_buyer_searches_on_fas_using_company_details(
    context, buyer_alias, company_alias
):
    fas_search_using_company_details(
        context, buyer_alias, company_alias, table_of_details=context.table
    )


@when('"{actor_alias}" chooses to view following pages in "{language}" language')
def when_actor_views_pages_in_selected_language(context, actor_alias, language):
    generic_view_pages_in_selected_language(
        context, actor_alias, pages_table=context.table, language=language
    )


@when('"{buyer_alias}" searches for FAS companies with empty search query')
def when_fas_buyer_searches_with_emtpy_search_query(context, buyer_alias):
    fas_search_with_empty_query(context, buyer_alias)


@when('"{buyer_alias}" searches for ISD companies with empty search query')
def when_isd_buyer_searches_with_emtpy_search_query(context, buyer_alias):
    isd_search(context, buyer_alias, term="")


@when(
    '"{buyer_alias}" sends a Trade Profiles feedback request from "{page_name}" FAS page'
)
def when_buyer_sends_feedback_request(context, buyer_alias, page_name):
    fas_send_feedback_request(context, buyer_alias, page_name)


@when(
    '"{buyer_alias}" searches for Suppliers using product name, service name and a keyword'
)
def when_buyer_search_using_product_servive_keyword(context, buyer_alias):
    fas_search_with_product_service_keyword(context, buyer_alias, context.table)


@when('"{buyer_alias}" sends a message to company "{company_alias}"')
def when_buyer_sends_message_to_supplier(context, buyer_alias, company_alias):
    fas_send_message_to_supplier(context, buyer_alias, company_alias)


@when('"{supplier_alias}" attempts to change business details')
def when_supplier_provide_company_details(context, supplier_alias):
    profile_provide_business_details(context, supplier_alias, context.table)


@when(
    '"{supplier_alias}" attempts to change products and services offered by the company'
)
def when_supplier_provide_products_and_services(context, supplier_alias):
    profile_provide_products_and_services(context, supplier_alias, context.table)


@when(
    '"{actor_alias}" follows all the links to industries associated with the case study from the Company Showcase'
)
def when_actor_follows_case_study_links_to_sectors(context, actor_alias):
    fas_follow_case_study_links_to_related_sectors(context, actor_alias)


@when('"{actor_alias}" browse Suppliers by every available sector filter')
def when_actor_browse_suppliers_using_every_sector_filter(context, actor_alias):
    fas_browse_suppliers_using_every_sector_filter(context, actor_alias)


@when('"{actor_alias}" browse Suppliers by multiple sector filters')
def when_actor_browse_suppliers_by_multiple_sectors(context, actor_alias):
    fas_browse_suppliers_by_multiple_sectors(context, actor_alias)


@when('"{actor_alias}" attempts to browse Suppliers by invalid sector filter')
def when_actor_browse_suppliers_by_invalid_sectors(context, actor_alias):
    fas_browse_suppliers_by_invalid_sectors(context, actor_alias)


@when('"{actor_alias}" clears the search filters')
def when_actor_clears_search_filters(context, actor_alias):
    fas_clear_search_filters(context, actor_alias)


@when(
    '"{actor_alias}" browse first "{pages_to_scan:d}" pages of Suppliers filtered by all sectors associated with company "{company_alias}"'
)
def when_browse_suppliers_by_company_sectors(
    context, actor_alias, pages_to_scan: int, company_alias
):
    fas_browse_suppliers_by_company_sectors(
        context, actor_alias, company_alias, pages_to_scan
    )


@when('"{actor_alias}" gets the slug for case study "{case_alias}"')
def when_actor_gets_case_study_slug(context, actor_alias, case_alias):
    fas_get_case_study_slug(context, actor_alias, case_alias)


@when('"{actor_alias}" searches for Suppliers using "{search_term}" term')
def step_impl(context, actor_alias, search_term):
    fas_search_with_term(context, actor_alias, search_term)


@when(
    '"{supplier_alias}" goes to the verification link from the letter as authenticated user'
)
def when_supplier_goes_to_verify_page_auth(context, supplier_alias):
    profile_go_to_letter_verification(context, supplier_alias, True)


@when(
    '"{supplier_alias}" goes to the verification link from the letter as unauthenticated user'
)
def when_supplier_goes_to_verify_page_unauth(context, supplier_alias):
    profile_go_to_letter_verification(context, supplier_alias, False)


@when('"{supplier_alias}" decides to verify her identity with the address')
def when_supplier_decides_to_verify_with_address(context, supplier_alias):
    fab_choose_to_verify_with_code(context, supplier_alias)


@when('"{supplier_alias}" submits the verification code')
def when_supplier_submits_verification_code(context, supplier_alias):
    fab_submit_verification_code(context, supplier_alias)


@when('"{supplier_alias}" attempts to add a case study using following values')
def when_supplier_attempts_to_add_case_study(context, supplier_alias):
    profile_attempt_to_add_case_study(context, supplier_alias, context.table)


@when('"{supplier_alias}" requests password reset')
def when_supplier_resets_password(context, supplier_alias):
    sso_request_password_reset(context, supplier_alias)


@when('"{supplier_alias}" signs in to SSO/great.gov.uk account from "{page_name}"')
@when('"{supplier_alias}" signs in to SSO/great.gov.uk account')
def when_supplier_signs_in_to_sso_account(
    context, supplier_alias, *, page_name: str = None
):
    sso_sign_in(context, supplier_alias, from_page=page_name)


@when(
    '"{supplier_alias}" changes the password to a new one using the password reset link'
)
def when_supplier_change_password(context, supplier_alias):
    sso_change_password_with_password_reset_link(context, supplier_alias, new=True)


@when('"{supplier_alias}" opens the password reset link')
def when_supplier_opens_password_reset_link(context, supplier_alias):
    sso_open_password_reset_link(context, supplier_alias)


@when(
    '"{supplier_alias}" changes the password to the same one using the password reset link'
)
def when_supplier_changes_password_to_the_same_one(context, supplier_alias):
    sso_change_password_with_password_reset_link(context, supplier_alias, same=True)


@when('"{supplier_alias}" goes to "{page_name}" page')
def when_supplier_goes_sud_page(context, supplier_alias, page_name):
    go_to_page(context, supplier_alias, page_name)


@when('"{actor_alias}" goes to specific pages')
def when_actor_goes_to_specific_pages(context, actor_alias):
    go_to_pages(context, actor_alias, context.table)


@when(
    '"{supplier_alias}" attempts to change the password to one with only letters and using the password reset link'
)
def when_supplier_tries_to_change_password_to_letters_only(context, supplier_alias):
    sso_change_password_with_password_reset_link(
        context, supplier_alias, new=True, letters_only=True
    )


@when(
    '"{supplier_alias}" decides to add "{collaborator_aliases}" as an "{role}" collaborator'
)
@when(
    '"{supplier_alias}" decides to add "{collaborator_aliases}" as a "{role}" collaborator'
)
def when_owner_adds_a_collaborator(context, supplier_alias, collaborator_aliases, role):
    profile_add_collaborator(context, supplier_alias, collaborator_aliases, role)


@when(
    '"{collaborator_alias}" confirms that he wants to be added to the company "{company_alias}" Find a Buyer profile'
)
@when(
    '"{collaborator_alias}" confirms that she wants to be added to the company "{company_alias}" Find a Buyer profile'
)
def when_collaborator_confirms_the_collaboration_request(
    context, collaborator_alias, company_alias
):
    profile_confirm_collaboration_request(context, collaborator_alias, company_alias)


@when(
    '"{collaborator_alias}" opens the invitation from company "{company_alias}", creates a SSO/great.gov.uk account and confirms that he wants to be added to the FAB profile'
)
@when(
    '"{collaborator_alias}" opens the invitation from company "{company_alias}", creates a SSO/great.gov.uk account and confirms that she wants to be added to the FAB profile'
)
def when_collaborator_creates_sso_account_and_confirms_email(
    context, collaborator_alias, company_alias
):
    fab_collaborator_create_sso_account_and_confirm_email(
        context, collaborator_alias, company_alias
    )


@when(
    '"{supplier_alias}" decides to transfer the ownership of company\'s "{company_alias}" Find a Buyer profile to "{new_owner_alias}"'
)
def when_supplier_decides_to_transfer_profile_ownership(
    context, supplier_alias, company_alias, new_owner_alias
):
    profile_send_transfer_ownership_request(
        context, supplier_alias, company_alias, new_owner_alias
    )


@when(
    '"{supplier_alias}" transfers the ownership of company\'s "{company_alias}" Find a Buyer profile to "{new_owner_alias}"'
)
def when_supplier_transfers_the_account_ownership(
    context, supplier_alias, company_alias, new_owner_alias
):
    fab_transfer_ownership(context, supplier_alias, company_alias, new_owner_alias)


@when(
    '"{supplier_alias}" removes "{collaborators_aliases}" from the list of collaborators to the company "{company_alias}"'
)
def when_supplier_removes_collaborators(
    context, supplier_alias, collaborators_aliases, company_alias
):
    fab_remove_collaborators(
        context, supplier_alias, collaborators_aliases, company_alias
    )


@when('"{actor_alias}" creates an "{account_type}" profile')
def when_user_creates_a_profile(
    context: Context, actor_alias: str, account_type: str, *, company_alias: str = None
):
    profile_enrol_user(context, actor_alias, account_type, company_alias=company_alias)


@when('"{actor_alias}" decides to unpublish profile from Find a Supplier service')
def when_actor_unpublishes_profile(context: Context, actor_alias: str):
    profile_unpublish_profile_from_fas(context, actor_alias)


@when('"{actor_alias}" requests to verify her company profile')
def when_actor_requests_verification(context: Context, actor_alias: str):
    profile_request_to_verify(context, actor_alias)
