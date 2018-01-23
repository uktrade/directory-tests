Feature: Header-Footer


  @ED-3118
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo (with boat) in the page header and footer
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Home                                |
      | SSO registration                    |
      | SSO sign in                         |
      | SSO profile about                   |
      | Get finance                         |
      | Interim export opportunities        |
      | Triage - what do you want to export |
      | Find a Buyer                        |
#      | Find a Supplier                     |
#      | Events                              |


  @ED-3118
  @bug
  @ED-3116
  @fixme
  @logo
  @header
  @footer
  Scenario Outline: Any Exporter should see correct DIT logo (with boat) in the page header and footer
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<selected>" page
    And "Robert" should see correct DIT logo in page header

    Examples:
      | selected                            |
      | Export Opportunities                |
      | Selling Online Overseas             |


  @ED-3091
  @favicon
  Scenario Outline: Any user should see the correct favicon on whichever page they're on
    Given "Robert" visits the "<specific>" page

    Then "Robert" should see the correct favicon

    Examples: Export Readiness pages
      | specific                            |
      | Home                                |
      | Triage - what do you want to export |
      | Interim export opportunities        |

    Examples: FABS pages
      | specific        |
      | Find a Buyer    |
      | Find a Supplier |

    Examples: SSO pages
      | specific          |
      | SSO Registration  |
      | SSO Sign in       |
      | SSO Profile about |

    Examples: SOO pages
      | specific                |
      | Selling Online Overseas |

    Examples: Export Opportunities
      | specific             |
      | Export Opportunities |


  @ED-3215
  @home-page
  @<specific-page>
  Scenario Outline: Any Exported should be able to get to the Domestic Home page via Home link in the header menu
    Given "Robert" visits the "Home" page

    When "Robert" goes to the "<specific>" page via "General" links in header menu

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific            | expected                   |
      | Home                | Home                       |

    @bug
    @ED-3216
    @fixme
    Examples:
      | specific            | expected                   |
      | Your export journey | Create your export journey |
