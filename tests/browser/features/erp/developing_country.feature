@erp
@uk_consumer
Feature: ERP - An exporter from developing country


  @TT-2121
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


  @TT-2122
  Scenario: An exporter from developing country should see a list of product codes which might be affected by Brexit
    Given "Robert" got to "ERP - Select country (Developing country)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (Developing country)" page
