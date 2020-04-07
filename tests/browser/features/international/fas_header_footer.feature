@fas
@header-footer
@allure.suite:International
Feature: FAS - Common header & Footer

  Background:
    Given test authentication is done


  Scenario Outline: Buyers should be able to see correct header & footer on "Find a Supplier - <specific>" page
    Given "Robert" visits the "Find a Supplier - <specific>" page

    Then "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |

    Examples:
      | specific             |
      | Landing              |
      | Empty search results |


  Scenario: Buyers should be able to see correct header & footer on "Find a Supplier - Search results" page
    Given "Robert" visits the "Find a Supplier - Landing" page

    When "Robert" searches for companies using "Drilling" keyword in "Mining" sector

    Then "Robert" should be on the "Find a Supplier - Search results" page
    And "Robert" should see following sections
      | Sections                    |
      | Header                      |
      | Subscribe for email updates |
      | Footer                      |


  Scenario: Buyers should see correct header & footer on "Company Profile" page
    Given "Robert" searched for companies using "food" keyword in "any" sector

    When "Robert" decides to view "random" company profile

    Then "Robert" should be on the "Find a Supplier - Company profile" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Footer   |
