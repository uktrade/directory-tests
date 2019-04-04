Feature: Header-Footer


  @bug
  @ED-3116
  @fixed
  @ED-3118
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct EIG header logo & GREAT footer logo on "<selected>" page
    Given basic authentication is done for "<selected>" page
    And "Robert" visits the "<selected>" page

    Then "Robert" should see correct "EIG" logo
    And "Robert" should see correct "Great - footer" logo

    Examples:
      | selected                       |
      | Export Readiness - Get finance |
      | Export Readiness - Home        |
      | Find a Buyer - Home            |
      | Selling Online Overseas - Home |
      | Single Sign-On - Profile about |
      | Single Sign-On - Registration  |
      | Single Sign-On - Sign in       |


  @stage-only
  @ED-3118
  @logo
  @header
  @footer
  Scenario: Any Exporter should see correct EIG header logo & GREAT footer logo on "Export Opportunities - Home" page
    Given "Robert" visits the "Export Opportunities - Home" page

    Then "Robert" should see correct "EIG" logo
    And "Robert" should see correct "Great - footer" logo


  @bug
  @ED-3116
  @fixed
  @ED-3118
  @events
  @logo
  @header
  @footer
  Scenario: Any Exporter should see correct Business Is Great (BIG) header & footer logo on "Events - Home" page
    Given "Robert" visits the "Events - Home" page

    Then "Robert" should see correct "EVENTS Business Is Great - header" logo
    And "Robert" should see correct "EVENTS Business Is Great - footer" logo


  @ED-3118
  @logo
  @header
  @footer
  Scenario: Any Exporter should see correct GREAT header & footer logo on "Find a Supplier - Home" page
    Given basic authentication is done for "Find a Supplier - Home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    Then "Robert" should see correct "Great - header" logo
    And "Robert" should see correct "Great - footer" logo


  @ED-3587
  @logo
  @header
  @footer
  @ED-3118
  Scenario Outline: Any Exporter should be able to get to the Export Readiness Home page from "<selected>" page by using DIT logo in the page header and footer
    Given basic authentication is done for "<selected>" page
    And "Robert" visits the "<selected>" page

    When "Robert" decides to click on the DIT logo in the "header"

    Then "Robert" should be on the "Export Readiness - Home" page or on the International page

    Examples:
      | selected                                        |
      | Export Readiness - Home                         |
      | Export Readiness - Get finance                  |
      | Single Sign-On - Registration                   |
      | Single Sign-On - Sign in                        |
      | Find a Buyer - Home                             |
      | Selling Online Overseas - Home                  |

    @bug
    @TT-886
    @fixme
    Examples:
      | selected                                        |
      | Profile - About                                 |

    @stage-only
    Examples:
      | selected                                        |
      | Export Opportunities - Home                     |


  @ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on "<specific>" page
    Given basic authentication is done for "<specific>" page
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Export Readiness pages
      | specific                       |
      | Export Readiness - Home        |
      | Find a Buyer - Home            |
      | Find a Supplier - Home         |
      | Single Sign-On - Registration  |
      | Single Sign-On - Sign in       |
      | Profile - About                |
      | Selling Online Overseas - Home |

    @stage-only
    Examples: Export Opportunities
      | specific                       |
      | Export Opportunities - Home    |
