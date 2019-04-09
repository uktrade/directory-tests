# -*- coding: utf-8 -*-
"""Find a Supplier - Common header/footer selectors"""

from selenium.webdriver.common.by import By

from pages.common_actions import Selector

HEADER_FOOTER_SELECTORS = {
    "header": {
        "itself": Selector(By.ID, "great-header"),
        "find out more about cookies": Selector(
            By.CSS_SELECTOR, "#header-cookie-notice a"
        ),
        "dismiss cookie notice": Selector(By.ID, "dismiss-cookie-notice"),
        "for uk businesses": Selector(By.ID, "great-global-header-domestic-link"),
        "for international businesses": Selector(
            By.ID, "great-global-header-international-link"
        ),
        "language switcher": Selector(By.ID, "country-selector-activator"),
        "logo": Selector(By.ID, "great-header-logo"),
        "invest": Selector(By.ID, "header-invest"),
        "find a uk supplier": Selector(By.ID, "header-fas-search"),
        "industries": Selector(By.ID, "header-industries"),
        "how to do business with the uk": Selector(
            By.ID, "header-how-to-do-business-with-the-uk"
        ),
    },
    "footer": {
        "itself": Selector(By.ID, "great-footer"),
        "dit logo": Selector(By.ID, "great-footer-dit-logo"),
        "great logo": Selector(By.ID, "great-footer-great-logo"),
        "contact us footer": Selector(By.ID, "footer-contact"),
        "privacy and cookies": Selector(By.ID, "footer-privacy-and-cookies"),
        "terms and conditions": Selector(By.ID, "footer-terms-and-conditions"),
        "dit": Selector(By.ID, "footer-dit"),
        "go to the page for uk businesses": Selector(By.ID, "footer-domestic"),
        "great global logo": Selector(By.ID, "great-global-footer-logo"),
        "copyright": Selector(By.ID, "great-footer-copyright"),
    },
}
