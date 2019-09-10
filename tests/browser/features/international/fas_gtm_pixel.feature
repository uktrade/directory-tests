@gtm
@pixels
Feature: FAS - Google Tag Manager

  Background:
    Given basic authentication is done for "International - Landing" page

  @bug
  @CMS-1634
  @fixed
  @TT-1500
  Scenario Outline: GTM properties should be properly set on "Find a Supplier - <selected>" page
    When "Robert" goes to the "Find a Supplier - <selected>" page

    Then Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |
    Examples: Listing pages
      | selected             | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection | userId |
      | Landing              | FindASupplier | False       | en-gb        | HomePage    | Empty string   | None   |
      | Empty search results | FindASupplier | False       | en-gb        | Companies   | Search         | None   |

  @bug
  @CMS-1634
  @fixed
  @TT-1500
  Scenario Outline: GTM properties should be properly set on "Find a Supplier - Company profile" page
    Given "Robert" searched for companies using "food" keyword in "any" sector

    When "Robert" decides to view "random" company profile

    Then "Robert" should be on the "Find a Supplier - Company profile" page
    And Google Tag Manager properties should be set to proper values
      | businessUnit   | loginStatus   | siteLanguage   | siteSection   | siteSubsection   | userId   |
      | <businessUnit> | <loginStatus> | <siteLanguage> | <siteSection> | <siteSubsection> | <userId> |

    Examples: Listing pages
      | businessUnit  | loginStatus | siteLanguage | siteSection | siteSubsection         | userId |
      | FindASupplier | False       | en-gb        | Companies   | PublishedProfileDetail | None   |


  @stage-only
  @bug
  @CMS-1634
  @fixed
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
      | Landing  | Deutsch            | FindASupplier | False       | de           | HomePage    | Empty string   | None   |
      | Landing  | Français           | FindASupplier | False       | fr           | HomePage    | Empty string   | None   |
      | Landing  | español            | FindASupplier | False       | es           | HomePage    | Empty string   | None   |
      | Landing  | Português          | FindASupplier | False       | pt           | HomePage    | Empty string   | None   |
      | Landing  | 简体中文            | FindASupplier | False       | zh-hans      | HomePage    | Empty string   | None   |
