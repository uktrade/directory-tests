@allure.link:ED-3580
@fas-home-page
@no-sso-email-verification-required
@allure.suite:International
Feature: FAS - Landing page

  Background:
    Given basic authentication is done for "International - Landing" page

  Scenario: Visitors should be able to go to "<expected_service>" page from the International page
    Given "Robert" visits the "International - Landing" page

    When "Robert" decides to find out more about "Buy from the UK"

    Then "Robert" should be on the "International - How we help you buy from the UK" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | FAS Header      |
      | Hero            |
      | Breadcrumbs     |
      | Teaser          |
      | eBook           |
      | Services        |
      | Contact us      |
      | Error reporting |
      | Footer          |


  Scenario Outline: Visitors looking for UK Suppliers should be able to "<subsection>" from the International page
    Given "Robert" visits the "International - How we help you buy from the UK" page

    When "Robert" decides to find out more about "<subsection>"

    Then "Robert" should be on the "<expected>" page

    Examples: FAS pages
      | subsection      | expected                                        |
      | How we help     | International - How we help you buy from the UK |
      | Find a supplier | Find a Supplier - landing                       |
      | Contact us      | International - Find a UK business partner      |


  @allure.link:ED-4242
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


  @allure.link:ED-4245
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


  @allure.link:ED-4248
  @industry-page
  Scenario: Buyers should be able to find out more about featured industries from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to read about one of listed industries

    Then "Robert" should be on the "International - Industry" page


  @allure.link:ED-4249
  @industries-page
  Scenario: Buyers should be able to see more UK industries from the "Find a Supplier - Landing" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" decides to "see more industries"

    Then "Robert" should be on the "International - Industries" page


  @bug
  @allure.issue:TT-1512
  @fixed
  @search
  Scenario: Buyers should be able to find UK suppliers using arbitrary search term
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" searches for companies using "food" keyword

    Then "Robert" should be on the "Find a Supplier - Search results" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Search form     |
      | Filters         |
      | Results         |
      | Footer          |
