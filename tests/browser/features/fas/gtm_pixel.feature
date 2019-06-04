@gtm
@pixels
Feature: Google Tag Manager

  Background:
    Given basic authentication is done for "Find a Supplier - Home" page

  @TT-1500
  Scenario Outline: GTM properties should be properly set on "Find a Supplier - <selected>" page
    When "Robert" goes to the "Find a Supplier - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    @bug
    @CMS-1634
    @fixme
    Examples: Listing pages
      | selected   | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection     | userId |
      | Home       | FindASupplier | False       | en-gb        | HomePage    | Empty string       | None   |

    Examples: Listing pages
      | selected   | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection     | userId |
      | Industries | FindASupplier | False       | en-gb        | Industries  | LandingPage        | None   |
      | Contact us | FindASupplier | False       | en-gb        | Industries  | LandingPageContact | None   |

    @industry
    Examples: Industry pages
      | selected                                      | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Aerospace - Industry                          | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Agritech - Industry                           | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Automotive - Industry                         | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Business & Government Partnerships - Industry | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Consumer & retail - Industry                  | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Creative services - Industry                  | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Cyber security - Industry                     | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Education - Industry                          | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Energy - Industry                             | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Engineering - Industry                        | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Food and drink - Industry                     | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Healthcare - Industry                         | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Infrastructure - Industry                     | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Innovation - Industry                         | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Legal services - Industry                     | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Life sciences - Industry                      | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Marine - Industry                             | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Professional & financial services - Industry  | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Space - Industry                              | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Sports economy - Industry                     | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |
      | Technology - Industry                         | FindASupplier | False       | en-gb        | Industries  | Detail         | None   |


  @bug
  @CMS-1634
  @fixme
  @TT-1500
  @internationalisation
  Scenario Outline: GTM properties should be properly set on "Find a Supplier - <selected>" page viewed in "<preferred_language>"
    Given "Robert" visits the "Find a Supplier - <selected>" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Various pages
      | selected | preferred_language | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Home     | Deutsch            | FindASupplier | False       | de           | HomePage    | Empty string   | None   |
      | Home     | Français           | FindASupplier | False       | fr           | HomePage    | Empty string   | None   |
      | Home     | español            | FindASupplier | False       | es           | HomePage    | Empty string   | None   |
      | Home     | Português          | FindASupplier | False       | pt           | HomePage    | Empty string   | None   |
      | Home     | 简体中文            | FindASupplier | False       | zh-hans      | HomePage    | Empty string   | None   |
