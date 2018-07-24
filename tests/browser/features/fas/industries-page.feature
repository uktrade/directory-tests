@ED-3190
@industries-page
@no-sso-email-verification-required
Feature: Find a Supplier - Industries page


  @ED-4253
  Scenario: Buyers should be able to view "Find a Supplier - Industries" page
    Given "Annette Geissinger" visits the "Find a Supplier - Industries" page

    Then "Annette Geissinger" should see following sections
      | Sections         |
      | Hero             |
      | Breadcrumbs      |
      | Contact us       |
      | Industries       |
      | More Industries  |
#      | Report this page |


  @ED-4254
  @industry-pages
  Scenario Outline: Buyers should be able to find out more about "<specific>" industry from the "Find a Supplier - Industries" page
    Given "Robert" visits the "Find a Supplier - Industries" page

    When "Robert" decides to find out out more about "Find a Supplier - <specific> - industry"

    Then "Robert" should be on the "Find a Supplier - <specific> - industry" page
    And "Robert" should see content specific to "Find a Supplier - <specific> - industry" page

    Examples: promoted industries
      | specific          |
      | Aerospace         |
      | Agritech          |
      | Consumer retail   |
      | Creative services |
      | Cyber security    |
      | Food and drink    |
      | Healthcare        |
#      | Life sciences     |  # there are no companies in this industry on DEV
      | Sports economy    |
      | Technology        |

    Examples: more industries
      | specific          |
      | Legal services    |


  @ED-4255
  @breadcrumbs
  Scenario: Buyers should be able to go back to the "Find a Supplier - Home" page via breadcrumbs on the "Find a Supplier - Industries" page
    Given "Robert" visits the "Find a Supplier - Industries" page

    When "Robert" decides to use "Home" breadcrumb on the "Find a Supplier - Industries" page

    Then "Robert" should be on the "Find a Supplier - Home" page


  @ED-4256
  @contact-us
  Scenario: Buyers should be able to get to the "Contact us" page from the "Find a Supplier - Industries" page
    Given "Robert" visits the "Find a Supplier - Industries" page

    When "Robert" decides to "contact us" via "Find a Supplier - Industries" page

    Then "Robert" should be on the "Find a Supplier - Contact us" page


  @ED-4257
  @contact-us
  Scenario: Buyers should be able to contact us (DIT) from the Find a Supplier - home page
    Given "Robert" visits the "Find a Supplier - Industries" page
    And "Robert" decided to "contact us" via "Find a Supplier - Industries" page

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "Find a Supplier - Thank you for your message" page


  @wip
  @ED-4258
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "Find a Supplier - Industries" page
    Given "Robert" visits the "Find a Supplier - Industries" page

    When "Robert" decides to report problem with the "Find a Supplier - Industries" page
    And "Robert" fills out and submits the "Help us improve great.gov.uk" form

    Then "Robert" should be on the "Find a Supplier - Thank you for your message" page
