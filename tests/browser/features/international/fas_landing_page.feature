@ED-3580
@fas-home-page
@no-sso-email-verification-required
Feature: Find a Supplier - Landing page

  Background:
    Given basic authentication is done for "International - Landing" page

  @ED-4242
  Scenario: Buyers should be able to view "Find a Supplier home" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    Then "Robert" should see following sections
      | Sections          |
      | Header            |
      | Hero              |
      | Find UK Suppliers |
      | Contact us        |
      | UK Industries     |
      | How we can help   |
      | Footer            |


  @ED-4245
  @search
  Scenario Outline: Buyers should be able to "Find UK suppliers" in "<specific>" industry from the "Find a Supplier home" page using "<following>" keyword
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" searches for companies using "<following>" keyword in "<specific>" sector

    Then "Robert" should be on the "<expected>" page

    Examples:
      | following | specific       | expected                               |
      | no        | any            | Find a Supplier - Empty search results |
      | Food      | any            | Find a Supplier - Search results       |
      | no        | Mining         | Find a Supplier - Search results       |


  @ED-4248
  @industry-page
  Scenario: Buyers should be able to find out more about featured industries from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to read about one of listed industries

    Then "Robert" should be on the "International - Industry" page


  @ED-4249
  @industries-page
  Scenario: Buyers should be able to see more UK industries from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to "see more industries"

    Then "Robert" should be on the "International - Industries" page
