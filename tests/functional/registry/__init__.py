# -*- coding: utf-8 -*-
"""FABS Page Registry"""
from tests.functional.pages import (
    fab_ui_account_add_collaborator,
    fab_ui_account_confrim_password,
    fab_ui_account_remove_collaborator,
    fab_ui_account_transfer_ownership,
    fab_ui_confim_your_collaboration,
    fab_ui_confim_your_ownership,
    fab_ui_confirm_identity,
    fab_ui_confirm_identity_letter,
    fab_ui_edit_online_profiles,
    fab_ui_edit_sector,
    fab_ui_landing,
    fab_ui_verify_company,
    fas_ui_creative_industry,
    fas_ui_creative_industry_summary,
    fas_ui_find_supplier,
    fas_ui_food_and_drink_industry,
    fas_ui_food_and_drink_industry_summary,
    fas_ui_health_industry,
    fas_ui_health_industry_summary,
    fas_ui_industries,
    fas_ui_profile,
    fas_ui_tech_industry,
    fas_ui_tech_industry_summary,
    profile_about,
    profile_case_study_basic,
    profile_edit_company_description,
    profile_edit_company_profile,
    profile_enrol,
    profile_upload_logo,
    sso_ui_confim_your_email,
    sso_ui_login,
    sso_ui_logout,
    sso_ui_password_reset,
    sso_ui_register,
    sud_ui_export_opportunities,
    sud_ui_find_a_buyer,
    sud_ui_selling_online_overseas,
)

from tests import get_absolute_url

FAS_PAGE_REGISTRY = {
    "fas landing": {"url": "ui-supplier:landing", "po": None},
    "fas industries": {
        "url": "ui-supplier:industries",
        "po": fas_ui_industries,
    },
    "fas search": {"url": "ui-supplier:search", "po": fas_ui_find_supplier},
    "fas health industry": {
        "url": "ui-supplier:industries-health",
        "po": fas_ui_health_industry,
    },
    "fas tech industry": {
        "url": "ui-supplier:industries-tech",
        "po": fas_ui_tech_industry,
    },
    "fas creative industry": {
        "url": "ui-supplier:industries-creative",
        "po": fas_ui_creative_industry,
    },
    "fas food and drink industry": {
        "url": "ui-supplier:industries-food",
        "po": fas_ui_food_and_drink_industry,
    },
    "fas health industry summary": {
        "url": "ui-supplier:industries-health-summary",
        "po": fas_ui_health_industry_summary,
    },
    "fas tech industry summary": {
        "url": "ui-supplier:industries-tech-summary",
        "po": fas_ui_tech_industry_summary,
    },
    "fas creative industry summary": {
        "url": "ui-supplier:industries-creative-summary",
        "po": fas_ui_creative_industry_summary,
    },
    "fas food and drink industry summary": {
        "url": "ui-supplier:industries-food-summary",
        "po": fas_ui_food_and_drink_industry_summary,
    },
    "fas - company profile": {
        "url": "ui-supplier:industries-food-summary",
        "po": fas_ui_profile,
    },
}

SSO_PAGE_REGISTRY = {
    "sso landing": {"url": "sso:landing", "po": None},
    "sso login": {"url": "sso:login", "po": sso_ui_login},
    "sso register": {"url": "sso:signup", "po": sso_ui_register},
    "sso logout": {"url": "sso:logout", "po": sso_ui_logout},
    "sso password change": {"url": "sso:password_change", "po": None},
    "sso password set": {"url": "sso:password_set", "po": None},
    "sso password reset": {
        "url": "sso:password_reset",
        "po": sso_ui_password_reset,
    },
    "sso confirm email": {
        "url": "sso:email_confirm",
        "po": sso_ui_confim_your_email,
    },
    "sso inactive": {"url": "sso:inactive", "po": None},
    "sso health": {"url": "sso:health", "po": None},
    "sso session user": {"url": "sso:user", "po": None},
}

FAB_PAGE_REGISTRY = {
    "fab landing": {"url": "ui-buyer:landing", "po": fab_ui_landing},
    "fab register": {"url": "ui-buyer:register", "po": None},
    "fab confirm company selection": {
        "url": "ui-buyer:register-confirm-company",
        "po": None,
    },
    "fab confirm export status": {
        "url": "ui-buyer:register-confirm-export-status",
        "po": None,
    },
    "fab finish registration": {"url": "ui-buyer:register-finish", "po": None},
    "fab submit account details": {
        "url": "ui-buyer:register-submit-account-details",
        "po": None,
    },
    "fab upload logo": {
        "url": "profile:upload-logo",
        "po": profile_upload_logo,
    },
    "fab company company address": {
        "url": "ui-buyer:confirm-company-address",
        "po": fab_ui_verify_company,
    },
    "fab company identity": {
        "url": "ui-buyer:confirm-identity",
        "po": fab_ui_confirm_identity,
    },
    "fab company identity via letter": {
        "url": "ui-buyer:confirm-identity-letter",
        "po": fab_ui_confirm_identity_letter,
    },
    "fab edit company profile": {
        "url": "ui-buyer:company-edit",
        "po": fab_ui_edit_online_profiles,
    },
    "fab edit company address": {
        "url": "ui-buyer:company-edit-address",
        "po": None,
    },
    "fab edit company sectors": {
        "url": "ui-buyer:company-edit-sectors",
        "po": fab_ui_edit_sector,
    },
    "fab edit company contact": {
        "url": "ui-buyer:company-edit-contact",
        "po": None,
    },
    "fab edit social media links": {
        "url": "ui-buyer:company-edit-social-media",
        "po": fab_ui_edit_online_profiles,
    },
    "fab add collaborator": {
        "url": "ui-buyer:account-add-collaborator",
        "po": fab_ui_account_add_collaborator,
    },
    "fab remove collaborator": {
        "url": fab_ui_account_remove_collaborator.URL,
        "po": fab_ui_account_remove_collaborator,
    },
    "fab confirm you want to be added to the profile": {
        "url": None,
        "po": fab_ui_confim_your_collaboration,
    },
    "fab transfer ownership": {
        "url": fab_ui_account_transfer_ownership.URL,
        "po": fab_ui_account_transfer_ownership,
    },
    "fab confirm password": {
        "url": fab_ui_account_confrim_password.URL,
        "po": fab_ui_account_confrim_password,
    },
    "fab confirm ownership transfer": {
        "url": fab_ui_confim_your_ownership.URL,
        "po": fab_ui_confim_your_ownership,
    },
}

SUD_PAGE_REGISTRY = {
    "sud landing": {"url": "profile:landing", "po": profile_about},
    "sud selling online overseas": {
        "url": "profile:soo",
        "po": sud_ui_selling_online_overseas,
    },
    "sud export opportunities": {
        "url": "profile:exops-applications",
        "po": sud_ui_export_opportunities,
    },
    "sud export opportunities applications": {
        "url": "profile:exops-applications",
        "po": None,
    },
    "sud export opportunities email alerts": {
        "url": "profile:exops-alerts",
        "po": None,
    },
    "profile - about": {"url": "profile:about", "po": profile_about},
    "profile - enrol": {
        "url": "profile:enrol",
        "po": profile_enrol,
    },
    "profile - edit company profile": {
        "url": "ui-buyer:company-profile",
        "po": profile_edit_company_profile,
    },
    "profile - edit company description": {
        "url": "ui-buyer:company-edit-description",
        "po": profile_edit_company_description,
    },
    "profile add case study": {
        "url": "ui-buyer:case-study-add",
        "po": profile_case_study_basic,
    },
    "profile - find a buyer": {"url": "profile:fab", "po": sud_ui_find_a_buyer},
}

PAGE_REGISTRY = {}
PAGE_REGISTRY.update(FAB_PAGE_REGISTRY)
PAGE_REGISTRY.update(FAS_PAGE_REGISTRY)
PAGE_REGISTRY.update(SSO_PAGE_REGISTRY)
PAGE_REGISTRY.update(SUD_PAGE_REGISTRY)


def get_fabs_page_url(page_name: str, *, language_code: str = None):
    url = get_absolute_url(PAGE_REGISTRY[page_name.lower()]["url"])
    if language_code:
        url += "?lang={}".format(language_code)
    return url


def get_fabs_page_object(page_name: str):
    page = PAGE_REGISTRY[page_name.lower()]["po"]
    return page
