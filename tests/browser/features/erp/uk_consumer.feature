@erp
@uk_consumer
Feature: ERP - UK consumer


  Scenario: An enquirer representing a "UK consumer" should be able to tell which goods are affected
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents a "UK consumer"

    Then "Robert" should be on the "ERP - Product search (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Hierarchy codes |
      | Footer          |


  @drill
  Scenario: A UK customer should be able to select goods affected by Brexit
    Given "Robert" got from "ERP - User type" to "ERP - Product search (UK consumer)" via "UK consumer"

    When "Robert" selects a random product code from the hierarchy of product codes

    Then "Robert" should be on the "ERP - Product detail (UK consumer)" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Beta bar        |
      | Go back         |
      | Form            |
      | Save for later  |
      | Footer          |