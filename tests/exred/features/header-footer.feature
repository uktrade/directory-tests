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
