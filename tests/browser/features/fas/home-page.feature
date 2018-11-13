@ED-3580
@fas-home-page
@no-sso-email-verification-required
Feature: Find a Supplier - home page


  @ED-4242
  Scenario: Buyers should be able to view "Find a Supplier home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    Then "Robert" should see following sections
      | Sections          |
      | Header            |
      | Hero              |
      | Find UK Suppliers |
      | Contact us        |
      | UK Industries     |
      | UK Services       |
      | Footer            |


  @ED-4245
  @search
  Scenario Outline: Buyers should be able to "Find UK suppliers" in "<specific>" industry from the "Find a Supplier home" page using "<following>" keyword
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" searches for companies using "<following>" keyword in "<specific>" sector

    Then "Robert" should be on the "<expected>" page

    Examples:
      | following | specific       | expected                               |
      | no        | any            | Find a Supplier - Empty search results |
      | Food      | any            | Find a Supplier - Search results       |
      | no        | Mining         | Find a Supplier - Search results       |


  @ED-4246
  @contact-us
  Scenario: Buyers should be able to get to the "Contact us" page from the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" decides to use "Contact us" button

    Then "Robert" should be on the "Find a Supplier - Contact us" page


  @ED-4247
  @captcha
  @dev-only
  @contact-us
  Scenario: Buyers should be able to contact DIT from the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page
    And "Robert" decided to use "contact us" button

    When "Robert" fills out and submits the contact us form

    Then "Robert" should be on the "Find a Supplier - Thank you for your message" page


  @ED-4248
  @industry-page
  Scenario: Buyers should be able to find out more about featured industries from the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" decides to read about one of listed industries

    Then "Robert" should be on the "Find a Supplier - Industry" page


  @ED-4249
  @industries-page
  Scenario: Buyers should be able to see more UK industries from the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" decides to see more UK industries

    Then "Robert" should be on the "Find a Supplier - Industries" page


  @wip
  @captcha
  @dev-only
  @ED-4250
  @report-this-page
  Scenario: Buyers should be able to report a problem with the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" decides to report problem with the "Find a Supplier - home" page
    And "Robert" fills out and submits the "Help us improve great.gov.uk" form

    Then "Robert" should be on the "Find a Supplier - Thank you for your feedback" page


  @wip
  @ED-4251
  @marketing-content-page
  Scenario: Buyers should be able to view the Marketing Content from the "Find a Supplier - home" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" decides to go to learn more about marketing on the "Find a Supplier - home" page

    Then "Robert" should be on the "Find a Supplier - Marketing content" page
