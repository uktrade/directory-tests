@gtm
@pixels
Feature: Google Tag Manager

  Background:
    Given basic authentication is done for "International - Landing" page

  @TT-1500
  Scenario Outline: GTM properties should be properly set on "International - <selected>" page
    When "Robert" goes to the "International - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Listing pages
      | selected                | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing                 | International | False       | en-gb        | HomePage    | Empty string   | None   |
      | Industries              | International | False       | en-gb        | Topic       | ListingPage    | None   |
      | How to set up in the UK | Invest        | False       | en-gb        | Guide       | ListingPage    | None   |

    @dev-only
    Examples: Industry pages
      | selected                                 | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Engineering and manufacturing - Industry | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Healthcare and Life Sciences - Industry  | International | False       | en-gb        | Sector      | DetailPage     | None   |

    @stage-only
    Examples: Industry pages
      | selected                                       | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Engineering and manufacturing - Industry       | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Creative industries - Industry                 | International | False       | en-gb        | Sector      | DetailPage     | None   |

    @uat-only
    Examples: Industry pages
      | selected                                 | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Automotive - Industry                    | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Aerospace - Industry                     | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Creative industries - Industry           | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Education - Industry                     | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Engineering and manufacturing - Industry | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Financial services - Industry            | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Healthcare and Life Sciences - Industry  | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Legal services - Industry                | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Space - Industry                         | International | False       | en-gb        | Sector      | DetailPage     | None   |
      | Technology - Industry                    | International | False       | en-gb        | Sector      | DetailPage     | None   |

    @dev-only
    Examples: UK setup guides
      | selected                                                          | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide                         | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Establish a UK business base - UK setup guide                     | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Hire skilled workers for your UK operations - UK setup guide      | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide                  | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Register a company in the UK - UK setup guide                     | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Research and development (R&D) support in the UK - UK setup guide | International | False       | en-gb        | Article     | DetailPage     | None   |
      | UK tax and incentives - UK setup guide                            | International | False       | en-gb        | Article     | DetailPage     | None   |
      | UK visas and migration - UK setup guide                           | International | False       | en-gb        | Article     | DetailPage     | None   |

    @stage-only
    Examples: UK setup guides
      | selected                                                          | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide                         | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide                  | International | False       | en-gb        | Article     | DetailPage     | None   |

    @uat-only
    Examples: UK setup guides
      | selected                                                          | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Access finance in the UK - UK setup guide                         | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Establish a UK business base - UK setup guide                     | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Hire skilled workers for your UK operations - UK setup guide      | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Open a UK business bank account - UK setup guide                  | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Register a company in the UK - UK setup guide                     | International | False       | en-gb        | Article     | DetailPage     | None   |
      | Research and development (R&D) support in the UK - UK setup guide | International | False       | en-gb        | Article     | DetailPage     | None   |
      | UK tax and incentives - UK setup guide                            | International | False       | en-gb        | Article     | DetailPage     | None   |
      | UK visas and migration - UK setup guide                           | International | False       | en-gb        | Article     | DetailPage     | None   |


  @TT-1500
  @internationalisation
  Scenario Outline: GTM properties should be properly set on "International - <selected>" page viewed in "<preferred_language>"
    Given "Robert" visits the "International - <selected>" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Various pages
      | selected | preferred_language | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing  | Deutsch            | International | False       | de           | HomePage    | Empty string   | None   |
      | Landing  | Français           | International | False       | fr           | HomePage    | Empty string   | None   |
      | Landing  | español            | International | False       | es           | HomePage    | Empty string   | None   |
      | Landing  | Português          | International | False       | pt           | HomePage    | Empty string   | None   |
      | Landing  | 简体中文            | International | False       | zh-hans      | HomePage    | Empty string   | None   |
