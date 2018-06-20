@ED-3190
@industries-page
@no-sso-email-verification-required
Feature: FAS Industries page


  @ED-4253
  Scenario: Buyers should be able to view "FAS Industries" page
    Given "Annette Geissinger" visits the "FAS Industries" page

    Then "Annette Geissinger" should see expected sections on "FAS Industries" page
      | Sections         |
      | Hero             |
      | Breadcrumbs      |
      | Contact us       |
      | Industries       |
      | More Industries  |
#      | Report this page |


  @ED-4254
  @industry-pages
  Scenario Outline: Buyers should be able to find out more about "<specific>" industry from the "FAS Industries" page
    Given "Robert" visits the "FAS Industries" page

    When "Robert" decides to find out out more about "<specific>" industry

    Then "Robert" should be on the "FAS Industry" page
    And "Robert" should see content specific to "<specific>" industry page

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
  Scenario: Buyers should be able to go back to the "FAS Home" page via breadcrumbs on the "FAS Industries" page
    Given "Robert" visits the "FAS Industries" page

    When "Robert" decides to use "Home" breadcrumb on the "FAS Industries" page

    Then "Robert" should be on the "FAS Landing" page


  @ED-4256
  @contact-us
  Scenario: Buyers should be able to get to the "Contact us" page from the "FAS Industries" page
    Given "Robert" visits the "FAS Industries" page

    When "Robert" decides to "contact us" via "FAS Industries" page

    Then "Robert" should be on the "FAS Contact us" page


  @ED-4257
  @contact-us
  Scenario: Buyers should be able to contact us (DIT) from the FAS home page
    Given "Robert" visits the "FAS Industries" page
    And "Robert" decided to "contact us" via "FAS Industries" page

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "FAS Thank you for your message" page


  @wip
  @ED-4258
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "FAS Industries" page
    Given "Robert" visits the "FAS Industries" page

    When "Robert" decides to report problem with the "FAS Industries" page
    And "Robert" fills out and submits the "Help us improve great.gov.uk" form

    Then "Robert" should be on the "FAS Thank you for your message" page
