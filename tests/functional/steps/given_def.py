# -*- coding: utf-8 -*-
# flake8: noqa
"""Given step definitions."""
from behave import given

from tests.functional.steps.then_impl import (
    fas_should_see_png_logo_thumbnail,
    profile_should_see_all_case_studies,
    profile_should_see_logo_picture,
    reg_should_get_verification_email,
    should_be_at,
    sso_should_be_signed_in_to_sso_account,
    sso_should_be_signed_out_from_sso_account,
    sso_should_get_request_for_collaboration_email,
)
from tests.functional.steps.when_impl import (
    create_actor_with_or_without_sso_account,
    create_actor_with_verified_or_unverified_fab_profile,
    profile_add_collaborator,
    fab_confirm_collaboration_request,
    fab_decide_to_verify_profile_with_letter,
    fab_find_published_company,
    fab_open_collaboration_request_link,
    fab_transfer_ownership,
    fas_find_company_by_name,
    fas_get_company_slug,
    go_to_page,
    profile_add_business_description,
    profile_add_case_study,
    profile_add_online_profiles,
    profile_add_product_and_services_keywords,
    profile_create_unverified_business_profile,
    profile_create_verified_and_published_business_profile,
    profile_create_verified_yet_unpublished_business_profile,
    profile_edit_business_details,
    profile_supplier_uploads_logo,
    reg_create_standalone_unverified_sso_account,
    reg_should_get_verification_letter,
    sso_create_standalone_unverified_sso_account,
    sso_create_standalone_verified_sso_account,
    sso_get_password_reset_link,
    stannp_send_verification_letter,
    unauthenticated_buyer,
    unauthenticated_supplier,
)


@given('"{supplier_alias}" is an unauthenticated supplier')
def given_an_unauthenticated_supplier(context, supplier_alias):
    context.add_actor(unauthenticated_supplier(supplier_alias))


@given('"{supplier_alias}" created an unverified SSO/great.gov.uk account')
def when_supplier_creates_standalone_sso_account(context, supplier_alias):
    reg_create_standalone_unverified_sso_account(context, supplier_alias)


@given('"{alias}" received the email verification message with the email confirmation link')
def given_supplier_received_verification_email(context, alias):
    reg_should_get_verification_email(context, alias)


@given('"{supplier_alias}" set the company description')
def given_supplier_set_company_description(context, supplier_alias):
    profile_add_business_description(context, supplier_alias)


@given('"{supplier_alias}" has created verified and published business profile for randomly selected company "{company_alias}"')
def given_supplier_creates_verified_and_published_profile(
        context, supplier_alias, company_alias):
    profile_create_verified_and_published_business_profile(
        context, supplier_alias, company_alias
    )


@given('"{supplier_alias}" has created verified yet unpublished business profile for randomly selected company "{company_alias}"')
def given_supplier_creates_verified_but_unpublished_profile(
        context, supplier_alias, company_alias):
    profile_create_verified_yet_unpublished_business_profile(
        context, supplier_alias, company_alias
    )


@given('"{supplier_alias}" created a standalone SSO/great.gov.uk account with unverified email address')
def given_supplier_creates_standalone_unverified_sso_account(
        context, supplier_alias):
    sso_create_standalone_unverified_sso_account(context, supplier_alias)


@given('"{supplier_alias}" has a verified standalone SSO/great.gov.uk account')
def given_verified_standalone_sso_account(context, supplier_alias):
    sso_create_standalone_verified_sso_account(context, supplier_alias)


@given('"{supplier_alias}" is signed in to SSO/great.gov.uk account')
def given_supplier_is_signed_in_to_sso(context, supplier_alias):
    sso_should_be_signed_in_to_sso_account(context, supplier_alias)


@given('"{supplier_alias}" signed out from SSO/great.gov.uk account')
def given_supplier_is_signed_out_from_sso(context, supplier_alias):
    sso_should_be_signed_out_from_sso_account(context, supplier_alias)


@given('"{supplier_alias}" has added links to online profiles')
def given_supplier_adds_valid_links_to_online_profiles(
        context, supplier_alias):
    profile_add_online_profiles(context, supplier_alias, context.table)


@given('"{supplier_alias}" has set "{picture}" picture as company\'s logo')
def given_supplier_sets_logo_picture(context, supplier_alias, picture):
    profile_supplier_uploads_logo(context, supplier_alias, picture)


@given('"{supplier_alias}" can see that logo on FAB Company\'s Directory Profile page')
def given_supplier_can_see_correct_logo_on_fab_profile(
        context, supplier_alias):
    profile_should_see_logo_picture(context, supplier_alias)


@given('"{supplier_alias}" added a complete case study called "{case_alias}"')
def given_supplier_added_complete_case_study(
        context, supplier_alias, case_alias):
    profile_add_case_study(context, supplier_alias, case_alias)
    profile_should_see_all_case_studies(context, supplier_alias)


@given('"{buyer_alias}" is an anonymous visitor')
@given('"{buyer_alias}" is a buyer')
def given_unauthenticated_buyer(context, buyer_alias):
    buyer = unauthenticated_buyer(buyer_alias)
    context.add_actor(buyer)


@given('"{buyer_alias}" has found a company "{company_alias}" on Find a Supplier site')
def given_buyer_finds_company_by_name(context, buyer_alias, company_alias):
    fas_find_company_by_name(context, buyer_alias, company_alias)


@given('"{actor_alias}" can see a PNG logo thumbnail on FAS Company\'s Directory Profile page')
def given_actor_can_see_logo_on_fas_profile_page(context, actor_alias):
    fas_should_see_png_logo_thumbnail(context, actor_alias)


@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_views_fas_page(context, actor_alias, page_name):
    go_to_page(context, actor_alias, page_name)


@given('"{actor_alias}" finds a Supplier "{company_alias}" with a published profile associated with at least "{min_number_sectors}" different sectors')
def given_actor_finds_published_company_with_min_n_sectors(
        context, actor_alias, company_alias, min_number_sectors: int):
    fab_find_published_company(
        context, actor_alias, company_alias,
        min_number_sectors=min_number_sectors)


@given('"{actor_alias}" gets the slug for company "{company_alias}"')
def given_actor_gets_company_slug(context, actor_alias, company_alias):
    fas_get_company_slug(context, actor_alias, company_alias)


@given('"{supplier_alias}" received the letter with verification code')
def given_supplier_received_verification_letter(context, supplier_alias):
    reg_should_get_verification_letter(context, supplier_alias)


@given('"{supplier_alias}" received a password reset email')
def given_supplier_received_password_reset_email(context, supplier_alias):
    sso_get_password_reset_link(context, supplier_alias)


@given('"{actor_alias}" has created "{verified_or_not}" profile for randomly selected company "{company_alias}"')
def given_actor_with_verified_or_not_profile(
        context, actor_alias, verified_or_not, company_alias):
    create_actor_with_verified_or_unverified_fab_profile(
        context, actor_alias, verified_or_not, company_alias)


@given('"{actor_aliases}" "{has_or_does_not_have}" an SSO/great.gov.uk account')
def given_actor_with_or_without_sso_account(
        context, actor_aliases, has_or_does_not_have):
    create_actor_with_or_without_sso_account(
        context, actor_aliases, has_or_does_not_have)


@given('"{supplier_alias}" added "{collaborator_aliases}" as a collaborator')
def given_supplier_added_a_collaborator(
        context, supplier_alias, collaborator_aliases):
    profile_add_collaborator(context, supplier_alias, collaborator_aliases)


@given('"{supplier_alias}" has received an email with a request to confirm that he\'s been added to company "{company_alias}" Find a Buyer profile')
@given('"{supplier_alias}" has received an email with a request to confirm that she\'s been added to company "{company_alias}" Find a Buyer profile')
def given_actor_should_receive_email_with_request_for_collaboration(
        context, supplier_alias, company_alias):
    sso_should_get_request_for_collaboration_email(
        context, supplier_alias, company_alias)


@given('"{actor_alias}" should be on "{page_name}" page')
def given_actor_is_on_specific_page(context, actor_alias, page_name):
    should_be_at(context, actor_alias, page_name)


@given('"{collaborator_alias}" decides to open the invitation from company "{company_alias}"')
def given_collaborator_decides_to_open_invitation(
        context, collaborator_alias, company_alias):
    fab_open_collaboration_request_link(
        context, collaborator_alias, company_alias)


@given('"{collaborator_alias}" confirmed that he wants to be added to the company "{company_alias}" Find a Buyer profile')
@given('"{collaborator_alias}" confirmed that she wants to be added to the company "{company_alias}" Find a Buyer profile')
def given_collaborator_confirms_the_collaboration_request(
        context, collaborator_alias, company_alias):
    fab_confirm_collaboration_request(
        context, collaborator_alias, company_alias)


@given('"{supplier_alias}" transferred the ownership of company\'s "{company_alias}" Find a Buyer profile to "{new_owner_alias}"')
def given_supplier_transfers_the_account_ownership(
        context, supplier_alias, company_alias, new_owner_alias):
    fab_transfer_ownership(
        context, supplier_alias, company_alias, new_owner_alias)


@given('"{actor_alias}" sends a test verification letter via StanNP for randomly selected company')
def given_actor_sends_a_verification_letter(context, actor_alias):
    stannp_send_verification_letter(context, actor_alias)


@given('"{supplier_alias}" created an unverified business profile for randomly selected company "{company_alias}"')
def given_unverified_profile_new_reg_flow(context, supplier_alias, company_alias):
    profile_create_unverified_business_profile(
        context, supplier_alias, company_alias
    )


@given('"{actor_alias}" has added random keywords to describe the products and services his business offers')
def given_supplier_added_products_and_services_keywords(context, actor_alias):
    profile_add_product_and_services_keywords(context, actor_alias)


@given('"{actor_alias}" has updated business details')
def given_supplier_edit_business_details(context, actor_alias):
    """This step was added as a workaround for bug TT-1256"""
    profile_edit_business_details(
        context, actor_alias, table_of_details=context.table
    )


@given('"{supplier_alias}" decided to verify her identity with a verification letter')
@given('"{supplier_alias}" decided to verify his identity with a verification letter')
def given_supplier_decided_to_verify_with_letter(context, supplier_alias):
    fab_decide_to_verify_profile_with_letter(context, supplier_alias)
