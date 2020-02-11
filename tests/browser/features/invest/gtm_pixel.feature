@gtm
@pixels
@allure.suite:Invest
Feature: Invest - Google Tag Manager

  Background:
    Given basic authentication is done for "International - Landing" page

  @allure.link:TT-1500
  Scenario Outline: GTM properties should be properly set on "Invest - <selected>" page
    When "Robert" goes to the "Invest - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    @bug
    @allure.issue:CMS-1634
    @fixed
    Examples: Listing pages
      | selected                | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing                 | Invest       | False       | en-gb        | HomePage    | Empty string   | None   |
      | Contact us              | Invest       | False       | en-gb        | Contact     | Empty string   | None   |
      | How to set up in the UK | Invest       | False       | en-gb        | Guide       | ListingPage    | None   |

    @hpo
    @dev-only
    Examples: High-potential opportunities in Dev
      | selected                                      | businessUnit | loginStatus | siteLanguage | siteSection                | siteSubsection | userId |
      | High productivity food production (Dev) - HPO | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Lightweight structures - HPO                  | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Rail infrastructure - HPO                     | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |

    @hpo
    @stage-only
    Examples: High-potential opportunities in Staging
      | selected                                          | businessUnit | loginStatus | siteLanguage | siteSection                | siteSubsection | userId |
      | High productivity food production (Staging) - HPO | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Lightweight structures - HPO                      | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Rail infrastructure - HPO                         | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |


  @bug
  @allure.issue:CMS-1634
  @fixed
  @allure.link:TT-1500
  @internationalisation
  Scenario Outline: GTM properties should be properly set on "Invest - <selected>" page viewed in "<preferred_language>"
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Various pages
      | selected | preferred_language | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing  | Deutsch            | Invest       | False       | de           | HomePage    | Empty string   | None   |
      | Landing  | Français           | Invest       | False       | fr           | HomePage    | Empty string   | None   |
      | Landing  | español            | Invest       | False       | es           | HomePage    | Empty string   | None   |
      | Landing  | Português          | Invest       | False       | pt           | HomePage    | Empty string   | None   |
      | Landing  | 简体中文            | Invest       | False       | zh-hans      | HomePage    | Empty string   | None   |
