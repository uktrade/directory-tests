@erp
@uk_consumer
Feature: ERP - UK consumer


  Scenario: An enquirer representing a "UK consumer" should be able to tell which goods are affected
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents a "UK consumer"

    Then "Robert" should be on the "ERP - Product search (UK consumer)" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |
