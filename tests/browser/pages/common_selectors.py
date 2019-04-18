# -*- coding: utf-8 -*-
"""Selectors for various common page components"""
from pages import ElementType
from pages.common_actions import By, Selector
from settings import (
    EIG_LOGO_MD5_CHECKSUM,
    EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM,
    EVENTS_BIG_HEADER_LOGO_MD5_CHECKSUM,
    GREAT_LOGO_MD5_CHECKSUM,
)

HEADER = {
    "header": {
        # cookie notice
        "itself": Selector(By.ID, "header-cookie-notice", is_visible=False),
        "find out more about cookies": Selector(
            By.CSS_SELECTOR, "#header-cookie-notice a", is_visible=False
        ),
        "dismiss cookie notice": Selector(
            By.ID, "dismiss-cookie-notice", is_visible=False
        ),
        # global header
        "global header": Selector(By.ID, "great-global-header"),
        "great global logo": Selector(By.ID, "great-global-header-logo"),
        "for uk businesses": Selector(By.ID, "great-global-header-domestic-link"),
        "for international businesses": Selector(
            By.ID, "great-global-header-international-link"
        ),
        # header menu
        "header menu": Selector(By.ID, "great-header-menu"),
        "eig logo": Selector(By.ID, "great-header-logo"),
        "advice": Selector(By.ID, "header-advice", type=ElementType.LINK),
        "markets": Selector(By.ID, "header-markets", type=ElementType.LINK),
        "services": Selector(By.ID, "header-services", type=ElementType.LINK),
        "search box": Selector(By.ID, "search-box", type=ElementType.INPUT),
        "search button": Selector(
            By.CSS_SELECTOR,
            "#search-box ~ button[type=submit]",
            type=ElementType.BUTTON,
        ),
    }
}
SSO_LOGGED_IN = {
    "sso links - logged out": {
        "account": Selector(By.ID, "header-profile-link", is_visible=False),
        "sign out": Selector(By.ID, "header-sign-out-link", is_visible=False),
    },
}
SSO_LOGGED_OUT = {
    "sso links - logged out": {
        "sign in": Selector(By.ID, "header-sign-in-link", is_visible=False),
    },
}

BETA_BAR = {
    "beta bar": {
        "itself": Selector(By.ID, "header-beta-bar"),
        "badge": Selector(By.CSS_SELECTOR, "#header-beta-bar .phase-tag"),
        "message": Selector(By.CSS_SELECTOR, "#header-beta-bar span"),
        "link": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    }
}

BREADCRUMBS = {
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
        "current page": Selector(
            By.CSS_SELECTOR, ".breadcrumbs li[aria-current='page']"
        ),
        "links": Selector(By.CSS_SELECTOR, ".breadcrumbs a"),
    }
}

ERROR_REPORTING = {
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    }
}

FOOTER = {
    "footer": {
        "great footer logo": Selector(By.ID, "great-footer-great-logo"),
        "contact us": Selector(By.ID, "footer-contact"),
        "privacy and cookies": Selector(By.ID, "footer-privacy-and-cookies"),
        "terms and conditions": Selector(By.ID, "footer-terms-and-conditions"),
        "performance": Selector(By.ID, "footer-performance"),
        "department for international trade on gov.uk": Selector(By.ID, "footer-dit"),
        "go to the page for international businesses": Selector(
            By.ID, "footer-international"
        ),
        "dit footer logo": Selector(By.ID, "great-global-footer-logo"),
        "copyright notice": Selector(By.ID, "great-footer-copyright"),
    }
}

FAVICON = Selector(By.CSS_SELECTOR, "link[rel='shortcut icon']")
EXOPPS_FAVICON = Selector(By.CSS_SELECTOR, "link[rel='icon']")
EIG_LOGO = Selector(By.CSS_SELECTOR, "#great-header-logo > img")
REGISTRATION_LINK = Selector(By.ID, "header-register-link")
SIGN_IN_LINK = Selector(By.ID, "header-sign-in-link")
PROFILE_LINK = Selector(By.ID, "header-profile-link")
SIGN_OUT_LINK = Selector(By.ID, "header-sign-out-link")

LOGOS = {
    "eig": {"selector": EIG_LOGO, "md5": EIG_LOGO_MD5_CHECKSUM},
    "great - header": {
        "selector": Selector(By.CSS_SELECTOR, "#great-header-logo img"),
        "md5": GREAT_LOGO_MD5_CHECKSUM,
    },
    "great - footer": {
        "selector": Selector(By.ID, "great-footer-great-logo"),
        "md5": GREAT_LOGO_MD5_CHECKSUM,
    },
    "events business is great - header": {
        "selector": Selector(By.CSS_SELECTOR, "header img"),
        "md5": EVENTS_BIG_HEADER_LOGO_MD5_CHECKSUM,
    },
    "events business is great - footer": {
        "selector": Selector(By.CSS_SELECTOR, "#footer_section img"),
        "md5": EVENTS_BIG_FOOTER_LOGO_MD5_CHECKSUM,
    },
}

HEADER_INTERNATIONAL = {
    "header": {
        # cookie notice
        "itself": Selector(By.ID, "header-cookie-notice", is_visible=False),
        "find out more about cookies": Selector(
            By.CSS_SELECTOR, "#header-cookie-notice a", is_visible=False
        ),
        "dismiss cookie notice": Selector(
            By.ID, "dismiss-cookie-notice", is_visible=False
        ),
        # global header
        "global header": Selector(By.ID, "great-global-header"),
        "great global logo": Selector(By.ID, "great-global-header-logo"),
        "for uk businesses": Selector(By.ID, "great-global-header-domestic-link"),
        "for international businesses": Selector(
            By.ID, "great-global-header-international-link"
        ),
        # language selector
        "language selector": Selector(By.ID, "great-header-language-select", type=ElementType.SELECT),
        # header menu
        "header menu": Selector(By.ID, "great-header-menu"),
        "eig logo": Selector(By.ID, "great-header-logo"),
        "invest": Selector(By.ID, "header-invest", type=ElementType.LINK),
        "find a uk supplier": Selector(By.ID, "header-fas", type=ElementType.LINK),
        "industries": Selector(By.ID, "header-industries", type=ElementType.LINK),
    }

}
FOOTER_INTERNATIONAL = {
    "footer": {
        "great footer logo": Selector(By.ID, "great-footer-great-logo"),
        "contact us": Selector(By.ID, "footer-contact"),
        "privacy and cookies": Selector(By.ID, "footer-privacy-and-cookies"),
        "terms and conditions": Selector(By.ID, "footer-terms-and-conditions"),
        "department for international trade on gov.uk": Selector(By.ID, "footer-dit"),
        "go to the page for uk businesses": Selector(
            By.ID, "footer-domestic"
        ),
        "dit footer logo": Selector(By.ID, "great-global-footer-logo"),
        "copyright notice": Selector(By.ID, "great-footer-copyright"),
    }
}
