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
  @<business_type>
  Scenario Outline: An exporter from developing country should see a list of product codes which might be affected by Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2123
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to select goods affected by Brexit
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |


  @TT-2124
  @<business_type>
  Scenario Outline: An exporter from developing country should should be able to change the goods previously selected
    Given "Robert" got to "ERP - Select country (<business_type>)" from "ERP - User type" via "exporter from developing country"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    When "Robert" decides to "change goods"
    Then "Robert" should be on the "ERP - Product search (<business_type>)" page

    When "Robert" selects a random product code from the hierarchy of product codes
    Then "Robert" should be on the "ERP - Product detail (<business_type>)" page

    Examples: business type
      | business_type      |
      | Developing country |
