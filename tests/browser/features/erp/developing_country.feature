@erp
@uk_consumer
Feature: ERP - An exporter from developing country


  Scenario: An enquirer representing an "exporter from developing country" should be able to tell which country they are from
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents an "exporter from developing country"

    Then "Robert" should be on the "ERP - Select country (Developing country)" page
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |
