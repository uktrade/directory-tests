# -*- coding: utf-8 -*-
"""Given step definitions."""
from behave import given

from steps.then_impl import (
    personalised_journey_should_not_see_banner_and_top_10_table,
    should_be_on_page,
    should_see_sections
)
from steps.when_impl import (
    actor_classifies_himself_as,
    articles_open_any,
    articles_open_any_but_the_last,
    articles_open_first,
    articles_open_group,
    articles_read_a_number_of_them,
    articles_show_all,
    case_studies_go_to_random,
    export_readiness_open_category,
    get_geo_ip,
    guidance_open_category,
    guidance_open_random_category,
    registration_create_and_verify_account,
    set_online_marketplace_preference,
    set_sector_preference,
    sign_in,
    start_triage,
    triage_classify_as,
    triage_create_exporting_journey,
    visit_page
)


@given('"{actor_alias}" went to the "{page_name}" page')
@given('"{actor_alias}" goes to the "{page_name}" page')
@given('"{actor_alias}" visits the "{page_name}" page')
def given_actor_visits_page(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name)


@given('"{actor_alias}" visits the "{page_name}" page for the first time')
def given_actor_visits_page_for_the_first_time(context, actor_alias, page_name):
    visit_page(context, actor_alias, page_name, first_time=True)


@given('"{actor_alias}" is on the "{page_name}" page')
def given_actor_is_on_page(context, actor_alias, page_name):
    should_be_on_page(context, actor_alias, page_name)


@given('"{actor_alias}" classifies herself as "{exporter_status}" exporter')
@given('"{actor_alias}" classifies himself as "{exporter_status}" exporter')
def given_actor_classifies_as(context, actor_alias, exporter_status):
    actor_classifies_himself_as(context, actor_alias, exporter_status)


@given('"{actor_alias}" was classified as "{exporter_status}" exporter in the triage process')
def given_actor_was_classified_as(context, actor_alias, exporter_status):
    triage_classify_as(context, actor_alias, exporter_status=exporter_status)


@given('"{actor_alias}" answered triage questions')
def given_actor_answered_triage_questions(context, actor_alias):
    triage_classify_as(context, actor_alias)


@given('"{actor_alias}" accessed "{category}" guidance articles using "{location}"')
def given_actor_opened_guidance(context, actor_alias, category, location):
    guidance_open_category(context, actor_alias, category, location)


@given('"{actor_alias}" decided to build her exporting journey')
@given('"{actor_alias}" decided to build his exporting journey')
def given_actor_starts_exporting_journey(context, actor_alias):
    start_triage(context, actor_alias)


@given('"{actor_alias}" decided to create her personalised journey page')
@given('"{actor_alias}" decided to create his personalised journey page')
def given_actor_decided_to_create_personalised_page(context, actor_alias):
    triage_create_exporting_journey(context, actor_alias)


@given('"{actor_alias}" was classified as "{exporter_status}" Exporter which "{is_incorporated}" incorporated the company')
def given_actor_was_classified_as(
        context, actor_alias, exporter_status, is_incorporated):
    triage_classify_as(
        context, actor_alias, exporter_status=exporter_status,
        is_incorporated=is_incorporated)


@given('"{actor_alias}" exports "{goods_or_services}"')
def given_actor_sets_sector_preference(context, actor_alias, goods_or_services):
    set_sector_preference(
        context, actor_alias, goods_or_services=goods_or_services)


@given('"{actor_alias}" "{used_or_not}" online marketplaces before')
def given_actor_set_preferences_for_online_marketplaces(
        context, actor_alias, used_or_not):
    set_online_marketplace_preference(context, actor_alias, used_or_not)


@given('"{actor_alias}" opened first Article from the list')
def given_actor_opened_first_article(context, actor_alias):
    articles_open_first(context, actor_alias)


@given('"{actor_alias}" accessed Export Readiness articles for "{category}" Exporters via "{location}"')
def given_actor_goes_to_export_readiness_articles(
        context, actor_alias, category, location):
    export_readiness_open_category(context, actor_alias, category, location)


@given('"{actor_alias}" opened any Article but the last one')
def given_actor_opens_any_article_but_the_last_one(context, actor_alias):
    articles_open_any_but_the_last(context, actor_alias)


@given('"{actor_alias}" opened any Article')
def given_actor_opens_any_article(context, actor_alias):
    articles_open_any(context, actor_alias)


@given('"{actor_alias}" is on the "{group}" Article List for randomly selected category')
def given_actor_is_on_article_list(context, actor_alias, group):
    articles_open_group(context, actor_alias, group)


@given('"{actor_alias}" went to randomly selected Guidance Articles category')
def given_actor_selects_random_guidance_category(context, actor_alias):
    guidance_open_random_category(context, actor_alias)


@given('"{actor_alias}" went to randomly selected "{group}" Article category via "{location}"')
def given_actor_is_on_article_list(context, actor_alias, group, location):
    articles_open_group(context, actor_alias, group, location=location)


@given('"{actor_alias}" exports "{service}" service')
def given_actor_sets_sector_service_preference(context, actor_alias, service):
    set_sector_preference(context, actor_alias, service=service)


@given('"{actor_alias}" can see "{sections}" section on "{page_name}" page')
@given('"{actor_alias}" can see "{sections}" sections on "{page_name}" page')
def given_can_see_sections(context, actor_alias, sections, page_name):
    should_see_sections(context, actor_alias, sections.split(", "), page_name)


@given('"{actor_alias}" exports "{good}" good')
def given_actor_sets_sector_good_preference(context, actor_alias, good):
    set_sector_preference(context, actor_alias, good=good)


@given('"{actor_alias}" cannot see the Top Importer banner and Top 10 Importers table for their sector')
def given_actor_cannot_see_banner_and_top_10_table(context, actor_alias):
    personalised_journey_should_not_see_banner_and_top_10_table(
        context, actor_alias)


@given('"{actor_alias}" read "{number}" of articles and stays on the last read article page')
def given_actor_reads_few_articles(context, actor_alias, number):
    articles_read_a_number_of_them(
        context, actor_alias, number, stay_on_last_article_page=True)


@given('"{actor_alias}" read "{number}" of articles')
def given_actor_reads_few_articles(context, actor_alias, number):
    articles_read_a_number_of_them(context, actor_alias, number)


@given('"{actor_alias}" is a registered and verified user')
def given_actor_is_registered_and_verified(context, actor_alias):
    registration_create_and_verify_account(
        context, actor_alias, fake_verification=True)


@given("{actor_alias} checks her geoip")
@given("{actor_alias} checks his geoip")
def given_actor_checks_the_goeip(context, actor_alias):
    get_geo_ip(context, actor_alias)


@given('"{actor_alias}" signed in using link in the "{location}"')
@given('"{actor_alias}" is signed in')
def given_actor_is_signed_in(context, actor_alias, *, location="top bar"):
    sign_in(context, actor_alias, location)


@given('"{actor_alias}" is on the Case Study page accessed via "{page_name}" page')
def given_actor_is_on_random_case_study_page(context, actor_alias, page_name):
    case_studies_go_to_random(context, actor_alias, page_name)


@given('"{actor_alias}" shows all of the articles on the page')
def given_actor_shows_all_articles(context, actor_alias):
    articles_show_all(context, actor_alias)
