@fas
@header-footer
Feature: Find a Supplier - Common header & Footer

  Background:
    Given basic authentication is done for "Find a Supplier - Home" page

  Scenario Outline: Buyers should be able to see correct header & footer on "Find a Supplier - <specific>" page
    Given "Robert" visits the "Find a Supplier - <specific>" page

    Then "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |

    Examples:
      | specific             |
      | Home                 |
      | Empty search results |
      | Industries           |
      | Energy - industry    |
      | Contact us           |


  Scenario: Buyers should be able to see correct header & footer on "Find a Supplier - Search results" page
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" searches for companies using "Drilling" keyword in "Mining" sector

    Then "Robert" should be on the "Find a Supplier - Search results" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |


  Scenario: Buyers should be able to subscribe to newsletter and see correct header & footer on "Find a Supplier - Thank you for registering" page
    Given "Robert" searched for companies using "food" keyword in "any" sector

    When "Robert" fills out and submits the newsletter form

    Then "Robert" should be on the "Find a Supplier - Thank you for registering" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |


  @captcha
  @dev-only
  Scenario: Buyers should be able to send a query to supplier and see correct header & footer on "Find a Supplier - Thank you for contacting supplier" page
    Given "Robert" searched for companies using "food" keyword in "any" sector

    When "Robert" decides to view "random" company profile
    Then "Robert" should be on the "Find a Supplier - Company profile" page

    When "Robert" decides to "Email company"
    Then "Robert" should be on the "Find a Supplier - Contact supplier" page

    When "Robert" fills out and submits the newsletter form
    Then "Robert" should be on the "Find a Supplier - Thank you for contacting supplier" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |
