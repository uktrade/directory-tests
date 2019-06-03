@gtm
@pixels
Feature: Google Tag Manager

  Background:
    Given basic authentication is done for "Invest - Home" page

  @TT-1500
  Scenario Outline: GTM properties should be properly set on "Invest - <selected>" page
    When "Robert" goes to the "Invest - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Listing pages
      | selected   | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Home       | Invest       | False       | en-gb        | LandingPage | Empty string   | None   |
      | Industries | Invest       | False       | en-gb        | Industries  | ListingPage    | None   |
      | Contact us | Invest       | False       | en-gb        | Contact     | DetailPage     | None   |


    @industry
    @dev-only
    Examples: Industry pages
      | selected                                       | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Advanced manufacturing - Industry              | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Aerospace - Industry                           | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Agri-tech - Industry                           | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Asset management - Industry                    | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Automotive - Industry                          | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Automotive research and development - Industry | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Automotive supply chain - Industry             | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Capital investment - Industry                  | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Chemicals - Industry                           | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Creative content and production - Industry     | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Creative industries - Industry                 | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Data analytics - Industry                      | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Digital media - Industry                       | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Electrical networks - Industry                 | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Energy - Industry                              | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Energy from waste market - Industry            | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Financial services - Industry                  | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Financial technology - Industry                | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Food and drink - Industry                      | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Food service and catering - Industry           | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Free-from foods - Industry                     | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Health and life sciences - Industry            | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Meat, poultry and dairy - Industry             | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Medical technology - Industry                  | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Motorsport - Industry                          | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Nuclear energy - Industry                      | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Offshore wind energy - Industry                | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Oil and gas - Industry                         | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Pharmaceutical manufacturing - Industry        | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Retail - Industry                              | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |
      | Technology - Industry                          | Invest       | False       | en-gb        | Industries  | DetailPage     | None   |

    @hpo
    @dev-only
    Examples: High-potential opportunities
      | selected                       | businessUnit | loginStatus | siteLanguage | siteSection                | siteSubsection | userId |
      | Advanced food production - HPO | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Lightweight structures - HPO   | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |
      | Rail infrastructure - HPO      | Invest       | False       | en-gb        | HighPotentialOpportunities | DetailPage     | None   |


  @TT-1500
  @internationalisation
  Scenario Outline: GTM properties should be properly set on "Invest - <selected>" page viewed in "<preferred_language>"
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Various pages
      | selected | preferred_language | businessUnit | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Home     | Deutsch            | Invest       | False       | de           | LandingPage | DetailPage     | None   |
      | Home     | Français           | Invest       | False       | fr           | LandingPage | DetailPage     | None   |
      | Home     | español            | Invest       | False       | es           | LandingPage | DetailPage     | None   |
      | Home     | Português          | Invest       | False       | pt           | LandingPage | DetailPage     | None   |
      | Home     | 简体中文            | Invest       | False       | zh-hans      | LandingPage | DetailPage     | None   |
