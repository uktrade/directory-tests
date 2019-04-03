Feature: Header-Footer

  Background:
    Given basic authentication is done for "Export Readiness - Home" page

  @ED-3118
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo, one with the boat, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should see correct DIT logo in page header

    Examples:
      | selected                                        |
      | Export Readiness - Home                         |
      | Single Sign-On - Registration                   |
      | Single Sign-On - Sign in                        |
      | Single Sign-On - Profile about                  |
      | Export Readiness - Get finance                  |
      | Export Opportunities - Home                     |
      | Find a Buyer - Home                             |

    # these services use different logo
    @wip
    Examples:
      | selected                                        |
      | Find a Supplier - Home                          |
      | Events - Home                                   |


  @bug
  @ED-3116
  @fixed
  @logo
  @header
  @footer
  @ED-3118
  Scenario Outline: Any Exporter should see correct DIT logo, one with the boat, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Export Opportunities - Home         |
      | Selling Online Overseas - Home      |


  @ED-3587
  @logo
  @header
  @footer
  @ED-3118
  Scenario Outline: Any Exporter should be able to get to the Export Readiness Home page from "<selected>" page by using DIT logo in the page header and footer
    Given "Robert" visits the "<selected>" page

    When "Robert" decides to click on the DIT logo in the "header"

    Then "Robert" should be on the "Export Readiness - Home" page or on the International page

    Examples:
      | selected                                        |
      | Export Readiness - Home                         |
      | Single Sign-On - Registration                   |
      | Single Sign-On - Sign in                        |
      | Export Readiness - Get finance                  |
      | Export Opportunities - Home                     |
      | Find a Buyer - Home                             |
      | Export Opportunities - Home                     |
    @bug
    # There's no SOO DEV env
    @fixme
    Examples:
      | selected                                        |
      | Selling Online Overseas - Home                  | 

    @bug
    @TT-886
    @fixme
    Examples:
      | selected                                        |
      | Single Sign-On - Profile about                  |


  @ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on "<specific>" page
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Export Readiness pages
      | specific                                        |
      | Export Readiness - Home                         |
      | Export Opportunities - Home                     |

    Examples: FABS pages
      | specific               |
      | Find a Buyer - Home    |
      | Find a Supplier - Home |

    Examples: SSO pages
      | specific                       |
      | Single Sign-On - Registration  |
      | Single Sign-On - Sign in       |
      | Single Sign-On - Profile about |

    Examples: SOO pages
      | specific                       |
      | Selling Online Overseas - Home |

    Examples: Export Opportunities
      | specific                    |
      | Export Opportunities - Home |


  @bug
  @ED-3216
  @fixed
  @ED-3215
  @header
  @home-page
  @<specific>
  Scenario Outline: Any Exported should be able to get to the Domestic "<expected>" page via "<specific>" link in the "<selected section>"
    Given "Robert" visits the "Export Readiness - Home" page

    When "Robert" goes to the "<specific>" page via "General" links in "Export Readiness - <selected section>"

    Then "Robert" should be on the "<expected>" page or on the International page

    Examples:
      | specific            | expected                                      | selected section |
      | Home                | Export Readiness - Home                       | header           |
