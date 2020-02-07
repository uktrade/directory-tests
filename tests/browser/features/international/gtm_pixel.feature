@wip
@gtm
@pixels
@allure.suite:International
Feature: INTL - Google Tag Manager

  Background:
    Given basic authentication is done for "International - Landing" page

  @TT-1500
  Scenario Outline: GTM properties should be properly set on "International - <selected>" page
    When "Robert" goes to the "International - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    @bug
    @CMS-1634
    @fixed
    Examples: Landing page
      | selected | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing  | GreatInternational | False       | en-gb        | HomePage    | Empty string   | None   |

    Examples: Listing pages
      | selected                | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Industries              | GreatInternational | False       | en-gb        | Topic       | ListingPage    | None   |

    @dev-only
    Examples: Industry pages
      | selected                                 | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Aerospace - Industry                     | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Automotive - Industry                    | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Creative industries - Industry           | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Education - Industry                     | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Engineering and manufacturing - Industry | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Financial services - Industry            | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Health and Life Sciences - Industry      | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Legal services - Industry                | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Space - Industry                         | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Technology - Industry                    | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |

    @stage-only
    Examples: Industry pages
      | selected                                 | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Engineering and manufacturing - Industry | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Creative industries - Industry           | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |

    @uat-only
    Examples: Industry pages
      | selected                                 | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Automotive - Industry                    | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Aerospace - Industry                     | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Creative industries - Industry           | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Education - Industry                     | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Engineering and manufacturing - Industry | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Financial services - Industry            | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Health and Life Sciences - Industry      | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Legal services - Industry                | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Space - Industry                         | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |
      | Technology - Industry                    | GreatInternational | False       | en-gb        | Sector      | DetailPage     | None   |

    @dev-only
    Examples: UK setup guides
      | selected                                                          | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide                         | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Establish a UK business base - UK setup guide                     | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Hire skilled workers for your UK operations - UK setup guide      | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide                  | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Register a company in the UK - UK setup guide                     | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Research and development (R&D) support in the UK - UK setup guide | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | UK tax and incentives - UK setup guide                            | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | UK visas and migration - UK setup guide                           | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |

    @stage-only
    Examples: UK setup guides
      | selected                                         | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide        | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |

    @uat-only
    Examples: UK setup guides
      | selected                                                          | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide                         | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Establish a UK business base - UK setup guide                     | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Hire skilled workers for your UK operations - UK setup guide      | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide                  | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Register a company in the UK - UK setup guide                     | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | Research and development (R&D) support in the UK - UK setup guide | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | UK tax and incentives - UK setup guide                            | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |
      | UK visas and migration - UK setup guide                           | GreatInternational | False       | en-gb        | Article     | DetailPage     | None   |


  @bug
  @CMS-1634
  @fixed
  @TT-1500
  @internationalisation
  Scenario Outline: GTM properties should be properly set on "International - <selected>" page viewed in "<preferred_language>"
    Given "Robert" visits the "International - <selected>" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Various pages
      | selected | preferred_language | businessUnit       | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing  | Deutsch            | GreatInternational | False       | de           | HomePage    | Empty string   | None   |
      | Landing  | Français           | GreatInternational | False       | fr           | HomePage    | Empty string   | None   |
      | Landing  | español            | GreatInternational | False       | es           | HomePage    | Empty string   | None   |
      | Landing  | Português          | GreatInternational | False       | pt           | HomePage    | Empty string   | None   |
      | Landing  | 简体中文            | GreatInternational | False       | zh-hans      | HomePage    | Empty string   | None   |
