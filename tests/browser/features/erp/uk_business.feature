@erp
@uk_business
Feature: ERP - UK business


  Scenario: An enquirer representing a "UK business" should be able to tell whether they're importing from overseas or not
    Given "Robert" visits the "ERP - User type" page

    When "Robert" says that he represents a "UK business"

    Then "Robert" should be on the "ERP - Import from overseas (UK business)" page
    And "Robert" should see following options
      | options |
      | Yes     |
      | No      |
    And "Robert" should see following sections
      | Sections |
      | Header   |
      | Beta bar |
      | Go back  |
      | Form     |
      | Footer   |
